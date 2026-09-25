# Relatório — Sprint 1 do Projeto Caatinga.AI

Disciplina: Inteligência Artificial — UniRios — 2026.2 · Prof. Ronierison Maciel

**Matrícula-semente:** `24114060` · **Ordem de expansão dos vizinhos (todas as estratégias):** Norte, Sul, Oeste, Leste · **O A\* reabre nós:** sim.

## 0. O pomar e o sensor

```
. . . ~ . # . . . . # .
. . ~ ~ ~ # . . # . . .
# . . ~ . . . . # . ~ .
# ~ ~ . . . . ~ . . ~ .
~ ~ ~ # . . ~ # . . ~ #
. . # # . . . ~ ~ # ~ .
. ~ . . . ~ . . . # ~ .
. ~ ~ . ~ # . ~ . # ~ #
# ~ . ~ . . ~ . . ~ . ~
. . ~ . # # . . ~ . . .
# . # . # ~ ~ . . . ~ .
. ~ ~ . ~ . # # . . . .
```

`.` carreador (custo 1) · `~` encharcado (custo 4) · `#` bloqueado. Portão (0,0), coleta (11,11): 80 carreadores, 39 encharcados, 25 bloqueados.

Sensor: prevalência 0,0462 · sensibilidade 0,95 · taxa de falso positivo 0,08 · 800 talhões/semana.

## Parte 1 — O agente antes do código

### 1.1 Ficha PEAS

| Componente | Especificação |
|---|---|
| **P** (desempenho) | (i) **custo da rota** em unidades de custo de entrada (1 un. ≈ 3 min, premissa nossa) — minimizar; ótimo neste pomar = 27 un.; (ii) **recall de talhões infestados sinalizados** (%) — meta ≥ sensibilidade do sensor (95%); (iii) **horas de agrônomo por semana gastas com alertas falsos** (h/semana) — hoje 12,21 h/semana (item 4.3c) |
| **E** (ambiente) | Pomar 12 × 12 (`.`, `~`, `#`), portão (0,0), coleta (11,11), pragas com prevalência de 4,6%, umidade/irrigação, agrônomos que recebem os alertas |
| **A** (atuadores) | Mover Norte/Sul/Oeste/Leste (um talhão por vez); sinalizar talhão suspeito para inspeção humana |
| **S** (sensores) | Posição (i,j); tipo do talhão à frente (custo/bloqueio); sensor óptico de pragas (positivo/negativo) |

### 1.2 Classificação do ambiente

| Dimensão | Classificação | Frase do cenário que sustenta |
|---|---|---|
| Observável | **Parcialmente** ⚠ discutível | “O pomar é uma grade de 12 × 12 talhões. Cada talhão é de um dos três tipos” (mapa conhecido) × “sensor óptico … que aponta talhões **suspeitos**” (a praga só é inferida) |
| Determinístico | **Navegação sim; sensor não (estocástico)** ⚠ discutível | “só se move nas quatro direções ortogonais” × sensibilidade < 100% e falso positivo > 0 nos parâmetros |
| Episódico/sequencial | **Sequencial** | “Custo do caminho = soma do custo dos talhões em que ele entra” — cada passo muda a posição e o custo acumulado |
| Estático/dinâmico | **Estático** (para a rota) | “percorre um pomar … precisa chegar ao ponto de coleta”; nada diz que o terreno mude durante a rota |
| Discreto/contínuo | **Discreto** | “grade de 12 × 12 talhões”, “quatro direções ortogonais”, custos 1 e 4 |
| Agente único | **Único** | “um agente que percorre um pomar” (o agrônomo só entra depois, ao receber o alerta) |

**Duas dimensões discutíveis e a informação que falta:**

