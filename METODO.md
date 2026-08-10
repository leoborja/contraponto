# Contraponto — Método de produção

Este documento não é resumo do `CLAUDE.md`. É o **procedimento** para o episódio sair nota 9 no primeiro rascunho, em vez de nota 8 depois de quatro rodadas.

O `CLAUDE.md` diz *quais* são as regras. Aqui está *em que ordem* aplicá-las, *qual erro* cada etapa previne e *qual comando* prova que a etapa foi cumprida.

**Ponto de partida honesto**: nenhum dos sete episódios saiu 9 de primeira. O ep. 7 chegou a 9,0 depois de quatro rodadas, e a lição registrada no próprio review é que as quatro rodadas **não mudaram a nota final** — só trocaram qual eixo era o gargalo. Este método existe para que o ep. 8 comece onde o 7 terminou.

---

## 1. A ordem que funciona

A descoberta central da série é que **a ordem das etapas é causal, não organizacional**.

| # | Etapa | Artefato | Erro que esta ordem previne |
|---|---|---|---|
| 0 | Pergunta e orçamento | `curriculum.json` (esqueleto) | roteiro que responde outra pergunta; cobertor curto |
| 1 | Pesquisa com leitura integral | `fontes_primarias_lidas` | citar autor que não se leu |
| 2 | **Steel-man ANTES do roteiro** | `steelman.json` | um lado nasce fraco e ninguém percebe até a revisão |
| 3 | Currículo | `curriculum.json` (completo) | profundidade aparente; número sem procedência |
| 4 | Roteiro dentro do orçamento | `script.json` | prolixidade; narrador dominante; monólogo |
| 5 | Verificação automatizada | saída dos comandos | afirmar métrica sem medir |
| 6 | Revisão adversarial | `review.json` | nota inflada; lacuna declarada e não corrigida |
| 7 | Mapa, resumo e publicação | `debate_map.json`, `summary.md` | card vazio publicado silenciosamente |

### Por que o steel-man vem antes do roteiro

Porque **um roteiro escrito antes do steel-man já nasceu com um lado fraco**, e revisão não conserta isso: reescreve.

A prova é o ep. 5. O melhor argumento disponível para o Friedman era que a comparação "Brasil 12,1% da força de trabalho no setor público contra 20,8% da OCDE" não é homogênea, porque Noruega e Dinamarca chegam a 30% empregando quem cuida de criança e de idoso, funções que no Brasil são familiares ou privadas. Esse argumento não estava em nenhum lugar do episódio. Foi descoberto na revisão adversarial, com o episódio **já publicado**, e o próprio review o classifica como "a maior falha de steel-man do episódio". Custou um episódio inteiro para pagar (o ep. 6).

O `steelman.json` do ep. 6 abre dizendo exatamente isso, e a estreia do artefato pegou na hora o argumento simétrico: **Sobral pertence à direita também** ("só funcionou porque alguém podia ser tirado do cargo"), com a anotação `"este é o argumento que eu quase deixei de fora, porque o caso parece pertencer à esquerda"`. Sem o steel-man prévio, aquele caso ia inteiro para a esquerda.

A flag `me_incomoda: true` é o mecanismo que faz o artefato funcionar. Ela marca o argumento que enfraquece a posição para a qual o texto naturalmente pende. No ep. 7 ela pegou a assimetria mais embaraçosa possível: o relatório do piloto britânico não declara nenhuma limitação metodológica própria, enquanto o estudo do IBRE (o do "outro lado") declara a premissa dele. Anotação: *"eu ia usar o piloto britânico como evidência forte sem notar que ele não se autolimita, enquanto cobrei exatamente isso do estudo do outro lado."*

**Regra**: se um argumento do `steelman.json` não entrar no roteiro, a revisão explica por quê. Placar: ep. 6 = 12 de 12 entraram; ep. 7 = 15 de 16 (o Tirole faltou na primeira versão e foi inserido).

---

## 2. Etapa 0 — Pergunta e orçamento (antes de qualquer pesquisa)

Duas decisões, cinco minutos, e elas determinam a nota de dois eixos inteiros.

### 2.1 A pergunta

Escrever em `curriculum.json:pergunta_do_leo` a pergunta **na forma literal em que ele fez**. Se a pergunta foi formulada por você a partir de um tema do backlog, registrar isso explicitamente (o ep. 7 registra: *"tema escolhido do backlog; a pergunta de valor foi formulada por mim e aprovada por ele"*) e **submeter a pergunta à aprovação dele antes de pesquisar**.

Em seguida, escrever `regra_zero` com três campos. Modelo do ep. 7, que tirou 9,5 em fidelidade:

```json
"regra_zero": {
  "quem_defende_SIM": "host_a (Marx) — sim, por lei, e sem esperar negociação. Não recua.",
  "quem_defende_NAO": "host_b (Friedman) — não por lei; jornada é contrato entre partes. Não recua.",
  "proibido": "convergir para 'reduzir aos poucos com negociação coletiva'. Essa é literalmente a posição da entidade patronal que eu li, e adotá-la como conclusão seria entregar o debate a um lado fingindo equilíbrio."
}
```

O campo `proibido` é o que faz diferença. Ele nomeia a síntese confortável **antes** de ela ser tentadora, e no ep. 7 essa síntese era a posição institucional de uma das fontes. Sem o campo, a convergência entra achando que é equilíbrio: foi exatamente o que aconteceu no ep. 4, cuja nota de fidelidade despencou porque a pergunta "deveriam existir bilionários?" virou "que tipo de bilionário é aceitável?".

### 2.2 O eixo inegociável

Um por personagem, com três campos: `tese`, `municao` e — o mais importante — `onde_ele_PODE_ceder`.

O terceiro campo é o que impede o efeito colateral do próprio eixo inegociável, que é o personagem virar pedra. Ele delimita o território de concessão de antemão, então a concessão que aparece no roteiro é **desenhada** e não acidental. Modelo do ep. 7:

