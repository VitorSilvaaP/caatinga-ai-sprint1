"""Buscas no pomar: BFS, DFS, UCS e A*.

Estado = posicao (i, j) do talhao. Todas as buscas guardam os estados ja
visitados (busca em grafo), entao nao entram em laco infinito.

Cada busca devolve um dicionario com:
    rota            lista de estados, do portao ao ponto de coleta
    custo           soma do custo dos talhoes em que entrou (o inicial nao conta)
    passos          numero de movimentos da rota
    nos_expandidos  quantas vezes tiramos um no da fronteira e geramos seus vizinhos
    fronteira_max   maior tamanho que a fronteira teve DURANTE a execucao
    tempo_ms        tempo gasto

ORDEM DE EXPANSAO DOS VIZINHOS (igual para todas as estrategias):
    Norte, Sul, Oeste, Leste
"""
import heapq
import time
from collections import deque

from gerador_pomar import BLOQUEADO, CUSTO

ORDEM = [("Norte", -1, 0), ("Sul", 1, 0), ("Oeste", 0, -1), ("Leste", 0, 1)]
ORDEM_TXT = "Norte, Sul, Oeste, Leste"


# ----------------------------------------------------------------------
# Funcoes auxiliares
# ----------------------------------------------------------------------
def vizinhos(grade, s):
    """Devolve [(estado_vizinho, custo_do_passo), ...] na ordem declarada."""
    n = len(grade)
    lista = []
    for _, di, dj in ORDEM:
        i, j = s[0] + di, s[1] + dj
        if 0 <= i < n and 0 <= j < n and grade[i][j] != BLOQUEADO:
            lista.append(((i, j), CUSTO[grade[i][j]]))
    return lista


def custo_da_rota(grade, rota):
    """Soma o custo de entrar em cada talhao da rota (menos o inicial)."""
    total = 0
    for i, j in rota[1:]:
        total += CUSTO[grade[i][j]]
    return total


def monta_rota(pai, s):
    """Volta pelos 'pais' ate o inicio e devolve a rota na ordem certa."""
    rota = []
    while s is not None:
        rota.append(s)
        s = pai[s]
    rota.reverse()
    return rota


def resultado(grade, rota, expandidos, fronteira_max, t0):
    return {
        "rota": rota,
        "custo": custo_da_rota(grade, rota) if rota else None,
        "passos": len(rota) - 1 if rota else None,
        "nos_expandidos": expandidos,
        "fronteira_max": fronteira_max,
        "tempo_ms": (time.time() - t0) * 1000,
    }


def confere_tempo(t0, limite_s, expandidos):
    """Usado no experimento de escala: aborta se passar do limite de tempo."""
    if limite_s is not None and expandidos % 2000 == 0:
        if time.time() - t0 > limite_s:
            raise TimeoutError("passou de %s s" % limite_s)


# ----------------------------------------------------------------------
# BFS - fila (FIFO). Testa o objetivo quando GERA o no.
# ----------------------------------------------------------------------
def bfs(grade, limite_s=None):
    t0 = time.time()
    n = len(grade)
    inicio, objetivo = (0, 0), (n - 1, n - 1)
    fila = deque([inicio])
    pai = {inicio: None}          # tambem serve para lembrar quem ja foi visto
    expandidos = 0
    fronteira_max = 1
    while fila:
        s = fila.popleft()
        expandidos += 1
        confere_tempo(t0, limite_s, expandidos)
        for viz, _ in vizinhos(grade, s):
            if viz not in pai:
                pai[viz] = s
                if viz == objetivo:                       # teste na geracao
                    return resultado(grade, monta_rota(pai, viz), expandidos, fronteira_max, t0)
                fila.append(viz)
                fronteira_max = max(fronteira_max, len(fila))
    return resultado(grade, [], expandidos, fronteira_max, t0)


# ----------------------------------------------------------------------
# DFS - pilha (LIFO), com conjunto de explorados (senao entra em laco).
# ----------------------------------------------------------------------
def dfs(grade, limite_s=None):
    t0 = time.time()
    n = len(grade)
    inicio, objetivo = (0, 0), (n - 1, n - 1)
    pilha = [(inicio, None)]      # (estado, pai). Pode ter estados repetidos.
    pai = {}
    explorados = set()
    expandidos = 0
    fronteira_max = 1
    while pilha:
        s, quem_gerou = pilha.pop()
        if s in explorados:
            continue
        explorados.add(s)
        pai[s] = quem_gerou
        if s == objetivo:
            return resultado(grade, monta_rota(pai, s), expandidos, fronteira_max, t0)
        expandidos += 1
        confere_tempo(t0, limite_s, expandidos)
        # empilha ao contrario, para o 1o vizinho da ORDEM ser o primeiro a sair
        for viz, _ in reversed(vizinhos(grade, s)):
            if viz not in explorados:
                pilha.append((viz, s))
        fronteira_max = max(fronteira_max, len(pilha))
    return resultado(grade, [], expandidos, fronteira_max, t0)


# ----------------------------------------------------------------------
# Heuristica h1 = 0 (usada pelo UCS). As outras entram no proximo commit.
# ----------------------------------------------------------------------
def h1(s, objetivo):
    return 0


# ----------------------------------------------------------------------
# UCS e A*: fila de PRIORIDADE ordenada por f = g + h.
#   - UCS e o A* com h = 0.
#   - Testa o objetivo quando TIRA o no da fronteira (nao quando gera).
#   - REABRE nos: se acha um caminho mais barato ate um estado, ele volta
#     para a fronteira e pode ser expandido de novo.
# ----------------------------------------------------------------------
def astar(grade, h=h1, limite_s=None):
    t0 = time.time()
    n = len(grade)
    inicio, objetivo = (0, 0), (n - 1, n - 1)
    melhor_g = {inicio: 0}                 # menor custo conhecido ate cada estado
    pai = {inicio: None}
    heap = [(h(inicio, objetivo), 0, 0, inicio)]     # (f, desempate, g, estado)
    na_fronteira = {inicio}                # estados distintos esperando na fronteira
    desempate = 1
    expandidos = 0
    fronteira_max = 1
    while heap:
        f, _, g, s = heapq.heappop(heap)
        if g > melhor_g[s]:
            continue                       # entrada velha: ja achamos caminho melhor
        na_fronteira.discard(s)
        if s == objetivo:                  # teste na expansao
            return resultado(grade, monta_rota(pai, s), expandidos, fronteira_max, t0)
        expandidos += 1
        confere_tempo(t0, limite_s, expandidos)
        for viz, c in vizinhos(grade, s):
            g_novo = g + c
            if g_novo < melhor_g.get(viz, float("inf")):   # achou caminho mais barato
                melhor_g[viz] = g_novo
                pai[viz] = s
                heapq.heappush(heap, (g_novo + h(viz, objetivo), desempate, g_novo, viz))
                desempate += 1
                na_fronteira.add(viz)
        fronteira_max = max(fronteira_max, len(na_fronteira))
    return resultado(grade, [], expandidos, fronteira_max, t0)


def ucs(grade, limite_s=None):
    return astar(grade, h1, limite_s)
