"""Caixa de afericao do enunciado (matricula ficticia 20231045).
Rode: python src/teste_afericao.py
Custo e passos precisam bater EXATAMENTE; nos expandidos ate +-20%."""
import buscas as B
from gerador_pomar import gerar_pomar

grade = gerar_pomar(20231045)
ok = True


def confere(nome, condicao):
    global ok
    print("OK   " if condicao else "FALHA", nome)
    ok = ok and condicao


u, b, d = B.ucs(grade), B.bfs(grade), B.dfs(grade)
confere("UCS custo == 34", u["custo"] == 34)
confere("BFS custo == 55", b["custo"] == 55)
confere("BFS passos == 22", b["passos"] == 22)
confere("UCS nos ~112 (obtido %d)" % u["nos_expandidos"], abs(u["nos_expandidos"] - 112) <= 0.2 * 112)
confere("DFS chega ao objetivo", d["rota"][-1] == (11, 11))
if hasattr(B, "h2"):
    a = B.astar(grade, B.h2)
    confere("A* h2 custo == 34", a["custo"] == 34)
    confere("A* h2 nos ~93 (obtido %d)" % a["nos_expandidos"], abs(a["nos_expandidos"] - 93) <= 0.2 * 93)
print("TUDO CERTO" if ok else "TEM ALGO ERRADO")