1. **Observável.** O texto não diz se o agente **recebe o mapa antes de sair** ou o descobre andando, nem se a praga é visível sem o sensor. *Decide:* “o agente conhece a grade inteira antes de sair?” (sim → mapa totalmente observável e a busca offline das Partes 2–3 é legítima) e “existe leitura direta da praga?” (não → a infestação é parcialmente observável; por isso a Parte 4 usa probabilidade).
2. **Determinístico.** O movimento é determinístico no modelo, mas o sensor não. *Decide:* “entrar em `~` pode falhar (atolar) ou só custa 4?” e “duas leituras do sensor no mesmo talhão são independentes?”. Se o movimento sempre dá certo, a navegação é determinística e o sensor é estocástico.

### 1.3 Tipo de agente

**Baseado em objetivos** (com custo de caminho).

- Não é *reflexo simples*: a ação certa num talhão não sai da percepção atual; depende de onde está o objetivo e do custo acumulado (um passo barato pode levar a um beco).
- Não basta *reflexo com modelo*: tem o mapa, mas sem **objetivo explícito** não sabe para onde ir; aqui há teste de objetivo (“chegou a (11,11)?”) e custo aditivo — a entrada de BFS/UCS/A\*.
- Não é *baseado em utilidade* na navegação: há um só objetivo e um custo escalar. **Ressalva:** a escolha dos K talhões (3.4) usa uma função objetivo que pondera risco × bateria; nessa etapa o agente age como baseado em utilidade.
- Não é *com aprendizado*: o enunciado não dá histórico nem realimentação.

### 1.4 Métrica perversa

- **Métrica que parece razoável:** “**custo médio de deslocamento por talhão inspecionado** (un. de custo/talhão) — quanto menor, melhor”.
- **Comportamento aprendido:** inspecionar sempre os talhões *mais baratos de alcançar*. Com K = 15, ele escolhe os 15 mais baratos a partir do portão; **6 de 15** são `~`, e eles cobrem só **1,6%** do risco total (nosso mapa de risco), contra **43,6%** que os 15 de maior risco cobririam.
- **Onde aparece no pomar:** nas zonas caras de alcançar — por exemplo (6,10), (11,0), (6,11), (10,5) — e nos focos de infestação do nosso mapa de risco: (9,2) [custo de acesso 24, posição 93 de 117], (1,10) [custo de acesso 18, posição 56 de 117], (11,0) [custo de acesso 30, posição 116 de 117], (8,11) [custo de acesso 28, posição 111 de 117]. Nenhum foco entra entre os 15 mais baratos: o agente nunca vai lá. (O mapa de risco é **modelo nosso**, gerado da matrícula; a premissa é que solo encharcado/irrigação favorece pragas.)
- **Correção:** trocar a métrica por **risco coberto** (soma do risco dos talhões inspecionados) **sujeito ao orçamento de bateria** (≤ 60 un. de deslocamento com K = 15). É a função objetivo da 3.4: passa a premiar detectar praga, não andar pouco.

## Parte 2 — Formulação e busca cega

### 2.1 Os cinco componentes

| Componente | Para o nosso pomar |
|---|---|
| Estado inicial | `(0, 0)` |
| Ações(s) | Norte, Sul, Oeste, Leste, tirando as que saem da grade ou entram em `#` |
| Modelo de transição | `Resultado((i,j), a) = (i+di, j+dj)`, com (di,dj) ∈ {(-1,0),(1,0),(0,-1),(0,1)} |
| Teste de objetivo | `s == (11, 11)` |
| Custo do caminho | soma do custo de entrada de cada talhão da rota, sem o inicial: `.`=1, `~`=4 |

**Número de estados:** o estado é só a posição (i,j) (não guardamos quais talhões já foram inspecionados). Contando na grade: 12 × 12 = 144 − 25 bloqueados = **119 estados**; todos são alcançáveis do portão.

### 2.2 BFS, DFS e UCS

BFS testa o objetivo **ao gerar** o nó; UCS e A\* testam **ao expandir**. “Nós expandidos” = nós retirados da fronteira que tiveram vizinhos gerados. Fronteira máxima = maior tamanho durante a execução.

