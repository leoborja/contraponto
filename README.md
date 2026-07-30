# Contraponto 🎙️

**https://contraponto.leoborja.com.br**

Podcast de debate político gerado por IA. Cada episódio pega um tema em disputa (uma lei, uma política econômica, um modelo de país) e monta um **debate profundo de ~25-30 min** entre dois personagens que discordam de verdade — Karl Marx (esquerda) e Milton Friedman (direita) — mediados por Sócrates, que ensina o tema antes do debate e fecha com **onde os dois concordam** e **quais perguntas seguem abertas**.

## Como funciona

```
tema → pesquisa multi-fonte (web PT/EN + YouTube, com "cadeira do cético")
     → curriculum.json (o que um especialista sabe)
     → roteiro pro ouvido (3 vozes, debate eixo-por-eixo)
     → revisão (equilíbrio · factual · ouvido · profundidade + ponto-cego)
     → áudio ElevenLabs multi-voz → publicação no site
```

- **Pesquisa e escrita**: Claude (na sessão do Claude Code)
- **Vozes**: ElevenLabs `eleven_multilingual_v2`, 3 vozes PT-BR
- **Site**: GitHub Pages (`docs/`) com player mobile-first — posição salva por episódio, ±15/30s, velocidade, controles na tela de bloqueio

## Princípios editoriais

- **Steel-man dos dois lados**: cada personagem usa as posições reais dos pensadores (o Friedman do podcast inventou o voucher e o imposto de renda negativo, como o real)
- **Evidência com nome e sobrenome**: todo eixo cita estudos e números verificáveis; as fontes ficam no card de cada episódio
- **A discordância sobrevive**: concessões só depois de pushback; o fecho mapeia consenso real e desacordo real — sem falso equilíbrio nem falsa síntese
- **"Que dado te faria mudar de ideia?"** — ritual de todo episódio

## Estrutura do repo

| Caminho | Papel |
|---|---|
| `CLAUDE.md` | **Runbook completo** — como gerar um episódio do zero |
| `podcast.py` + `pipeline/` | CLI e módulos (áudio/TTS com normalização, YouTube via guru, utilitários) |
| `config/` | vozes/personas e calibrações |
| `scripts/publish.py` | publica episódios de `output/` para `docs/` |
| `scripts/custo.py` | consumo ElevenLabs do mês por voz |
| `docs/` | o site (Pages): player, manifesto de episódios, MP3s, logo |
| `branding/` | conceitos de logo (Gemini/Nano Banana Pro) |
| `output/` | artefatos por episódio (pesquisa, currículo, roteiro, revisão) — não versionado |

## Rodar

```bash
cp .env.example .env          # ELEVENLABS_API_KEY
pip install -r requirements.txt && brew install ffmpeg
# geração de episódio: ver CLAUDE.md (o motor de pesquisa/escrita é o Claude Code)
python podcast.py --audio output/<episodio>   # roteiro → MP3
python scripts/publish.py                     # → docs/ → git push publica
```
