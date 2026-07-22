"""Estágio [2]: pesquisa multi-ângulo com verificação adversarial.

Método portado da lógica do deep-research, mas com viés desenhado pro projeto:
para cada ângulo (factual / esquerda / direita / críticas) o modelo busca na
web e devolve afirmações com fontes. Depois, uma passada adversarial checa as
afirmações mais fortes ("isso procede?"). Salva research.json.
"""
from __future__ import annotations

import json

from . import llm, youtube

_ANGULOS = {
    "factual": (
        "Levante os FATOS objetivos e verificáveis: o que a lei / projeto / política "
        "realmente propõe, números, prazos, quem é afetado, status atual da tramitação. "
        "Nada de opinião — só o que é fato documentado."
    ),
    "esquerda": (
        "Reúna os MELHORES argumentos da perspectiva progressista / de esquerda. "
        "Steel-man: a versão mais forte e honesta do caso a favor (ou contra, conforme "
        "o lado), com a evidência que sustenta cada ponto."
    ),
    "direita": (
        "Reúna os MELHORES argumentos da perspectiva conservadora / de direita. "
        "Steel-man: a versão mais forte e honesta do caso, com a evidência de cada ponto."
    ),
    "criticas": (
        "Reúna as OBJEÇÕES técnicas e econômicas mais sérias — de qualquer lado do "
        "espectro: riscos, custos, efeitos colaterais, o que especialistas apontam de "
        "fraco na proposta e nos contra-argumentos."
    ),
}

_SYS_ANGULO = (
    "Você é um pesquisador rigoroso e imparcial. Busca fontes reais e recentes na web. "
    "Prioriza fontes primárias (texto de lei, dados oficiais) e veículos de credibilidade. "
    "Não inventa. Se algo é incerto, marca como incerto."
)

_FMT_ANGULO = """
Pesquise sobre o tema abaixo sob este ângulo específico.

TEMA: {tema}

ÂNGULO: {instr}

Depois de buscar, responda APENAS com um JSON neste formato:
{{
  "resumo": "2-3 frases sintetizando o que você achou neste ângulo",
  "afirmacoes": [
    {{"afirmacao": "...", "evidencia": "...", "forca": "alta|media|baixa",
      "fontes": [{{"titulo": "...", "url": "..."}}]}}
  ]
}}
"""

_SYS_VERIF = (
    "Você é um verificador de fatos adversarial. Sua função é TENTAR REFUTAR cada "
    "afirmação. Seja cético. Se não há base sólida, diga 'nao_confirmado'."
)

_FMT_VERIF = """
Verifique as afirmações de 'força alta' abaixo, buscando na web de forma independente.

AFIRMAÇÕES:
{lista}

Responda APENAS com JSON:
{{
  "verificacoes": [
    {{"afirmacao": "...", "veredito": "confirmado|parcial|nao_confirmado",
      "nota": "o que a checagem encontrou"}}
  ]
}}
"""


# ─── YouTube como fonte ──────────────────────────────────────────────────────

_SYS_QUERIES = (
    "Você gera queries de busca no YouTube para pesquisar um debate. Uma delas "
    "DEVE ser cética (procurar quem critica/contradiz a tese dominante)."
)

_FMT_QUERIES = """
Gere {n} queries curtas de YouTube para pesquisar este tema sob vários ângulos
(inclua obrigatoriamente ao menos uma query cética, tipo "crítica a X", "por que X
não funciona", "X é um erro"). Idioma: o do público-alvo do tema.

TEMA: {tema}

Responda APENAS com JSON: {{"queries": ["...", "..."]}}
"""

_SYS_SELECT = (
    "Você seleciona vídeos como fontes de pesquisa. Aplica: corroboração > "
    "autoridade, diversidade de canal, e a CADEIRA DO CÉTICO (ao menos 1 vídeo que "
    "contradiz/critica a tese dominante). Nunca 2 vídeos do mesmo canal."
)

_FMT_SELECT = """
Escolha os {k} MELHORES vídeos como fontes para o tema, aplicando a rubrica
(relevância, autoridade, diversidade de canal, cadeira do cético).

TEMA: {tema}

CANDIDATOS (JSON):
{cands}

Responda APENAS com JSON: {{"escolhidos": ["url1", "url2", ...]}}
"""

_SYS_VIDEO = (
    "Você extrai afirmações de transcrições de vídeo para pesquisa jornalística. "
    "Vídeo é relato de criador, não fato verificado. Você classifica cada afirmação "
    "e cruza com os comentários da audiência (auditoria da multidão)."
)

_FMT_VIDEO = """
Extraia as afirmações relevantes ao tema desta transcrição de vídeo. Classifique
cada uma num balde:
- confirmado (✅): dado/demo verificável ou mecanismo documentado
- plausivel (🟡): anedota repetida, a testar
- lore (🔵): opinião/experiência única do criador
- red_flag (🔴): enviesado, conflito de interesse, cherry-pick

Use os COMENTÁRIOS pra ajustar (a audiência endossa ou refuta?).

TEMA: {tema}
VÍDEO: {titulo} — {canal}
TRANSCRIÇÃO (trechos):
{transcricao}

COMENTÁRIOS (auditoria da multidão):
{comentarios}

Responda APENAS com JSON:
{{
  "afirmacoes": [
    {{"afirmacao": "...", "balde": "confirmado|plausivel|lore|red_flag",
      "nota": "por quê / o que os comentários dizem"}}
  ]
}}
"""


