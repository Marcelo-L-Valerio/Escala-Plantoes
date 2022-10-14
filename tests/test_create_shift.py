import unittest
from src.entities.doctor import Doctor
from src.entities.shift import Shift

class test_create_shift(unittest.TestCase):
    
    def setUp(self) -> None:

        self.doc1 = Doctor('Marcelo', [1, 3, 5], [5], True, 3)
        self.doc2 = Doctor('Jonas', [1], [1, 3, 5], True, 3)

        self.shift = Shift('Turno teste', [1, 3, 5], [self.doc1, self. doc2], 1, 1, 'Hospital teste')
        #Para testar esse algoritmo pseudo-aleatorio, serão testados os pontos-chave, que possuem solução
        #única para o caso criado acima

    def test_create_shift(self):

        #when
        shift_df, std_df = self.shift.best_shift(1)

        #then
        # test plantonistas dia 3 (uma solução apenas)
        self.assertEqual(shift_df["1° Plantonista"][1], 'Marcelo')
        self.assertEqual(shift_df["1° Plantonista Noturno"][1], 'Jonas')
        # test desvio padrao (erro ao acessar as keys pelo nome)
        self.assertEqual(std_df[0][1], 0)
        # test contagem de plantões totais (solução ótima - plantoes iguais)
        self.assertEqual(std_df[1][1], 3)
        self.assertEqual(std_df[2][1], 3)

    def test_doctor_not_enough(self):

        #given
        shift1 = Shift('Turno teste', [1, 2, 3, 5], [self.doc1, self. doc2], 1, 1, 'Hospital teste')

        #when
        shift_df, std_df = shift1.best_shift(1)

        #then
        self.assertEqual(shift_df["1° Plantonista"][1], 'Plantonistas Insuficientes')
        self.assertEqual(shift_df["1° Plantonista Noturno"][1], 'Plantonistas Insuficientes')

    def test_daily_shift_only(self):

        #given
        shift1 = Shift('Turno teste', [1, 3, 5], [self.doc1, self. doc2], 1, 0, 'Hospital teste')

        #when
        shift_df, std_df = shift1.best_shift(1)

        #then
        self.assertEqual(shift_df["1° Plantonista"][0], 'Jonas')
        self.assertEqual(shift_df["1° Plantonista"][1], 'Marcelo')
        self.assertEqual(std_df[0][1], 0.5)