# Testes do simulador. Para executar: python testes.py
import unittest

import deadlock
import memoria

BELADY = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
CLASSICA = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]


class TestMemoria(unittest.TestCase):
    def test_fifo_belady_3_frames(self):
        r = memoria.fifo(BELADY, 3)
        self.assertEqual((r["faltas"], r["hits"]), (9, 3))

    def test_fifo_belady_4_frames(self):
        r = memoria.fifo(BELADY, 4)
        self.assertEqual((r["faltas"], r["hits"]), (10, 2))

    def test_lru_belady_3_frames(self):
        r = memoria.lru(BELADY, 3)
        self.assertEqual((r["faltas"], r["hits"]), (10, 2))

    def test_lru_belady_4_frames(self):
        r = memoria.lru(BELADY, 4)
        self.assertEqual((r["faltas"], r["hits"]), (8, 4))

    def test_sequencia_classica_3_frames(self):
        self.assertEqual(memoria.fifo(CLASSICA, 3)["faltas"], 10)
        self.assertEqual(memoria.lru(CLASSICA, 3)["faltas"], 9)

    def test_hit_no_lru_muda_a_ordem(self):
        # com 2 frames: 1 2 1 3. No LRU a pagina 1 foi usada de novo,
        # entao sai a 2. No FIFO sai a 1.
        self.assertEqual(memoria.lru([1, 2, 1, 3], 2)["passos"][-1][2], [1, 3])
        self.assertEqual(memoria.fifo([1, 2, 1, 3], 2)["passos"][-1][2], [2, 3])

    def test_substituicao_registra_pagina_que_saiu(self):
        passos = memoria.fifo([1, 2, 3, 4], 3)["passos"]
        self.assertEqual(passos[3][3], 1)

    def test_um_frame(self):
        r = memoria.fifo([1, 1, 2, 2], 1)
        self.assertEqual((r["faltas"], r["hits"]), (2, 2))

    def test_belady_aparece_no_fifo(self):
        tabela = memoria.faltas_por_frames(memoria.fifo, BELADY, 4)
        self.assertIn((3, 4), memoria.achar_belady(tabela))

    def test_belady_nao_aparece_no_lru(self):
        tabela = memoria.faltas_por_frames(memoria.lru, BELADY, 6)
        self.assertEqual(memoria.achar_belady(tabela), [])

    def test_sem_belady_em_sequencia_comum(self):
        tabela = memoria.faltas_por_frames(memoria.fifo, CLASSICA, 6)
        self.assertEqual(memoria.achar_belady(tabela), [])


class TestDeadlock(unittest.TestCase):
    def rodar(self, cenario):
        processos, recursos = cenario()
        return deadlock.simular(processos, recursos, mostrar=False)

    def test_deadlock_simples(self):
        r = self.rodar(deadlock.cenario_deadlock_simples)
        self.assertTrue(r["deadlock"])
        self.assertEqual(sorted(r["ciclo"]), ["P1", "P2"])

    def test_ordem_global_evita_deadlock(self):
        r = self.rodar(deadlock.cenario_ordem_global)
        self.assertFalse(r["deadlock"])

    def test_ciclo_com_tres_processos(self):
        r = self.rodar(deadlock.cenario_tres_processos)
        self.assertTrue(r["deadlock"])
        self.assertEqual(sorted(r["ciclo"]), ["P1", "P2", "P3"])

    def test_processo_fora_do_ciclo_nao_entra_no_ciclo(self):
        r = self.rodar(deadlock.cenario_com_processo_fora_do_ciclo)
        self.assertEqual(sorted(r["ciclo"]), ["P1", "P2"])
        self.assertIn("P3", r["bloqueados"])

    def test_processo_sozinho_termina(self):
        r = deadlock.simular([deadlock.Processo("P1", ["R1", "R2"])], ["R1", "R2"], mostrar=False)
        self.assertFalse(r["deadlock"])

    def test_achar_ciclo_sem_ciclo(self):
        self.assertEqual(deadlock.achar_ciclo({"P1": "P2", "P2": None}), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
