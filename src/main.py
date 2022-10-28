
from business.shift_generator import multi_shift_generator
from business.import_data import import_data

def main():

    dados = import_data("escala_plantao.xlsx")
    plantoes = multi_shift_generator(dados)

if __name__=="__main__":
    main()

