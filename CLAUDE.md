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
1. `curriculum.json` — o que um especialista sabe: conceitos, história, evidências COM números, pensadores com posições REAIS, options_map dos pontos-crux, números-âncora. **Campos obrigatórios adicionais**: `pergunta_do_leo` (a pergunta na forma literal em que ele fez) e `eixo_inegociavel` para cada personagem (ver Regra Zero e "Eixo inegociável" abaixo)
2. `script.json` — turnos `{speaker: narrador|host_a|host_b, text}`. Auditar contra o curriculum.
3. `debate_map.json` — **schema FIXO lido pelo `publish.py`**, ver seção de lições
4. `review.json` — equilíbrio/factual/ouvido/profundidade (0-10) + passada de ponto-cego ("o que um PhD diria que falta?") ANTES do áudio. **Checar também**: a Regra Zero foi cumprida? cada personagem sustentou o `eixo_inegociavel`? o narrador ficou abaixo de 35%?
5. `summary.md` — resumo pro Leo aprovar
6. `script.md` — versão legível (gerar via `pipeline.script.to_markdown`)

### 3. Regras do roteiro

#### ⚠️ REGRA ZERO: responder a pergunta na forma em que o Leo fez (feedback do ep. 4)
Se a pergunta é de valor ("**deveriam** existir bilionários?"), o episódio tem que ter alguém defendendo **sim** e alguém defendendo **não**, com convicção. NÃO converter em pergunta de calibragem ("que tipo de bilionário é aceitável?", "como dosar a estabilidade?").

**Por quê**: no ep. 4 o Leo perguntou se deveriam existir bilionários e recebeu um episódio sobre que tipo de bilionário é tolerável. Reação dele: *"não sei se respondeu minha dúvida 100%, esperava mais algo da esquerda falando que não aceitava bilionários nunca"*. A causa é um viés sistemático: trocar pergunta de valor por pergunta de evidência, porque evidência é mais fácil de sustentar. A síntese pode aparecer, mas não pode ser o único destino do episódio.

**Como checar**: escrever a pergunta literal do Leo em `curriculum.json:pergunta_do_leo` e, no fim, apontar os turnos em que cada extremo foi defendido sem recuo.

#### Eixo inegociável (feedback do ep. 4)
Cada personagem tem UM eixo em que não concede nada e defende a versão forte da própria posição, declarado no `curriculum.json` ANTES de escrever o roteiro.

**Por quê**: "cadeira do cético" + "concessão após 2 rodadas" + "evidência nova por eixo" são boas regras isoladas, mas juntas premiam quem cede e punem quem sustenta. O ep. 4 passou em todas as métricas de equilíbrio e ainda assim frustrou, porque o Marx aceitou que riqueza de mercado não faz mal e com isso aceitou bilionários. **Concessão em todos os eixos vira convergência.**

**Corolário**: a tese radical tem que ser defendida por quem acredita nela, nunca ensinada pelo Sócrates. Colocar a posição maximalista na boca do narrador a neutraliza.

#### Peso das vozes
- **Narrador no máximo 35% das palavras.** Nos eps. 1 a 4 ficou entre 41% e 50%: o formato está derivando de debate para aula com ilustrações de debate
- **Os números vão para os personagens.** Dado técnico na boca de quem discute é argumento; na boca do professor é conteúdo. O Sócrates fica com definição, arbitragem e o fecho
- Medir **monólogo**, não só duração: nenhum bloco sem contraditório acima de ~4 min (o ep. 4 tinha 11)

#### Demais regras
- **Estrutura**: Sócrates define o mínimo necessário → debate eixo-por-eixo (cada crux percorre o options_map inteiro) → Brasil concreto → fecho: consensos + perguntas abertas + "se levar 3 coisas" com números-âncora
- **Dialética**: concessão só após 2 rodadas de pushback, EXCETO no eixo inegociável; evidência nova NOMEADA por eixo; ritual "que dado te faria mudar de ideia?"; a discordância filosófica SOBREVIVE ao fim
- **Personagens usam posições reais**: Friedman inventou o NIT e o voucher; usar isso
- **Casting**: Marx e Friedman são economistas e rendem em economia política. Em temas morais/culturais (drogas, IA) a dupla aperta — quando chegar lá, decidir com o Leo entre esticar os personagens ou abrir casting variável
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
4. **Deveriam existir bilionários?** (36:48, 3/ago) — Musk cruza US$ 1 tri (jun/26), Nozick em vez do argumento meritocrático, Bagchi-Svejnar (riqueza politicamente conectada arrasta crescimento; Brasil 27%, EUA 1%), Zucman (0,3% de imposto efetivo vs 7,5% de retorno), bloco da régua de pobreza (linha subiu 40% em jun/25 sem ninguém empobrecer)

## Backlog de temas (Leo escolhe)
Fim da escala 6x1 / semana de 4 dias · Legalizar drogas (Portugal vs Oregon) · Controle de aluguel e crise da moradia · Regular a IA (AI Act vs EUA vs PL 2338) · Nuclear na transição energética · Privatizar ou não (Correios/Sabesp/Petrobras) · **Medição e estatística política** (sobra do ep. 4: Pritchett, Reddy-Pogge, Ravallion, medidas FGT, MPI, Dinamarca×Paquistão — pesquisa já feita em `output/2026-08-03-bilionarios/curriculum.json`)

## Histórico de lições (não repetir erros)
- Travessões quebraram a entonação do ep. 2 (75 ocorrências) → regras TTS acima + normalizador
- Revisor v1 dava 9/9/9 em roteiro raso → eixo "profundidade" + auditoria contra curriculum + ponto-cego (pegou erros factuais nos eps. 2, 3 e 4 antes do áudio)
- **O primeiro rascunho é sistematicamente descuidado com atualidade de fonte** — no ep. 4 dados de 1987-2002 (Bagchi-Svejnar) foram apresentados como atuais. Sempre checar o ANO de cada estudo antes de colocar número na boca de personagem; quando o dado é velho, fazer o adversário apontar isso (vira dialética em vez de erro)
- Ep. 4 passou em equilíbrio (Marx 31%, Friedman 28%) e ainda assim frustrou o Leo → métrica de palavras não mede convicção. Ver Regra Zero e eixo inegociável
- Trilha/série de episódios foi considerada e DESCARTADA — um episódio completo é melhor
- **`debate_map.json` tem schema fixo lido pelo `publish.py`**: `tema`, `modo`, `tese_esquerda`, `tese_direita`, `pontos[{tensao, visao_esquerda, visao_direita}]`, `consenso[]`, `perguntas_abertas[]`, `fontes_chave[{titulo,url}]`. Inventar chaves novas publica um card VAZIO sem erro nenhum (quase aconteceu no ep. 4) — sempre conferir contra o debate_map do episódio anterior
- Medir monólogo, não só duração: o ep. 4 tinha 11 min de narrador seguido sem contraditório. Quebrar com intervenção dos personagens vale mais que cortar palavras
- Evitar CAIXA ALTA para ênfase no roteiro (o TTS pode soletrar); siglas conhecidas como IBGE e UBS são lidas corretamente
- Cache DNS negativo: não testar domínio antes do registro existir (roteador guarda NXDOMAIN por ~30 min)