```json
"host_a": {
  "tese": "Tem que ser por lei. A jornada nunca foi reduzida por negociação voluntária em lugar nenhum do mundo.",
  "municao": "O Capital, capítulo 8. As oito horas vieram de lei em todo lugar. A PEC 221 passou por 461 a 19.",
  "onde_ele_PODE_ceder": "no desenho e na transição, e no fato de que os pilotos internacionais não testaram o comércio de rua brasileiro"
}
```

### 2.3 O orçamento de palavras — o item que ninguém escreveu até hoje

**Nenhum dos sete `curriculum.json` tem campo de orçamento.** É a causa direta do efeito cobertor curto do ep. 7. Adicionar:

```json
"orcamento": {
  "palavras_alvo": 4900,
  "minutos_esperados": "32 a 33 (154 wpm medido)",
  "teto_duro": 5200,
  "regra_de_saque": "toda inserção acima do alvo exige um corte de tamanho equivalente no mesmo commit"
}
```

**Calibração real, medida nos seis episódios publicados** (não use os 165 wpm do `config/settings.yaml`, que subestimam a duração):

| Ep | Palavras | Duração real | wpm |
|---|---|---|---|
| 1 RBU | 4.931 | 33:10 | 148,7 |
| 2 Bukele | 4.286 | 27:43 | 154,6 |
| 3 Educação | 4.065 | 27:35 | 147,4 |
| 4 Bilionários | 5.873 | 36:49 | 159,6 |
| 5 Funcionalismo | 4.609 | 29:34 | 155,9 |
| 6 Funcionalismo 2 | 4.667 | 30:11 | 154,6 |

**Use 154 wpm para planejar e 147 para o pior caso.** Conversão pronta:

| Minutos alvo | Palavras (154 wpm) | Pior caso a 147 |
|---|---|---|
| 28 | 4.300 | 29,3 min |
| 32 | 4.900 | 33,3 min |
| 36 | 5.550 | 37,8 min |

Lembre que duração **não derruba nota** (correção de 10/ago: o eixo "ouvido" mede prolixidade). O orçamento não existe para encurtar o episódio; existe para que **melhorar um eixo não derrube outro**. Sem orçamento, cada inserção de conteúdo empurra a duração, a duração pressiona o ritmo, e a nota final anda de lado — foi o que aconteceu nas quatro rodadas do ep. 7.

---

## 3. Etapa 1 — Pesquisa com leitura integral

O leque multi-ângulo (factual, esquerda, direita, críticas, PT e EN) e a cadeira do cético estão no `CLAUDE.md`. O que falta lá é o **controle de proveniência**.

### A regra dura que emergiu de três episódios seguidos

| Ep | Fonte | O que aconteceu |
|---|---|---|
| 5 | Evans-Rauch | usado como **pilar** do argumento central sem dizer que é de 1999 com dados de 1970-1990, e sem consultar a literatura posterior. O review classifica como REGRESSÃO: o ep. 4 já tinha aprendido isso com o Bagchi-Svejnar |
| 6 | Relatório ENAP | tratado como prova de que "ninguém no mundo sabe medir produtividade", quando o documento se declara **síntese rápida e não exaustiva** |
| 7 | Paper de Cuello (JRC) | críticas citadas a partir de resenhas; o original só foi lido na **quarta rodada** |

Três episódios, três vezes o mesmo erro em formas diferentes. A regra que fecha isso:

> **Sem leitura integral, o personagem não cita o autor pelo nome.** O dado entra como afirmação genérica sem autoria ("há crítica metodológica a esses pilotos"), ou não entra.

Ela dói na hora e economiza uma rodada inteira. Nomear autor é o que dá peso retórico, e é exatamente por isso que a tentação existe.

### Mínimo: 3 fontes primárias lidas na íntegra

Comparação que sustenta o número: o ep. 4 leu 3 PDFs e tirou 9,0 em factual; o ep. 5 fez 18 buscas, leu zero, e tirou 6,5. O ep. 6 leu 3 e a leitura primária **desmentiu um snippet** (OSS "mais eficientes" → o TCE achou mais caras).

Registrar em `curriculum.json`:

```json
"fontes_primarias_lidas": [
  {"titulo": "...", "url": "...", "como": "WebFetch integral", "data": "2026-08-XX",
   "o_que_mudou": "o resumo dizia X, o original diz Y"}
]
```

O campo `o_que_mudou` é o que justifica o esforço. Em dois dos três casos em que a leitura integral foi feita, ela contradisse o resumo.

**Fonte atrás de WAF**: quando `curl`/WebFetch é bloqueado, a solução que funcionou no ep. 7 foi Playwright com navegação real clicando no link de download. Vale o esforço: no ep. 7 o conteúdo real era **mais forte que os resumos** e trouxe a nuance decisiva (o autor não conclui que a semana de 4 dias não funciona; conclui que os pilotos foram mal desenhados, e faz dez recomendações para melhorá-los). Essa nuance virou a réplica do Marx e é o que impediu o bloco de virar propaganda de um lado.

### Ano de cada estudo, sempre

Anotar o ano ao lado de cada número no currículo. Quando o dado é velho, **faça o adversário apontar isso em voz alta** — vira dialética em vez de erro. Feito no ep. 4 (Friedman aponta que o Bagchi-Svejnar termina em 2002) e no ep. 6 (o Sócrates diz que o estudo das OSS é de 2010). Não feito no ep. 5, e custou o eixo factual.

### Pendências como bloqueio explícito

O `curriculum.json` do ep. 7 tem o padrão certo em `pendencias_de_verificacao`:

```
"A correlação de -0,68 entre horas e produtividade apareceu em fonte secundária atribuída à OCDE. NÃO usar sem rastrear o estudo original"
"O número de 25,6 horas semanais para a Alemanha é média que inclui tempo parcial. Não usar como comparação de jornada legal"
```

Ambos foram **descartados** e não entraram no roteiro. Isso é a etapa funcionando: pendência é lista de proibição, não lista de desejos.

