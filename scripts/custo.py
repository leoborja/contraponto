#!/usr/bin/env python3
"""Mostra o consumo ElevenLabs do podcast (por voz) no mês corrente.

Uso:  python scripts/custo.py            # mês atual
      python scripts/custo.py 2026-06    # mês específico
"""
from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# vozes do podcast (personas.yaml) — prefixos dos nomes no ElevenLabs
VOZES_PODCAST = {
    "Cassio Cruz": "Sócrates",
    "Yuri - Deep": "Karl Marx",
    "Vagner de Souza": "Milton Friedman",
}

# Plano do Leo: SCALE — Multilingual v2 = US$0,10/1k chars, 2.990.000 chars/mês inclusos
PRECO_1K_MULTI_V2 = 0.10
INCLUSO_MES = 2_990_000


def main() -> None:
    key = None
    env = ROOT / ".env"
    for line in env.read_text().splitlines():
        if line.startswith("ELEVENLABS_API_KEY="):
            key = line.split("=", 1)[1].strip()
    if not key:
        sys.exit("ELEVENLABS_API_KEY não encontrada no .env")

    if len(sys.argv) > 1:
        ano, mes = map(int, sys.argv[1].split("-"))
    else:
        hoje = dt.date.today()
        ano, mes = hoje.year, hoje.month
    ini = int(dt.datetime(ano, mes, 1).timestamp() * 1000)
    prox = dt.datetime(ano + (mes == 12), (mes % 12) + 1, 1)
    fim = int(prox.timestamp() * 1000)

    url = (f"https://api.elevenlabs.io/v1/usage/character-stats"
           f"?start_unix={ini}&end_unix={fim}&breakdown_type=voice")
    out = subprocess.run(["curl", "-s", "-H", f"xi-api-key: {key}", url],
                         capture_output=True, text=True).stdout
    d = json.loads(out)
    if "usage" not in d:
        sys.exit(f"resposta inesperada: {out[:200]}")

    podcast, outros = 0, 0
    print(f"\n📊 ElevenLabs — {ano}-{mes:02d}\n")
    for voz, serie in sorted(d["usage"].items(), key=lambda kv: -sum(kv[1])):
        s = sum(serie)
        if not s:
            continue
        papel = next((p for pref, p in VOZES_PODCAST.items() if voz.startswith(pref)), None)
        if papel:
            podcast += s
            print(f"  🎙️ {papel:16s} ({voz[:30]}): {s:>9,.0f}")
        else:
            outros += s
    total = podcast + outros
    print(f"\n  🎙️ PODCAST: {podcast:,.0f} chars | outros usos: {outros:,.0f} | total conta: {total:,.0f}")
    print(f"  cota Scale (multilingual v2): {total:,.0f} / {INCLUSO_MES:,.0f} ({100*total/INCLUSO_MES:.0f}% usada)")
    print(f"  podcast a US$0,10/1k: US$ {podcast/1000*PRECO_1K_MULTI_V2:.2f}"
          f" ({'dentro da cota inclusa — custo marginal zero' if total <= INCLUSO_MES else 'ACIMA da cota — excedente cobrado'})")
    print()


if __name__ == "__main__":
    main()
