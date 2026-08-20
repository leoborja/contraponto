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
4. `review.json` — **ver a seção "Revisor v3" abaixo**. Obrigatório ANTES do áudio
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
- **Narrador no máximo 35% das palavras.** ⚠️ **CORREÇÃO de 8/ago**: eu havia escrito aqui que "nos eps. 1 a 4 ficou entre 41% e 50%". **Isso estava errado.** Medindo: ep. 1 = 25%, ep. 2 = 31%, ep. 3 = 22%, ep. 4 = 41%. **Só o ep. 4 estourou.** Eu medi um episódio, generalizei para quatro e escrevi como fato. A regra do teto segue válida, a justificativa histórica não era
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
- **Alvo**: 4.200-4.800 palavras ≈ 27-31 min, **mas é referência e não teto** (feedback do Leo em 10/ago).
  - ⚠️ **DIMENSIONAR O ORÇAMENTO PELO NÚMERO DE DOMÍNIOS** (lição do ep. 8): o ep. 7 ensinou a *fixar* orçamento no curriculum e não ensinou a *calibrá-lo*. No ep. 8 eu fixei 4.700 e entreguei 5.729, doze por cento acima, porque era um episódio de **dois domínios** (droga e órgão), cada um com evidência, casos e bloco brasileiro próprios. Não havia gordura para cortar: medi n-gramas e os únicos repetidos eram datas e bookends intencionais. **Regra**: ~4.700 palavras para tema único, ~5.800 para tema duplo. Estourar sem prolixidade é erro de calibragem, não de escrita, e o desconto na nota é pela disciplina quebrada, não pelos minutos Passar disso é aceitável se cada bloco adicionar argumento novo; o que não é aceitável é repetir. Eps. 1 a 7 ficaram entre 26 e 38 min e o Leo nunca reclamou de duração — reclamou de falta de casos concretos (ep. 5) e de convergência (ep. 4). **Calibração real medida**: 147-160 wpm (ep. 3: 4.065 palavras = 27:34 → 147 wpm; ep. 5: 4.609 = 29:33 → 156 wpm; ep. 4: 5.873 = 36:48 → 160 wpm; **ep. 8: 5.899 = 37:11 → 158,6 wpm**). Episódios longos ficam na ponta alta da faixa, então usar **158 wpm** para estimar episódio acima de 5.000 palavras e 150 para os curtos. O `settings.yaml` assume 165, que subestima a duração — usar a faixa medida para estimar

### 3.5 Revisor v3 (reescrito em 5/ago após o Leo pedir mais autocrítica)

**O problema que este revisor resolve**: eu sou autor e revisor do mesmo texto, então a nota sai inflada por construção. Prova histórica: dei média **8,88** ao ep. 4 e **9,12** ao ep. 5, e o Leo encontrou falha ESTRUTURAL nos dois. A nota subiu enquanto as falhas continuavam. Erro sistemático medido: **cerca de +1,5 ponto**.

#### Princípio
A revisão não pergunta "está bom?". Pergunta **"por onde eu destruiria este episódio se quisesse humilhá-lo?"**. O `review.json` é um documento de acusação. **Proibido elogiar** — o que ficou bom vai no `summary.md`, que é comunicação; o review é caça a erro.

#### Régua calibrada (a âncora é o Leo, não o meu gosto)
| Nota | Significado operacional |
|---|---|
| 10 | tentei destruir e não achei nada |
| 9 | falha que só um especialista da área notaria |
| 8 | falha que um ouvinte atento notaria |
| **7** | **falha que o LEO notaria** ← eps. 4 e 5 estavam aqui |
| 6 | duas ou mais falhas que o Leo notaria |
| 5 | o eixo não foi trabalhado |
| <5 | não publicar |

#### Nota final = a MENOR das notas, nunca a média
Um episódio 9/9/9/5 é um episódio **5**. O ouvinte sente a falha, não a média. Média foi exatamente o que deixou a acionabilidade 5,0 do ep. 5 passar escondida atrás de três notas 9.

**Abaixo de 7 não gera áudio antes de consertar.**

