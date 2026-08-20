# Contraponto Legislativo — especificação da série

Série paralela à principal. Vale tudo que está no `CLAUDE.md` (regras TTS, Regra Zero,
eixo inegociável, revisor v3, peso das vozes). Este arquivo registra **só o que muda**.

## O que é

Cada episódio parte de **um projeto de lei ou emenda real, em tramitação** — municipal,
estadual, federal, brasileiro ou estrangeiro. Sócrates explica o que o texto faz, que
problema ele alega resolver e em que pé está o trâmite. Marx e Friedman debatem se
aquilo deveria virar lei.

O ep. 7 (PEC 221/19) foi o protótipo acidental disto, e deu a maior nota da série (9,0).

## Por que a série existe: ela paga três dívidas de graça

1. **Fonte primária.** O texto do projeto, a justificativa do autor e o parecer do relator
   são canônicos, públicos e curtos. O buraco do ep. 5 (18 buscas, zero leituras integrais)
   fica estruturalmente impossível — a leitura integral é o ponto de partida, não uma
   virtude opcional.
2. **Acionabilidade nível pessoal.** Projeto em trâmite tem consulta pública aberta
   (e-Cidadania no Senado, Enquete na Câmara), relator com nome e comissão com data. A
   pergunta "o que eu faço com isso na segunda de manhã" tem resposta literal, e não
   depende de eu ser criativo.
3. **Regra Zero.** O objeto é binário e existe uma votação real. Converter "isso deveria
   virar lei?" em "que tipo de lei seria aceitável" fica visível na hora.

## Os seis riscos NOVOS (o runbook principal não cobre nenhum)

### R1 — Virar aula de processo legislativo
**Sintoma:** Sócrates narrando CCJ → CAE → plenário → volta à Câmara.
**Por que mata:** estoura o teto de 35% do narrador e derruba o eixo ouvido, que já é uma
das menores notas da série.
**Regra:** o bloco de tramitação tem **teto de 90 segundos (~230 palavras)** e só entra o
passo que muda o que está em jogo. Trâmite entra como **aposta**, não como procedimento:
"está a uma votação de comissão de virar lei" ou "está parado há quatro anos e morre".
**Comando:**
```python
import json; t=json.load(open('output/<slug>/script.json'))['turnos']
bloco=[x for x in t if x.get('bloco')=='tramitacao']
print(sum(len(x['text'].split()) for x in bloco), "palavras (teto 230)")
```

### R2 — O texto vira o debate (debate de advogado)
**Sintoma:** discutir se o artigo 3º diz "poderá" ou "deverá". Não é matéria pra Marx e
Friedman, é matéria pra consultoria legislativa.
**Regra:** separar **o FIM** (que problema o projeto quer resolver) do **MEIO** (o
dispositivo que ele usa), e fazer os dois personagens responderem às duas perguntas em
blocos separados.

Este é o **movimento-assinatura do formato** e não existe na série principal. Ele produz
quatro resultados, e os dois cruzados são os que valem episódio:

| | concordam no meio | discordam no meio |
|---|---|---|
| **concordam no fim** | episódio fraco, vira consenso | **o caso comum e bom** |
| **discordam no fim** | **o caso raro e o mais valioso**: discordam do problema e mesmo assim concordam que o dispositivo é ruim | debate padrão |

