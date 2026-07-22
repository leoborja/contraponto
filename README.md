# Podcast de Debate 🎙️

Você escolhe um tema (uma lei em debate, uma política econômica, um projeto de
cidade) e a ferramenta pesquisa em várias fontes de diferentes posicionamentos,
monta um **debate entre dois apresentadores** que discordam (esquerda × direita)
com um narrador neutro, revisa a si mesma e gera um **áudio de 10–15 min** pra
você ouvir na academia.

## Fluxo

```
tema → pesquisa → síntese → roteiro → revisa → melhora → RESUMO (você aprova)
                                                              ↓
                                                    --audio → ElevenLabs → MP3
```

Cada estágio salva seu resultado em `output/<data>-<slug>/`. O áudio (que consome
crédito do ElevenLabs) só roda quando você aprova o resumo.

A pesquisa cruza **web + YouTube**: além das buscas por ângulo, usa a ferramenta
`guru` (`/Users/leoborja/guru`) pra buscar vídeos, transcrever (caption-first) e
auditar comentários — com uma "cadeira do cético" obrigatória (sempre ≥1 fonte que
contradiz a tese dominante). Vídeo entra como relato de criador, nunca fonte única.
Desligável em `config/settings.yaml` (`pesquisa.youtube.ativo: false`).

## Setup

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # preencha ANTHROPIC_API_KEY e ELEVENLABS_API_KEY
brew install ffmpeg           # necessário pra montar o MP3 (pydub)
```

Depois, edite `config/personas.yaml` e cole os `voice_id` das três vozes
(narrador + 2 hosts) da sua conta ElevenLabs.

## Uso

```bash
# Etapa 1 — pesquisa e roteiro (imprime o resumo pra você aprovar)
python podcast.py "reforma tributária 2026: IVA dual"

# leia o resumo; se curtir, gere o áudio:
python podcast.py --audio output/2026-07-22-reforma-tributaria-2026-iva-dual
```

## Estrutura

| Arquivo | Papel |
|---|---|
| `podcast.py` | CLI que orquestra os estágios |
| `pipeline/research.py` | pesquisa multi-ângulo (factual/esquerda/direita/críticas) + verificação adversarial |
| `pipeline/youtube.py` | YouTube como fonte via `guru`: busca, transcreve e audita comentários (cadeira do cético) |
| `pipeline/synthesize.py` | mapa do debate: teses, tensões, consensos, perguntas abertas |
| `pipeline/script.py` | roteiro escrito pro ouvido, 3 vozes |
| `pipeline/review.py` | revisor (equilíbrio/factual/ouvido) + melhoria |
| `pipeline/summary.py` | resumo pra aprovação |
| `pipeline/audio.py` | ElevenLabs multi-voz + montagem do MP3 |
| `config/settings.yaml` | modelos, alvo de palavras, ângulos, thresholds do revisor |
| `config/personas.yaml` | nomes, `voice_id` e temperamento das vozes |

## Artefatos por episódio (`output/<data>-<slug>/`)

- `research.json` — pesquisa bruta com fontes citadas
- `debate_map.json` — o mapa do debate
- `script.json` / `script.md` — roteiro final (json p/ áudio, md p/ ler)
- `review.json` — histórico de críticas e scores
- `summary.md` — o resumo que você aprova
- `podcast.mp3` — o episódio (após `--audio`)
