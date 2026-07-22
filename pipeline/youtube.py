"""YouTube como fonte — wrapper fino em cima da ferramenta `guru`.

Reaproveita /Users/leoborja/guru (search.py / extract.py / comments.py) para
buscar vídeos, transcrever (caption-first) e auditar comentários. Degrada com
elegância: se o guru não existir ou um vídeo falhar, retorna vazio e a pesquisa
segue só com a web.

Regra de velocidade: transcrição usa timeout curto — vídeo sem legenda cairia no
Whisper (lento), então estoura o timeout e é pulado, exatamente como a skill.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

GURU = Path("/Users/leoborja/guru")
GURU_PY = GURU / ".venv" / "bin" / "python"


def disponivel() -> bool:
    return GURU_PY.exists() and (GURU / "search.py").exists()


def _run(script: str, *args: str, timeout: int) -> str | None:
    try:
        proc = subprocess.run(
            [str(GURU_PY), str(GURU / script), *args],
            cwd=str(GURU),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout


def search(query: str, n: int = 10, timeout: int = 60) -> list[dict]:
    out = _run("search.py", query, "-n", str(n), timeout=timeout)
    if not out:
        return []
    try:
        return json.loads(out).get("results", [])
    except json.JSONDecodeError:
        return []


def transcribe(url: str, timeout: int = 90) -> dict | None:
    """Retorna {metadata, transcript} ou None (sem legenda/erro/timeout)."""
    out = _run("extract.py", url, "--stdout", timeout=timeout)
    if not out:
        return None
    try:
        data = json.loads(out)
    except json.JSONDecodeError:
        return None
    # se caiu no whisper e demorou, ainda vale; mas priorizamos caption
    return data


def comments(url: str, n: int = 20, timeout: int = 45) -> str:
    """Top comentários como texto (auditoria da multidão). '' se falhar."""
    out = _run("comments.py", url, "-n", str(n), timeout=timeout)
    if not out:
        return ""
    try:
        data = json.loads(out)
        itens = data.get("comments", data) if isinstance(data, dict) else data
        linhas = []
        for c in itens[:n]:
            if isinstance(c, dict):
                txt = c.get("text", "")
                likes = c.get("like_count", c.get("likes", ""))
                linhas.append(f"[{likes}👍] {txt}")
            else:
                linhas.append(str(c))
        return "\n".join(linhas)
    except json.JSONDecodeError:
        return out[:2000]
