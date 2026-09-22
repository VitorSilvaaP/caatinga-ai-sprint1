# Relatório — Sprint 1 do Projeto Caatinga.AI

Disciplina: Inteligência Artificial — UniRios — 2026.2 · Prof. Ronierison Maciel

**Matrícula-semente:** `20231045` · **Ordem de expansão dos vizinhos (todas as estratégias):** Norte, Sul, Oeste, Leste · **O A\* reabre nós:** sim.

> ⚠ **PARA A DUPLA:** os números abaixo são da matrícula fictícia do enunciado (20231045). Ao rodar `python src/main.py <sua matrícula>` (e `python src/escala.py <sua matrícula>`), o arquivo `resultados/saida.txt` traz todos os números da *sua* semente. **Troque os números deste texto pelos da sua saída** (partes 0, 1.4, 2, 3, 4.3 e 5) e apague este aviso. As explicações continuam valendo, mas confira as frases marcadas com “Se na sua semente…”.

## 0. O pomar e o sensor

```
. . ~ . . ~ . ~ . . . .
~ ~ # # . # # ~ . ~ ~ ~
# ~ . . . . ~ . # ~ . ~
. # . # . ~ . ~ . ~ . #
# # ~ . # . # ~ ~ ~ # ~
~ # # . . . . . . . . .
. . . . ~ . . . ~ ~ . ~
. . ~ . . ~ . . . ~ ~ .
. # . ~ . ~ ~ . . . ~ #
. ~ ~ ~ ~ ~ # ~ ~ . # .
# # ~ # . # ~ # . ~ ~ ~
. ~ ~ . . . ~ . . # . .
```

`.` carreador (custo 1) · `~` encharcado (custo 4) · `#` bloqueado. Portão (0,0), coleta (11,11): 69 carreadores, 49 encharcados, 26 bloqueados.

Sensor: prevalência 0,0337 · sensibilidade 0,99 · taxa de falso positivo 0,03 · 1200 talhões/semana.

## Parte 1 — O agente antes do código

### 1.1 Ficha PEAS

| Componente | Especificação |
|---|---|
| **P** (desempenho) | (i) **custo da rota** em unidades de custo de entrada (1 un. ≈ 3 min, premissa nossa) — minimizar; ótimo neste pomar = 34 un.; (ii) **recall de talhões infestados sinalizados** (%) — meta ≥ sensibilidade do sensor (99%); (iii) **horas de agrônomo por semana gastas com alertas falsos** (h/semana) — hoje 6,96 h/semana (item 4.3c) |
| **E** (ambiente) | Pomar 12 × 12 (`.`, `~`, `#`), portão (0,0), coleta (11,11), pragas com prevalência de 3,4%, umidade/irrigação, agrônomos que recebem os alertas |
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
- **Comportamento aprendido:** inspecionar sempre os talhões *mais baratos de alcançar*. Com K = 15, ele escolhe os 15 mais baratos a partir do portão; **5 de 15** são `~`, e eles cobrem só **1,1%** do risco total (nosso mapa de risco), contra **37,8%** que os 15 de maior risco cobririam.
- **Onde aparece no pomar:** nas zonas caras de alcançar — por exemplo (9,11), (11,0), (10,6), (10,11) — e nos focos de infestação do nosso mapa de risco: (5,10) [custo de acesso 21, posição 50 de 115], (9,4) [25, posição 84], (8,9) [23, posição 71] e (10,6) [36, posição 111 de 115]. Nenhum foco entra entre os 15 mais baratos: o agente nunca vai lá. (O mapa de risco é **modelo nosso**, gerado da matrícula; a premissa é que solo encharcado/irrigação favorece pragas.)
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

**Número de estados:** o estado é só a posição (i,j) (não guardamos quais talhões já foram inspecionados). Contando na grade: 12 × 12 = 144 − 26 bloqueados = **118 estados**; 117 são alcançáveis do portão (o talhão (3,0) está cercado por `#`).