| Estratégia | Custo da rota (un.) | Nº de passos | Nós expandidos (nº) | Fronteira máx. (nós) | Tempo (ms) | Rota é ótima em custo? |
|---|---:|---:|---:|---:|---:|---|
| BFS | 46 | 22 | 117 | 11 | 0,208 | **Não** (+19 un., +70%) |
| DFS | 113 | 62 | 94 | 67 | 0,242 | **Não** (+86 un., +319%) |
| UCS | 27 | 24 | 109 | 14 | 0,240 | **Sim** (garantido) |

*Por que a fronteira máxima da BFS é 11 e não o dobro?* A fila guarda só nós **gerados e ainda não expandidos**; na grade a frente de onda é uma diagonal. Os nós já visitados ficam num dicionário à parte, que não conta como fronteira.

### 2.3 Por que a BFS devolveu rota mais cara (não é bug)

A BFS achou custo **46** com **22** passos, o menor número possível. O UCS achou **27**, com 24 passos — **mais** passos, porém mais barato. A BFS minimiza **passos**, não **custo**, e só é ótima em custo quando **todas as ações têm o mesmo custo**. **Hipótese da Aula 03 violada: custo de passo uniforme** — aqui um passo custa 1 (`.`) ou 4 (`~`), então a rota com menos passos pode atravessar `~` e sair mais cara. O UCS aceita dar mais passos se cada um for barato: generaliza a BFS expandindo por menor custo acumulado g(n).

### 2.4 Escalando n até falhar (`python src/escala.py 24114060`, limite 60 s)

| n | Estados (n²) | Estratégia | Status | Nós expandidos (nº) | Fronteira máx. (nós) | Tempo (s) |
|---:|---:|---|---|---:|---:|---:|
| 12 | 144 | BFS | ok | 114 | 13 | 0,00 |
| 12 | 144 | DFS | ok | 103 | 60 | 0,00 |
| 12 | 144 | UCS | ok | 111 | 23 | 0,00 |
| 40 | 1.600 | BFS | ok | 1.286 | 41 | 0,00 |
| 40 | 1.600 | DFS | ok | 1.085 | 569 | 0,00 |
| 40 | 1.600 | UCS | ok | 1.278 | 57 | 0,00 |
| 100 | 10.000 | BFS | ok | 8.015 | 101 | 0,01 |
| 100 | 10.000 | DFS | ok | 6.432 | 3.740 | 0,01 |
| 100 | 10.000 | UCS | ok | 8.015 | 140 | 0,02 |
| 300 | 90.000 | BFS | ok | 71.881 | 293 | 0,12 |
| 300 | 90.000 | DFS | ok | 57.297 | 35.428 | 0,12 |
| 300 | 90.000 | UCS | ok | 71.881 | 451 | 0,21 |
| 1.000 | 1.000.000 | BFS | ok | 798.893 | 923 | 1,53 |
| 1.000 | 1.000.000 | DFS | ok | 626.867 | 404.943 | 2,33 |
| 1.000 | 1.000.000 | UCS | ok | 798.893 | 1.477 | 3,23 |
| 2.000 | 4.000.000 | BFS | ok | 3.194.526 | 1.823 | 6,75 |
| 2.000 | 4.000.000 | DFS | ok | 2.476.537 | 1.603.423 | 22,44 |
| 2.000 | 4.000.000 | UCS | ok | 3.194.523 | 2.951 | 14,32 |
| 3.000 | 9.000.000 | BFS | ok | 7.187.682 | 2.699 | 16,43 |
| 3.000 | 9.000.000 | **DFS** | **tempo>60s** | — | — | **> 60** |
| 3.000 | 9.000.000 | UCS | ok | 7.187.681 | 4.412 | 35,56 |

**Conclusão (nossa execução, nossa semente):**

