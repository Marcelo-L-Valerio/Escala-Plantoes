from entities.shift import Shift
import statistics as stt
import pandas as pd
from tabulate import tabulate


def create_shift_list(number_of_iteractions: int, shift) -> tuple[list, int, float, float]:
    '''Metodo interno da classe, que, dada o numero de iterações, gera uma lista de n turnos, e retorna uma lista
    de turnos, no formato de dicionarios, com dados como o turno bruto, contagem de plantoes vazios e outros.'''

    shift_list = []

    for i in range(number_of_iteractions):
        shift_count_list = []
        graduated_list = []
        shift_desc = shift.create_shift()

        empty_shifts = []
        for day in shift_desc:
            empty_shifts.append(day.count('Plantonistas Insuficientes'))
        empty_shifts_count = sum(empty_shifts)

        docs_dict = {}
        for doctor in shift.doctors:

            shift_count_list.append(doctor.shift_count)
            graduated_list.append(doctor.graduated_from)
            docs_dict[doctor.name] = doctor.shift_count
        std = stt.pstdev(shift_count_list)

        pontuation = shift_pontuator(graduated_list, shift)
        if empty_shifts_count != 0:
            pontuation = pontuation/(empty_shifts_count+1)
            std = std*(empty_shifts_count+1) ##auxiliar para alterar o valor do desvio, para que, na filtragem posterior,
            ## o mesmo considere prioritariamente turnos com o maior numero de plantoes preenchidos, mesmo que, casualmente, um turno com
            ## menos plantoes preenchidos possa possuir menor desvio padrao, posteriormente o mesmo sera retomado ao valor original

        shift_dict = {
            'obj': shift,
            'shift': shift_desc,
            'std': std,
            'shift_count': docs_dict,
            'empty_shifts': empty_shifts_count,
            'pontuation': pontuation
        }
        shift_list.append(shift_dict)

    return shift_list

def shift_pontuator(graduated_list: list, shift) -> int:
    '''Metodo interno, que calcula a pontuacao do turno, com base no numero de turno dos medicos mais prestigiados, como os com
    mais tempo de formado, o fato de o medico ser ou nao do hospital, e dele ser ou nao especialista, por exemplo'''

    graduated_list.sort()
    sorted_list = list(set(graduated_list))
    pontuation = 0

    for doctor in shift.doctors:
        
        pontuation = doctor.pontuation(sorted_list, pontuation)

    return pontuation

def best_shift(number_of_iteractions: int, shift) -> tuple[pd.DataFrame, pd.DataFrame]:
    '''Metodo externo da classe, que define o numero n de iterações desejadas, compara os turnos de uma dada lista
    entre si para retornar a, ou uma das melhores combinações, geradas combinadas com a aleatoriedade, priorizando
    primeiramente os turnos com menos dias sem plantonistas, e depois os turnos com uma melhor distribuição 
    (menor desvio padrão) de turnos entre os médicos, e então o imprime e retorna'''

    shift_list = create_shift_list(number_of_iteractions, shift)

    std_min = min(shift_list, key=lambda x:x['std'])['std']
    empty_shifts_min = min(shift_list, key=lambda x:x['empty_shifts'])['empty_shifts']
    for shift in range(len(shift_list)-1, -1, -1):

        if shift_list[shift]['empty_shifts'] != empty_shifts_min:
            shift_list.pop(shift)
        elif shift_list[shift]['std'] != std_min:
            shift_list.pop(shift)
    print(len(shift_list))
    max_pontuation = max(shift_list, key=lambda x:x['pontuation'])['pontuation']
    for shift in range(len(shift_list)-1, -1, -1):
        
        if shift_list[shift]['pontuation'] != max_pontuation:
            shift_list.pop(shift)

    for shift in shift_list:

        if shift['empty_shifts'] != 0:
            std_l = list(map(lambda x: x, shift['shift_count'].values()))
            shift['std'] = stt.pstdev(std_l) ##retomando o valor original do desvio padrão

        name_list = ['Desvio Padrao', 'Pontuação']
        count_list = [round(shift['std'], 6), round(shift['pontuation'], 2)]
        shift_df = shift['obj'].print_shift(shift['shift'])

        for doctor in shift['shift_count'].keys():
            name_list.append(doctor)
            count_list.append(shift['shift_count'][doctor])

        final_list = [name_list, count_list]
        aditional_data_df = pd.DataFrame(final_list)
        print(tabulate(aditional_data_df, tablefmt='fancy_grid', showindex=False))

        return shift_df, aditional_data_df