### Banco de casos: consultar antes, alimentar depois

`casos/README.md` e `casos/funcionalismo.md` são ativo reutilizável. **Regra: todo caso precisa de número verificável, fonte e contra-argumento obrigatório. Caso sem contra-argumento é propaganda, não caso.**

Consultar antes de escrever. Se um eixo do debate não tem caso concreto disponível, ou pesquise um, ou declare na revisão que o eixo ficou abstrato. Depois de gravar, **devolver os casos novos ao banco** — o motivo declarado da criação do banco é que o Sobral do ep. 3 não foi reaproveitado no ep. 5, e a falha de acionabilidade do ep. 5 "não foi falta de esforço, foi falta de repertório".

Atenção: o ep. 6 usou Sobral **sem** contra-argumento técnico (estreitamento curricular, pressão sobre professor) e o próprio review registra isso como "violação consciente" da regra que ele mesmo escreveu, com a instrução de completar o caso em `casos/funcionalismo.md`. **A instrução não foi executada** — o arquivo continua com o contra-argumento apenas ideológico. Corrigir antes de reusar o caso.

---

## 4. Etapa 2 — Steel-man

Arquivo `steelman.json`, escrito **antes de qualquer turno de diálogo**. Estrutura validada nos eps. 6 e 7:

```json
{
  "proposito": "por que este episódio precisa deste artefato (o risco específico deste tema)",
  "melhores_argumentos_da_esquerda": [
    {"argumento": "...", "forca": "por que é difícil de responder",
     "me_incomoda": false, "nota": "opcional"}
  ],
  "melhores_argumentos_da_direita": [ ... ],
  "vieses_de_fonte_declarados": ["..."],
  "o_que_nenhum_dos_dois_quer_enfrentar": ["..."]
}
```

Alvo: 6 a 8 argumentos por lado. Ep. 6 teve 6+6, ep. 7 teve 6+8.

Três seções fazem trabalho que o roteiro sozinho não faz:

**`me_incomoda`** — a auto-suspeita explícita. Marque `true` no argumento que enfraquece o lado para o qual o texto pende. Se nenhum argumento estiver marcado, você não procurou o suficiente.

**`vieses_de_fonte_declarados`** — no ep. 7 as três declarações eram: o informe mais detalhado sobre a França é de federação de indústrias; os relatórios dos pilotos são publicados por organizações que fazem advocacia pela redução; CNC e IPEA chegam a 21% e 1% para a mesma pergunta e nenhum é parte desinteressada. Isso virou item novo no checklist de regressão (`vies_de_fonte_declarado`) porque o Sócrates **diz em voz alta** de quem é a fonte. O review recomenda que vire padrão da série. **Vire padrão.**

**`o_que_nenhum_dos_dois_quer_enfrentar`** — o achado de maior valor por linha escrita. No ep. 7 produziu a observação que nenhuma cobertura fez: nenhum piloto de quatro dias no mundo testou o setor que mais usa a 6x1 no Brasil (comércio de rua, supermercado, farmácia, com horário fixo). Foi um dos dois itens que puxaram profundidade para 9,5.

---

## 5. Etapa 3 — Currículo

Campos obrigatórios, consolidando o que os eps. 5 a 7 usaram e o que faltou:

| Campo | Por que existe |
|---|---|
| `pergunta_do_leo` | Regra Zero (ep. 4) |
| `pergunta_do_episodio` | quando a pergunta foi reformulada, deixa a reformulação auditável |
| `regra_zero` | quem defende sim, quem defende não, e o que é proibido |
| `eixo_inegociavel` | tese, munição e onde pode ceder, por personagem (ep. 4) |
| `orcamento` | **novo** — evita o cobertor curto (ep. 7) |
| `gancho_factual` | matéria-prima do cold open |
| `numeros_ancora` | agrupados por bloco, com ano e fonte em cada um |
| `options_map` | cada crux com as opções percorridas inteiras |
| `fontes_primarias_lidas` | **novo** — controle de proveniência |
| `pendencias_de_verificacao` | lista de proibição |
| `consensos_previstos`, `perguntas_abertas`, `ritual_que_dado_mudaria` | alimentam o fecho e o `debate_map` |
| `casos_por_eixo` | **novo** — um caso concreto por eixo, nomeado, ANTES do roteiro |

O último campo é a prevenção estrutural da falha mais cara da série. Contagem de casos concretos nomeados por episódio: **23, 26, 31, 6, 3, 37, 18**. Os eps. 1 a 3 eram muito mais concretos que os 4 e 5, e o fundo do poço foi exatamente o episódio que o Leo criticou. A causa registrada: nenhuma métrica olhava para isso. Se os casos são escolhidos **antes**, um por eixo, a regressão não tem por onde acontecer.

⚠️ **O ep. 6 não tem `curriculum.json`.** Foi para o ar com 8,5 e o item "profundidade auditada contra o curriculum" simplesmente **desapareceu do checklist** daquele review, em vez de aparecer como FALHOU. Não repita: a ausência de artefato tem que aparecer como falha, não como silêncio (ver o comando de presença na seção 7).

---

## 6. Etapa 4 — Roteiro

### Checklist pré-roteiro (gate: nada de diálogo antes de tudo isto estar escrito em arquivo)

- [ ] **Pergunta literal do Leo** em `pergunta_do_leo` — e, se você a reformulou, a reformulação foi aprovada por ele
- [ ] **Quem defende sim e quem defende não**, nomeados, com "não recua" explícito
- [ ] **A síntese proibida**, nomeada — qual convergência confortável está vetada e por quê
- [ ] **Eixo inegociável de cada personagem**, com tese, munição e onde pode ceder
- [ ] **Orçamento de palavras** com alvo, teto duro e a regra do saque
- [ ] **Um caso concreto por eixo**, com número, fonte e contra-argumento (do banco `casos/` ou pesquisado agora)
- [ ] **`steelman.json` completo**, com pelo menos um `me_incomoda: true` por lado e os vieses de fonte declarados
- [ ] **3 fontes primárias lidas na íntegra**, registradas com o que mudou em relação ao resumo
- [ ] **Pendências de verificação** escritas como proibições