1. **Em qual n falhou:** n = **3000**.
2. **Qual estratégia falhou:** **DFS**, com status `tempo>60s` no `escala.csv`.
3. **Qual limite foi atingido:** o **limite de tempo** (60 s), não memória — a DFS nem chegou a lançar `MemoryError`, só não terminou a tempo.
4. **Relação com a fórmula da Aula 03:** em busca em árvore, BFS/UCS/DFS custariam O(b^d); guardando estados visitados (busca em grafo), o custo cai para O(n²) estados. Isso bate com os dados: em n = 3000 a BFS expandiu 7.187.682 nós para 9.000.000 de estados (79,9%), bem perto da fração esperada de talhões livres (P(bloqueado) = 0,20 → ~80% livres). A fronteira da BFS/UCS cresce quase linearmente com n (293 → 1.823 → 2.699 de n=300 a n=3000, ~9× para 10× de n), enquanto a fronteira da DFS explode: 35.428 (n=300) → 404.943 (n=1000) → 1.603.423 (n=2000), um crescimento muito mais que linear. É exatamente essa fronteira gigante — nossa DFS empilha estados repetidos antes de descartá-los — que faz ela estourar o tempo primeiro, antes da BFS e da UCS.

## Parte 3

## Parte 3 — Busca informada

### 3.1 A\* com três heurísticas (versão que **reabre nós**)

| Heurística | Custo da rota (un.) | Nós expandidos (nº) | Admissível? (prova) |
|---|---:|---:|---|
| h1(n) = 0 | 27 | 109 | **Sim.** 0 ≤ h\*(n), pois todo passo custa ≥ 1. (A\* com h1 é o UCS.) |
| h2(n) = Manhattan | 27 | 45 | **Sim.** De n ao objetivo são necessários ≥ Manhattan(n) passos, cada um custa ≥ 1, logo h\*(n) ≥ Manhattan(n). Conferido por força bruta: 0 violações nos 119 estados alcançáveis. |
| h3(n) = 4×Manhattan | 28 | 24 | **Não.** Superestima em 118 dos 119 estados (ex.: (0,0): h3 = 88 > h\* = 27). |

### 3.2 Admissibilidade de h2 e violação de h3

**h2 admissível.** Seja c_min = 1 o menor custo de entrada em um talhão. Qualquer caminho de (i,j) até (11,11) precisa de pelo menos |11−i| + |11−j| movimentos, e cada um entra num talhão de custo ≥ c_min = 1. Logo h\*(n) ≥ Manhattan(n) = h2(n). ∎

**h3 superestima** (h\* = custo real restante, calculado por Dijkstra):

| Talhão n | Objetivo | Manhattan | h3(n) | h\*(n) real | Excesso |
|---|---|---:|---:|---:|---:|
| (0, 0) | (11, 11) | 22 | 88 | 27 | +61 |
| (10, 11) | (11, 11) | 1 | 4 | 1 | +3 |

### 3.3 h3 versus UCS

O custo de h3 foi **28** contra **27** do UCS: ficou **maior**. Perda = (28 − 27) / 27 = **3,7%** (≈ 3 min a mais num trajeto de 81 min, pela nossa conversão de 3 min/un.). Em troca, expandiu **24** nós contra 109 do UCS: **85 nós de expansão comprados** (78% a menos; o A\* com h2 expandiu 45). A perda respeita a cota teórica: custo ≤ 4·C\* = 108. **Isso já refuta a ideia de que h3 é ótima:** basta esta grade como contraexemplo, sem precisar de teoria.

**Quando trocar garantia por velocidade (condição verificável).** Trocar A\*-h2 por A\*-h3 só vale se **(a)** o replanejamento tiver um limite de latência L e o tempo medido do A\*-h2 na malha real passar de L, **e (b)** a perda medida de custo for ≤ τ. Limiares a validar com a cooperativa: L = 200 ms por replanejamento e τ = 10% do custo da rota. Na nossa medição, (b) é satisfeita (perda de 3,7% ≤ 10%), mas **(a) não é**: o A\*-h2 leva ≈ 0,10 ms ≪ 200 ms no 12 × 12. Logo **mantém-se a garantia de otimalidade**. Só passaria a valer em malhas grandes, onde o tempo do A\*-h2 medido na 2.4 passasse de L.

### 3.4 Busca local: escolher K = 15 talhões