### 2.2 BFS, DFS e UCS

BFS testa o objetivo **ao gerar** o nó; UCS e A\* testam **ao expandir**. “Nós expandidos” = nós retirados da fronteira que tiveram vizinhos gerados. Fronteira máxima = maior tamanho durante a execução.

| Estratégia | Custo da rota (un.) | Nº de passos | Nós expandidos (nº) | Fronteira máx. (nós) | Tempo (ms) | Rota é ótima em custo? |
|---|---:|---:|---:|---:|---:|---|
| BFS | 55 | 22 | 114 | 13 | 0,145 | **Não** (+21 un., +62%) |
| DFS | 84 | 36 | 103 | 60 | 0,157 | **Não** (+50 un., +147%) |
| UCS | 34 | 22 | 111 | 23 | 0,216 | **Sim** (garantido) |

*Por que a fronteira máxima da BFS é 13 e não o dobro?* A fila guarda só nós **gerados e ainda não expandidos**; na grade a frente de onda é uma diagonal. Os nós já visitados ficam num dicionário à parte, que não conta como fronteira.

### 2.3 Por que a BFS devolveu rota mais cara (não é bug)

A BFS achou custo **55** com **22** passos, o menor número possível. O UCS achou **34**, também com 22 passos. A BFS minimiza **passos**, não **custo**, e só é ótima em custo quando **todas as ações têm o mesmo custo**. **Hipótese da Aula 03 violada: custo de passo uniforme** — aqui um passo custa 1 (`.`) ou 4 (`~`), então a rota com menos passos pode atravessar `~` e sair mais cara. O UCS generaliza a BFS: expande por menor custo acumulado g(n).

> Se na sua semente a BFS deu o mesmo custo do UCS, diga que foi coincidência de grade (a BFS não garante). Se o UCS tiver mais passos que a BFS, diga: “mais passos, porém mais barato”.

### 2.4 Escalando n até falhar (`python src/escala.py 20231045`, limite 60 s)

| n | Estados (n²) | Estratégia | Status | Nós expandidos (nº) | Fronteira máx. (nós) | Tempo (s) |
|---:|---:|---|---|---:|---:|---:|
| 1000 | 1.000.000 | BFS | ok | 798.893 | 923 | 1,53 |
| 1000 | 1.000.000 | DFS | ok | 626.867 | 404.943 | 2,33 |
| 1000 | 1.000.000 | UCS | ok | 798.893 | 1.477 | 3,23 |
| 2000 | 4.000.000 | BFS | ok | 3.194.526 | 1.823 | 6,75 |
| 2000 | 4.000.000 | DFS | ok | 2.476.537 | 1.603.423 | 22,44 |
| 2000 | 4.000.000 | UCS | ok | 3.194.523 | 2.951 | 14,32 |
| 3000 | 9.000.000 | BFS | ok | 7.187.682 | 2.699 | 16,43 |
| 3000 | 9.000.000 | DFS | **tempo > 60 s** | — | — | — |
| 3000 | 9.000.000 | UCS | ok | 7.187.681 | 4.412 | 35,56 |

(Todas as linhas, de n = 12 a 3000, estão em `resultados/escala.csv`. Tempos dependem da máquina; estes foram medidos no computador em que rodamos.)

**Falhou:** a **DFS**, em **n = 3000**, por **tempo (> 60 s)**. O UCS já levava 35,6 s nesse n e seria o próximo a falhar.

