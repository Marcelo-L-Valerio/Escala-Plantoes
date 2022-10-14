
from entities.shift import Shift
from business.import_data import import_data
from business.shift_generator import multi_shift_generator

def main():
    resultados = import_data("escala_plantao.xlsx")

    plantao = Shift(resultados[0], resultados[1], resultados[2], resultados[3], resultados[4], resultados[5], resultados[6])

    multi_shift_generator(plantao, resultados[7])

if __name__=="__main__":
    main()

# # test input

# from business.doctors_list_generator import random_list
# dias = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# lista_medicos = random_list(10, dias, 7, 7)
# n_opcoes = 5
# plantao = Shift('fds_outubro', dias, lista_medicos, 4, 1, 'hospital teste')
# multi_shift_generator(plantao, n_opcoes)