- *Estado:* conjunto de 15 talhões livres. *Vizinhança:* **troca** (tira um, põe outro).
- *Objetivo (maximizar):* soma do risco − 2 × (custo do tour que passa de 60 un.). Bateria 6 h = 360 min; inspeção 12 min × 15 = 180 min; sobram 180 min de deslocamento = 60 un. (premissa nossa: 1 un. = 3 min). Tour: portão → talhões (sempre ao mais próximo) → coleta.
- *Risco:* mapa **nosso** (o enunciado não dá): 4 focos gerados da matrícula em (9,2), (1,10), (11,0), (8,11).

| Método (30 execuções) | Média | Desvio-padrão | Melhor | Pior |
|---|---:|---:|---:|---:|
| Subida de encosta | 86,29 | 13,99 | 97,38 | 60,70 |
| Têmpera simulada (T0 = 6, Tf = 0,05, 20.000 passos) | 97,00 | 0,29 | 97,38 | 96,32 |

**Por que aceitar piora ajuda (Aula 04).** A subida de encosta só aceita vizinhos melhores; ao chegar a um ponto onde todos os vizinhos são piores (ótimo local) ela **para**, mesmo havendo algo melhor do outro lado de um “vale”. A têmpera aceita um vizinho pior com probabilidade exp(Δ/T): com T alto atravessa vales, com T baixo refina como a subida de encosta.

**Onde isso aparece nos 30 resultados** (`resultados/busca_local.csv`):
- A subida terminou em **19 valores distintos** em 30 execuções (repetiu ótimos locais) e sua pior execução ficou em **60,70**, bem abaixo do melhor global (97,38). O melhor global foi alcançado por **3** execução(ões) da subida e por **6** da têmpera.
- Comparando execução a execução (mesmo estado inicial): têmpera **melhor em 23**, igual em 1, pior em 6.
- O desvio-padrão da têmpera (0,29) é muito menor que o da subida (13,99): ela quase sempre termina perto do topo, enquanto a subida depende de onde começou.
- A têmpera aceitou em média **580 movimentos piores** por execução. Isso mostra o mecanismo em ação; o que mostra que ele *ajuda* é a comparação execução a execução acima.

*Transparência:* 20.000 passos foram escolhidos comparando 6.000 e 20.000 na semente de referência (20231045); T0 e Tf não foram otimizados.

### Bônus — Liga de IA: contraexemplo 8 × 8 para a DFS (`python src/contraexemplo.py`)

```
. . . . . . . .
~ . . . . . . .
~ . . . . . . .
~ . . . . . . .
~ . . . . . . .
~ . . . . . . .
~ . . . . . . .
~ ~ ~ ~ ~ ~ ~ .
```

- **DFS: custo 95**; **ótimo: custo 14** (razão 6,79×, mais que o dobro).
- Rota ótima: (0,0)→(0,1)→(1,1)→(2,1)→(3,1)→(4,1)→(5,1)→(6,1)→(6,2)→(6,3)→(6,4)→(6,5)→(6,6)→(6,7)→(7,7).
- **Rota devolvida pela DFS** (56 passos, custo 95): (0,0)→(1,0)→(2,0)→(3,0)→(4,0)→(5,0)→(6,0)→(7,0)→(7,1)→(6,1)→(5,1)→(4,1)→(3,1)→(2,1)→(1,1)→(0,1)→(0,2)→(1,2)→(2,2)→(3,2)→(4,2)→(5,2)→(6,2)→(7,2)→(7,3)→(6,3)→(5,3)→(4,3)→(3,3)→(2,3)→(1,3)→(0,3)→(0,4)→(1,4)→(2,4)→(3,4)→(4,4)→(5,4)→(6,4)→(7,4)→(7,5)→(6,5)→(5,5)→(4,5)→(3,5)→(2,5)→(1,5)→(0,5)→(0,6)→(1,6)→(2,6)→(3,6)→(4,6)→(5,6)→(6,6)→(7,6)→(7,7)
- Em palavras: desce toda a coluna 0 até (7,0), vira a Leste em (7,1), sobe a coluna 1 até (0,1), avança a Leste, desce a coluna 2, e assim por diante em serpentina até (7,6) → (7,7).