#### Os seis eixos (0-10 cada)
1. **Equilíbrio** — simetria de concessões e de qualidade dos argumentos
   - ⚠️ **DÍVIDA ABERTA, diagnosticada 2x e nunca corrigida: a ÚLTIMA PALAVRA.** O review do ep. 6 registra "Friedman ganha o último turno de quase todos os casos" e o do ep. 7 registra "Friedman fecha mais eixos com a última palavra". Dois episódios, mesmo resíduo, zero ação. É o candidato mais provável a gargalo do ep. 8, porque equilíbrio já é uma das menores notas
   - **Como medir**: contar quem fala por último em cada eixo. Teto sugerido de 60% para um lado. Percentual de palavras igual (37% x 37% no ep. 7) NÃO capta isso, porque quem fecha o bloco leva a impressão de vitória mesmo empatando no volume
2. **Factual** — números conferidos, fontes atuais, nada apresentado fora de contexto
3. **Ouvido** — cold open, ritmo, TTS, peso das vozes, monólogo, e **prolixidade**
   - ⚠️ **CORREÇÃO de 10/ago (feedback do Leo)**: este eixo mede **prolixidade, NÃO duração**. *"não queria ser tão duro com a parte de tempo de episódio! só não ser prolixo, mas não tem problema ser um pouco maior."*
   - **Episódio mais longo não perde nota.** 36 min densos > 28 min repetitivos. O que perde nota é gordura: repetir o mesmo dado, frase que não adiciona, exemplo redundante
   - **Como medir prolixidade** (objetivo, não impressão): contar n-gramas de 6 a 7 palavras repetidos literalmente, e conceitos-chave ditos mais de 2x fora do fecho. No ep. 7 isso achou "vinte e um dólares por hora" 3x e "noventa e nove por cento dos negócios" 2x — repetição real, cortada. Repetição NO FECHO é intencional (a estrutura "se levar três coisas") e não conta
   - Eu penalizei o ep. 7 duas vezes por ter 36 min, o que estava errado: o critério era meu, não do Leo
4. **Profundidade** — o ouvinte aprendeu algo que não acharia num resumo
5. **Acionabilidade** *(novo, ep. 5)* — cada eixo tem ao menos um caso concreto, de preferência brasileiro, e o episódio diz o que já funcionou em algum lugar. Explicar por que o problema é difícil sem dizer o que se faz com ele é meio trabalho
   - ⚠️ **REFINAMENTO de 10/ago: acionabilidade tem DOIS níveis, e o Leo cobra o segundo.** Nível **político** (o que o Congresso ou o governo deveria fazer) e nível **pessoal** (o que o ouvinte faz na segunda-feira de manhã). Os eps. 4 e 5, as duas piores notas da série, tinham só o político. O salto de 8,5 para 9,5 no ep. 7 foi exatamente adicionar o pessoal: a NR-1, a comunicação de acidente de trabalho e a denúncia ao MPT, que valem HOJE e não dependem da PEC
   - A redação antiga ("ao menos um caso concreto por eixo") é uma condição que o ep. 5 poderia cumprir e ainda assim frustrar. **A pergunta certa é: o ouvinte sai com uma frase que ele pode repetir numa reunião ou usar na própria vida?**
   - Bônus observado: o bloco pessoal saiu **de graça em equilíbrio**, porque os dois personagens discordam sobre a lei do início ao fim e concordam inteiramente sobre o que uma pessoa pode fazer amanhã. Isso é material de fecho, não de meio
6. **Fidelidade à pergunta** *(novo, ep. 4)* — a Regra Zero como NOTA, não como caixinha de sim/não

#### Painel adversarial (quatro ataques, escritos por extenso)
Não basta responder "ok". Cada um escreve a crítica mais dura que conseguir:
- **O especialista da área**: que erro factual ou omissão material um PhD apontaria?
- **O militante de esquerda**: onde o Marx foi mal defendido ou virou espantalho?
- **O militante de direita**: onde o Friedman foi mal defendido ou virou espantalho?
- **O ouvinte no trânsito**: em que minuto eu desliguei? e o que eu faço com isso na segunda-feira?

#### ⚠️ REGRA DE OURO DO CHECKLIST (descoberta em 10/ago, a mais importante desta seção)
**Item de checklist sem comando associado converge para "OK" automático.** Não é preguiça pontual: é o comportamento padrão de quem verifica a si mesmo.

