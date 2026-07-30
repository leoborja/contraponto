# Contraponto — Runbook Operacional

Podcast de debate político gerado por IA. Marx (esquerda) × Friedman (direita), mediados por Sócrates. Site: **https://contraponto.leoborja.com.br**

## Decisão de arquitetura (NÃO mudar sem o Leo pedir)
- **Motor de pesquisa/escrita = Claude Code na sessão** (grátis, qualidade máxima). NUNCA usar a Anthropic API metered (`pipeline/llm.py` e `research.py` existem mas estão dormentes — Leo recusou API paga).
- **Só o áudio custa dinheiro** (ElevenLabs, plano Scale — na prática custo marginal zero; checar com `python scripts/custo.py`).
- **Modo profundo é o padrão** (~25-30 min): Leo quer virar especialista no tema, não só se informar. Um episódio completo > vários rasos.

## Como gerar um episódio (o fluxo completo)

### 1. Pesquisa (na sessão, WebSearch/WebFetch)
- Leque multi-ângulo em paralelo: factual, esquerda, direita, críticas técnicas + **PT e EN**
- **Cadeira do cético obrigatória**: sempre ≥1 fonte que contradiz a tese dominante
- Ler fontes canônicas INTEIRAS (WebFetch), não só snippets
- YouTube opcional via `guru` (`~/guru`, wrapper `pipeline/youtube.py`) — vídeo é relato de criador, nunca fonte única
- Checklist do professor: triangular o dado mais forte, evidência de saúde/bem-estar, alternativas rivais ao tema, efeitos de captura de preço, auditar premissas macro

### 2. Artefatos (salvar em `output/<data>-<slug>/`)
1. `curriculum.json` — o que um especialista sabe: conceitos, história, evidências COM números, pensadores com posições REAIS, options_map dos pontos-crux, números-âncora
2. `script.json` — turnos `{speaker: narrador|host_a|host_b, text}`. Auditar contra o curriculum.
3. `debate_map.json` — teses, tensões, consensos, perguntas abertas, fontes (alimenta o card do site)
4. `review.json` — equilíbrio/factual/ouvido/profundidade (0-10) + passada de ponto-cego ("o que um PhD diria que falta?") ANTES do áudio
5. `summary.md` — resumo pro Leo aprovar
6. `script.md` — versão legível (gerar via `pipeline.script.to_markdown`)

### 3. Regras do roteiro
- **Estrutura**: Sócrates ensina primeiro (definições, variantes, história) → debate eixo-por-eixo (cada crux percorre o options_map inteiro) → Brasil concreto → fecho: consensos + perguntas abertas + "se levar 3 coisas" com números-âncora
- **Dialética**: concessão só após 2 rodadas de pushback; evidência nova NOMEADA por eixo; ritual "que dado te faria mudar de ideia?"; a discordância filosófica SOBREVIVE ao fim
- **Personagens usam posições reais**: Friedman inventou o NIT e o voucher; usar isso
- **Abertura**: cold open visceral (caso concreto, número que choca) — nunca "hoje vamos falar de..."
- **⚠️ REGRAS TTS (feedback do Leo, inegociáveis)**:
  - NUNCA travessão (—) | NUNCA reticências (...) | enumerações de no máx. 2 itens por vírgula (listas longas viram frase corrida com "e")
  - `audio.py:normalizar_tts()` limpa —/... como rede de segurança, mas enumeração é estilo: escrever certo na fonte
  - Números por extenso ("três vírgula dois pontos percentuais")
- **Alvo**: 4.200-4.800 palavras ≈ 25-30 min (texto TTS-safe roda ~147-165 wpm; ep. 3 deu 4.065 palavras = 27:34)

### 4. Áudio e publicação
```bash
python podcast.py --audio output/<pasta>     # ElevenLabs → podcast.mp3 (~US$2,50/ep)
python scripts/publish.py                     # copia MP3 pra docs/ + regenera episodes.json
git add -A && git commit && git push          # site atualiza em ~1 min
```
- Python: `/opt/homebrew/bin/python3.12` | Segredos: `.env` (ELEVENLABS_API_KEY) — NUNCA commitar
- `output/` é gitignored (roteiros ficam só locais); o site publica MP3 + card

## Vozes (config/personas.yaml)
| Papel | Nome | Voz ElevenLabs |
|---|---|---|
| narrador | Sócrates | Cassio Cruz `TY3h8ANhQUsJaa0Bga5F` |
| host_a (esquerda) | Karl Marx | Yuri `WSBwiRQRmi2mEG7BfKwS` |
| host_b (direita) | Milton Friedman | Vagner de Souza `IlrWo5tGgTuxNTHyGhWD` |

Modelo `eleven_multilingual_v2`, PT-BR.

## Site e domínio
- **https://contraponto.leoborja.com.br** — GitHub Pages (repo `leoborja/contraponto`, serve de `/docs`), HTTPS enforced
- DNS: CNAME `contraponto` → `leoborja.github.io` na zona leoborja.com.br do Cloudflare, **DNS-only (nuvem cinza)** — não ligar o proxy (quebra o cert do GitHub)
- `leoborja.github.io/contraponto` redireciona pro domínio
- Player: posição salva por episódio (localStorage), ±15/30s, velocidade, MediaSession na tela de bloqueio. Relógios ficam SOB a barra (não na linha dos botões — estourava no mobile)
- Logo: `docs/logo.png` (header/capa) + `docs/icon.png` (favicon, crop do mic). Conceitos alternativos em `branding/`. Gerada com Gemini `gemini-3-pro-image` (key em `~/livro-colorir/.env`)

## Episódios publicados
1. **Renda Básica Universal: o dossiê completo** (33:09, 22/jul) — NIT/Friedman, 5 portas de financiamento, Quênia/Alasca/Irã/SIME-DIME, Lei Suplicy
2. **O modelo Bukele: segurança a qualquer preço?** (27:42, 29/jul) — armadilha de Formosa como parábola, pacto El Faro, mano dura 2003, CV/PCC nascidos em presídios
3. **Educação: pública, privada, e quem paga a conta** (27:34, 30/jul) — matriz financiar×operar, tribunal dos 70 anos de vouchers, Tooley, Jackson, a grande inversão, Sobral

## Backlog de temas (Leo escolhe)
Fim da escala 6x1 / semana de 4 dias · Taxar os super-ricos (Zucman/G20) · Legalizar drogas (Portugal vs Oregon) · Controle de aluguel e crise da moradia · Regular a IA (AI Act vs EUA vs PL 2338) · Nuclear na transição energética · Privatizar ou não (Correios/Sabesp/Petrobras)

## Histórico de lições (não repetir erros)
- Travessões quebraram a entonação do ep. 2 (75 ocorrências) → regras TTS acima + normalizador
- Revisor v1 dava 9/9/9 em roteiro raso → eixo "profundidade" + auditoria contra curriculum + ponto-cego (pegou erros factuais nos eps. 2 e 3 antes do áudio)
- Trilha/série de episódios foi considerada e DESCARTADA — um episódio completo é melhor
- Cache DNS negativo: não testar domínio antes do registro existir (roteador guarda NXDOMAIN por ~30 min)