**Relação com a fórmula da Aula 03.** Em *busca em árvore*, BFS/UCS custam O(b^d) tempo e memória: com b ≈ 3 (uma das 4 direções volta ao pai) e d = 22 já em n = 12, seriam ~3²² ≈ 3×10¹⁰ nós. Como guardamos os estados visitados (*busca em grafo*), o custo cai para O(n²) estados. Medido: em n = 3000 a BFS expandiu 7.187.682 nós = **79,9%** dos 9.000.000 estados, coerente com ~80% dos talhões livres (P(`#`) = 0,20). A fronteira da BFS/UCS cresce ~n (2.699 em n = 3000), mas a da DFS cresce ~n² (1.603.423 em n = 2000 ≈ 0,4·n²), porque nossa DFS empilha estados repetidos; por isso ela gasta ~9 µs por nó contra ~2 µs da BFS e estoura o tempo primeiro. *(Não medimos memória nesta versão. As fórmulas são as de AIMA cap. 3; confira a notação exata da Aula 03.)*

## Parte 3 — Busca informada

### 3.1 A\* com três heurísticas (versão que **reabre nós**)

| Heurística | Custo da rota (un.) | Nós expandidos (nº) | Admissível? (prova) |
|---|---:|---:|---|
| h1(n) = 0 | 34 | 111 | **Sim.** 0 ≤ h\*(n), pois todo passo custa ≥ 1. (A\* com h1 é o UCS.) |
| h2(n) = Manhattan | 34 | 90 | **Sim.** De n ao objetivo são necessários ≥ Manhattan(n) passos, cada um custa ≥ 1, logo h\*(n) ≥ Manhattan(n). Conferido por força bruta: 0 violações nos 117 estados alcançáveis. |
| h3(n) = 4×Manhattan | 34 | 24 | **Não.** Superestima em 114 dos 117 estados (ex.: (0,0): h3 = 88 > h\* = 34). |

### 3.2 Admissibilidade de h2 e violação de h3

**h2 admissível.** Seja c_min = 1 o menor custo de entrada em um talhão. Qualquer caminho de (i,j) até (11,11) precisa de pelo menos |11−i| + |11−j| movimentos, e cada um entra num talhão de custo ≥ c_min = 1. Logo h\*(n) ≥ Manhattan(n) = h2(n). ∎

**h3 superestima** (h\* = custo real restante, calculado por Dijkstra):

| Talhão n | Objetivo | Manhattan | h3(n) | h\*(n) real | Excesso |
|---|---|---:|---:|---:|---:|
| (0, 0) | (11, 11) | 22 | 88 | 34 | +54 |
| (10, 11) | (11, 11) | 1 | 4 | 1 | +3 |

### 3.3 h3 versus UCS

O custo de h3 foi **34 = 34** (igual ao UCS). **Isso prova que h3 é admissível? Não.** Admissibilidade é uma propriedade para *todos* os estados (∀n: h(n) ≤ h\*(n)); um resultado ótimo numa instância é compatível com heurística inadmissível — e já exibimos em 3.2 talhões onde h3 > h\*. O que h3 garante é só uma cota: como h3 ≤ 4·h\*, o A\* devolve custo ≤ 4·C\* = 136; nesta grade ele simplesmente não perdeu. O ganho foi real: **24 nós** contra 111 do UCS (−87, 78% a menos) e 90 do A\* com h2.

> Se na sua semente o custo de h3 ficou **maior**: perda % = (custo_h3 − custo_UCS) / custo_UCS × 100, e nós “comprados” = nós_UCS − nós_h3.

**Quando trocar garantia por velocidade (condição verificável).** Trocar A\*-h2 por A\*-h3 só vale se **(a)** o replanejamento tiver um limite de latência L e o tempo medido do A\*-h2 na malha real passar de L, **e (b)** a perda medida de custo for ≤ τ. Limiares a validar com a cooperativa: L = 200 ms por replanejamento e τ = 10% do custo da rota (≈ 10 min de um trajeto de 102 min). No 12 × 12 o A\*-h2 leva ≈ 0,2 ms ≪ 200 ms, então **(a) não é satisfeita: mantém-se a garantia de otimalidade**. Só passaria a valer em malhas grandes (na 2.4 o UCS já leva 35 s em n = 3000).

### 3.4 Busca local: escolher K = 15 talhões