**Prova**: o review do ep. 7 declarava "0 enumerações de 3+" e havia **6** no `script.json` em disco (turnos 41, 61, 88, 108, 116 e 117 — ex.: *"randomizar a seleção das empresas, escolher grupo de comparação válido, dar acesso transparente aos dados e usar amostras maiores"*, quatro itens). Passou porque meu detector contava vírgulas, gerava falsos positivos com apostos, e eu descartei o lote inteiro como falso positivo **sem olhar item por item**. E o `normalizar_tts()` NÃO conserta enumeração — ele só limpa travessão e reticência. Foi um agente externo lendo o arquivo que encontrou.

**Detector correto de enumeração** (filtra apostos exigindo itens curtos e paralelos):
```python
import json, re
t=json.load(open('output/<slug>/script.json'))['turnos']
for i,x in enumerate(t):
    for s in re.split(r'(?<=[.!?])\s+', x['text']):
        m=re.search(r'((?:[^,.;]+,\s*){1,}[^,.;]+\s+e\s+[^,.;]+)', s)
        if m:
            itens=[p for p in re.split(r',\s*|\s+e\s+', m.group(1)) if p.strip()]
            if len(itens)>=3 and all(len(it.split())<=6 for it in itens):
                print(f"[{i}] ({len(itens)} itens) {m.group(1)[:90]}")
```

⚠️ **CORREÇÃO de 17/ago (ep. 8): o quantificador era `{2,}` e estava ERRADO.** `{2,}` exige
duas vírgulas, então o detector só pegava listas de **4+ itens** e deixava passar toda
enumeração de 3 ("A, B e C"), que é exatamente a forma mais comum. Trocado para `{1,}`.
No ep. 8 a correção achou **10 violações reais** que a versão antiga não achava — ex.:
*"distribuir seringa, abrir sala de consumo supervisionado e tratar dependência como doença"*.

**A lição é mais séria que o regex.** A regra de ouro diz que item sem comando vira OK
automático. O ep. 8 mostra o degrau seguinte: **item COM comando errado vira OK automático
com aparência de rigor**, que é pior, porque o número falso encerra a investigação. Sempre
que um detector retornar zero ou só falsos positivos, testar se ele consegue achar um caso
que você plantou de propósito. Um detector nunca validado é uma opinião com sintaxe.

