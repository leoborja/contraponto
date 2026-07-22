"""Estágio [7]: resumo pra aprovação.

Você não lê o roteiro inteiro — lê um resumo curto: do que o episódio trata, os
pontos de tensão, onde os dois lados concordam, as perguntas em aberto, os scores
do revisor, duração estimada e as fontes. Com isso você decide se gera o áudio.
"""
from __future__ import annotations


def build(tema: str, mapa: dict, script: dict, criticas: list[dict], cfg: dict) -> str:
    ppm = cfg["roteiro"]["palavras_por_minuto"]
    palavras = script.get("palavras", 0)
    dur = palavras / ppm
    ultima = criticas[-1]["scores"] if criticas else {}

    L = [f"# Resumo — {script.get('titulo', tema)}", ""]
    L.append(f"**Tema:** {tema}")
    L.append(f"**Duração estimada:** ~{dur:.0f} min ({palavras} palavras)")
    if ultima:
        L.append(
            f"**Revisor:** equilíbrio {ultima.get('equilibrio')}/10 · "
            f"factual {ultima.get('factual')}/10 · ouvido {ultima.get('ouvido')}/10"
        )
    L.append("")

    L.append("## Os dois lados")
    L.append(f"- **Esquerda:** {mapa.get('tese_esquerda', '—')}")
    L.append(f"- **Direita:** {mapa.get('tese_direita', '—')}")
    L.append("")

    if mapa.get("pontos"):
        L.append("## Pontos de tensão")
        for p in mapa["pontos"]:
            L.append(f"- {p.get('tensao', '—')}")
        L.append("")

    if mapa.get("consenso"):
        L.append("## Onde os dois concordam")
        for c in mapa["consenso"]:
            L.append(f"- {c}")
        L.append("")

    if mapa.get("perguntas_abertas"):
        L.append("## Perguntas em aberto")
        for q in mapa["perguntas_abertas"]:
            L.append(f"- {q}")
        L.append("")

    fontes = mapa.get("fontes_chave", [])
    if fontes:
        L.append("## Fontes-chave")
        for f in fontes[:10]:
            L.append(f"- [{f.get('titulo', f.get('url', '—'))}]({f.get('url', '')})")
        L.append("")

    L.append("---")
    L.append("Para gerar o áudio: `python podcast.py --audio <pasta>`")
    return "\n".join(L)
