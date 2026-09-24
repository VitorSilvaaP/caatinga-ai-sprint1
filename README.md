# Caatinga.AI — Sprint 1

## 1. Identificação

- **Disciplina:** Inteligência Artificial — UniRios — 2026.2 (Prof. Ronierison Maciel)
- **Integrante 1:** `[Vitor da Silva Pereira]` — matrícula `[24114060]`
- **Integrante 2:** `[Emylly Vitória Pereira de Sousa Silva]` — matrícula `[MATRÍCULA]`
- **Matrícula usada como semente (integrante mais velho):** `[MATRÍCULA]`

> ⚠ Os números vêm de `python src/main.py 24114060`. Falta rodar `python src/escala.py 24114060` neste computador e preencher a seção 2.4 do `RELATORIO.md`.

## 2. O que este projeto faz

Agente de inspeção de pragas num pomar de manga (grade 12 × 12 gerada da matrícula). Implementa busca cega (BFS, DFS, UCS) e informada (A\* com três heurísticas) contando nós expandidos e fronteira; busca local (subida de encosta e têmpera simulada) para escolher K talhões; um mini sistema especialista com encadeamento para trás; e os cálculos de Bayes do sensor.

## 3. Como rodar

Python 3.10+ (testado em 3.12). Única dependência: `matplotlib`.

```bash
pip install -r requirements.txt
python src/main.py <matricula>       # gera resultados/pomar.txt, resultados.csv, grafico.png e saida.txt
python src/escala.py <matricula>     # Parte 2.4 (demora alguns minutos; usa muita memória)
python src/teste_afericao.py         # confere a caixa de aferição do enunciado
```

## 4. Tabela-resumo dos resultados (semente 24114060)

| Estratégia | Heurística | Custo da rota (un.) | Passos (nº) | Nós expandidos (nº) | Fronteira máx. (nós) |
|---|---|---:|---:|---:|---:|
| BFS | - | 46 | 22 | 117 | 11 |
| DFS | - | 113 | 62 | 94 | 67 |
| UCS | - | 27 | 24 | 109 | 14 |
| A\* | h1 (=0) | 27 | 24 | 109 | 14 |
| A\* | h2 (Manhattan) | 27 | 24 | 45 | 24 |
| A\* | h3 (4×Manhattan) | 28 | 22 | 24 | 24 |

## 5. Decisões declaradas

- **Ordem de expansão dos vizinhos (todas as estratégias):** Norte, Sul, Oeste, Leste.
- **Teste de objetivo:** na *geração* (BFS); na *expansão* (DFS, UCS, A\*).
- **O A\* reabre nós?** **Sim.** Guarda o menor custo conhecido por estado; se acha caminho mais barato, o estado volta à fronteira.
- **Fronteira máxima:** maior tamanho durante a execução (BFS/DFS: itens da estrutura; UCS/A\*: estados distintos esperando).

## 6. Mapa do repositório

| Arquivo | O que resolve |
|---|---|
| [`RELATORIO.md`](RELATORIO.md) | Relatório com as Partes 1 a 5 |
| [`ANEXO_IA.md`](ANEXO_IA.md) | Parte 6: uso de IA |
| `src/gerador_pomar.py` | Gerador do enunciado, **intacto** |
| `src/buscas.py` | BFS, DFS, UCS, A\*, heurísticas e verificação de admissibilidade |
| `src/busca_local.py` | Subida de encosta e têmpera simulada (K = 15) |
| `src/especialista.py` | Regras SE/ENTÃO, encadeamento para trás e explicação |
| `src/bayes.py` | Cálculos da Parte 4.3 |
| `src/escala.py` | Experimento da Parte 2.4 (n até falhar) |
| `src/contraexemplo.py` | Bônus: pomar 8 × 8 em que a DFS custa mais que o dobro do ótimo |
| `src/main.py` | Comando principal |
| `src/teste_afericao.py` | Confere custo/passos/nós com a caixa de aferição |
| `resultados/` | `resultados.csv`, `grafico.png`, `pomar.txt`, `saida.txt`, `escala.csv`, `busca_local.csv` |

## 7. Limitações conhecidas

- O **mapa de risco** da 3.4 é modelo nosso (o enunciado não dá um). O tour usa “vizinho mais próximo”, não o TSP ótimo, e 1 un. de custo = 3 min é premissa nossa.
- **Experimento de escala:** o n de falha depende da máquina. Não medimos memória; só tempo, nós expandidos e fronteira.
- A DFS é iterativa, então não estoura a pilha de recursão.
- A **base de regras** não cobre o caso “armadilha positiva, seco, pulverizado há ≤ 14 dias” (`sem_conclusao`).
- As fórmulas de complexidade citadas são as de AIMA cap. 3; conferir com a notação da Aula 03.
- O item 4 da Parte 5 supõe leituras independentes do sensor.
- **`gerador_pomar.py`:** o PDF do enunciado perdeu a indentação do código ao virar texto (todas as linhas apareceram com o mesmo recuo). Reconstruímos a indentação seguindo a lógica óbvia do algoritmo (a lógica é a mesma; só a formatação foi inferida). Os resultados batem com a caixa de aferição do enunciado (matrícula 20231045: UCS=34, BFS=55/22 passos), o que confirma que a lógica ficou igual à do professor.