**Construção.** A DFS tira da pilha na ordem Norte, Sul, Oeste, Leste: em (0,0) o Norte não existe, então **desce** a coluna 0 (toda `~`). Em (7,0) vira a Leste; em (7,1) o Norte ainda está livre e vem antes do Leste, então **sobe**. Ela varre o pomar em serpentina passando pela coluna 0 e pela linha 7 (caras). O ótimo desce a coluna 1 e vai a Leste pela linha 6. O custo da DFS depende da **ordem dos vizinhos**, não do custo dos talhões, então podemos desenhar a grade para punir essa ordem. *(Minha primeira previsão era que a DFS seguiria a linha 7; a execução mostrou a serpentina — ver `ANEXO_IA.md`.)*

## Parte 4 — Regras e incerteza

### 4.1 Mini sistema especialista (encadeamento para trás)

Regras (`src/especialista.py`). A base inicial tem 7; a R8 entra em 4.2.

```
R1: SE armadilha_positiva E umidade_alta E pulverizado_ha_mais_de_14_dias ENTAO risco_alto
R2: SE sensor_positivo E folhas_danificadas ENTAO infestacao_provavel
R3: SE infestacao_provavel ENTAO inspecionar_prioridade_alta
R4: SE risco_alto ENTAO inspecionar_prioridade_alta
R5: SE sensor_positivo E nao folhas_danificadas ENTAO inspecionar_rotina
R6: SE solo_encharcado E umidade_alta E armadilha_positiva ENTAO risco_alto
R7: SE nao sensor_positivo E nao armadilha_positiva ENTAO monitorar_normal
R8: SE infestacao_provavel E pulverizado_ha_ate_7_dias ENTAO reinspecionar_em_7_dias
```

O programa parte da **meta** (a decisão) e procura regras que a concluam, provando as premissas (fatos dados ou conclusões de outras regras). Prioridade das decisões: `reinspecionar_em_7_dias` (só após R8) > `inspecionar_prioridade_alta` > `inspecionar_rotina` > `monitorar_normal`. Saída real para o caso B (sensor positivo, folhas danificadas):

```
META inspecionar_prioridade_alta? tentando R3: SE infestacao_provavel ENTAO inspecionar_prioridade_alta
  META infestacao_provavel? tentando R2: SE sensor_positivo E folhas_danificadas ENTAO infestacao_provavel
    fato dado: sensor_positivo = True
    fato dado: folhas_danificadas = True
  OK: infestacao_provavel provado por R2
OK: inspecionar_prioridade_alta provado por R3
Conclui 'inspecionar_prioridade_alta' porque:
  - R2: SE sensor_positivo E folhas_danificadas ENTAO infestacao_provavel
  - R3: SE infestacao_provavel ENTAO inspecionar_prioridade_alta
```

### 4.2 Quebrando a própria base

**Caso legítimo classificado errado (caso G):** sensor positivo, folhas danificadas, **pulverizado há 2 dias**. A base de 7 regras conclui `inspecionar_prioridade_alta` (cadeia R2 → R3). No domínio, 2 dias após pulverizar o dano visível é em grande parte **residual** (a praga já foi combatida) e o sensor pode apontar material morto; mandar o agrônomo com prioridade alta é alarme falso evitável.

**Regra que corrige (R8):** `SE infestacao_provavel E pulverizado_ha_ate_7_dias ENTAO reinspecionar_em_7_dias`, com prioridade acima das outras decisões.

**Traço ANTES** (base com 7 regras):

```
META inspecionar_prioridade_alta? tentando R3: SE infestacao_provavel ENTAO inspecionar_prioridade_alta
  META infestacao_provavel? tentando R2: SE sensor_positivo E folhas_danificadas ENTAO infestacao_provavel
    fato dado: sensor_positivo = True
    fato dado: folhas_danificadas = True
  OK: infestacao_provavel provado por R2
OK: inspecionar_prioridade_alta provado por R3
Conclui 'inspecionar_prioridade_alta' porque:
  - R2: SE sensor_positivo E folhas_danificadas ENTAO infestacao_provavel
  - R3: SE infestacao_provavel ENTAO inspecionar_prioridade_alta
```

