import unittest
from energia.modelo import energia_kwh, carregar_premissas, comparar, consumo_mensal_chuveiro
from energia.assistente import Assistente


class TestModelo(unittest.TestCase):
    def test_energia(self):
        self.assertAlmostEqual(energia_kwh(5500, 60), 5.5)
        self.assertAlmostEqual(energia_kwh(1000, 30), 0.5)

    def test_negativo(self):
        with self.assertRaises(ValueError):
            energia_kwh(-1, 10)

    def test_consumo_base(self):
        p = carregar_premissas()
        self.assertAlmostEqual(consumo_mensal_chuveiro(p), 5.5 * (32 / 60) * 30, places=3)

    def test_alternativas_reduzem_consumo(self):
        r = comparar(carregar_premissas())
        self.assertTrue(all(x.kwh_mes_rede <= r[0].kwh_mes_rede for x in r[1:]))

    def test_assistente(self):
        a = Assistente()
        self.assertIn("kWh", a.responder("quanto gasta meu chuveiro"))
        self.assertIn("Comparação", a.responder("comparar alternativas"))
        self.assertIn("ESTIMATIVAS", a.responder("solar vale a pena?"))
        self.assertIn("kWh/mês", a.responder("2000 W 30 min"))


if __name__ == "__main__":
    unittest.main()
