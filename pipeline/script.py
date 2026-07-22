"""Estágio [4]: roteiro escrito PRO OUVIDO.

Converte o mapa do debate num roteiro de 3 vozes (narrador + 2 hosts) em formato
de turnos. Foco total em oralidade: frases curtas, sem listas, com sinalização
verbal ("primeiro... por outro lado... mas tem um porém"). Salva script.json e
script.md (legível).
"""
from __future__ import annotations

import json

from . import llm

_SYS = (
    "Você é roteirista de podcast. Escreve para o OUVIDO, não para o olho: frases "
    "curtas, linguagem falada, zero listas ou bullets, sinalização verbal entre ideias. "
    "Monta um debate afiado mas civil entre dois apresentadores que discordam de verdade, "
    "com um narrador neutro conduzindo."
)

_FMT = """
Escreva o roteiro do episódio a partir do MAPA DO DEBATE.

TEMA: {tema}

MAPA DO DEBATE (JSON):
{mapa}

PERSONAS:
- narrador ({narrador_nome}): {narrador_papel}
- host_a ({host_a_nome}): {host_a_papel}
- host_b ({host_b_nome}): {host_b_papel}

Requisitos:
- Idioma: {idioma}. Tom: afiado mas civil. Nunca caricato, nunca espantalho.
- Alvo: entre {pmin} e {pmax} palavras no TOTAL (≈ 10-15 min falados).
- Estrutura: narrador abre o tema em poucas frases → debate alternando host_a e
  host_b pelos pontos de tensão (cada um ancorado em fatos, reconhecendo o ponto
  forte do outro quando é real) → narrador fecha com ONDE OS DOIS CONCORDAM e as
  PERGUNTAS EM ABERTO.
- Escreva pro ouvido: frases curtas, conectivos falados, nada de "primeiramente/
  em suma". Pode usar reticências e perguntas retóricas.

Responda APENAS com JSON:
{{
  "titulo": "título curto e chamativo do episódio",
  "turnos": [
    {{"speaker": "narrador|host_a|host_b", "text": "fala corrida, sem marcações"}}
  ]
}}
"""


def _contar_palavras(turnos: list[dict]) -> int:
    return sum(len(t["text"].split()) for t in turnos)


def run(tema: str, mapa: dict, personas: dict, cfg: dict) -> dict:
    model = cfg["models"]["script"]
    raw = llm.complete(
        model=model,
        system=_SYS,
        user=_FMT.format(
            tema=tema,
            mapa=json.dumps(mapa, ensure_ascii=False),
            idioma=cfg["idioma"],
            pmin=cfg["roteiro"]["palavras_min"],
            pmax=cfg["roteiro"]["palavras_max"],
            narrador_nome=personas["narrador"]["nome"],
            narrador_papel=personas["narrador"]["papel"],
            host_a_nome=personas["host_a"]["nome"],
            host_a_papel=personas["host_a"]["papel"],
            host_b_nome=personas["host_b"]["nome"],
            host_b_papel=personas["host_b"]["papel"],
        ),
        max_tokens=8192,
    )
    data = llm.extract_json(raw)
    data["palavras"] = _contar_palavras(data.get("turnos", []))
    return data


def to_markdown(script: dict, personas: dict, cfg: dict) -> str:
    """Versão legível do roteiro (só para inspeção humana)."""
    ppm = cfg["roteiro"]["palavras_por_minuto"]
    dur = script.get("palavras", 0) / ppm
    nomes = {k: personas[k]["nome"] for k in ("narrador", "host_a", "host_b")}
    linhas = [
        f"# {script.get('titulo', 'Episódio')}",
        "",
        f"_{script.get('palavras', 0)} palavras · ~{dur:.0f} min_",
        "",
    ]
    for t in script.get("turnos", []):
        nome = nomes.get(t["speaker"], t["speaker"])
        linhas.append(f"**{nome}:** {t['text']}")
        linhas.append("")
    return "\n".join(linhas)
