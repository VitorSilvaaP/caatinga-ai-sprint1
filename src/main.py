"""Ponto de entrada. Uso:

    python src/main.py <matricula>

Gera:
    resultados/pomar.txt        grade + parametros do sensor (matricula na 1a linha)
    resultados/resultados.csv   estrategia,heuristica,custo,passos,nos_expandidos,fronteira_max,tempo_ms
    resultados/grafico.png      nos expandidos x estrategia
    resultados/saida.txt        TUDO que foi impresso (use para preencher o RELATORIO.md)

O experimento de escala (Parte 2.4) e separado, porque demora:
    python src/escala.py <matricula>
"""
import os
import sys

import bayes
import buscas as B
import busca_local as BL
import contraexemplo
import especialista
from gerador_pomar import gerar_pomar, parametros_sensor

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RESULTADOS = os.path.join(RAIZ, "resultados")
saida = []


def escreve(texto=""):
    """Imprime na tela e guarda para gravar em resultados/saida.txt."""
    print(texto)
    saida.append(texto)


def roda_as_buscas(grade):
    """Roda as 6 buscas. Devolve uma lista de dicionarios."""
    lista = [
        ("BFS", "-", lambda: B.bfs(grade)),
        ("DFS", "-", lambda: B.dfs(grade)),
        ("UCS", "-", lambda: B.ucs(grade)),
        ("A*", "h1 (=0)", lambda: B.astar(grade, B.h1)),
        ("A*", "h2 (Manhattan)", lambda: B.astar(grade, B.h2)),
        ("A*", "h3 (4xManhattan)", lambda: B.astar(grade, B.h3)),
    ]
    resultados = []
    for estrategia, heuristica, rodar in lista:
        tempos = []
        for _ in range(5):                    # roda 5 vezes e guarda a mediana do tempo
            r = rodar()
            tempos.append(r["tempo_ms"])
        r["tempo_ms"] = sorted(tempos)[2]
        r["estrategia"], r["heuristica"] = estrategia, heuristica
        resultados.append(r)
    return resultados


def grava_csv(resultados):
    with open(os.path.join(RESULTADOS, "resultados.csv"), "w") as f:
        f.write("estrategia,heuristica,custo,passos,nos_expandidos,fronteira_max,tempo_ms\n")
        for r in resultados:
            f.write("%s,%s,%d,%d,%d,%d,%.3f\n" % (
                r["estrategia"], r["heuristica"], r["custo"], r["passos"],
                r["nos_expandidos"], r["fronteira_max"], r["tempo_ms"]))


def grava_grafico(resultados, matricula):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    nomes = []
    for r in resultados:
        if r["heuristica"] == "-":
            nomes.append(r["estrategia"])
        else:
            nomes.append("A*\n" + r["heuristica"].split()[0])
    valores = [r["nos_expandidos"] for r in resultados]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    barras = ax.bar(nomes, valores)
    ax.bar_label(barras)
    ax.set_xlabel("Estrategia de busca (A* com heuristica h1, h2, h3)")
    ax.set_ylabel("Nos expandidos (contagem)")
    ax.set_title("Nos expandidos por estrategia - semente %d" % matricula)
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTADOS, "grafico.png"), dpi=150)