### R3 — A justificativa do autor é peça de parte
**Sintoma:** usar a justificativa como descrição neutra do problema. Isso entrega o
enquadramento a um lado antes de o debate começar, e é a versão legislativa do erro do
ep. 4 (perder o eixo antes do primeiro turno).
**Regra:** Sócrates apresenta a justificativa **marcada como peça de parte** ("é o que o
autor alega, e o autor é parte"), e o personagem do lado contrário tem o **primeiro tiro**
nela. O `projeto.json` separa `problema_declarado` de `problema_real`. Quando os dois
divergem, a divergência é material de episódio, não nota de rodapé.

### R4 — A dívida da última palavra (aqui ela morre)
Diagnosticada nos reviews dos eps. 6 e 7, nunca corrigida — "Friedman fecha mais eixos".
Este formato dá o conserto limpo, porque tem um objeto simétrico no fim:
**Regra:** o episódio fecha numa **votação declarada**. Cada personagem diz literalmente
como votaria: *"voto sim"*, *"voto não"*, *"voto sim com destaque para suprimir o artigo
tal"*. Quem fecha cada eixo do meio **alterna**, e o voto final é simétrico por construção:
os dois falam por último, cada um do seu voto.
**Comando:**
```python
import json; t=json.load(open('output/<slug>/script.json'))['turnos']
from collections import Counter
ult=Counter()
for i,x in enumerate(t):
    if x.get('fecha_eixo'): ult[x['speaker']]+=1
print(ult, "→ teto de 60% para um lado")
```

### R5 — Casting: o projeto tem que ser matéria pra eles
**Sintoma:** Marx e Friedman debatendo estacionamento rotativo municipal.
**Filtro de seleção — os quatro são obrigatórios:**
- [ ] tem eixo **distributivo** (quem ganha e quem perde tem nome) **ou de coerção estatal**
      (o Estado está proibindo ou obrigando alguém a algo)
- [ ] **os dois lados têm argumento forte de verdade.** Se Marx e Friedman concordariam,
      não é episódio (é o que elimina, por exemplo, a PEC da Blindagem)
- [ ] texto integral público e legível
- [ ] está **vivo** no trâmite, ou morreu de um jeito que ensina

### R6 — O episódio caduca
Projeto anda depois de publicado.
**Regra:** Sócrates declara a **data de corte em voz alta** ("na data desta gravação,
dezessete de agosto de dois mil e vinte e seis"). O `projeto.json` registra
`gatilho_de_atualizacao`: qual evento específico torna o episódio desatualizado.

## Estrutura do episódio

1. **Cold open** — o caso concreto de quem a lei atinge. Nunca "hoje vamos falar do PL tal".
2. **O que o texto faz** (Sócrates, teto ~90s) — dispositivo por dispositivo, em português
   comum. Não é a ementa: é o que muda na prática, pra quem.
3. **O que ele alega resolver** (Sócrates, marcado como peça de parte) + **qual é o
   problema real** segundo a evidência. Contra-tiro do lado oposto ao autor.
4. **Onde está** (Sócrates, teto ~90s) — trâmite como aposta, com data de corte declarada.
5. **Rodada do FIM** — esse problema existe? é problema do Estado resolver?
6. **Rodada do MEIO** — eixo por eixo sobre o dispositivo, percorrendo o options_map.
   Alternar quem fecha cada eixo.
7. **Quem ganha e quem perde** — com nome, número e caso brasileiro.
8. **Precedente** — alguém já fez isso em algum lugar? o que aconteceu? (alimentado pelo
   banco `casos/`, que exige contra-argumento obrigatório por caso)
9. **A votação declarada** — cada um diz seu voto e o destaque que pediria.
10. **Fecho de Sócrates** — consensos, perguntas abertas, "se levar três coisas", e a ação
    de segunda-feira: consulta pública, relator, comissão, **e o que já vale hoje sem esse
    projeto** (foi exatamente isso, a NR-1, que levou o ep. 7 de 8,5 a 9,5 em acionabilidade).

## Artefato novo: `projeto.json`

Escrito **antes** do `curriculum.json`. Sem ele não se começa o roteiro.

```json
{
  "id": "PL 2338/2023",
  "esfera": "federal",
  "casa_atual": "Câmara dos Deputados",
  "pais": "Brasil",
  "autor": "Rodrigo Pacheco (PSD-MG)",
  "data_apresentacao": "2023-05-03",
  "ementa_oficial": "<texto literal da ementa>",

  "o_que_muda": [
    {"dispositivo": "art. 14", "em_portugues": "...", "quem_afeta": "...", "e_novo_ou_ja_existe": "..."}
  ],

  "problema_declarado": "<o que a justificativa do autor alega — PEÇA DE PARTE>",
  "problema_real": "<o que a evidência diz, que pode divergir do declarado>",
  "divergencia_declarado_real": "<se houver, isso é bloco de episódio>",

  "tramitacao": [{"data": "2026-05-27", "orgao": "...", "o_que_aconteceu": "..."}],
  "situacao_atual": "...",
  "proximo_passo": "...",
  "probabilidade_de_virar_lei": {"leitura": "alta|média|baixa", "porque": "..."},
  "data_de_corte": "2026-08-17",
  "gatilho_de_atualizacao": "<que evento torna este episódio desatualizado>",

  "participacao_publica": {"canal": "e-Cidadania", "url": "...", "aberta": true,
                           "relator": "...", "comissao": "..."},

  "pareceres_e_notas_tecnicas": [
    {"orgao": "FGV IBRE", "conclusao": "...", "premissa_declarada": "<lição do ep. 7: a premissa que o estudo assume é o argumento>", "url": "..."}
  ],

  "precedente": [{"onde": "...", "o_que_aconteceu": "...", "contra_argumento": "..."}],
  "quem_ganha": ["<com nome e número>"],
  "quem_perde": ["<com nome e número>"],
  "custo_declarado": "...",
  "custo_estimado_por_terceiros": [{"fonte": "...", "numero": "..."}],

  "fontes_primarias_lidas_na_integra": ["<url do texto integral>", "<justificativa>", "<parecer>"]
}
```

O `curriculum.json` mantém tudo, e `pergunta_do_leo` vira **`pergunta_do_episodio`**, que
nesta série tem forma fixa: *"este projeto deveria virar lei, como está?"* — a menos que o
Leo dê outro recorte.

## Revisor: sétimo eixo

Os seis eixos do v3 continuam, com dois ajustes e um eixo novo. **Nota final continua sendo
a MENOR, nunca a média.**

- **Factual** — cada afirmação sobre o conteúdo do projeto tem que citar artigo conferível
  no texto integral.
- **Acionabilidade** — piso obrigatório: consulta pública, relator e comissão com nome e
  data, **mais** o que já vale hoje sem esse projeto.
- **7º eixo — Fidelidade ao texto** *(novo)*: o episódio descreve o projeto que existe, e
  não a caricatura dele que circula na imprensa. **Errar o que o projeto faz é falha grave
  (teto de 6), porque é o objeto do episódio.** Auditoria: reler o texto integral com o
  `script.json` do lado.

**Painel adversarial ganha um quinto atacante: o assessor legislativo** — "onde vocês
descreveram errado o que o texto faz, ou ignoraram um dispositivo que muda tudo?"

## Checklist de regressão da série (cada item com comando, pela regra de ouro)

- [ ] Bloco de tramitação ≤230 palavras (comando em R1)
- [ ] Quem fecha eixo ≤60% para um lado (comando em R4)
- [ ] Data de corte dita em voz alta — `grep -c "data desta gravação" script.json`
- [ ] Votação declarada presente para os dois personagens
- [ ] Justificativa marcada como peça de parte, com contra-tiro do lado oposto
- [ ] Blocos FIM e MEIO existem e são separados
- [ ] `projeto.json` com ≥3 fontes primárias lidas na íntegra
- [ ] Filtro de casting (R5) respondido item por item, por escrito
- [ ] Todo o checklist do `CLAUDE.md` (TTS, narrador ≤35%, monólogo ≤4min, debate_map schema)

## Publicação

`debate_map.json` ganha uma chave opcional `serie` (o `publish.py` a lê; episódios sem ela
seguem publicando exatamente como hoje):

```json
"serie": {"id": "legislativo", "nome": "Contraponto Legislativo", "numero": 2,
          "projeto": "PL 2338/2023", "situacao": "comissão especial na Câmara"}
```

Mesmo feed RSS. Ver a seção "Feed" no `CLAUDE.md` para o porquê.
