
import pandas as pd
from business.shift_selector import best_shift

def multi_shift_generator(shift, shift_quantity: int) -> list:
    '''Dados o turno e a quantidade de opções de turno desejada, printa no terminal, e também salva num 
    arquivo excel chamado 'Turnos.xlsx' os dados do plantão montado'''

    lista_turnos = []
    while len(lista_turnos) < shift_quantity:
        div = '='
        print(f'\n\n {50*div} Turnos de {shift.nome}, em {shift.local}, opção {len(lista_turnos) + 1} {50*div}\n')
        turno, outros_dados = best_shift(1000, shift)
        lista_turnos.append(turno)
        if len(lista_turnos) == 1:
            engine = 'xlsxwriter'
            mode = 'w'
        else:
            engine = 'openpyxl'
            mode = 'a'
        aux_df = pd.DataFrame(['Distribuição de turnos:'])

        df_final = pd.concat([turno, aux_df, outros_dados], axis=1)

        with pd.ExcelWriter('Turnos.xlsx', engine=engine, mode=mode) as writer:
            df_final.to_excel(writer, sheet_name=f'Turno {len(lista_turnos)}', index=False)

    return lista_turnos