Se qualquer linha estiver vazia, o roteiro vai custar uma rodada extra. Todas as nove existem porque a ausência de uma delas produziu uma nota abaixo de 7 em algum episódio.

### Estrutura

Sócrates define o mínimo necessário → debate eixo por eixo, cada crux percorrendo o `options_map` inteiro → Brasil concreto → **bloco do que o ouvinte faz** → fecho com consensos, perguntas abertas e "se levar três coisas" com números-âncora.

O bloco do "o que o ouvinte faz" é a inserção do ep. 7 que subiu acionabilidade de 8,5 para 9,5. Ver seção 9.

### Peso das vozes

Narrador **no máximo 35%** das palavras. Medido nos sete: 24,5% · 30,5% · 22,5% · **41,1%** · 27,3% · 23,0% · 26,6%. Só o ep. 4 estourou, e estourou por causa de um bloco pedagógico longo do Sócrates.

Os números vão para os personagens. Dado técnico na boca de quem discute é argumento; na boca do professor é conteúdo. O Sócrates fica com definição, arbitragem, declaração de viés de fonte e o fecho.

### Dialética

Concessão só após duas rodadas de pushback, exceto no eixo inegociável. Evidência nova nomeada por eixo. Ritual "que dado te faria mudar de ideia?". A discordância filosófica **sobrevive** ao fim.

**Concessão simétrica é o que salvou o equilíbrio do ep. 7 (9,0, o mais simétrico da série).** O padrão que funcionou: cada lado **retira** uma evidência quando corrigido. Friedman retira a Bélgica da lista quando o Marx aponta que a lei belga é de horas comprimidas e não de redução; o Marx aceita que o estudo da OMS mede 55 horas ou mais e não 44, com o Friedman notando que ele esticou a evidência exatamente como ele próprio havia feito. O review chama essa simetria de erro reconhecido de "melhor momento do episódio". **Desenhe uma retirada de evidência por lado.**

### TTS

Zero travessão, zero reticência, zero dígito, zero caixa alta (siglas conhecidas como IBGE e INSS passam). Números por extenso. **Enumeração de no máximo 2 itens por vírgula** — listas maiores viram frase corrida com "e".

O normalizador (`pipeline/audio.py:normalizar_tts`) limpa travessão e reticência como rede de segurança, mas **não conserta enumeração**, que é estilo e tem que sair certo na fonte. E é justamente onde a série ainda falha: o review do ep. 7 declara "0 enumerações de 3+" e o script em disco tem pelo menos **seis** (turnos 41, 61, 88, 108, 116 e 117 — por exemplo *"randomizar a seleção das empresas, escolher grupo de comparação válido, dar acesso transparente aos dados e usar amostras maiores"*, com quatro itens). O item do checklist foi marcado OK sem ninguém rodar o detector.

### Última palavra

Alternar quem fecha cada eixo. Os reviews dos eps. 6 e 7 registram o **mesmo** resíduo de equilíbrio — *"Friedman ganha o último turno de quase todos os casos"*, *"Friedman fecha mais eixos com a última palavra"* — e ele nunca virou regra. Conte os fechamentos antes de gravar: se um lado fecha mais de 60% dos eixos, redistribua.

---

## 7. Etapa 5 — Verificações automatizadas

Rodar **antes** de escrever o `review.json`. O review então cita os números medidos, em vez de estimá-los.

Contexto: todos os comandos abaixo assumem `cd /Users/leoborja/contraponto` e Python em `/opt/homebrew/bin/python3.12`.

### 7.1 Auditoria de forma (palavras, duração, vozes, monólogo, TTS, prolixidade)

