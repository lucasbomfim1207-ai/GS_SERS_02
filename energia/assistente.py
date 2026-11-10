"""Assistente de texto (CLI) – funcionalidades de energia do Citizen Assist AI.

Baseado em regras + resultados de modelo.py (sem LLM), para que cada resposta seja
rastreável aos cálculos e às premissas.
"""
import re
from .modelo import carregar_premissas, comparar, consumo_mensal_chuveiro, energia_kwh, sensibilidade_tarifa

AVISO = ("⚠️ Valores são ESTIMATIVAS baseadas em premissas (ver docs/referencias.md). "
         "Não são garantia de economia. Confira a tarifa na sua conta e peça orçamentos.")


def _brl(v):
    return "R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _pb(x):
    if x is None:
        return "não se paga no horizonte"
    return "imediato (sem investimento)" if x == 0 else f"{x:.1f} anos".replace(".", ",")


class Assistente:
    def __init__(self):
        self.p = carregar_premissas()
        self.moradia = None  # 'propria' ou 'alugada'

    def definir_moradia(self, resposta):
        r = resposta.strip().lower()
        self.moradia = "alugada" if "alug" in r else "propria"

    def ajuda(self):
        return ("Posso ajudar com energia em casa. Experimente:\n"
                "• 'quanto gasta meu chuveiro'  • 'configurar' (pessoas/minutos/tarifa)\n"
                "• 'comparar alternativas'  • 'solar vale a pena?'  • 'dicas'\n"
                "• 'aparelho: 5500 W por 30 min'  • 'fontes' / 'limitações'  • 'sair'")

    def chuveiro(self):
        kwh = consumo_mensal_chuveiro(self.p)
        t = self.p["tarifa_kwh_com_tributos"]
        return (f"Com {int(self.p['pessoas_domicilio'])} pessoas, {self.p['duracao_banho_min']:.0f} min de banho "
                f"e chuveiro de {self.p['potencia_chuveiro_w']:.0f} W, o consumo é ≈ {kwh:.0f} kWh/mês, "
                f"cerca de {_brl(kwh * t)}/mês (tarifa estimada {_brl(t)}/kWh).\n"
                f"Cálculo: E = P × t = {self.p['potencia_chuveiro_w']/1000:.1f} kW × horas de banho no mês.\n{AVISO}")

    def aparelho(self, watts, minutos_dia):
        kwh_mes = energia_kwh(watts, minutos_dia) * self.p["dias_mes"]
        return (f"Um aparelho de {watts:.0f} W usado {minutos_dia:.0f} min/dia consome ≈ {kwh_mes:.1f} kWh/mês "
                f"≈ {_brl(kwh_mes * self.p['tarifa_kwh_com_tributos'])}/mês.\n{AVISO}")

    def comparacao(self):
        r = comparar(self.p)
        anos = int(self.p["horizonte_anos"])
        out = [f"Comparação para a MESMA necessidade (banho quente da família) em {anos} anos:\n"]
        for x in r:
            out.append(f"• {x.nome}\n   rede: {x.kwh_mes_rede:.0f} kWh/mês | economia: {_brl(x.economia_rs_mes)}/mês | "
                       f"investimento: {_brl(x.investimento_rs)} | retorno: {_pb(x.payback_anos)} | "
                       f"custo total em {anos} anos: {_brl(x.custo_total_horizonte_rs)} | "
                       f"CO₂ evitado: {x.evitado_kgco2_ano:.0f} kg/ano")
        melhor = min(r[1:], key=lambda z: z.custo_total_horizonte_rs)
        out.append(f"\n👉 Pelo menor custo total estimado, destaca-se: {melhor.nome}. "
                   "Comece pelo que não custa nada (A) e peça orçamentos para B ou C.\n" + AVISO)
        return "\n".join(out)

    def solar(self):
        r = comparar(self.p)
        b, c = r[2], r[3]
        sens = sensibilidade_tarifa(self.p, [0.80, 1.10, 1.40])
        linhas = "\n".join(f"   tarifa {_brl(t)}: solar térmico {_pb(pb)} | fotovoltaico {_pb(pc)}" for t, pb, pc in sens)
        aviso_aluguel = ""
        if self.moradia == "alugada":
            aviso_aluguel = ("Como você mora de aluguel, B e C dependem de autorização do proprietário e o "
                             "investimento pode não compensar: comece pela alternativa A.\n")
        return (f"Solar pode valer a pena, depende do seu caso.\n{aviso_aluguel}"
                f"• Aquecedor solar: retorno ≈ {_pb(b.payback_anos)} (investimento {_brl(b.investimento_rs)}).\n"
                f"• Fotovoltaico: retorno ≈ {_pb(c.payback_anos)} (investimento {_brl(c.investimento_rs)}).\n"
                f"Sensibilidade à tarifa:\n{linhas}\n"
                "Condições: telhado próprio com sol, sem sombra, e capacidade de investir/financiar. "
                "Quem mora de aluguel ou tem pouco espaço deve priorizar a alternativa A.\n" + AVISO)

    def dicas(self):
        return ("Dicas de baixo custo: 1) banhos mais curtos; 2) use a posição 'verão' quando o clima permitir; "
                "3) troque lâmpadas por LED; 4) tire da tomada aparelhos que não usa (stand-by); "
                "5) verifique a etiqueta Procel/ENCE ao comprar. Consulte sua conta para ver onde está o maior gasto.")

    def fontes(self):
        return ("Fontes: ANEEL (tarifas), Lei 14.300/2022 (microgeração), Atlas Brasileiro de Energia Solar – INPE, "
                "CRESESB/SunData, Inmetro-PBE/Procel, MCTI (fator de emissão). Detalhes em docs/referencias.md.")

    def limitacoes(self):
        return ("Limitações: dados estimados e não personalizados; tarifa varia por distribuidora e mês (bandeiras); "
                "custos variam por orçamento; geração depende de sombra, orientação e clima; "
                "não considera inflação nem juros de financiamento; o CO₂ evitado é pequeno porque a rede brasileira já é "
                "majoritariamente renovável. Não substitui um projeto técnico.")

    def configurar(self, entrada=input, saida=print):
        campos = [("pessoas_domicilio", "Quantas pessoas moram na casa?"),
                  ("duracao_banho_min", "Quantos minutos dura um banho (média)?"),
                  ("potencia_chuveiro_w", "Potência do chuveiro em W (veja a etiqueta)?"),
                  ("tarifa_kwh_com_tributos", "Valor do kWh na sua conta (R$/kWh, com impostos)?")]
        for chave, pergunta in campos:
            while True:
                bruto = entrada(f"{pergunta} [atual: {self.p[chave]}] ").strip().replace(",", ".")
                if bruto == "":
                    break
                try:
                    v = float(bruto)
                    if v <= 0:
                        raise ValueError
                    self.p[chave] = v
                    break
                except ValueError:
                    saida("Digite um número maior que zero (ou Enter para manter).")
        return "Dados atualizados. " + self.chuveiro()

    def responder(self, texto):
        t = texto.lower()
        m = re.search(r"(\d+[.,]?\d*)\s*w\b.*?(\d+[.,]?\d*)\s*min", t)
        if m:
            return self.aparelho(float(m.group(1).replace(",", ".")), float(m.group(2).replace(",", ".")))
        if any(k in t for k in ["compar", "alternativ"]):
            return self.comparacao()
        if any(k in t for k in ["solar", "renov", "fotovolt", "vale a pena"]):
            return self.solar()
        if "chuveiro" in t or "banho" in t:
            return self.chuveiro()
        if "dica" in t or "economizar" in t:
            return self.dicas()
        if "fonte" in t or "refer" in t:
            return self.fontes()
        if "limit" in t:
            return self.limitacoes()
        return "Não entendi. " + self.ajuda()


def main():
    a = Assistente()
    print("Citizen Assist AI – módulo Energia")
    try:
        a.definir_moradia(input("Antes de começar: você mora em imóvel próprio ou alugado? "))
    except (EOFError, KeyboardInterrupt):
        return
    print(a.ajuda())
    while True:
        try:
            msg = input("\nVocê: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if msg.lower() in {"sair", "exit"}:
            break
        print("\nAssistente:", a.configurar() if msg.lower().startswith("config") else a.responder(msg))


if __name__ == "__main__":
    main()
