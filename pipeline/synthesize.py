"""Estágio [3]: mapa do debate.

Transforma a pesquisa bruta num mapa estruturado: tese de cada lado, pontos de
tensão com a visão dos dois lados + os fatos, onde há consenso, e perguntas em
aberto. Esse mapa é o que alimenta o roteiro. Salva debate_map.json.
"""
from __future__ import annotations

import json

from . import llm

_SYS = (
    "Você é um analista político imparcial. Sua função é mapear um debate de forma "
    "justa com os dois lados, ancorada nos fatos. Você não toma partido e não deixa "
    "nenhum lado virar espantalho."
)

_FMT = """
A partir da pesquisa abaixo, monte o MAPA DO DEBATE sobre o tema.

TEMA: {tema}

PESQUISA (JSON):
{pesquisa}

Regras:
- Cada lado deve aparecer na sua versão mais forte e honesta (steel-man).
- Ancore em fatos: use as afirmações verificadas; sinalize o que é incerto.
- Afirmações vindas de "videos" são RELATO DE CRIADOR (transcrição), não fato
  verificado: só use as marcadas confirmado/plausivel, e nunca como fonte única.
- Consenso = pontos em que, apesar da divergência, os dois lados concordam de fato.
- Perguntas em aberto = o que ainda não tem resposta / depende de dados futuros.

Responda APENAS com JSON:
{{
  "tema": "...",
  "tese_esquerda": "1-2 frases",
  "tese_direita": "1-2 frases",
  "pontos": [
    {{"tensao": "o eixo de discordância",
      "visao_esquerda": "...", "visao_direita": "...",
      "fatos": "o que é factual/verificado sobre esse ponto"}}
  ],
  "consenso": ["ponto em que os dois lados concordam", "..."],
  "perguntas_abertas": ["...", "..."],
  "fontes_chave": [{{"titulo": "...", "url": "..."}}]
}}
"""


def run(tema: str, research: dict, cfg: dict) -> dict:
    model = cfg["models"]["synthesize"]
    raw = llm.complete(
        model=model,
        system=_SYS,
        user=_FMT.format(tema=tema, pesquisa=json.dumps(research, ensure_ascii=False)),
        max_tokens=4096,
    )
    return llm.extract_json(raw)
