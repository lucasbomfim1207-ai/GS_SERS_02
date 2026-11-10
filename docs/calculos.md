# Cálculos e comparação de alternativas

Período de referência comum: **10 anos**. Necessidade comum: **banho quente para 4 pessoas** (1 banho/dia cada).
Premissas: `data/premissas.csv` (cada linha indica se é *oficial*, *estimado* ou *premissa*).

## 1. Consumo-base
- Tempo de banho: 4 pessoas × 1 banho × 8 min = 32 min/dia = 0,533 h/dia
- Potência: 5.500 W = 5,5 kW
- Energia diária: E = P × t = 5,5 × 0,533 = **2,93 kWh/dia**
- Mensal (30 dias): **88 kWh/mês**
- Custo: 88 × R$ 1,10 (estimado) = **R$ 96,80/mês** → R$ 1.161,60/ano → R$ 11.616 em 10 anos

## 2. Alternativa A — Uso consciente
- Banho de 5 min: 4 × 5 = 20 min/dia → 5,5 × 0,333 × 30 = **55 kWh/mês**
- Economia: 33 kWh/mês × R$ 1,10 = **R$ 36,30/mês**; investimento R$ 0.
- CO₂ evitado: 33 × 12 × 0,06 ≈ 24 kg/ano.

## 3. Alternativa B — Aquecedor solar de água (renovável térmica)
- Fração solar anual: 70% → rede = 88 × 0,30 = **26,4 kWh/mês**
- Economia: 61,6 kWh × 1,10 = **R$ 67,76/mês**
- Investimento: R$ 4.500 (estimado); manutenção R$ 100/ano
- Payback = 4.500 / (67,76×12 − 100) = **6,3 anos**
- Custo 10 anos = 4.500 + 100×10 + (96,80 − 67,76)×120 = **R$ 8.985**

## 4. Alternativa C — Fotovoltaico (renovável elétrica)
- Dimensionamento: P_FV (kWp) = E_mensal / (HSP × dias × PR) = 88 / (4,5 × 30 × 0,80) = **0,81 kWp**
- Investimento: 0,81 kWp × 1.000 × R$ 5,00/Wp ≈ **R$ 4.074** (estimado)
- Economia: 88 × 1,10 × (1 − 0,10 de perdas por Fio B/taxas) = **R$ 87,12/mês**
- Payback = 4.074 / (87,12×12 − 80) = **4,2 anos**
- Custo 10 anos = 4.074 + 80×10 + (96,80 − 87,12)×120 = **R$ 6.036**

## 5. Sensibilidade à tarifa (retorno em anos)
| Tarifa (R$/kWh) | B solar térmico | C fotovoltaico |
|---|---|---|
| 0,80 | 9,2 | 6,0 |
| 0,95 | 7,5 | 5,0 |
| 1,10 | 6,3 | 4,2 |
| 1,25 | 5,5 | 3,7 |
| 1,40 | 4,8 | 3,3 |

## 6. Impactos ambientais
A rede brasileira é majoritariamente renovável (fator ≈ 0,06 kgCO₂/kWh, estimado); portanto o CO₂ evitado é **pequeno** (24 a 63 kg/ano). Benefícios reais: menor demanda de energia, e, na alternativa A, menor consumo de água. Fabricação e descarte de placas/coletores têm impacto não contabilizado aqui.

## 7. O que NÃO está considerado
Inflação e reajustes da tarifa, juros de financiamento, troca do inversor (~10–15 anos), valor residual, bandeiras tarifárias, taxa mínima (custo de disponibilidade), sombreamento específico, e **Tarifa Social** (famílias do CadÚnico têm tarifa menor, o que alonga o retorno das alternativas B e C).