```bash
cd /Users/leoborja/contraponto && EP=output/2026-08-08-SEU-SLUG /opt/homebrew/bin/python3.12 - <<'PY'
import json, os, re, unicodedata
from collections import Counter
EP = os.environ["EP"]
T = json.load(open(f"{EP}/script.json"))["turnos"]
W = lambda t: len(t.split())
tot = sum(W(t["text"]) for t in T)

print(f"PALAVRAS {tot} | duracao 147wpm {tot/147:.1f}min · 154wpm {tot/154:.1f}min · 160wpm {tot/160:.1f}min | {len(T)} turnos")

c = Counter()
for t in T: c[t["speaker"]] += W(t["text"])
for k, v in c.most_common():
    al = "   <<< ESTOUROU o teto de 35%" if k == "narrador" and v/tot > .35 else ""
    print(f"  {k:9s} {v:6d}  {100*v/tot:5.1f}%{al}")

def bloco_mesmo():
    m, i = (0, None, 0), 0
    while i < len(T):
        j, w = i, 0
        while j < len(T) and T[j]["speaker"] == T[i]["speaker"]:
            w += W(T[j]["text"]); j += 1
        if w > m[0]: m = (w, T[i]["speaker"], i)
        i = j
    return m
def bloco_sem_oposto():
    m = (0, None, 0)
    for lado in ("host_a", "host_b"):
        op = "host_b" if lado == "host_a" else "host_a"
        w, ini = 0, 0
        for n, t in enumerate(T):
            if t["speaker"] == op:
                if w > m[0]: m = (w, lado, ini)
                w, ini = 0, n + 1
            else: w += W(t["text"])
        if w > m[0]: m = (w, lado, ini)
    return m
for nome, (w, quem, n) in (("mesmo speaker", bloco_mesmo()), ("sem o lado oposto", bloco_sem_oposto())):
    print(f"MONOLOGO ({nome}): {w} palavras = {w/154:.1f} min · {quem}, a partir do turno #{n}"
          + ("   <<< PASSOU DE 4 MIN" if w/154 > 4 else ""))

v = Counter(); det = []
PATS = (("travessao", r"[—–]"), ("reticencias", r"\.{3}|…"), ("digito", r"\d"),
        ("caixa_alta", r"\b[A-ZÁÉÍÓÚÂÊÔÃÕÇ]{3,}\b"),
        ("enum_3+_CANDIDATO", r"(?:[^\s,.!?;:]+(?:\s+[^\s,.!?;:]+){0,4}),\s+(?:[^\s,.!?;:]+(?:\s+[^\s,.!?;:]+){0,4}),\s+(?:[^\s,.!?;:]+(?:\s+[^\s,.!?;:]+){0,4})\s+e\s+"))
for n, t in enumerate(T):
    for nome, pat in PATS:
        for m in re.finditer(pat, t["text"]):
            v[nome] += 1
            if nome != "digito":
                det.append(f"   {nome} turno {n}: ...{t['text'][max(0,m.start()-40):m.end()+30]}...")
print("TTS:", dict(v) or "limpo")
for d in det: print(d)

NUM = set("zero um uma dois duas tres quatro cinco seis sete oito nove dez onze doze treze quatorze catorze quinze dezesseis dezessete dezoito dezenove vinte trinta quarenta cinquenta sessenta setenta oitenta noventa cem cento duzentos trezentos quatrocentos quinhentos mil milhao milhoes bilhao bilhoes por cento virgula e de".split())
corte = int(len(T) * .88)   # o fecho é excluído: repetir lá é intencional
def norm(x):
    x = unicodedata.normalize("NFKD", x.lower())
    return re.findall(r"[a-z]+", "".join(ch for ch in x if not unicodedata.combining(ch)))
print(f"PROLIXIDADE (corpo = turnos 0..{corte-1}, fecho excluido)")
for N in (6, 7):
    g = Counter()
    for t in T[:corte]:
        w = norm(t["text"])
        for k in range(len(w) - N + 1):
            gram = tuple(w[k:k+N])
            if all(p in NUM for p in gram): continue   # "dois mil e vinte e cinco" não é prolixidade
            g[gram] += 1
    rep = sorted(((x, " ".join(k)) for k, x in g.items() if x > 1), reverse=True)
    print(f"  {N}-gramas repetidos: {len(rep)}")
    for x, k in rep[:10]: print(f"    {x}x  {k}")
PY
```

**Como ler a saída:**

- **Duração**: compare com o `orcamento`. Se passou do teto duro, a regra do saque manda cortar, não negociar.
- **Vozes**: narrador ≤35%. Marx e Friedman idealmente dentro de 4 pontos um do outro (ep. 7: 36,9% e 36,5%).
- **Monólogo**: duas métricas, porque "monólogo" nunca foi definido e por isso os números históricos não batem entre si. *Mesmo speaker* = turnos consecutivos da mesma voz. *Sem o lado oposto* = maior trecho em que o adversário não fala, que é o que realmente mede ausência de contraditório. Use a segunda como régua dos 4 min. Referência: ep. 4 = 6,6 / 7,1 min (ruim); ep. 7 = 2,1 / 3,3 min (bom).
- **`enum_3+_CANDIDATO`** gera falso positivo (aposto entre vírgulas, oração intercalada). **Leia os candidatos um por um.** No ep. 7 foram 17 candidatos e 6 enumerações reais. Não marque o item do checklist sem ter lido a lista.
- **Prolixidade**: qualquer n-grama de 6 ou 7 palavras repetido no corpo é candidato a corte. A lista de números é filtrada porque "dois mil e vinte e cinco" aparece por causa da regra de escrever número por extenso e não é gordura. Também conte à mão conceitos-chave ditos mais de 2 vezes fora do fecho: foi assim que o ep. 7 achou "vinte e um dólares por hora" (3x) e "noventa e nove por cento dos negócios" (2x).

### 7.2 Schema do `debate_map.json` e presença de artefatos

```bash
cd /Users/leoborja/contraponto && EP=output/2026-08-08-SEU-SLUG REF=output/2026-08-07-jornada-de-trabalho /opt/homebrew/bin/python3.12 - <<'PY'
import json, os
from pathlib import Path
EP, REF = Path(os.environ["EP"]), Path(os.environ["REF"])

OBRIGATORIOS = ["curriculum.json", "steelman.json", "script.json", "script.md",
                "debate_map.json", "review.json", "summary.md"]
falta = [f for f in OBRIGATORIOS if not (EP / f).exists()]
print("ARTEFATOS faltando:", falta or "nenhum")

d, r = json.loads((EP/"debate_map.json").read_text()), json.loads((REF/"debate_map.json").read_text())
print("SCHEMA  faltando:", sorted(set(r) - set(d)) or "nada",
      "| extra (nao publicado):", sorted(set(d) - set(r)) or "nada")

# o que o site realmente consome (publish.py + docs/index.html)
USADO = {"tema": str, "tese_esquerda": str, "tese_direita": str,
         "consenso": list, "perguntas_abertas": list, "fontes_chave": list}
for k, tipo in USADO.items():
    v = d.get(k)
    ok = isinstance(v, tipo) and len(v) > 0
    print(f"  {'OK  ' if ok else 'VAZIO'} {k}: {type(v).__name__} n={len(v) if hasattr(v,'__len__') else '-'}")
for i, f in enumerate(d.get("fontes_chave", [])):
    if not (isinstance(f, dict) and f.get("titulo") and f.get("url")):
        print(f"  !! fontes_chave[{i}] sem titulo/url: {f}")
s = json.loads((EP/"script.json").read_text())
print("script.json:", "titulo OK" if s.get("titulo") else "!! SEM 'titulo' — o card usa o tema como fallback")
print("podcast.mp3:", "existe" if (EP/'podcast.mp3').exists() else "!! AUSENTE — publish.py IGNORA a pasta em silencio")
PY
```

**Por que este comando existe**: o `publish.py` lê tudo com `m.get(chave, default)`. Chave errada não gera erro nenhum — gera **card vazio publicado**. E a pasta inteira é ignorada em silêncio se faltar `podcast.mp3`, `script.json` ou `debate_map.json`.

