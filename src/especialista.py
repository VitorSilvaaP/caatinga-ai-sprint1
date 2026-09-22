"""Parte 4.1 e 4.2 - Mini sistema especialista com ENCADEAMENTO PARA TRAS.

Cada regra tem um nome, uma lista de premissas e uma conclusao:
    ("R2", ["sensor_positivo", "folhas_danificadas"], "infestacao_provavel")
Uma premissa pode comecar com "nao " (ex.: "nao folhas_danificadas").

Encadeamento para tras: comecamos pela META ("inspecionar_prioridade_alta?")
e procuramos regras que a concluam; para cada regra, tentamos provar as
premissas (que podem ser fatos dados ou conclusoes de outras regras).
"""

REGRAS = [
    ("R1", ["armadilha_positiva", "umidade_alta", "pulverizado_ha_mais_de_14_dias"], "risco_alto"),
    ("R2", ["sensor_positivo", "folhas_danificadas"], "infestacao_provavel"),
    ("R3", ["infestacao_provavel"], "inspecionar_prioridade_alta"),
    ("R4", ["risco_alto"], "inspecionar_prioridade_alta"),
    ("R5", ["sensor_positivo", "nao folhas_danificadas"], "inspecionar_rotina"),
    ("R6", ["solo_encharcado", "umidade_alta", "armadilha_positiva"], "risco_alto"),
    ("R7", ["nao sensor_positivo", "nao armadilha_positiva"], "monitorar_normal"),
]
# Regra nova da Parte 4.2 (corrige um caso que a base errava):
R8 = ("R8", ["infestacao_provavel", "pulverizado_ha_ate_7_dias"], "reinspecionar_em_7_dias")

# Ordem de prioridade das decisoes finais (a primeira que for provada vence)
DECISOES = ["inspecionar_prioridade_alta", "inspecionar_rotina", "monitorar_normal"]


def texto_da_regra(regra):
    nome, premissas, conclusao = regra
    return "%s: SE %s ENTAO %s" % (nome, " E ".join(premissas), conclusao)


def provar(meta, fatos, regras, tracos, cadeia, nivel=0):
    """Tenta provar 'meta'. Escreve o passo a passo em 'tracos' e as regras que
    sustentaram a prova em 'cadeia'. Devolve True ou False."""
    recuo = "  " * nivel
    if meta in fatos:                                   # fato dado
        tracos.append("%sfato dado: %s = %s" % (recuo, meta, fatos[meta]))
        return fatos[meta]
    for regra in regras:
        nome, premissas, conclusao = regra
        if conclusao != meta:
            continue
        tracos.append("%sMETA %s? tentando %s" % (recuo, meta, texto_da_regra(regra)))
        provou_todas = True
        for p in premissas:
            if p.startswith("nao "):                    # negacao: nao conseguir provar
                ok = not provar(p[4:], fatos, regras, tracos, [], nivel + 1)
            else:
                ok = provar(p, fatos, regras, tracos, cadeia, nivel + 1)
            if not ok:
                provou_todas = False
                break
        if provou_todas:
            tracos.append("%sOK: %s provado por %s" % (recuo, meta, nome))
            cadeia.append(regra)
            return True
        tracos.append("%s%s nao se aplica" % (recuo, nome))
    return False


def decidir(fatos, regras, decisoes):
    """Devolve (decisao, cadeia_de_regras, traco)."""
    tracos = []
    for d in decisoes:
        cadeia = []
        if provar(d, fatos, regras, tracos, cadeia):
            return d, cadeia, tracos
    return "sem_conclusao", [], tracos


def porque(decisao, cadeia):
    """Resposta a 'por que voce concluiu isso?'."""
    if not cadeia:
        return "Nenhuma regra sustenta uma conclusao."
    linhas = ["Conclui '%s' porque:" % decisao]
    for regra in cadeia:
        linhas.append("  - " + texto_da_regra(regra))
    return "\n".join(linhas)


def fatos(**kw):
    """Cria um talhao com todos os fatos falsos, menos os que voce passar."""
    base = dict(armadilha_positiva=False, umidade_alta=False, solo_encharcado=False,
                sensor_positivo=False, folhas_danificadas=False,
                pulverizado_ha_mais_de_14_dias=False, pulverizado_ha_ate_7_dias=False)
    base.update(kw)
    return base


CASOS = {
    "A armadilha+, umido, pulverizado ha 20 dias": fatos(armadilha_positiva=True, umidade_alta=True, pulverizado_ha_mais_de_14_dias=True),
    "B sensor+ e folhas danificadas": fatos(sensor_positivo=True, folhas_danificadas=True),
    "C sensor+ sem dano visivel": fatos(sensor_positivo=True),
    "D tudo negativo": fatos(),
    "E encharcado, umido, armadilha+": fatos(solo_encharcado=True, umidade_alta=True, armadilha_positiva=True),
    "F armadilha+, seco, pulverizado ha 10 dias": fatos(armadilha_positiva=True),
    "G sensor+ e folhas danificadas, pulverizado ha 2 dias": fatos(sensor_positivo=True, folhas_danificadas=True, pulverizado_ha_ate_7_dias=True),
}
CASO_QUE_QUEBRA = "G sensor+ e folhas danificadas, pulverizado ha 2 dias"


def demonstracao():
    """Devolve o texto do 4.1 (traco), 4.2 (antes/depois) e da regressao."""
    out = []
    regras_novas = REGRAS + [R8]
    decisoes_novas = ["reinspecionar_em_7_dias"] + DECISOES

    out.append("=== 4.1 Traco de execucao (caso B) ===")
    d, cadeia, traco = decidir(CASOS["B sensor+ e folhas danificadas"], REGRAS, DECISOES)
    out += traco + [porque(d, cadeia), ""]

    out.append("=== 4.2 ANTES (base com 7 regras) - caso G ===")
    d, cadeia, traco = decidir(CASOS[CASO_QUE_QUEBRA], REGRAS, DECISOES)
    out += traco + [porque(d, cadeia), ""]

    out.append("=== 4.2 DEPOIS de adicionar " + texto_da_regra(R8) + " ===")
    d, cadeia, traco = decidir(CASOS[CASO_QUE_QUEBRA], regras_novas, decisoes_novas)
    out += traco + [porque(d, cadeia), ""]

    out.append("=== Regressao: os 7 casos antes x depois ===")
    mudaram = 0
    for nome, f in CASOS.items():
        antes = decidir(f, REGRAS, DECISOES)[0]
        depois = decidir(f, regras_novas, decisoes_novas)[0]
        marca = "" if antes == depois else "   <-- MUDOU"
        mudaram += antes != depois
        out.append("%-56s antes=%-28s depois=%s%s" % (nome, antes, depois, marca))
    out.append("casos que mudaram: %d (esperado: 1, so o caso G)" % mudaram)
    return "\n".join(out)


if __name__ == "__main__":
    print(demonstracao())
