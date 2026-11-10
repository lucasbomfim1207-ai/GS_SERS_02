"""Cálculos de consumo e comparação de alternativas (mesma necessidade: banho quente
de uma família, período de referência comum = horizonte_anos).

Todas as fórmulas estão documentadas em docs/calculos.md.
"""
import csv
import os
from dataclasses import dataclass

CAMINHO_PREMISSAS = os.path.join(os.path.dirname(__file__), "..", "data", "premissas.csv")


def carregar_premissas(caminho=CAMINHO_PREMISSAS):
    p = {}
    with open(caminho, encoding="utf-8") as f:
        for linha in csv.DictReader(f):
            p[linha["parametro"]] = float(linha["valor"])
    return p


def energia_kwh(potencia_w, minutos):
    """E (kWh) = P (kW) x t (h)."""
    if potencia_w < 0 or minutos < 0:
        raise ValueError("Potência e tempo não podem ser negativos.")
    return (potencia_w / 1000.0) * (minutos / 60.0)


def consumo_mensal_chuveiro(p):
    minutos_dia = p["pessoas_domicilio"] * p["banhos_por_pessoa_dia"] * p["duracao_banho_min"]
    return energia_kwh(p["potencia_chuveiro_w"], minutos_dia) * p["dias_mes"]


@dataclass
class Resultado:
    nome: str
    kwh_mes_rede: float
    economia_kwh_mes: float
    economia_rs_mes: float
    investimento_rs: float
    custo_manut_ano_rs: float
    payback_anos: float  # None se não se paga
    custo_total_horizonte_rs: float  # investimento + manutenção + energia paga no horizonte
    evitado_kgco2_ano: float
    observacao: str


def _payback(inv, economia_mes, manut_ano):
    if inv == 0:
        return 0.0
    liquida_ano = economia_mes * 12 - manut_ano
    return inv / liquida_ano if liquida_ano > 0 else None


def comparar(p, tarifa=None):
    """Retorna [base, A (uso consciente), B (solar térmico), C (fotovoltaico)]."""
    t = tarifa if tarifa is not None else p["tarifa_kwh_com_tributos"]
    anos = p["horizonte_anos"]
    base_kwh = consumo_mensal_chuveiro(p)
    ef = p["fator_emissao_rede_kgco2_kwh"]

    def montar(nome, kwh_rede, inv, manut, obs, econ_rs=None):
        econ_kwh = base_kwh - kwh_rede
        econ_rs_mes = econ_rs if econ_rs is not None else econ_kwh * t
        total = inv + manut * anos + (base_kwh * t - econ_rs_mes) * 12 * anos
        return Resultado(nome, round(kwh_rede, 1), round(econ_kwh, 1), round(econ_rs_mes, 2),
                         round(inv, 2), manut, _payback(inv, econ_rs_mes, manut),
                         round(total, 2), round(econ_kwh * 12 * ef, 1), obs)

    base = montar("Base: chuveiro elétrico (situação atual)", base_kwh, 0, 0, "Referência para comparação.")

    p_a = dict(p, duracao_banho_min=p["duracao_banho_min"] - p["reducao_banho_alt_a_min"])
    a = montar("A) Uso consciente (banho mais curto)", consumo_mensal_chuveiro(p_a), 0, 0,
               "Custo zero; depende de mudança de hábito. Reduz também consumo de água.")

    b = montar("B) Aquecedor solar de água + apoio elétrico", base_kwh * (1 - p["fracao_solar_aquecedor"]),
               p["custo_aquecedor_solar_rs"], p["manutencao_aquecedor_solar_rs_ano"],
               "Exige telhado com sol, reservatório e encanamento; vida útil ~"
               f"{int(p['vida_util_aquecedor_anos'])} anos.")

    kwp = base_kwh / (p["irradiacao_hsp_kwh_m2_dia"] * p["dias_mes"] * p["desempenho_global_pr"])
    inv_c = kwp * 1000 * p["custo_fv_rs_por_wp"]
    econ_rs_c = base_kwh * t * (1 - p["fator_perda_fio_b"])
    c = montar(f"C) Energia solar fotovoltaica ({kwp:.2f} kWp)", 0.0, inv_c, p["manutencao_fv_rs_ano"],
               "Compensa o consumo na conta (GD, Lei 14.300/2022); exige análise da "
               "distribuidora, telhado adequado e pode haver taxa mínima.", econ_rs=econ_rs_c)
    return [base, a, b, c]


def sensibilidade_tarifa(p, tarifas):
    """Payback (anos) de B e C para diferentes tarifas."""
    out = []
    for t in tarifas:
        r = comparar(p, tarifa=t)
        out.append((t, r[2].payback_anos, r[3].payback_anos))
    return out