Duas armadilhas confirmadas lendo o `publish.py` e o `docs/index.html`:

- **`pontos` e `modo` nunca são publicados.** O `CLAUDE.md` os lista como parte do "schema fixo lido pelo publish.py", mas nem o `publish.py` nem o `index.html` os tocam. O que aparece no card é: título (que vem do **`script.json`**, não do debate_map), tema, `tese_esquerda`, `tese_direita`, `consenso`, `perguntas_abertas` e `fontes_chave`. Escrever `pontos` continua útil como documento de trabalho — só não confunda com conteúdo publicado.
- `fontes_chave` precisa de itens `{titulo, url}`. Item sem `url` renderiza link quebrado sem avisar.

### 7.3 Comparativo da série (para saber se o episódio novo regrediu)

```bash
cd /Users/leoborja/contraponto && /opt/homebrew/bin/python3.12 - <<'PY'
import json, glob, re
from collections import Counter
W = lambda t: len(t.split())
print(f"{'ep':38s} {'palav':>6s} {'~min':>6s} {'narr':>6s} {'A':>5s} {'B':>5s} {'monol':>7s} {'trav':>5s} {'ret':>4s} {'dig':>4s}")
for p in sorted(glob.glob("output/*/script.json")):
    T = json.load(open(p))["turnos"]; tot = sum(W(t["text"]) for t in T)
    c = Counter()
    for t in T: c[t["speaker"]] += W(t["text"])
    b = 0
    for lado in ("host_a", "host_b"):
        op = "host_b" if lado == "host_a" else "host_a"; w = 0
        for t in T:
            if t["speaker"] == op: b = max(b, w); w = 0
            else: w += W(t["text"])
        b = max(b, w)
    x = " ".join(t["text"] for t in T)
    print(f"{p.split('/')[1]:38s} {tot:6d} {tot/154:6.1f} {100*c['narrador']/tot:5.1f}% "
          f"{100*c['host_a']/tot:4.0f}% {100*c['host_b']/tot:4.0f}% {b/154:6.1f}m "
          f"{len(re.findall(r'[—–]',x)):5d} {len(re.findall(r'\.{3}|…',x)):4d} {len(re.findall(r'\d',x)):4d}")
PY
```

Saída de referência (a série até hoje):

```
ep                                      palav   ~min   narr     A     B   monol  trav  ret  dig
2026-07-22-renda-basica-universal        4931   32.0  24.5%   34%   41%    3.8m     0   23    0
2026-07-29-modelo-bukele                 4286   27.8  30.5%   34%   36%    4.8m    75   23   12
2026-07-30-educacao-publica-privada      4065   26.4  22.5%   37%   41%    4.2m     0    0    0
2026-08-03-bilionarios                   5873   38.1  41.1%   31%   28%    7.1m     0    0    0
2026-08-05-funcionalismo                 4609   29.9  27.3%   39%   34%    3.7m     0    0    0
2026-08-06-funcionalismo-parte-2         4667   30.3  23.0%   37%   40%    3.1m     0    0    0
2026-08-07-jornada-de-trabalho           5966   38.7  26.6%   37%   37%    3.3m     0    0    0
```

---

## 8. Etapa 6 — Revisão adversarial

A régua, os seis eixos, o painel de quatro ataques e a regra da menor nota estão no `CLAUDE.md` §3.5. O que este método adiciona é **disciplina de encerramento**.

### Nota final = a MENOR das notas

Um episódio 9/9/9/5 é um episódio 5. Média foi exatamente o que escondeu a acionabilidade 4,0 do ep. 5 atrás de três notas 9 e produziu um 9,12 que o Leo derrubou com uma frase.

### Lacuna declarada é TAREFA

Cada item do painel adversarial recebe destino, e só existem **dois** destinos válidos:

- **CORRIGIDA** — com o número do turno que prova a correção
- **DESCARTADA** — com o motivo escrito

**"PENDENTE" não é destino.** É a forma sofisticada de não fazer o trabalho, e ela ainda está viva: o ep. 5 fechou com 6 pendentes, o ep. 6 com 2, o ep. 7 com 2 mais um destino inventado ("ACEITA COM RESSALVA"). A origem do problema está escrita no review do ep. 5: *"eu escrevi no próprio review que o episódio discute custo e proteção, nunca resultado, e é a maior lacuna, e é honesta — e não fiz nada. Usei a declaração de limitação como absolvição."*

Se a lacuna não vai ser corrigida neste episódio, ela **sai do review e entra em outro arquivo com dono**: uma linha em `casos/`, ou um item no backlog do `CLAUDE.md`, ou um `pendencias_de_verificacao` do próximo currículo. Lacuna que só existe dentro do review é lacuna que ninguém vai ler de novo.

### Previsão falsificável

O review termina respondendo "se o Leo reclamar de algo neste episódio, do que vai ser?". Histórico de aproveitamento: ep. 4 não previu; ep. 5 previu e ignorou (e a previsão era exatamente a reclamação dele); ep. 6 previu duas e ele não comentou; ep. 7 previu três.

**Regra que faltava**: a previsão principal é uma **acusação contra si mesmo, com prazo neste episódio**. Se você consegue prever a reclamação, você consegue corrigi-la agora. Prever e publicar sem corrigir é o pior resultado possível, porque prova que a informação estava disponível.

### Proibido elogiar

O `review.json` é documento de acusação. O que ficou bom vai no `summary.md`, que é comunicação. Os campos se chamam `acusacao` por isso, e os melhores reviews da série (5 e 7) usam a palavra "REGRESSÃO" e "QUARTA rodada" sobre o próprio trabalho.

### Depois de qualquer edição no script, reabrir o review

O review do ep. 7 registra "5.607 palavras" e o `script.json` em disco tem **5.966**. O texto cresceu na última rodada e o review não foi reaberto, então os números de duração dele (32 min num lugar, 35 a 38 noutro) descrevem uma versão que não existe mais. **Rode a auditoria da §7.1 de novo depois da última edição e cole os números no review.**