- *Estado:* conjunto de 15 talhões livres. *Vizinhança:* **troca** (tira um, põe outro). 
- *Objetivo (maximizar):* soma do risco − 2 × (custo do tour que passa de 60 un.). Bateria 6 h = 360 min; inspeção 12 min × 15 = 180 min; sobram 180 min de deslocamento = 60 un. (premissa nossa: 1 un. = 3 min). Tour: portão → talhões (sempre ao mais próximo) → coleta.
- *Risco:* mapa **nosso** (o enunciado não dá): 4 focos gerados da matrícula em (5,10), (9,4), (8,9), (10,6).

| Método (30 execuções) | Média | Desvio-padrão | Melhor | Pior |
|---|---:|---:|---:|---:|
| Subida de encosta | 114,50 | 16,70 | 126,08 | 36,17 |
| Têmpera simulada (T0 = 6, Tf = 0,05, 20.000 passos) | 123,47 | 3,28 | 126,45 | 115,14 |

**Por que aceitar piora ajuda (Aula 04).** A subida de encosta só aceita vizinhos melhores; ao chegar a um ponto onde todos os vizinhos são piores (ótimo local) ela **para**, mesmo havendo algo melhor do outro lado de um “vale”. A têmpera aceita um vizinho pior com probabilidade exp(Δ/T): com T alto atravessa vales, com T baixo refina como a subida de encosta.

**Onde isso aparece nos 30 resultados** (`resultados/busca_local.csv`):
- A subida terminou em **18 valores distintos** em 30 execuções (repetiu ótimos locais) e **nenhuma** execução chegou ao melhor valor global (126,45); a **têmpera chegou 9 vezes**.
- Comparando execução a execução (mesmo estado inicial): têmpera **melhor em 22**, igual em 2, pior em 6.
- A pior execução da subida ficou em 36,17 (presa longe do resto); a pior da têmpera foi 115,14.
- A têmpera aceitou em média **337 movimentos piores** por execução. Isso mostra o mecanismo em ação; o que mostra que ele *ajuda* é a comparação execução a execução acima.

*Transparência:* 20.000 passos foram escolhidos comparando 6.000 e 20.000 na semente de referência; T0 e Tf não foram otimizados.

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

Prevalência = 0,0337; sensibilidade = 0,99; falso positivo = 0,03; 1200 talhões/semana.

**(a)** P(infestado | positivo) = sens·prev / (sens·prev + fpr·(1−prev))
= (0,99 × 0,0337) / (0,99 × 0,0337 + 0,03 × 0,9663) = 0,033363 / (0,033363 + 0,028989) = 0,033363 / 0,062352 = **0,5351 (53,5%)**

**(b)** “A cada 100 alertas do meu sistema, cerca de **46** serão falsos.”

**(c)** Falsos por semana = 1200 × 0,9663 × 0,03 = **34,79 alertas falsos/semana**. Horas = 34,79 × 12 min / 60 = **6,96 h/semana** perseguindo alerta falso. (Premissa: todos os 1200 talhões passam pelo sensor e cada alerta gera uma inspeção de 12 min.)

**(d)** Com sensibilidade 99,9%: VPP = (0,999 × 0,0337) / (0,999 × 0,0337 + 0,03 × 0,9663) = **0,5373 (53,7%)**, contra 53,5%: ganho de 0,2 ponto percentual. **Não melhorou:** os falsos alertas continuam 34,79/semana (6,96 h), porque só dependem de N·(1−prev)·fpr — a sensibilidade não aparece nessa conta. **Eu mexeria na taxa de falsos positivos** (ou na prevalência dos talhões testados): com fpr pela metade (0,015), o VPP vai a **69,7%** e os falsos caem a 17,4/semana (3,5 h). Ressalva: reduzir fpr costuma custar sensibilidade; alternativas são pré-triagem por risco ou confirmação em segundo estágio.

### 4.4 A regra que salva o modelo

