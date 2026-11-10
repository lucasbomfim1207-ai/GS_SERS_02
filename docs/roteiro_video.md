# Roteiro do vídeo (máx. 3 min) — Energia no Citizen Assist AI

| Tempo | Mostrar na tela | Fala sugerida |
|---|---|---|
| 0:00–0:20 | Slide/README com nomes e título | "Somos Lucas, Julia e Eduardo, da turma 1CCPJ. Esta é a contribuição de Energias Renováveis ao Citizen Assist AI." |
| 0:20–0:45 | README (seção Público e problema) | "Nosso público são famílias de Osasco e Grande SP. O problema: a conta de luz pesa, e o chuveiro elétrico de 5.500 W é um dos maiores consumos. Muita gente não sabe quanto ele custa nem quais alternativas existem." |
| 0:45–1:25 | `docs/calculos.md` e `data/premissas.csv` | "Usamos E = P × t. Para 4 pessoas, 8 min de banho: 88 kWh/mês, cerca de R$ 97 com tarifa estimada de R$ 1,10. Comparamos três alternativas para a mesma necessidade, em 10 anos: A, banho de 5 minutos; B, aquecedor solar; C, painel fotovoltaico de 0,81 kWp. Os dados estimados estão marcados na planilha de premissas." |
| 1:25–1:50 | Tabela de comparação (README/resultados) | "A economiza R$ 36 por mês sem custo. B economiza R$ 68, retorno em 6,3 anos. C economiza R$ 87, retorno em 4,2 anos. Como a rede brasileira já é muito renovável, o CO₂ evitado é pequeno: 24 a 63 kg por ano." |
| 1:50–2:30 | Terminal: `python -m energia.assistente` → digitar `quanto gasta meu chuveiro`, `configurar` (mudar tarifa), `comparar alternativas`, `solar vale a pena?` | "No assistente, o usuário pergunta em linguagem comum. Ele pode ajustar pessoas, minutos e a tarifa da própria conta, e as respostas usam os mesmos cálculos. Na pergunta sobre solar, ele mostra o retorno para tarifas diferentes." |
| 2:30–2:50 | Resposta de `limitações` e `fontes` | "Toda resposta avisa que são estimativas. Considerar: custo inicial, telhado próprio, aprovação da distribuidora, Tarifa Social e variação de preços. Por isso, recomendamos começar pela alternativa A e pedir orçamentos." |
| 2:50–3:00 | `docs/testes_usuarios.md` | "Testamos com [N] pessoas e ajustamos [o que mudaram]. Obrigado!" |

**Dicas:** grave a tela em 1080p, fonte do terminal grande, ensaie 1x (cronometre), suba no YouTube como **Não listado** e teste o link em aba anônima.
**Importante:** no último trecho, só cite testes que vocês realmente fizeram.
