"""Parte 4.3 - Bayes com os parametros do sensor (parametros_sensor).

  sensibilidade         = P(positivo | infestado)
  taxa_falso_positivo   = P(positivo | sadio)
  prevalencia           = P(infestado)

  VPP = P(infestado | positivo) = sens*prev / (sens*prev + fpr*(1-prev))
"""


def vpp(prev, sens, fpr):
    return sens * prev / (sens * prev + fpr * (1 - prev))


def calcula(par):
    prev = par["prevalencia"]
    sens = par["sensibilidade"]
    fpr = par["taxa_falso_positivo"]
    n = par["talhoes_por_semana"]

    r = {"prev": prev, "sens": sens, "fpr": fpr, "n": n}
    r["numerador"] = sens * prev
    r["falso_termo"] = fpr * (1 - prev)
    r["vpp"] = vpp(prev, sens, fpr)                                   # (a)
    r["falsos_por_100"] = 100 * (1 - r["vpp"])                        # (b)
    r["falsos_semana"] = n * (1 - prev) * fpr                         # (c)
    r["horas_falsos"] = r["falsos_semana"] * 12 / 60                  # 12 min por inspecao
    r["vpp_sens_999"] = vpp(prev, 0.999, fpr)                         # (d)
    r["vpp_fpr_metade"] = vpp(prev, sens, fpr / 2)
    r["falsos_semana_fpr_metade"] = n * (1 - prev) * fpr / 2
    # dois testes positivos, ASSUMINDO que os erros sao independentes (Parte 5, item 4)
    r["vpp_dois_testes"] = sens ** 2 * prev / (sens ** 2 * prev + fpr ** 2 * (1 - prev))
    return r


if __name__ == "__main__":
    import sys
    from gerador_pomar import parametros_sensor
    matricula = int(sys.argv[1]) if len(sys.argv) > 1 else 20231045
    par = parametros_sensor(matricula)
    print(par)
    for nome, valor in calcula(par).items():
        print("%-26s %.6g" % (nome, valor))