**Decisão que deve ficar em regra explícita:** *autorizar a aplicação de defensivo em um talhão* (período de carência, distância de reservatório/mata). **Argumento de responsabilidade e auditabilidade (não de acurácia):** aplicar agrotóxico exige responsável técnico; se houver autuação ou lote recusado, alguém precisa **responder por quê**. Uma regra explícita gera o traço “disparou R_k porque os fatos F1..Fn”, é versionável linha a linha e muda por decisão humana quando a norma muda, sem retreinar. Um modelo aprendido pode ter acurácia maior, mas não oferece justificativa auditável nem responsável identificável para o caso individual.

## Parte 5 — Auditoria do laudo da AgroVision

| # | Afirmação | Veredito | Justificativa e número medido |
|---|---|---|---|
| 1 | “A\* com Manhattan×4 … rota sempre a mais barata” | **Incorreta** | h3 é **inadmissível**: no talhão (0,0) estima 88 contra h\* = 34 (3.2). A\* só é ótimo com heurística admissível; com 4×Manhattan só se garante custo ≤ 4·C\* = 136. Na nossa grade a rota saiu ótima (34 = 34), mas por coincidência, e o “sempre” é falso. |
| 2 | “BFS → A\*: custo caiu 38%; a heurística melhora a qualidade” | **Parcialmente correta** | O fato pode ocorrer: na nossa grade BFS 55 → A\* 34, queda de **38,2%**. A **causa está errada**: o A\* com h1 = 0 (sem heurística) dá o **mesmo custo 34**. A queda vem de o A\*/UCS considerar o custo g(n), não de h. A heurística só reduz nós expandidos (111 → 90 com h2) e, se inadmissível, pode até piorar a rota. |
| 3 | “99% de sensibilidade ⇒ entre os apontados, 99% infestados” | **Incorreta** | Confunde P(+\|infestado) (sensibilidade) com P(infestado\|+) (VPP). Com prevalência 0,0337 e fpr 0,03, o VPP é **53,5%** (4.3a): ~46 de cada 100 alertas são falsos. |
| 4 | “Dois testes positivos ⇒ confiança passa de 99%” | **Incorreta** | O “99%” era sensibilidade, não confiança. Mesmo supondo leituras **independentes**, VPP com 2 positivos = 0,99² · 0,0337 / (0,99² · 0,0337 + 0,03² · 0,9663) = **97,4%**, abaixo de 99%. E no mesmo talhão os erros do sensor tendem a ser correlacionados, então o valor real é menor. |
| 5 | “DFS usa menos memória; pomar estático e observável ⇒ DFS suficiente” | **Incorreta** | (i) Custo: DFS **84** contra ótimo **34** (+147%). (ii) A vantagem de memória O(bm) só existe se a DFS **não** guardar visitados (busca em árvore), o que traz de volta o laço infinito; com visitados, a fronteira da DFS foi **60** contra **13** da BFS (12×12) e **1.603.423** contra **1.823** em n = 2000, e ela levou 22,4 s contra 6,8 s. (iii) Ambiente estático e observável permite planejar com antecedência, mas não torna ótima uma busca que ignora o custo. |

**Recomendação à diretoria.** **Recusar a proposta no estado atual.** Quatro das cinco afirmações são incorretas e uma é parcialmente correta: a rota “ótima” usa heurística inadmissível (teto de 136 contra 34 na nossa grade), o detector esconde atrás da sensibilidade que 46 de cada 100 alertas são falsos (≈ 7 h/semana de agrônomo) e a DFS nem é ótima. **Muda para “contratar com ressalvas” se** a AgroVision (i) usar heurística admissível ou provar custo igual ao UCS em ≥ 100 pomares nossos; (ii) provar VPP ≥ 90% (ou ≤ 2 h/semana de falsos) num piloto de campo; (iii) medir, e não supor, a independência das leituras.

## Parte 6 — Uso de IA

Ver [`ANEXO_IA.md`](ANEXO_IA.md).
