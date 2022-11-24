
from time import time
import pandas as pd
from random import shuffle
from statistics import pstdev
from entities.shift import Shift

def create_shift_list(data: list) -> list:
    '''Funcao que, dada o numero de iteracoes, gera uma lista de n turnos, e retorna uma lista
    de turnos, e salva nos objetos dados como o turno bruto, contagem de plantoes vazios e desvio padrao.
    Para aumentar as chances de achar o melhor turno possível, para cada turno embaralha a lista de médicos
    e a lista de dias, para que cada iteração seja diferente da outra.'''

    shift_list = []

    for i in range(data[7]):

        shift = Shift(data[0], data[1], data[2], data[3], data[4], data[5], data[6])
        shuffle(shift.doctors)
        graduated_list = []

        if i%10 == 0:
            shuffle(shift.days)
        else:
            shift.days.sort()

        shift.create_shift()

        empty_shifts = []
        for day in shift.shift_data:
            empty_shifts.append(day.count('Plantonistas Insuficientes'))
        empty_shifts_count = sum(empty_shifts)

        docs_dict = {}
        for doctor in shift.doctors:
            graduated_list.append(doctor.graduated_from)
            docs_dict[doctor.name] = doctor.shift_count

        std = pstdev(docs_dict.values())
        graduated_list.sort(reverse=True)
        sorted_list = list(set(graduated_list))

        if empty_shifts_count != 0:
            std = std*(empty_shifts_count+1) ##auxiliar para alterar o valor do desvio, para que, na filtragem posterior,
            ## o mesmo considere prioritariamente turnos com o maior numero de plantoes preenchidos, mesmo que, casualmente, um turno com
            ## menos plantoes preenchidos possa possuir menor desvio padrao, posteriormente o mesmo sera retomado ao valor original

        shift.std = std
        shift.doctors_shift_count = docs_dict
        shift.empty_shifts = empty_shifts_count
        shift.graduated_list = sorted_list
        shift_list.append(shift)

    return shift_list

def best_shift(data: list) -> tuple[pd.DataFrame, pd.DataFrame]:
    '''Função que define o numero n de iterações desejadas, compara os turnos de uma dada lista
    entre si para retornar a, ou uma das melhores combinações, geradas combinadas com a aleatoriedade, priorizando
    primeiramente os turnos com menos dias sem plantonistas, e com uma melhor distribuição (menor desvio padrão),
    alem de pontuar os mesmos com fatores como quais medicos tem mais plantoes, e quais medicos sao diaristas, e
    então o imprime e retorna'''

    shift_list = create_shift_list(data)

    std_min = min(shift_list, key=lambda shift: shift.std).std
    empty_shifts_min = min(shift_list, key=lambda shift: shift.empty_shifts).empty_shifts

    shift_list = [shift for shift in shift_list if 
    (shift.empty_shifts == empty_shifts_min and shift.std == std_min)]

    for shift in shift_list:
        if shift.empty_shifts != 0:
            std_l = list(map(lambda x: x, shift.doctors_shift_count.values()))
            shift.std = pstdev(std_l) ## retomando o valor original do desvio padrão
        shift.diarist_selector()

    max_pontuation = max(shift_list, key=lambda shift: shift.pontuation).pontuation

    shift_list = [shift for shift in shift_list if shift.pontuation == max_pontuation]

    for shift in shift_list:

        shift_df, aditional_data_df = shift.print_shift(shift)

        return shift_df, aditional_data_df

def multi_shift_generator(data: list) -> list:
    '''com os dados do turno, chama a funcao best shift para encontrar a melhor combinacao de medicos, ou uma das, faz
    essa acao quantas vezes forem pedidas, e entao formata o terminal para cada opção, e também as salva num arquivo 
    excel chamado 'Turnos.xlsx' os dados dos plantoes montados, alem de cronometrar todo o processo, por ser a funcao
    que inicia e termina todo o algoritmo'''

    start_time = (time())
    shifts_list = []

    while len(shifts_list) < data[8]:
        div = '='
        print(f'\n\n {50*div} Turnos de {data[0]}, em {data[6]}, opção {len(shifts_list) + 1} {50*div}\n')
        final_shift, misc_data = best_shift(data)
        shifts_list.append([final_shift, misc_data])
        
        if len(shifts_list) == 1:
            writer = pd.ExcelWriter('Turnos.xlsx', engine='openpyxl', mode='w')
        else:
            writer = pd.ExcelWriter('Turnos.xlsx', engine='openpyxl', mode='a', if_sheet_exists='overlay')

        with writer as writer:
            final_shift.to_excel(writer, sheet_name=f'Turno {len(shifts_list)}', index=False)
            misc_data.to_excel(writer, sheet_name=f'Turno {len(shifts_list)}', index=False, startrow=(final_shift.shape[0]+2))

    end_time = (time())
    print(f'tempo de execução: {end_time - start_time}')

    return shifts_list
