#!/usr/bin/env python3
"""Publica os episódios de output/ para docs/ (site do GitHub Pages).

Varre output/<slug>/, lê debate_map.json + script.json, copia o podcast.mp3 para
docs/episodes/<slug>/, regenera docs/episodes.json (o manifesto que o
index.html consome) e gera docs/feed.xml (o feed RSS de podcast). Rode depois
de gerar um episódio novo:

    python scripts/publish.py
    git add docs && git commit -m "novo episódio" && git push

O feed.xml é o que permite assinar o Contraponto em Spotify, Apple Podcasts,
Pocket Casts e afins — e é o que dá download offline, porque esses apps
baixam episódio nativamente.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "output"
DOCS = ROOT / "docs"
PODCAST_NOME = "Contraponto"

# ---- configuração do feed RSS ----
SITE_URL = "https://contraponto.leoborja.com.br"
AUTOR = "Leo Borja"
# ⚠️ Este email fica PÚBLICO no feed XML e é usado por Spotify e Apple para
# verificar titularidade (o código de 8 dígitos chega nele).
# Trocar é seguro DEPOIS de a submissão estar concluída: a titularidade passa a
# viver na conta Spotify / Apple ID, não no endereço. Nunca trocar no meio de
# uma submissão pendente.
# Melhoria futura: criar contato@leoborja.com.br no Cloudflare Email Routing
# (grátis, o domínio já está lá) encaminhando para este Gmail. Aí o endereço
# público deixa de ser pessoal e o encaminhamento muda sem alterar o feed.
EMAIL_OWNER = "rgborja.leo@gmail.com"
CAPA = f"{SITE_URL}/cover.png"  # 1400x1400, mínimo exigido pela Apple
IDIOMA = "pt-BR"
# Categorias válidas da Apple: https://podcasters.apple.com/support/1691-apple-podcasts-categories
CATEGORIA = "News"
SUBCATEGORIA = "Politics"
DESCRICAO_PODCAST = (
    "Podcast de debate político gerado por IA. Cada episódio pega um tema em "
    "disputa e monta um debate profundo entre dois personagens que discordam de "
    "verdade, Karl Marx e Milton Friedman, mediados por Sócrates, que ensina o "
    "tema antes do debate e fecha mostrando onde os dois concordam e quais "
    "perguntas seguem abertas."
)


def _duracao_seg(mp3: Path) -> int:
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(mp3)],
            capture_output=True, text=True, timeout=30,
        )
        return int(float(out.stdout.strip()))
    except Exception:
        return 0


def _hhmmss(seg: int) -> str:
    h, resto = divmod(seg, 3600)
    m, s = divmod(resto, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def _pub_date(data_iso: str, ordem: int) -> str:
    """RFC 2822 a partir do YYYY-MM-DD do slug. A hora escalona por ordem para
    garantir ordenação estável quando dois episódios saem no mesmo dia."""
    try:
        d = datetime.strptime(data_iso, "%Y-%m-%d")
    except (ValueError, TypeError):
        d = datetime(2026, 1, 1)
    d = d.replace(hour=min(9 + ordem, 23), tzinfo=timezone.utc)
    return format_datetime(d)


def _numeracao_por_serie(episodes: list[dict]) -> list[tuple[int, int]]:
    """Devolve (temporada, numero_na_temporada) para cada episódio.

    A Apple espera <itunes:episode> reiniciando dentro de cada <itunes:season>, então
    a série principal é a temporada 1 e cada série nova ganha a sua. `episodes` vem do
    mais novo para o mais antigo; a numeração conta do mais antigo para o mais novo.
    """
    contagem: dict[int, int] = {}
    fora = []
    for e in reversed(episodes):
        temporada = (e.get("serie") or {}).get("numero", 1)
        contagem[temporada] = contagem.get(temporada, 0) + 1
        fora.append((temporada, contagem[temporada]))
    return list(reversed(fora))


def _gerar_feed(episodes: list[dict]) -> None:
    """Monta o RSS 2.0 com as extensões itunes exigidas pelos agregadores."""
    itens = []
    numeracao = _numeracao_por_serie(episodes)
    for i, e in enumerate(episodes):
        url_audio = f"{SITE_URL}/{e['audio']}"
        mp3 = DOCS / e["audio"]
        tamanho = mp3.stat().st_size if mp3.exists() else 0
        temporada, numero = numeracao[i]
        serie = e.get("serie") or {}
        # A Apple pede para NÃO repetir número de temporada/episódio no título, mas o
        # nome da série entra como prefixo porque é o único diferenciador que o Spotify
        # de fato mostra (ele ignora agrupamento por temporada).
        titulo_feed = f"{serie['nome']}: {e['titulo']}" if serie.get("nome") else e["titulo"]
        # <itunes:season> é o que faz a Apple agrupar (e só aparece a partir da 2ª
        # temporada). Vai em TODOS os episódios, inclusive os da série principal, senão
        # a temporada 1 fica sem marcação e o agrupamento sai pela metade.
        # <podcast:season name> dá temporada NOMEADA, que os apps Podcasting 2.0 exibem.
        tag_serie = f"\n      <itunes:season>{temporada}</itunes:season>"
        if serie.get("nome"):
            tag_serie += f'\n      <podcast:season name="{escape(serie["nome"])}">{temporada}</podcast:season>'

        resumo_partes = []
        if e.get("tese_esquerda"):
            resumo_partes.append(f"Esquerda: {e['tese_esquerda']}")
        if e.get("tese_direita"):
            resumo_partes.append(f"Direita: {e['tese_direita']}")
        if e.get("perguntas_abertas"):
            perguntas = " ".join(f"{p}" for p in e["perguntas_abertas"][:3])
            resumo_partes.append(f"Perguntas abertas: {perguntas}")
        if serie.get("projeto"):
            cabecalho = f"Projeto em debate: {serie['projeto']}"
            if serie.get("situacao"):
                cabecalho += f" ({serie['situacao']})"
            resumo_partes.insert(0, cabecalho)
        resumo = "\n\n".join(resumo_partes) or e.get("tema", "")

        itens.append(f"""    <item>
      <title>{escape(titulo_feed)}</title>
      <link>{SITE_URL}/#{escape(e['slug'])}</link>
      <guid isPermaLink="false">{escape(e['slug'])}</guid>
      <pubDate>{_pub_date(e.get('data', ''), len(episodes) - i)}</pubDate>
      <description>{escape(resumo)}</description>
      <itunes:summary>{escape(resumo)}</itunes:summary>
      <itunes:author>{escape(AUTOR)}</itunes:author>
      <itunes:duration>{_hhmmss(e.get('duracao_seg', 0))}</itunes:duration>
      <itunes:episode>{numero}</itunes:episode>{tag_serie}
      <itunes:episodeType>full</itunes:episodeType>
      <itunes:explicit>false</itunes:explicit>
      <enclosure url="{escape(url_audio)}" length="{tamanho}" type="audio/mpeg"/>
    </item>""")

    agora = format_datetime(datetime.now(timezone.utc))
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
     xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"
     xmlns:content="http://purl.org/rss/1.0/modules/content/"
     xmlns:podcast="https://podcastindex.org/namespace/1.0"
     xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{escape(PODCAST_NOME)}</title>
    <link>{SITE_URL}</link>
    <atom:link href="{SITE_URL}/feed.xml" rel="self" type="application/rss+xml"/>
    <language>{IDIOMA}</language>
    <copyright>{escape(AUTOR)}</copyright>
    <lastBuildDate>{agora}</lastBuildDate>
    <description>{escape(DESCRICAO_PODCAST)}</description>
    <itunes:summary>{escape(DESCRICAO_PODCAST)}</itunes:summary>
    <itunes:author>{escape(AUTOR)}</itunes:author>
    <itunes:type>episodic</itunes:type>
    <itunes:explicit>false</itunes:explicit>
    <itunes:image href="{CAPA}"/>
    <image>
      <url>{CAPA}</url>
      <title>{escape(PODCAST_NOME)}</title>
      <link>{SITE_URL}</link>
    </image>
    <itunes:owner>
      <itunes:name>{escape(AUTOR)}</itunes:name>
      <itunes:email>{escape(EMAIL_OWNER)}</itunes:email>
    </itunes:owner>
    <itunes:category text="{CATEGORIA}">
      <itunes:category text="{SUBCATEGORIA}"/>
    </itunes:category>
{chr(10).join(itens)}
  </channel>
</rss>
"""
    (DOCS / "feed.xml").write_text(feed, encoding="utf-8")


