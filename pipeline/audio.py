"""Estágio [8]: síntese de voz (ElevenLabs) + montagem do MP3.

Lê script.json, mapeia cada speaker para um voice_id em personas.yaml, gera o
áudio turno a turno via ElevenLabs e concatena tudo num único MP3, com uma
pequena pausa entre falas. Requer ffmpeg instalado (pydub).
"""
from __future__ import annotations

import io
import os

import requests

_TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"


def _tts(text: str, voice_id: str, voice_settings: dict, cfg: dict) -> bytes:
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        raise RuntimeError("ELEVENLABS_API_KEY não definida (veja .env.example)")
    url = _TTS_URL.format(voice_id=voice_id)
    resp = requests.post(
        url,
        headers={"xi-api-key": key, "accept": "audio/mpeg", "content-type": "application/json"},
        params={"output_format": cfg["audio"]["output_format"]},
        json={
            "text": text,
            "model_id": cfg["audio"]["model_id"],
            "voice_settings": voice_settings,
        },
        timeout=120,
    )
    resp.raise_for_status()
    return resp.content


def generate(script: dict, personas: dict, cfg: dict, out_path: str) -> str:
    """Gera o MP3 final em out_path. Retorna o caminho."""
    from pydub import AudioSegment  # import tardio: só precisa de ffmpeg no --audio

    speaker_map = {
        "narrador": personas["narrador"],
        "host_a": personas["host_a"],
        "host_b": personas["host_b"],
    }
    pausa = AudioSegment.silent(duration=cfg["audio"]["pausa_entre_turnos_ms"])
    final = AudioSegment.empty()

    turnos = script.get("turnos", [])
    for i, t in enumerate(turnos, 1):
        persona = speaker_map.get(t["speaker"])
        if persona is None:
            print(f"  ! turno {i}: speaker desconhecido '{t['speaker']}', pulando")
            continue
        if persona["voice_id"].startswith("COLOQUE_"):
            raise RuntimeError(
                f"voice_id não configurado para '{t['speaker']}' em config/personas.yaml"
            )
        print(f"  · áudio {i}/{len(turnos)} ({t['speaker']})")
        audio_bytes = _tts(t["text"], persona["voice_id"], persona["voice_settings"], cfg)
        seg = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")
        final += seg + pausa

    final.export(out_path, format="mp3")
    return out_path