---

## 9. O que fez a nota subir no ep. 7 — antes e depois

Quatro rodadas. Serve como exemplo concreto de que tipo de correção move quais eixos.

| Eixo | Antes | Depois | O que mudou de fato |
|---|---|---|---|
| Factual | 8,0 | **9,5** | o paper de Cuello foi lido na íntegra (WAF bloqueava curl; resolvido com Playwright em navegação real) e o bloco foi reescrito com material verificado |
| Acionabilidade | 8,5 | **9,5** | trocou "o que o Senado deveria fazer" por "o que o ouvinte faz sem depender da PEC" |
| Ouvido | 8,0 | **9,0** | correção de **critério**, não de conteúdo: duração deixou de ser penalizada, prolixidade passou a ser medida |
| Profundidade | 9,0 | **9,5** | entrou a ressalva de que a OMS mede 55 horas e não 44, com o Friedman apontando a simetria de erro |
| Equilíbrio | 9,0 | 9,0 | não mudou; segue limitado pela última palavra concentrada no Friedman |
| **Nota final** | **8,0** | **9,0** | |

### Antes e depois, no detalhe

**Factual.** *Antes*: as críticas metodológicas aos pilotos de quatro dias eram citadas a partir de resenhas, com o nome do autor na boca do personagem. *Depois*: leitura integral, e o conteúdo real era mais forte que os resumos — todos os pilotos de setor privado usam comparação antes-e-depois com uma exceção; apenas metade das empresas forneceu dados administrativos suficientes; o piloto capturou redução estatisticamente significativa em custos de creche, que não tem relação com a política, provando que o desenho captura ruído. **E a nuance que nenhum resumo tinha: o autor não conclui que a semana de 4 dias não funciona, conclui que os pilotos foram mal desenhados, e faz dez recomendações para melhorá-los.** Essa nuance virou a réplica do Marx e é o que impediu o bloco de virar propaganda de um lado. Lição: ler a fonte inteira não é só evitar erro, é **achar o material melhor**.

**Acionabilidade — a correção mais transferível.** *Antes*: o episódio dizia o que o Senado deveria fazer. *Depois*: um bloco de fecho com o que já vale hoje sem depender da PEC — a NR-1, cuja fiscalização começou em 26 de maio de 2026, tornou o gerenciamento de risco psicossocial obrigação de toda empresa com empregado CLT, exigindo plano de ação com prazo e responsável; mais três caminhos concretos (documentar com médico, a comunicação de acidente de trabalho, denúncia ao MPT com prazo de 2 anos); mais a ressalva honesta de que o STF suspendeu por 90 dias as multas em 26 de junho, mantendo o dever; mais o Sócrates declarando que nada ali é orientação jurídica.

> **Acionabilidade tem dois níveis, e o que o Leo cobra é o segundo.** Nível político (o que o Congresso/governo faz) e nível pessoal (o que o ouvinte faz na segunda-feira). Sete episódios de evidência: as duas notas baixas de acionabilidade vieram de episódios que só tinham o nível político.

O melhor efeito colateral: os dois personagens discordam sobre a emenda do início ao fim e **concordam inteiramente** sobre o que uma pessoa pode fazer amanhã, o que o Marx usa para dizer algo sobre onde o debate público gasta energia. Isso é acionabilidade sem custo de equilíbrio.

**Ouvido.** O eixo subiu porque o critério estava errado, não porque o texto mudou. O revisor penalizou o episódio **duas vezes** por ter 36 minutos, e o Leo corrigiu: *"não queria ser tão duro com a parte de tempo de episódio! só não ser prolixo, mas não tem problema ser um pouco maior."* Sob o critério certo (n-gramas repetidos no corpo, fecho excluído), as repetições reais foram achadas e cortadas: "vinte e um dólares por hora" 3x, "noventa e nove por cento dos negócios" 2x, e a descrição da PEC 2x. **Uma parte da autocrítica pode ser critério importado, não falha do texto.** Vale checar de onde vem cada penalização antes de mexer no roteiro.

### A lição que o próprio review tira

> *"Quatro rodadas de melhoria subiram o factual de 8,0 para 9,5 e a nota final não mudou, porque cada inserção de conteúdo empurrou a duração para cima e derrubou o ouvido. É o efeito cobertor curto: sem um orçamento de palavras fixado ANTES, melhorar um eixo piora outro indefinidamente."*

É por isso que a §2.3 existe.

---

## 10. Os erros que se repetiram — tabela de prevenção

| Erro | Onde aconteceu | Prevenção (etapa) |
|---|---|---|
| **Fonte além do que se leu** | ep. 5 Evans-Rauch · ep. 6 ENAP · ep. 7 Cuello — três episódios seguidos | §3: sem leitura integral, o personagem não cita o autor pelo nome. `fontes_primarias_lidas` no currículo |
| **Sobreinterpretar fonte** | documento que se declara "síntese rápida, não exaustiva" usado para provar afirmação universal (ENAP) | §3: quando o limite existe, um personagem o aponta em voz alta — vira dialética |
| **Dado velho como atual** | ep. 4 Bagchi-Svejnar (1987-2002) · ep. 5 Evans-Rauch (1999) | §3: ano ao lado de cada número; o adversário aponta a data |
| **Generalizar sem medir** | o runbook afirmava narrador entre 41% e 50% nos eps. 1-4; medido: 25, 31, 22, 41 — só um estourou. O review do ep. 4 diz 45% e 9 min de monólogo; o real é 41,1% e 6,6 min | §7: nenhuma afirmação quantitativa entra em review ou runbook sem o comando que a produziu |
| **Chave inventada no `debate_map`** | quase aconteceu no ep. 4; `publish.py` usa `.get()` e publica card vazio sem erro | §7.2: diff de schema contra o episódio anterior |
| **Cobertor curto** | ep. 7: quatro rodadas, nota final igual, porque cada inserção derrubava outro eixo | §2.3: `orcamento` no currículo + regra do saque (inserir exige cortar) |
| **Lacuna declarada como absolvição** | ep. 5 declarou a maior lacuna no review e não fez nada; 6 itens PENDENTE | §8: só CORRIGIDA ou DESCARTADA; pendência migra para arquivo com dono |
| **Prever e não corrigir** | ep. 5 previu a reclamação exata do Leo e publicou assim | §8: a previsão é acusação com prazo neste episódio |
| **Artefato ausente sem alarme** | ep. 6 sem `curriculum.json`, e o item de auditoria desapareceu do checklist em vez de falhar | §7.2: checagem de presença de arquivos |
| **Marcar checklist sem rodar o detector** | ep. 7 declara "0 enumerações de 3+" e tem pelo menos 6 | §7.1: colar a saída do comando no item do checklist |
| **Eixo sem métrica regride** | acionabilidade: 23, 26, 31, 6, 3, 37, 18 casos concretos. Regrediu por 2 episódios sem ninguém notar, porque nenhuma métrica olhava | §5: `casos_por_eixo` escolhido antes do roteiro |
| **Última palavra concentrada** | resíduo idêntico nos reviews 6 e 7, nunca virou regra | §6: contar fechamentos de eixo; máximo 60% para um lado |