def main() -> None:
    episodes = []
    for pasta in sorted(OUTPUT.glob("*"), reverse=True):
        mp3 = pasta / "podcast.mp3"
        dmap = pasta / "debate_map.json"
        scr = pasta / "script.json"
        if not (mp3.exists() and dmap.exists() and scr.exists()):
            continue
        slug = pasta.name
        data = slug[:10] if slug[:10].count("-") == 2 else ""
        m = json.loads(dmap.read_text(encoding="utf-8"))
        s = json.loads(scr.read_text(encoding="utf-8"))

        # copia o áudio para docs/
        dest_dir = DOCS / "episodes" / slug
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(mp3, dest_dir / "podcast.mp3")

        episodes.append({
            "slug": slug,
            "titulo": s.get("titulo", m.get("tema", slug)),
            "tema": m.get("tema", ""),
            "data": data,
            "duracao_seg": _duracao_seg(mp3),
            "audio": f"episodes/{slug}/podcast.mp3",
            "tese_esquerda": m.get("tese_esquerda", ""),
            "tese_direita": m.get("tese_direita", ""),
            "consenso": m.get("consenso", []),
            "perguntas_abertas": m.get("perguntas_abertas", []),
            "fontes": m.get("fontes_chave", []),
            # Opcional. Série principal não tem: sai como temporada 1 sem badge, igual a antes.
            "serie": m.get("serie"),
        })

    DOCS.mkdir(exist_ok=True)
    manifesto = {"podcast": PODCAST_NOME, "episodes": episodes}
    (DOCS / "episodes.json").write_text(
        json.dumps(manifesto, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    _gerar_feed(episodes)
    print(f"✅ {len(episodes)} episódio(s) publicado(s) em docs/")
    for e in episodes:
        mm, ss = divmod(e["duracao_seg"], 60)
        print(f"   · {e['titulo']} ({mm}:{ss:02d})")
    print(f"📡 feed.xml gerado ({SITE_URL}/feed.xml)")
    if not (DOCS / "cover.png").exists():
        print("   ⚠️  docs/cover.png não existe. O feed exige capa de 1400x1400 no mínimo.")


if __name__ == "__main__":
    main()