def _youtube(tema: str, cfg: dict, model: str) -> list[dict]:
    yt = cfg["pesquisa"].get("youtube", {})
    if not yt.get("ativo") or not youtube.disponivel():
        return []

    # 1) queries (com cética)
    raw = llm.complete(
        model=model, system=_SYS_QUERIES,
        user=_FMT_QUERIES.format(tema=tema, n=yt.get("num_queries", 3)),
        max_tokens=500,
    )
    try:
        queries = llm.extract_json(raw).get("queries", [])[: yt.get("num_queries", 3)]
    except ValueError:
        queries = [tema]

    # 2) buscar candidatos
    cands: list[dict] = []
    vistos: set[str] = set()
    for q in queries:
        print(f"  · youtube: '{q}'")
        for r in youtube.search(q, n=yt.get("resultados_por_query", 8)):
            if r["url"] not in vistos:
                vistos.add(r["url"])
                cands.append({k: r.get(k) for k in ("title", "channel", "url", "view_count", "duration")})
    if not cands:
        return []

    # 3) selecionar (diversidade + cadeira do cético)
    raw = llm.complete(
        model=model, system=_SYS_SELECT,
        user=_FMT_SELECT.format(tema=tema, k=yt.get("max_videos", 4),
                                cands=json.dumps(cands, ensure_ascii=False)),
        max_tokens=500,
    )
    try:
        urls = llm.extract_json(raw).get("escolhidos", [])
    except ValueError:
        urls = [c["url"] for c in cands[: yt.get("max_videos", 4)]]

    # 4) transcrever + comentários + extrair afirmações
    videos: list[dict] = []
    for url in urls[: yt.get("max_videos", 4)]:
        print(f"  · transcrevendo {url}")
        t = youtube.transcribe(url, timeout=yt.get("timeout_transcricao", 90))
        if not t:
            print("    (sem legenda / timeout — pulado)")
            continue
        meta = t.get("metadata", {})
        chunks = t.get("transcript", {}).get("chunks", [])
        trechos = "\n".join(c.get("text", "") for c in chunks)[:8000]
        coments = youtube.comments(url, n=yt.get("comentarios", 20)) if yt.get("auditar_comentarios", True) else ""
        raw = llm.complete(
            model=model, system=_SYS_VIDEO,
            user=_FMT_VIDEO.format(tema=tema, titulo=meta.get("title", ""),
                                   canal=meta.get("channel", ""), transcricao=trechos,
                                   comentarios=coments[:3000] or "(não auditados)"),
            max_tokens=2500,
        )
        try:
            af = llm.extract_json(raw).get("afirmacoes", [])
        except ValueError:
            af = []
        videos.append({
            "titulo": meta.get("title", ""), "canal": meta.get("channel", ""),
            "url": url, "afirmacoes": af,
        })
    return videos


def run(tema: str, cfg: dict) -> dict:
    model = cfg["models"]["research"]
    max_searches = cfg["pesquisa"]["max_buscas_por_angulo"]
    angulos = cfg["pesquisa"]["angulos"]

    resultado: dict = {"tema": tema, "angulos": {}, "videos": [], "verificacao": [], "fontes": []}
    fontes_seen: set[str] = set()

    for nome in angulos:
        instr = _ANGULOS[nome]
        print(f"  · pesquisando ângulo: {nome}")
        raw = llm.complete(
            model=model,
            system=_SYS_ANGULO,
            user=_FMT_ANGULO.format(tema=tema, instr=instr),
            max_tokens=4096,
            web_search=True,
            max_searches=max_searches,
        )
        try:
            data = llm.extract_json(raw)
        except ValueError:
            data = {"resumo": raw[:500], "afirmacoes": []}
        resultado["angulos"][nome] = data
        for af in data.get("afirmacoes", []):
            for f in af.get("fontes", []):
                url = f.get("url", "")
                if url and url not in fontes_seen:
                    fontes_seen.add(url)
                    resultado["fontes"].append(f)

    # YouTube como fonte (opcional, degrada com elegância)
    resultado["videos"] = _youtube(tema, cfg, model)

    # Verificação adversarial das afirmações fortes
    fortes = []
    for nome, data in resultado["angulos"].items():
        for af in data.get("afirmacoes", []):
            if af.get("forca") == "alta":
                fortes.append(af["afirmacao"])
    if fortes:
        print(f"  · verificando {len(fortes)} afirmações fortes")
        lista = "\n".join(f"- {a}" for a in fortes[:20])
        raw = llm.complete(
            model=model,
            system=_SYS_VERIF,
            user=_FMT_VERIF.format(lista=lista),
            max_tokens=3000,
            web_search=True,
            max_searches=max_searches,
        )
        try:
            resultado["verificacao"] = llm.extract_json(raw).get("verificacoes", [])
        except ValueError:
            pass

    return resultado
