"""Estágios [5] e [6]: revisor embutido + melhoria.

O revisor pontua o roteiro em três eixos (equilíbrio entre lados, fidelidade
factual, e quão bem soa no ouvido) e lista problemas concretos. Se algum score
fica abaixo do mínimo configurado, um passo de melhoria reescreve o roteiro
atendendo à crítica. Repete até passar ou atingir max_rodadas.
"""
from __future__ import annotations

import json

from . import llm, script as script_mod

_SYS_CRITICO = (
    "Você é um editor crítico e exigente de podcast jornalístico. Avalia sem dó, "
    "mas suas críticas são concretas e acionáveis. Você defende o ouvinte."
)

_FMT_CRITICO = """
Avalie o ROTEIRO abaixo contra o MAPA DO DEBATE que o originou.

MAPA DO DEBATE:
{mapa}

ROTEIRO (turnos JSON):
{roteiro}

Avalie três eixos, nota 0-10:
- equilibrio: nenhum lado virou espantalho? os dois aparecem na versão mais forte?
- factual: tudo ancorado no mapa/fatos? nada inventado ou distorcido?
- ouvido: soa como fala natural? frases curtas, sem lista, com sinalização verbal?

Responda APENAS com JSON:
{{
  "scores": {{"equilibrio": 0-10, "factual": 0-10, "ouvido": 0-10}},
  "problemas": ["problema concreto e como corrigir", "..."],
  "veredito": "aprovado|revisar"
}}
"""

_SYS_MELHORA = (
    "Você é roteirista de podcast. Reescreve o roteiro atendendo à crítica do editor, "
    "preservando o que já está bom. Mantém o formato de turnos e a escrita pro ouvido."
)

_FMT_MELHORA = """
Reescreva o ROTEIRO corrigindo os PROBLEMAS apontados pelo editor. Mantenha o alvo
de {pmin}-{pmax} palavras, o formato de 3 vozes e a escrita pro ouvido.

PROBLEMAS A CORRIGIR:
{problemas}

ROTEIRO ATUAL (JSON):
{roteiro}

Responda APENAS com JSON no mesmo formato:
{{"titulo": "...", "turnos": [{{"speaker": "...", "text": "..."}}]}}
"""


def _critica(mapa: dict, script: dict, model: str) -> dict:
    raw = llm.complete(
        model=model,
        system=_SYS_CRITICO,
        user=_FMT_CRITICO.format(
            mapa=json.dumps(mapa, ensure_ascii=False),
            roteiro=json.dumps(script.get("turnos", []), ensure_ascii=False),
        ),
        max_tokens=2000,
    )
    return llm.extract_json(raw)


def _melhora(script: dict, problemas: list[str], model: str, cfg: dict) -> dict:
    raw = llm.complete(
        model=model,
        system=_SYS_MELHORA,
        user=_FMT_MELHORA.format(
            problemas="\n".join(f"- {p}" for p in problemas),
            roteiro=json.dumps(script, ensure_ascii=False),
            pmin=cfg["roteiro"]["palavras_min"],
            pmax=cfg["roteiro"]["palavras_max"],
        ),
        max_tokens=8192,
    )
    data = llm.extract_json(raw)
    data["palavras"] = sum(len(t["text"].split()) for t in data.get("turnos", []))
    return data


def _passou(crit: dict, cfg: dict) -> bool:
    s = crit.get("scores", {})
    r = cfg["review"]
    return (
        s.get("equilibrio", 0) >= r["min_equilibrio"]
        and s.get("ouvido", 0) >= r["min_ouvido"]
        and s.get("factual", 0) >= r["min_factual"]
    )


def run(mapa: dict, script: dict, cfg: dict) -> tuple[dict, list[dict]]:
    """Retorna (roteiro_final, historico_de_criticas)."""
    model = cfg["models"]["review"]
    historico: list[dict] = []
    atual = script
    for rodada in range(cfg["review"]["max_rodadas"] + 1):
        crit = _critica(mapa, atual, model)
        crit["rodada"] = rodada
        historico.append(crit)
        s = crit.get("scores", {})
        print(
            f"  · revisão rodada {rodada}: equilíbrio={s.get('equilibrio')} "
            f"factual={s.get('factual')} ouvido={s.get('ouvido')}"
        )
        if _passou(crit, cfg) or rodada == cfg["review"]["max_rodadas"]:
            break
        atual = _melhora(atual, crit.get("problemas", []), model, cfg)
    return atual, historico
