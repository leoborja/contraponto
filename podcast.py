#!/usr/bin/env python3
"""Gerador de podcast de debate político — CLI.

Fluxo (duas etapas):
  1) python podcast.py "tema aqui"
       pesquisa → síntese → roteiro → revisa → melhora → resumo
       (salva tudo em output/<data>-<slug>/ e imprime o resumo pra você aprovar)

  2) python podcast.py --audio output/<data>-<slug>
       gera o MP3 com ElevenLabs a partir do roteiro já aprovado

Cada estágio persiste em disco; o áudio (que custa) só roda no passo 2.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

import yaml
from dotenv import load_dotenv

from pipeline import audio, research, review, script as script_mod, summary, synthesize

ROOT = Path(__file__).parent
OUTPUT = ROOT / "output"


def _load_cfg() -> tuple[dict, dict]:
    with open(ROOT / "config" / "settings.yaml", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    with open(ROOT / "config" / "personas.yaml", encoding="utf-8") as f:
        personas = yaml.safe_load(f)
    return cfg, personas


def _slug(tema: str) -> str:
    s = unicodedata.normalize("NFKD", tema).encode("ascii", "ignore").decode()
    s = re.sub(r"[^\w\s-]", "", s.lower()).strip()
    return re.sub(r"[\s_-]+", "-", s)[:50]


def _save(pasta: Path, nome: str, data) -> None:
    path = pasta / nome
    if nome.endswith(".json"):
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        path.write_text(data, encoding="utf-8")


def cmd_gerar(tema: str) -> None:
    cfg, personas = _load_cfg()
    pasta = OUTPUT / f"{date.today().isoformat()}-{_slug(tema)}"
    pasta.mkdir(parents=True, exist_ok=True)
    print(f"\n📁 {pasta}\n")

    print("[2/7] Pesquisando (multi-ângulo + verificação)...")
    pesquisa = research.run(tema, cfg)
    _save(pasta, "research.json", pesquisa)

    print("[3/7] Sintetizando o mapa do debate...")
    mapa = synthesize.run(tema, pesquisa, cfg)
    _save(pasta, "debate_map.json", mapa)

    print("[4/7] Escrevendo o roteiro pro ouvido...")
    roteiro = script_mod.run(tema, mapa, personas, cfg)

    print("[5-6/7] Revisando e melhorando...")
    roteiro, criticas = review.run(mapa, roteiro, cfg)
    _save(pasta, "script.json", roteiro)
    _save(pasta, "script.md", script_mod.to_markdown(roteiro, personas, cfg))
    _save(pasta, "review.json", criticas)

    print("[7/7] Montando o resumo...")
    resumo = summary.build(tema, mapa, roteiro, criticas, cfg)
    _save(pasta, "summary.md", resumo)

    print("\n" + "=" * 60)
    print(resumo)
    print("=" * 60)
    print(f"\n✅ Pronto. Para gerar o áudio:\n   python podcast.py --audio {pasta}\n")


def cmd_audio(pasta_str: str) -> None:
    cfg, personas = _load_cfg()
    pasta = Path(pasta_str)
    script_path = pasta / "script.json"
    if not script_path.exists():
        sys.exit(f"Não achei {script_path}. Rode a etapa 1 primeiro.")
    roteiro = json.loads(script_path.read_text(encoding="utf-8"))
    out = pasta / "podcast.mp3"
    print("Gerando áudio com ElevenLabs...")
    audio.generate(roteiro, personas, cfg, str(out))
    print(f"\n🎧 {out}\n")


def main() -> None:
    load_dotenv(ROOT / ".env")
    p = argparse.ArgumentParser(description="Gerador de podcast de debate político")
    p.add_argument("tema", nargs="?", help="tema do episódio (etapa 1)")
    p.add_argument("--audio", metavar="PASTA", help="gerar MP3 de uma pasta já processada (etapa 2)")
    args = p.parse_args()

    if args.audio:
        cmd_audio(args.audio)
    elif args.tema:
        cmd_gerar(args.tema)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
