#!/usr/bin/env python3
"""Publica os episódios de output/ para docs/ (site do GitHub Pages).

Varre output/<slug>/, lê debate_map.json + script.json, copia o podcast.mp3 para
docs/episodes/<slug>/ e regenera docs/episodes.json (o manifesto que o
index.html consome). Rode depois de gerar um episódio novo:

    python scripts/publish.py
    git add docs && git commit -m "novo episódio" && git push
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "output"
DOCS = ROOT / "docs"
PODCAST_NOME = "Contraponto"


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
        })

    DOCS.mkdir(exist_ok=True)
    manifesto = {"podcast": PODCAST_NOME, "episodes": episodes}
    (DOCS / "episodes.json").write_text(
        json.dumps(manifesto, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"✅ {len(episodes)} episódio(s) publicado(s) em docs/")
    for e in episodes:
        mm, ss = divmod(e["duracao_seg"], 60)
        print(f"   · {e['titulo']} ({mm}:{ss:02d})")


if __name__ == "__main__":
    main()
