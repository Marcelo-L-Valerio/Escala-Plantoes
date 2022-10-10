
from entities.shift import Shift
from business.import_data import import_data
from business.shift_generator import multi_shift_generator

def main():
    resultados = import_data("escala_plantao.xlsx")

    plantao = Shift(resultados[0], resultados[1], resultados[2], resultados[3], resultados[4], resultados[5])

    multi_shift_generator(plantao, resultados[6])

if __name__=="__main__":
    main()