---

## 11. Etapa 7 — Publicação

```bash
cd /Users/leoborja/contraponto
/opt/homebrew/bin/python3.12 podcast.py --audio output/<pasta>   # ElevenLabs → podcast.mp3
/opt/homebrew/bin/python3.12 scripts/publish.py                  # MP3 → docs/ + episodes.json + feed.xml
git add -A && git commit && git push                             # site em ~1 min
```

Antes do áudio: nota final ≥7 (a menor dos eixos) e §7.2 sem nada faltando. Depois do `publish.py`, confira que o número de episódios impresso subiu — se não subiu, a pasta foi ignorada em silêncio.

Depois de publicar: devolver os casos novos a `casos/`, atualizar o placar histórico do `CLAUDE.md` e registrar a previsão falsificável para comparar com o que o Leo disser.

---

## 12. Contradições entre arquivos (não resolvidas aqui, apontadas)

Encontradas ao cruzar `CLAUDE.md`, os `review.json`, `settings.yaml` e o código. Nenhuma foi corrigida por este documento.

| # | Contradição | O que os arquivos dizem | Medido |
|---|---|---|---|
| 1 | Nota do ep. 7 | placar do `CLAUDE.md`: **8,0**, derrubado por "ouvido — 35 a 38 min". `review.json`: **9,0**, com o critério de duração explicitamente revogado | o placar não foi atualizado depois da correção de critério de 10/ago, e ainda cita duração como causa da nota baixa |
| 2 | Narrador no ep. 4 | review: **45%**. `CLAUDE.md`: **41%** | **41,1%** — o `CLAUDE.md` está certo, o review do ep. 4 não |
| 3 | Monólogo do ep. 4 | review: "nove minutos de Sócrates sozinho". `CLAUDE.md`: "11 min" em um trecho e "6,5 min" no placar | **6,6 min** (mesmo speaker) / **7,1 min** (sem o lado oposto). Os três números divergem porque "monólogo" nunca foi definido — ver §7.1 |
| 4 | Palavras e duração do ep. 7 | review: 5.607 palavras, "32 minutos" no painel, "35 a 38 min" na previsão | **5.966 palavras** = 37 a 41 min. O review descreve uma versão anterior do script |
| 5 | Narrador no ep. 7 | 27% no eixo ouvido, 28% no checklist do mesmo arquivo | **26,6%** |
| 6 | Campo `nota_anterior` do ep. 7 | diz "8,0 (mesma nota…)" enquanto `NOTA_FINAL` é 9,0 | resíduo de rodada anterior não limpo |
| 7 | Schema do `debate_map` | `CLAUDE.md` lista `pontos` e `modo` como parte do "schema fixo lido pelo `publish.py`" | nem `publish.py` nem `docs/index.html` leem `pontos` ou `modo`. O card não publica os pontos. E o `titulo` vem do `script.json`, o que o `CLAUDE.md` não menciona |
| 8 | Palavras por minuto | `config/settings.yaml`: `palavras_por_minuto: 165`. `CLAUDE.md`: faixa medida de 147 a 160 | **147 a 160, mediana 155**. O `settings.yaml` subestima a duração em cerca de 7% e nunca foi corrigido |
| 9 | Alvo de palavras | `CLAUDE.md`: 4.200 a 4.800. `settings.yaml` modo profundo: 4.200 a 5.000 | divergência de teto; e os dois episódios melhor avaliados (4 e 7) passaram dos dois valores |
| 10 | "Abaixo de 7 não gera áudio" | o ep. 5 tirou 4,0 e está no ar | consistente na intenção (a nota veio de reavaliação pós-publicação), mas o `CLAUDE.md` não distingue review pré-áudio de reavaliação retroativa, e o placar mistura as duas coisas |
| 11 | Contra-argumento obrigatório em `casos/` | o review do ep. 6 manda adicionar o contra-argumento técnico de Sobral ao banco | `casos/funcionalismo.md` segue só com o contra-argumento ideológico. Instrução não executada |

---

## 13. Cartão de bolso

**Ordem**: pergunta e orçamento → pesquisa com leitura integral → steel-man → currículo → roteiro → medir → revisar adversarialmente → publicar.

**Cinco regras que valem mais que as outras:**

1. Sem leitura integral, o personagem não cita o autor pelo nome.
2. O orçamento de palavras é fixado antes do primeiro turno; inserir depois exige cortar.
3. Nenhuma métrica no review sem o comando que a produziu colado ao lado.
4. Lacuna tem dois destinos: corrigida com número de turno, ou descartada com motivo.
5. Acionabilidade é o que o ouvinte faz na segunda-feira, não o que o Congresso deveria fazer.
