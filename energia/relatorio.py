"""Gera resultados/*.csv a partir de data/premissas.csv. Uso: python -m energia.relatorio"""
import csv
import os
from dataclasses import asdict
from .modelo import carregar_premissas, comparar, sensibilidade_tarifa


def main():
    p = carregar_premissas()
    r = comparar(p)
    os.makedirs("resultados", exist_ok=True)
    with open("resultados/comparacao.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(asdict(r[0]).keys()))
        w.writeheader()
        for x in r:
            w.writerow(asdict(x))
    with open("resultados/sensibilidade_tarifa.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["tarifa_rs_kwh", "payback_solar_termico_anos", "payback_fotovoltaico_anos"])
        for t, b, c in sensibilidade_tarifa(p, [0.80, 0.95, 1.10, 1.25, 1.40]):
            w.writerow([t, None if b is None else round(b, 2), None if c is None else round(c, 2)])
    for x in r:
        print(x.nome, "|", x.kwh_mes_rede, "kWh |", x.economia_rs_mes, "R$/mês | inv", x.investimento_rs,
              "| payback", x.payback_anos, "| total", x.custo_total_horizonte_rs, "| CO2", x.evitado_kgco2_ano)
    print(open("resultados/sensibilidade_tarifa.csv").read())


if __name__ == "__main__":
    main()