**Traço DEPOIS** (com a R8):

```
META reinspecionar_em_7_dias? tentando R8: SE infestacao_provavel E pulverizado_ha_ate_7_dias ENTAO reinspecionar_em_7_dias
  META infestacao_provavel? tentando R2: SE sensor_positivo E folhas_danificadas ENTAO infestacao_provavel
    fato dado: sensor_positivo = True
    fato dado: folhas_danificadas = True
  OK: infestacao_provavel provado por R2
  fato dado: pulverizado_ha_ate_7_dias = True
OK: reinspecionar_em_7_dias provado por R8
Conclui 'reinspecionar_em_7_dias' porque:
  - R2: SE sensor_positivo E folhas_danificadas ENTAO infestacao_provavel
  - R8: SE infestacao_provavel E pulverizado_ha_ate_7_dias ENTAO reinspecionar_em_7_dias
```

R3 e R8 valem juntas para o caso G, mas não se contradizem: são recomendações **ordenadas por prioridade**, e R8 (mais específica) vence. Quando o talhão não foi pulverizado há ≤ 7 dias, R8 nunca dispara. Teste de regressão nos 7 casos: **só o caso G mudou**.

*Lacuna conhecida:* o caso F (armadilha positiva, seco, pulverizado há 10 dias) fica `sem_conclusao`; nenhuma regra o cobre (Limitações no README).

### 4.3 Bayes com os nossos números

Prevalência = 0,0462; sensibilidade = 0,95; falso positivo = 0,08; 800 talhões/semana.

**(a)** P(infestado | positivo) = sens·prev / (sens·prev + fpr·(1−prev))
= (0,95 × 0,0462) / (0,95 × 0,0462 + 0,08 × 0,9538) = 0,043890 / (0,043890 + 0,076304) = 0,043890 / 0,120194 = **0,3652 (36,5%)**

**(b)** “A cada 100 alertas do meu sistema, cerca de **63** serão falsos.”

**(c)** Falsos por semana = 800 × 0,9538 × 0,08 = **61,04 alertas falsos/semana**. Horas = 61,04 × 12 min / 60 = **12,21 h/semana** perseguindo alerta falso. (Premissa: todos os 800 talhões passam pelo sensor e cada alerta gera uma inspeção de 12 min.)

**(d)** Com sensibilidade 99,9%: VPP = (0,999 × 0,0462) / (0,999 × 0,0462 + 0,08 × 0,9538) = **0,3769 (37,7%)**, contra 36,5%: ganho de 1,17 ponto percentual. **Não melhorou de verdade:** os falsos alertas continuam 61,04/semana (12,21 h), porque só dependem de N·(1−prev)·fpr — a sensibilidade não aparece nessa conta. **Eu mexeria na taxa de falsos positivos** (ou na prevalência dos talhões testados): com fpr pela metade (0,04), o VPP vai a **53,5%** e os falsos caem a 30,52/semana (6,1 h). Ressalva: reduzir fpr costuma custar sensibilidade; alternativas são pré-triagem por risco ou confirmação em segundo estágio.

### 4.4 A regra que salva o modelo

**Decisão que deve ficar em regra explícita:** *autorizar a aplicação de defensivo em um talhão* (período de carência, distância de reservatório/mata). **Argumento de responsabilidade e auditabilidade (não de acurácia):** aplicar agrotóxico exige responsável técnico; se houver autuação ou lote recusado, alguém precisa **responder por quê**. Uma regra explícita gera o traço “disparou R_k porque os fatos F1..Fn”, é versionável linha a linha e muda por decisão humana quando a norma muda, sem retreinar. Um modelo aprendido pode ter acurácia maior, mas não oferece justificativa auditável nem responsável identificável para o caso individual.

