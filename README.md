# Citizen Assist AI — Contribuição de Energias Renováveis e Sustentáveis (Global Solution 2026)

> **Disciplina:** Soluções em Energias Renováveis e Sustentáveis · **Turma:** 1CCPJ
> Se este repositório for compartilhado com outras disciplinas, a contribuição desta disciplina está nas pastas `energia/`, `data/`, `docs/`, `tests/` e `resultados/`.

## Vídeo técnico (YouTube, não listado)


## Integrantes
| Nome | RM |
|---|---|
| Lucas Bomfim Leite | 570420 |
| Julia Johanson | 572220 |
| Eduardo Barcelos | 573274 |

## Público e problema
**Público:** famílias de baixa e média renda de Osasco/Grande São Paulo, em casas ou apartamentos com chuveiro elétrico (perfil-exemplo: 4 pessoas).
**Necessidade energética:** reduzir a conta de luz. O chuveiro elétrico (≈ 5.500 W) costuma ser um dos maiores consumos domésticos, e muitas pessoas não sabem quanto ele custa nem quais alternativas existem.
**Como ajudamos:** o assistente responde, em linguagem simples, quanto gasta o chuveiro (ou outro aparelho), compara alternativas para a *mesma necessidade* (banho quente) e informa condições e limites.

## Funcionalidades de energia
1. **Consumo do chuveiro/aparelho** — `E = P × t`, custo mensal com a tarifa do usuário.
2. **Configuração personalizada** — pessoas, minutos de banho, potência e tarifa (`configurar`).
3. **Comparação de alternativas** (horizonte de 10 anos):
   - **A)** Uso consciente (banho de 8 → 5 min) — sem custo.
   - **B)** Aquecedor solar de água com apoio elétrico — **fonte renovável (térmica)**.
   - **C)** Energia solar fotovoltaica dimensionada para o chuveiro — **fonte renovável (elétrica)**.
4. **"Solar vale a pena?"** — payback e sensibilidade à tarifa.
5. **Pergunta inicial sobre moradia** (própria ou alugada): se alugada, o assistente avisa que solar depende de autorização do proprietário e prioriza a alternativa A.
6. **Dicas, fontes e limitações** em toda resposta.

## Como executar
```bash
python -m energia.assistente      # assistente interativo (terminal)
python -m energia.relatorio       # gera resultados/comparacao.csv e sensibilidade_tarifa.csv
python -m unittest discover -s tests -t .   # testes automatizados
```
Exemplos de perguntas: `quanto gasta meu chuveiro`, `configurar`, `comparar alternativas`, `solar vale a pena?`, `aparelho: 2000 W por 30 min`, `fontes`, `limitações`.

## Estrutura
```
energia/        código (modelo.py = cálculos, assistente.py = respostas, relatorio.py)
data/           premissas.csv (valor, unidade, tipo oficial/estimado, origem)
docs/           calculos.md · justificativas.md · referencias.md · testes_usuarios.md
resultados/     comparacao.csv · sensibilidade_tarifa.csv
tests/          testes automatizados
```

## Resultado resumido (premissas-padrão — ver `docs/calculos.md`)
| Alternativa | kWh/mês (rede) | Economia/mês | Investimento | Retorno | Custo total 10 anos |
|---|---|---|---|---|---|
| Base (chuveiro) | 88 | — | — | — | R$ 11.616 |
| A) Uso consciente | 55 | R$ 36,30 | R$ 0 | imediato | R$ 7.260 |
| B) Aquecedor solar | 26 | R$ 67,76 | R$ 4.500 | 6,3 anos | R$ 8.985 |
| C) Fotovoltaico (0,81 kWp) | 0 | R$ 87,12 | R$ 4.074 | 4,2 anos | R$ 6.036 |

**Todos os valores são estimativas, não garantias.** Dados estimados estão marcados como tal em `data/premissas.csv`.

## Testes
- **Testes automatizados:** `python -m unittest discover -s tests -t .`
- **Testes com usuários:** registrados em `docs/testes_usuarios.md`.
