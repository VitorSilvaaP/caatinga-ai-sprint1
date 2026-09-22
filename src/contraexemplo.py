"""Bonus (Liga de IA): pomar 8x8 feito a mao em que a DFS (ordem Norte, Sul,
Oeste, Leste) devolve rota com mais que o DOBRO do custo otimo.

Ideia: a DFS quase sempre prefere ir para o SUL. Entao pomos '~' (custo 4)
na coluna 0 e na linha 7, por onde ela vai passar, e deixamos '.' (custo 1)
o resto, por onde o caminho otimo passa.

(Curiosidade que a execucao mostrou: a DFS nao segue so a linha 7. Em (7,1)
o Norte ainda esta livre e vem antes do Leste, entao ela sobe a coluna 1 e
varre o pomar em serpentina. O contraexemplo vale do mesmo jeito.)
"""
import buscas as B


def constroi():
    grade = [["." for _ in range(8)] for _ in range(8)]
    for k in range(1, 8):
        grade[k][0] = "~"              # coluna 0 (menos o portao)
    for k in range(1, 7):
        grade[7][k] = "~"              # linha 7 (menos a coleta)
    return grade


if __name__ == "__main__":
    grade = constroi()
    for linha in grade:
        print(" ".join(linha))
    d = B.dfs(grade)
    u = B.ucs(grade)
    print("DFS  custo", d["custo"], "rota", d["rota"])
    print("otimo custo", u["custo"], "rota", u["rota"])
    print("DFS custa", round(d["custo"] / u["custo"], 2), "vezes o otimo")