**Falsos positivos legítimos** (verificar um a um, nunca descartar o lote — lição do ep. 7):
números e datas por extenso ("Recife, dois mil e três"), apostos ("Quem decide, no hospital,
é a sua família") e orações coordenadas. No ep. 8 sobraram 7 candidatos, todos falso positivo,
conferidos individualmente.

**Consequência geral**: cada item do checklist abaixo precisa de um comando que retorne número, não de um julgamento meu. Onde não houver comando, presuma que o item nunca foi verificado.

#### Checklist de regressão (com EVIDÊNCIA, não com "sim")
Cada item exige o número do turno que prova o cumprimento:
- TTS limpo: 0 travessões, 0 reticências, 0 enumerações de 3+, 0 dígitos, 0 caixa alta (ep. 2)
- Profundidade auditada contra o `curriculum.json` (ep. 3)
- Regra Zero cumprida, com os turnos dos dois extremos (ep. 4)
- `eixo_inegociavel` sustentado por cada personagem (ep. 4)
- Atualidade de cada fonte checada; dado velho é apontado em voz alta por um personagem (ep. 4)
- Narrador ≤35% e nenhum monólogo >4 min (ep. 5)
- `debate_map.json` no schema fixo do `publish.py` (ep. 4)
- Acionabilidade: ao menos um caso concreto por eixo (ep. 5)

#### Lacuna declarada é TAREFA, não nota de rodapé
Toda lacuna do painel adversarial recebe um destino explícito: **corrigida** (com o turno) ou **descartada** (com o motivo escrito). Não existe "declarada e mantida".

**Por que esta regra existe**: no ep. 5 eu escrevi no próprio review que o episódio "discute custo e proteção, nunca resultado (…) é a maior lacuna, e é honesta" — e não fiz nada. Usei a declaração de limitação como absolvição. É a versão sofisticada de não fazer o trabalho.

#### Placar histórico pelo revisor v3 (medido em 8/ago/2026)
Os eixos objetivos foram medidos; os qualitativos dos eps. 1 a 4 são estimativa a partir dos artefatos, sem releitura integral.

| Ep | Tema | v3 | O que derruba (a menor nota) | Nota antiga |
|---|---|---|---|---|
| 1 | RBU | **7,0** | ouvido — 23 violações de TTS | 9/9/9 |
| 2 | Bukele | **5,0** | ouvido — **110 violações**, os travessões | 9/9/9/9 |
| 3 | Educação | **7,5** | equilíbrio — "Milton concede muito" (do próprio review) | 9/9/9/9 |
| 4 | Bilionários | **6,0** | fidelidade e acionabilidade — 6 casos, 41% narrador, 6,5 min de monólogo | 8,88 |
| 5 | Funcionalismo | **4,0** | acionabilidade — 3 casos concretos no episódio inteiro | 9,12 |
| 6 | Funcionalismo 2 | **8,5** | equilíbrio | — |
| 7 | Jornada | **9,0** | equilíbrio e ouvido (empatados) — nenhuma falha conhecida sem correção | — |

**Duas leituras que importam:**
1. **O projeto só passa do limiar de 7 a partir do ep. 6**, quando as regras entraram. Antes disso, o revisor dava 9 em tudo e não discriminava nada.
2. **A acionabilidade REGREDIU no meio da série.** Contagem de casos concretos nomeados por episódio: **23, 26, 31, 6, 3, 37, 18**. Os eps. 1 a 3 eram muito mais concretos que os 4 e 5. Eu fui ficando abstrato sem perceber, porque nenhuma métrica minha olhava para isso. O fundo do poço foi exatamente o episódio que o Leo criticou.

#### Previsão falsificável (fecha o loop)
O review termina respondendo: **"se o Leo reclamar de algo neste episódio, do que vai ser?"** A previsão fica registrada e é comparada com o que ele realmente disser. Histórico: no ep. 4 eu não previ (a crítica dele nem estava no review); no ep. 5 eu previ e ignorei. Um de dois previstos, e o previsto foi desperdiçado.

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
- **Feed RSS** (`docs/feed.xml`, gerado pelo `publish.py` desde 6/ago): é o que permite assinar em Spotify, Apple Podcasts e Pocket Casts — e **é o que dá download offline**, porque esses apps baixam episódio nativamente. O site em si NÃO funciona offline (sem service worker, `preload="metadata"`)
  - Capa do feed é `docs/cover.png` em **1400x1400** (mínimo da Apple; a `logo.png` tem 1024 e seria rejeitada). Regerar com `Image.open('docs/logo.png').resize((1400,1400), Image.LANCZOS)`
  - Config no topo do `publish.py`: `EMAIL_OWNER` fica **público** no feed e é exigido pela Apple para verificar titularidade. Categoria atual: News > Politics
  - Botão "Assinar no seu app de podcast" no header copia a URL do feed (clicar em `/feed.xml` mostraria XML cru). Autodiscovery via `<link rel="alternate">`
  - **Submetido ao Spotify em 7/ago/2026** (aguardando aprovação, leva algumas horas). Pendente: Apple Podcasts Connect. O Spotify entrega métricas de retenção, que é o dado que falta para avaliar roteiro com evidência em vez de impressão
- Logo: `docs/logo.png` (header/capa) + `docs/icon.png` (favicon, crop do mic). Conceitos alternativos em `branding/`. Gerada com Gemini `gemini-3-pro-image` (key em `~/livro-colorir/.env`)

## Episódios publicados
1. **Renda Básica Universal: o dossiê completo** (33:09, 22/jul) — NIT/Friedman, 5 portas de financiamento, Quênia/Alasca/Irã/SIME-DIME, Lei Suplicy
2. **O modelo Bukele: segurança a qualquer preço?** (27:42, 29/jul) — armadilha de Formosa como parábola, pacto El Faro, mano dura 2003, CV/PCC nascidos em presídios
3. **Educação: pública, privada, e quem paga a conta** (27:34, 30/jul) — matriz financiar×operar, tribunal dos 70 anos de vouchers, Tooley, Jackson, a grande inversão, Sobral
4. **Deveriam existir bilionários?** (36:48, 3/ago) — Musk cruza US$ 1 tri (jun/26), Nozick em vez do argumento meritocrático, Bagchi-Svejnar (riqueza politicamente conectada arrasta crescimento; Brasil 27%, EUA 1%), Zucman (0,3% de imposto efetivo vs 7,5% de retorno), bloco da régua de pobreza (linha subiu 40% em jun/25 sem ninguém empobrecer)
6. **Funcionalismo, parte 2: o que de fato funciona** (30:10, 6/ago) — complemento do ep. 5 para pagar a dívida de acionabilidade (nota 4,0 no revisor v3). Formato novo: **julgamento de casos** em vez de eixos temáticos, cada caso respondendo funcionou/por quê/dá para copiar. Sobral (1.407º → 1º do Brasil sem tirar estabilidade), PAIC/Ceará (Lei 14.026/2007, 184 municípios), gov.br (R$ 38 bi e 150 mi de horas/ano, zero demissões), reforma tributária, OSS de SP (TCE achou administração direta mais barata), Nova Zelândia (lei de 1988 revogada em 2020), ENAP (nos 6 casos examinados ninguém avalia produtividade). Abre se corrigindo: a comparação OCDE do ep. 5 não era homogênea. **Nota v3: 8,5**
5. **Funcionalismo público: estabilidade é proteção ou privilégio?** (29:33, 5/ago) — 1º episódio sob a Regra Zero; cold open do assassinato de Garfield por um caçador de emprego público (1881) → Pendleton Act; Brasil tem 12,1% da força de trabalho no setor público vs 20,8% OCDE mas gasta 13,5% do PIB vs 9,3% (Estado em formato de taça); EC 19/1998 já permite demitir por desempenho e a lei complementar nunca veio (28 anos); déficit militar de R$ 159 mil/beneficiário vs R$ 9,4 mil no INSS; vitaliciedade ≠ estabilidade
7. **Jornada de trabalho: a jornada deveria ser reduzida por lei?** (37:45, 7/ago) — cold open da folga que cai em dia útil (folga na quarta, escola do filho aberta, ninguém para conviver: não aparece em estudo de PIB nenhum). Atualidade: a **PEC 221/19** (fim da escala 6x1) foi aprovada na Câmara em dois turnos por **461 a 19 em 27/mai/2026** e está no Senado passando por comissões (já passou pela CCJ); transição prevista de 44→42h em 60 dias e 42→40h em 14 meses, sem redução de salário. O **estudo do FGV IBRE**, o mais citado contra a proposta, **declara por escrito que mantém "produtividade por hora e nível de emprego constantes"** — ou seja, assume que o mecanismo central defendido pelo outro lado quase não opera (IPEA calcula 1% de aumento de custo operacional). O **INSEE** achou **queda de 3,7% de produtividade** nas empresas francesas que adotaram as 35h, único caso de lei nacional comparável (Tirole chama de equívoco; França flexibilizou em 2003). O paper de **Cuello (JRC, Comissão Europeia)** demole o desenho dos pilotos: **todos os do setor privado analisados usam comparação antes-e-depois** (uma única exceção), método de alto risco porque supõe que nada mais mudou numa economia saindo de pandemia, e **a tentativa de montar grupo de comparação não entrou no relatório final** porque "não pareceu funcionar"; o piloto ainda acha efeito significativo em custo de creche, que não tem relação com semana de quatro dias. Contraponto de método pela esquerda: a Alemanha **teve** grupo de controle (7,7 vs 6,8, 73% mantiveram). Fecho onde os dois concordam: a **NR-1** (fiscalização de risco psicossocial em vigor desde este ano) é o que já vale hoje sem PEC nenhuma, porque cobra da empresa o resultado (trabalhador não adoecer) sem dizer quantas horas usar. **Nota v3: 9,0, a maior da série** (factual 9,5, profundidade 9,5, acionabilidade 9,5, equilíbrio e ouvido 9,0). Lição do processo: quatro rodadas de melhoria subiram o factual de 8,0 para 9,5 sem mover a nota final, porque cada inserção empurrou a duração e derrubou o ouvido (efeito cobertor curto) → fixar orçamento de palavras no curriculum

8. **Corpo e Estado: o Estado deveria proibir droga e venda de órgãos?** (37:11, 17/ago) — cold open da Operação Bisturi (19 moradores da periferia do Recife levados a Durban em 2003, até US$ 30 mil por rim) contrastada com os 38 mil brasileiros na fila do rim e 1.303 mortos esperando em 6 meses. **Achado estrutural: descriminalizar quem USA e legalizar quem VENDE são duas decisões diferentes**, e é aí que a discordância real mora — sem esse eixo o episódio viraria consenso morno, porque nenhum Marx plausível defende prender usuário. Marx defende travar o mercado (Suécia como proibicionismo de esquerda, Japão 2-3% de uso na vida contra 47% na Austrália); Friedman não trava nada (carta a Bennett lida na íntegra, com a réplica do Bennett junto: o crack foi inventado pela proibição; quase 1 mi de presos, 27,5% por droga, 69,6% negros). **Achado de pesquisa: Moeindarbari e Feizi (436 pares em Mashhad), o melhor estudo do único mercado legal de rins do mundo, DECLARA POR ESCRITO que não coletou dados sobre arrependimento, complicação pós-operatória nem consequência de longo prazo do doador** — mediu a fila, não a pessoa que vendeu. Uruguai (narcotráfico clássico de fonte principal para 6,7% do acesso, mas 2 em 3 fora do registro), De Braços Abertos (42→17 pedras/semana, e a checagem da Agência Pública com o rebote de 160% na Luz), Espanha com a lei de consentimento presumido DORMENTE, Paraná caindo de >70% para 25-30% de recusa. Fecho pessoal: **no Brasil não existe cadastro de doador, documento e cartório não valem, quem decide é a família e ela recusa 45%**. **Nota v3: 8,5** (profundidade e acionabilidade 9,5, factual 9,0, equilíbrio/ouvido/fidelidade 8,5)

## Séries

**Série principal** (temporada 1): tema em disputa proposto pelo Leo, Marx × Friedman.

**Contraponto Legislativo** (temporada 2, criada em 17/ago/2026): o episódio parte de **um
projeto de lei ou emenda real, em tramitação** — municipal, estadual, federal, Brasil ou
fora. Sócrates explica o que o texto faz, o que alega resolver e em que pé está o trâmite;
os dois debatem se aquilo deveria virar lei. **Especificação completa em `SERIE-LEGISLATIVO.md`**
— tem seis riscos novos, artefato `projeto.json` obrigatório e um sétimo eixo de revisão
(fidelidade ao texto). O ep. 7 (PEC 221/19) foi o protótipo acidental e deu 9,0.

### Feed: mesmo feed, e por quê
Séries convivem no mesmo RSS como **temporadas**. O que cada app de fato faz (verificado
em 17/ago/2026, não presumido):
- **Apple Podcasts**: agrupa por `<itunes:season>` com `<itunes:type>episodic</itunes:type>`
  ("Episodic with Seasons"). Só exibe a temporada **a partir da segunda** — ou seja, aparece
  exatamente quando o primeiro Legislativo sair. Mostra o **número**, não o nome
- **Spotify**: **não agrupa por temporada.** Lê a tag e ignora o agrupamento, exibindo tudo
  em ordem cronológica inversa. Não existe "duas séries no mesmo canal" no Spotify hoje
- **Apps Podcasting 2.0** (Fountain, Podverse, Pocket Casts): leem `<podcast:season name>`
  e exibem o **nome** da temporada

Como o Spotify é o canal principal e não agrupa, **o único diferenciador que funciona em
todo lugar é o prefixo no título** ("Contraponto Legislativo: ..."). O `publish.py` faz os
três ao mesmo tempo: prefixo, `itunes:season` e `podcast:season name`. Feed separado foi
descartado: exigiria nova submissão ao Spotify e à Apple e dividiria uma base de assinantes
que tem 10 dias de vida.

⚠️ A Apple pede para **não** repetir número de temporada/episódio no título — por isso o
prefixo é só o nome da série, sem "#1". A numeração vive em `itunes:episode`, que
**reinicia por temporada** (`_numeracao_por_serie` no `publish.py`).

## Backlog de temas (Leo escolhe)
Legalizar drogas (Portugal vs Oregon) · Controle de aluguel e crise da moradia · Regular a IA (AI Act vs EUA vs PL 2338) · Nuclear na transição energética · Privatizar ou não (Correios/Sabesp/Petrobras) · **Medição e estatística política** (sobra do ep. 4: Pritchett, Reddy-Pogge, Ravallion, medidas FGT, MPI, Dinamarca×Paquistão — pesquisa já feita em `output/2026-08-03-bilionarios/curriculum.json`)

## Histórico de lições (não repetir erros)
- Travessões quebraram a entonação do ep. 2 (75 ocorrências) → regras TTS acima + normalizador
- Revisor v1 dava 9/9/9 em roteiro raso → eixo "profundidade" + auditoria contra curriculum + ponto-cego (pegou erros factuais nos eps. 2, 3 e 4 antes do áudio)
- **O primeiro rascunho é sistematicamente descuidado com atualidade de fonte** — no ep. 4 dados de 1987-2002 (Bagchi-Svejnar) foram apresentados como atuais. Sempre checar o ANO de cada estudo antes de colocar número na boca de personagem; quando o dado é velho, fazer o adversário apontar isso (vira dialética em vez de erro)
- Ep. 4 passou em equilíbrio (Marx 31%, Friedman 28%) e ainda assim frustrou o Leo → métrica de palavras não mede convicção. Ver Regra Zero e eixo inegociável
- Trilha/série de episódios foi considerada e DESCARTADA — um episódio completo é melhor. **EXCEÇÃO aberta em 6/ago**: complemento é legítimo para pagar dívida de revisão (o ep. 6 completa o 5). Não vale para planejar série nova
- **`steelman.json` antes do roteiro** (novo, ep. 6): os 10 melhores argumentos de cada lado, com flag `me_incomoda`, escritos ANTES de qualquer turno. Se um argumento da lista não entrar no roteiro, a revisão explica por quê. Na estreia pegou o melhor argumento da direita sobre Sobral, que eu ia dar de graça pra esquerda
- **`casos/` é banco reutilizável** (novo, ep. 6): todo caso precisa de número, fonte e **contra-argumento obrigatório**. Caso sem contra-argumento é propaganda. Consultar ANTES de escrever
- **Mínimo 3 fontes primárias lidas na íntegra por episódio.** Comparação real: ep. 4 leu 3 PDFs e o factual ficou sólido; ep. 5 fez 18 buscas e leu ZERO, e daí veio o Evans-Rauch sem checar literatura posterior. No ep. 6 a leitura primária desmentiu um snippet (OSS "mais eficientes" → TCE achou mais caras)
- **Não sobreinterpretar fonte**: se o documento se declara "síntese rápida, não exaustiva" (relatório ENAP), ele não prova afirmação universal. Padrão recorrente meu — apareceu com Evans-Rauch (ep. 5) e ENAP (ep. 6). Quando acontecer, fazer um personagem apontar o limite: vira dialética em vez de erro
- **Formato de julgamento de casos** (ep. 6) garante acionabilidade por construção, mas produz MAIS concordância que debate de tese. Usar como complemento, não como padrão, se o Leo preferir atrito
- **`debate_map.json` tem schema fixo lido pelo `publish.py`**: `tema`, `modo`, `tese_esquerda`, `tese_direita`, `pontos[{tensao, visao_esquerda, visao_direita}]`, `consenso[]`, `perguntas_abertas[]`, `fontes_chave[{titulo,url}]`. Inventar chaves novas publica um card VAZIO sem erro nenhum (quase aconteceu no ep. 4) — sempre conferir contra o debate_map do episódio anterior
- Medir monólogo, não só duração: o ep. 4 tinha 11 min de narrador seguido sem contraditório. Quebrar com intervenção dos personagens vale mais que cortar palavras
- Evitar CAIXA ALTA para ênfase no roteiro (o TTS pode soletrar); siglas conhecidas como IBGE e UBS são lidas corretamente
- Cache DNS negativo: não testar domínio antes do registro existir (roteador guarda NXDOMAIN por ~30 min)
