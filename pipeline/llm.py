"""Helper fino em cima da Anthropic API.

Centraliza: criação do client, chamadas de texto, chamadas com web_search,
e extração robusta de JSON da resposta do modelo.
"""
from __future__ import annotations

import json
import os
import re
from typing import Any

import anthropic

_client: anthropic.Anthropic | None = None


def get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        key = os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise RuntimeError("ANTHROPIC_API_KEY não definida (veja .env.example)")
        _client = anthropic.Anthropic(api_key=key)
    return _client


def _collect_text(resp: Any) -> str:
    """Concatena todos os blocos de texto da resposta (ignora tool_use/results)."""
    parts = []
    for block in resp.content:
        if getattr(block, "type", None) == "text":
            parts.append(block.text)
    return "\n".join(parts).strip()


def complete(
    model: str,
    system: str,
    user: str,
    max_tokens: int = 4096,
    web_search: bool = False,
    max_searches: int = 5,
) -> str:
    """Uma chamada de texto. Se web_search=True, habilita a ferramenta de busca
    nativa da Anthropic (o modelo decide quando/quanto buscar)."""
    client = get_client()
    kwargs: dict[str, Any] = dict(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    if web_search:
        kwargs["tools"] = [
            {
                "type": "web_search_20250305",
                "name": "web_search",
                "max_uses": max_searches,
            }
        ]
    resp = client.messages.create(**kwargs)
    return _collect_text(resp)


def extract_json(text: str) -> Any:
    """Extrai JSON de uma resposta do modelo.

    Tenta, em ordem: bloco ```json ... ```, primeiro objeto/array balanceado,
    e por fim o texto inteiro. Levanta ValueError se nada parsear.
    """
    # 1) bloco cercado ```json
    m = re.search(r"```(?:json)?\s*(.+?)```", text, re.DOTALL)
    candidates = []
    if m:
        candidates.append(m.group(1))
    # 2) do primeiro { ou [ até o último } ou ]
    start = min(
        (i for i in (text.find("{"), text.find("[")) if i != -1),
        default=-1,
    )
    if start != -1:
        end = max(text.rfind("}"), text.rfind("]"))
        if end > start:
            candidates.append(text[start : end + 1])
    candidates.append(text)

    for c in candidates:
        try:
            return json.loads(c.strip())
        except json.JSONDecodeError:
            continue
    raise ValueError(f"Não consegui extrair JSON da resposta:\n{text[:500]}")
