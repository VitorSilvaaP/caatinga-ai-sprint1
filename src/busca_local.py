"""Parte 3.4 - Busca local: escolher K = 15 talhoes para inspecionar.

MODELAGEM
  Estado       S = conjunto de K talhoes livres (nao vale portao nem coleta).
  Vizinhanca   TROCA: tira um talhao de S e poe um talhao que estava fora.
  Objetivo     maximizar  f(S) = soma do risco dos talhoes de S
                                 - PENALIDADE * (quanto o tour passa da bateria)
  Risco        mapa de risco FEITO POR NOS (o enunciado nao da um): 4 focos de
               praga gerados a partir da matricula.
  Tour         portao -> talhoes (sempre indo ao mais proximo) -> ponto de coleta,
               usando o custo real de menor caminho entre os talhoes.
  Bateria      6 h = 360 min. Inspecao = 12 min/talhao -> 15*12 = 180 min.
               Sobram 180 min de deslocamento. Premissa nossa: 1 unidade de
               custo = 3 min -> ORCAMENTO = 60 unidades.
"""
import math
import random
import statistics

import buscas as B

K = 15
ORCAMENTO = (360 - K * 12) / 3          # = 60 unidades de custo
PENALIDADE = 2.0                        # pontos perdidos por unidade acima do orcamento


def prepara(grade, matricula):
    """Calcula tudo que a busca local precisa (distancias e mapa de risco)."""
    n = len(grade)
    inicio, fim = (0, 0), (n - 1, n - 1)
    livres = sorted(B.distancias(grade, inicio))          # talhoes alcancaveis
    candidatos = [t for t in livres if t != inicio and t != fim]
    D = {t: B.distancias(grade, t) for t in livres}       # D[a][b] = custo de a ate b

    rng = random.Random(matricula % 1_000_000 + 4242)
    focos = [(rng.choice(candidatos), rng.uniform(6, 10)) for _ in range(4)]
    risco = {}
    for t in candidatos:
        r = rng.uniform(0, 0.5)                           # ruido
        for (fi, fj), forca in focos:
            dist2 = (t[0] - fi) ** 2 + (t[1] - fj) ** 2
            r += forca * math.exp(-dist2 / (2 * 1.5 ** 2))
        risco[t] = r
    return {"inicio": inicio, "fim": fim, "candidatos": candidatos, "D": D,
            "risco": risco, "focos": [f for f, _ in focos]}


def custo_do_tour(P, S):
    D = P["D"]
    atual = P["inicio"]
    faltam = set(S)
    total = 0
    while faltam:
        proximo = None
        for t in faltam:                                  # acha o mais proximo
            if proximo is None or D[atual][t] < D[atual][proximo]:
                proximo = t
        total += D[atual][proximo]
        faltam.remove(proximo)
        atual = proximo
    return total + D[atual][P["fim"]]


def f(P, S):
    excesso = max(0, custo_do_tour(P, S) - ORCAMENTO)
    return sum(P["risco"][t] for t in S) - PENALIDADE * excesso


def estado_inicial(P, rng):
    return set(rng.sample(P["candidatos"], K))


def subida_de_encosta(P, rng):
    """Olha TODOS os vizinhos e vai para o melhor. Para quando nenhum melhora."""
    S = estado_inicial(P, rng)
    fS = f(P, S)
    while True:
        melhor, melhor_f = None, fS
        for sai in S:
            for entra in P["candidatos"]:
                if entra in S:
                    continue
                T = (S - {sai}) | {entra}
                fT = f(P, T)
                if fT > melhor_f:
                    melhor, melhor_f = T, fT
        if melhor is None:                                # otimo local: parou
            return S, fS
        S, fS = melhor, melhor_f


def tempera_simulada(P, rng, T0=6.0, Tf=0.05, passos=20000):
    """Aceita vizinho pior com probabilidade exp(delta/T); T vai caindo.
    Devolve o melhor estado visitado e quantas pioras foram aceitas."""
    S = estado_inicial(P, rng)
    fS = f(P, S)
    melhor, melhor_f = set(S), fS
    alfa = (Tf / T0) ** (1 / passos)                      # resfriamento geometrico
    T = T0
    pioras = 0
    for _ in range(passos):
        sai = rng.choice(sorted(S))
        entra = rng.choice(P["candidatos"])
        if entra not in S:
            T_ = (S - {sai}) | {entra}
            delta = f(P, T_) - fS
            if delta >= 0 or rng.random() < math.exp(delta / T):
                if delta < 0:
                    pioras += 1
                S, fS = T_, fS + delta
                if fS > melhor_f:
                    melhor, melhor_f = set(S), fS
        T = T * alfa
    return melhor, melhor_f, pioras


def roda_30(P, matricula):
    """30 execucoes de cada. A execucao r usa o MESMO estado inicial nos dois."""
    hc, sa, pioras = [], [], []
    for r in range(30):
        semente = matricula % 1_000_000 * 100 + r
        hc.append(subida_de_encosta(P, random.Random(semente))[1])
        _, valor, p = tempera_simulada(P, random.Random(semente))
        sa.append(valor)
        pioras.append(p)
    return hc, sa, pioras


def resumo(valores):
    return {"media": statistics.mean(valores), "desvio": statistics.stdev(valores),
            "melhor": max(valores), "pior": min(valores)}