def main():
    if len(sys.argv) < 2:
        sys.exit("uso: python src/main.py <matricula>")
    matricula = int(sys.argv[1])
    os.makedirs(RESULTADOS, exist_ok=True)

    grade = gerar_pomar(matricula)
    par = parametros_sensor(matricula)
    with open(os.path.join(RESULTADOS, "pomar.txt"), "w") as f:
        f.write("%d\n" % matricula)
        for linha in grade:
            f.write(" ".join(linha) + "\n")
        f.write(str(par) + "\n")

    escreve("=== POMAR (semente %d) ===" % matricula)
    for linha in grade:
        escreve(" ".join(linha))
    escreve(str(par))
    livres = sum(1 for linha in grade for c in linha if c != "#")
    escreve("talhoes livres (estados): %d de 144" % livres)

    # ---------------- Parte 2.2 e 3.1 ----------------
    resultados = roda_as_buscas(grade)
    grava_csv(resultados)
    grava_grafico(resultados, matricula)
    escreve("\n=== 2.2 e 3.1: TABELA (ordem de vizinhos: %s) ===" % B.ORDEM_TXT)
    escreve("| Estrategia | Heuristica | Custo | Passos | Nos expandidos | Fronteira max. | Tempo (ms) |")
    escreve("|---|---|---:|---:|---:|---:|---:|")
    for r in resultados:
        escreve("| %s | %s | %d | %d | %d | %d | %.3f |" % (
            r["estrategia"], r["heuristica"], r["custo"], r["passos"],
            r["nos_expandidos"], r["fronteira_max"], r["tempo_ms"]))

    otimo = resultados[2]["custo"]
    for r in resultados[:2]:
        escreve("%s: custo %d, otimo %d -> %s" % (
            r["estrategia"], r["custo"], otimo, "OTIMA" if r["custo"] == otimo else "NAO e otima"))

    # ---------------- Parte 3.2 ----------------
    escreve("\n=== 3.2: onde a heuristica superestima o custo real ===")
    for nome, h in [("h2", B.h2), ("h3", B.h3)]:
        lista = B.superestimacoes(grade, h)
        escreve("%s superestima em %d talhoes" % (nome, len(lista)))
        for excesso, s, valor_h, real in lista[:3]:
            escreve("   talhao %s: %s = %d, custo real restante = %d (excesso %d)" % (
                s, nome, valor_h, real, excesso))
    vizinho = B.vizinhos(grade, (11, 11))[0][0]            # um talhao livre ao lado do objetivo
    escreve("h3 no talhao vizinho do objetivo %s: h3 = %d, real = %d" % (
        vizinho, B.h3(vizinho, (11, 11)), B.distancias(grade, vizinho)[(11, 11)]))

    # ---------------- Parte 3.4 ----------------
    escreve("\n=== 3.4: busca local (K = %d, 30 execucoes cada) ===" % BL.K)
    P = BL.prepara(grade, matricula)
    escreve("focos de praga do mapa de risco: %s" % P["focos"])

    # ---------------- Parte 1.4 (dados para a metrica perversa) ----------------
    # Metrica ruim: "menor custo de deslocamento por talhao inspecionado".
    # O agente escolheria os K talhoes MAIS BARATOS de alcancar a partir do portao.
    custo_do_portao = P["D"][P["inicio"]]
    baratos = sorted(P["candidatos"], key=lambda t: custo_do_portao[t])[:BL.K]
    riscosos = sorted(P["candidatos"], key=lambda t: -P["risco"][t])[:BL.K]
    total_risco = sum(P["risco"].values())
    escreve("\n=== 1.4: dados da metrica perversa ===")
    escreve("os %d talhoes mais baratos de alcancar: %d sao '~'" % (
        BL.K, sum(1 for t in baratos if grade[t[0]][t[1]] == "~")))
    escreve("risco coberto por eles: %.1f%% do total" % (100 * sum(P["risco"][t] for t in baratos) / total_risco))
    escreve("risco coberto pelos %d de MAIOR risco: %.1f%% do total" % (
        BL.K, 100 * sum(P["risco"][t] for t in riscosos) / total_risco))
    for foco in P["focos"]:
        posicao = sorted(P["candidatos"], key=lambda t: custo_do_portao[t]).index(foco) + 1
        escreve("foco %s: custo de acesso %d, posicao %d de %d no ranking de custo" % (
            foco, custo_do_portao[foco], posicao, len(P["candidatos"])))
    caros = sorted(P["candidatos"], key=lambda t: -custo_do_portao[t])[:4]
    escreve("talhoes mais caros de alcancar: %s" % caros)
    hc, sa, pioras = BL.roda_30(P, matricula)
    for nome, valores in [("Subida de encosta", hc), ("Tempera simulada", sa)]:
        s = BL.resumo(valores)
        escreve("%-18s media %.2f  desvio %.2f  melhor %.2f  pior %.2f" % (
            nome, s["media"], s["desvio"], s["melhor"], s["pior"]))
    melhor_global = max(hc + sa)
    escreve("valores finais DISTINTOS da subida de encosta: %d de 30" % len({round(x, 3) for x in hc}))
    escreve("execucoes que chegaram ao melhor valor global (%.2f): subida %d, tempera %d" % (
        melhor_global, sum(1 for x in hc if x > melhor_global - 1e-6),
        sum(1 for x in sa if x > melhor_global - 1e-6)))
    escreve("comparacao pareada (mesmo inicio): tempera melhor em %d, igual em %d, pior em %d" % (
        sum(1 for a, b in zip(hc, sa) if b > a + 1e-6),
        sum(1 for a, b in zip(hc, sa) if abs(a - b) <= 1e-6),
        sum(1 for a, b in zip(hc, sa) if b < a - 1e-6)))
    escreve("pioras aceitas pela tempera por execucao (media): %.0f" % (sum(pioras) / 30))
    with open(os.path.join(RESULTADOS, "busca_local.csv"), "w") as f:
        f.write("execucao,subida_de_encosta,tempera_simulada,pioras_aceitas\n")
        for i in range(30):
            f.write("%d,%.4f,%.4f,%d\n" % (i + 1, hc[i], sa[i], pioras[i]))

    # ---------------- Parte 4 ----------------
    escreve("\n" + especialista.demonstracao())

    escreve("\n=== 4.3 Bayes ===")
    b = bayes.calcula(par)
    for nome, valor in b.items():
        escreve("%-26s %.6g" % (nome, valor))

    # ---------------- Bonus ----------------
    escreve("\n=== BONUS: contraexemplo 8x8 para a DFS ===")
    g8 = contraexemplo.constroi()
    for linha in g8:
        escreve(" ".join(linha))
    d, u = B.dfs(g8), B.ucs(g8)
    escreve("DFS custo %d | otimo %d | razao %.2f" % (d["custo"], u["custo"], d["custo"] / u["custo"]))

    with open(os.path.join(RESULTADOS, "saida.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(saida) + "\n")


if __name__ == "__main__":
    main()
