"""Parte 2.4 - aumenta o tamanho n do pomar ate uma estrategia falhar.

Uso:  python src/escala.py <matricula>
Gera: resultados/escala.csv

Uma estrategia "falha" quando:
  - passa de 60 segundos                     -> status "tempo>60s"
  - o computador fica sem memoria            -> status "MemoryError"
O n onde isso acontece depende do SEU computador.

CUIDADO: n = 3000 usa ~2 GB de memoria. Se o seu computador for fraco, tire
os numeros maiores da lista abaixo; se nada falhar, acrescente 4000, 5000...
"""
import sys

import buscas as B
from gerador_pomar import gerar_pomar

TAMANHOS = [12, 40, 100, 300, 1000, 2000, 3000]
ESTRATEGIAS = [("BFS", B.bfs), ("DFS", B.dfs), ("UCS", B.ucs)]


def main():
    matricula = int(sys.argv[1])
    arquivo = open("resultados/escala.csv", "w")
    arquivo.write("n,estados,estrategia,status,nos_expandidos,fronteira_max,tempo_s\n")
    for n in TAMANHOS:
        grade = gerar_pomar(matricula, n)
        alguem_falhou = False
        for nome, busca in ESTRATEGIAS:
            try:
                r = busca(grade, limite_s=60)
                linha = [n, n * n, nome, "ok", r["nos_expandidos"], r["fronteira_max"],
                         round(r["tempo_ms"] / 1000, 2)]
            except TimeoutError:
                linha = [n, n * n, nome, "tempo>60s", "", "", ""]
                alguem_falhou = True
            except MemoryError:
                linha = [n, n * n, nome, "MemoryError", "", "", ""]
                alguem_falhou = True
            print(linha, flush=True)
            arquivo.write(",".join(str(x) for x in linha) + "\n")
            arquivo.flush()
        if alguem_falhou:
            break
    arquivo.close()


if __name__ == "__main__":
    main()