## Parte 5 — Auditoria do laudo da AgroVision

| # | Afirmação | Veredito | Justificativa e número medido |
|---|---|---|---|
| 1 | “A\* com Manhattan×4 … rota sempre a mais barata” | **Incorreta** | h3 é **inadmissível** (no talhão (0,0) estima 88 contra h\* = 27, item 3.2). E na **nossa própria grade** ela devolveu **28** contra **27** ótimo (perda de 3,7%, item 3.3): contraexemplo medido para o “sempre”. A\* só é ótimo com heurística admissível; com 4×Manhattan só se garante custo ≤ 4·C\* = 108. |
| 2 | “BFS → A\*: custo caiu 38%; a heurística melhora a qualidade” | **Parcialmente correta** | O fato pode ocorrer: na nossa grade BFS 46 → A\* 27, queda de **41,3%** (o laudo diz 38%; o número depende da grade). A **causa está errada**: o A\* com h1 = 0 (sem heurística) dá o **mesmo custo 27**. A queda vem de o A\*/UCS considerar o custo g(n), não de h. A heurística só reduz nós expandidos (109 → 45 com h2) e, se inadmissível, pode até piorar a rota (h3: 28). |
| 3 | “99% de sensibilidade ⇒ entre os apontados, 99% infestados” | **Incorreta** | Confunde P(+\|infestado) (sensibilidade) com P(infestado\|+) (VPP). Com prevalência 0,0462 e fpr 0,08, o VPP é **36,5%** (4.3a): ~63 de cada 100 alertas são falsos. (A nossa sensibilidade é 0,95, não 99%, mas o erro de raciocínio é o mesmo.) |
| 4 | “Dois testes positivos ⇒ confiança passa de 99%” | **Incorreta** | O “99%” era sensibilidade, não confiança. Mesmo supondo leituras **independentes**, VPP com 2 positivos = 0,95² · 0,0462 / (0,95² · 0,0462 + 0,08² · 0,9538) = **87,2%**, abaixo de 99%. E no mesmo talhão os erros do sensor tendem a ser correlacionados, então o valor real é menor. |
| 5 | “DFS usa menos memória; pomar estático e observável ⇒ DFS suficiente” | **Incorreta** | (i) Custo: DFS **113** contra ótimo **27** (+319%). (ii) A vantagem de memória O(bm) só existe se a DFS **não** guardar visitados (busca em árvore), o que traz de volta o laço infinito; com visitados, a fronteira da DFS foi **67** contra **11** da BFS (12×12). Com o nosso próprio `escala.csv`: em n=300 a fronteira da DFS já era **35.428** contra **293** da BFS (121× maior); em n=2000, **1.603.423** contra **1.823** (879× maior), com a DFS levando 22,44 s contra 6,75 s da BFS. Em n=3000 a DFS nem terminou (passou de 60 s), enquanto a BFS terminou em 16,43 s e a UCS em 35,56 s. Ou seja: com estados visitados guardados (a única forma de não entrar em loop, ponto 1 da Seção 12 do enunciado), a DFS não economiza memória — ela consome muito mais que a BFS. (iii) Ambiente estático e observável permite planejar com antecedência, mas não torna ótima uma busca que ignora o custo. |

**Recomendação à diretoria.** **Recusar a proposta no estado atual.** Quatro das cinco afirmações são incorretas e uma é parcialmente correta: a rota “ótima” usa heurística inadmissível (custou 28 contra 27 na nossa grade), o detector esconde atrás da sensibilidade que 63 de cada 100 alertas são falsos (≈ 12 h/semana de agrônomo) e a DFS nem é ótima. **Muda para “contratar com ressalvas” se** a AgroVision (i) usar heurística admissível ou provar custo igual ao UCS em ≥ 100 pomares nossos; (ii) provar VPP ≥ 90% (ou ≤ 2 h/semana de falsos) num piloto de campo; (iii) medir, e não supor, a independência das leituras.

## Parte 6 — Uso de IA

Ver [`ANEXO_IA.md`](ANEXO_IA.md).
