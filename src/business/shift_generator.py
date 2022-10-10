
import pandas as pd


def multi_shift_generator(shift, shift_quantity):
    '''Dados o turno e a quantidade de opções de turno desejada, printa no terminal, e também salva num 
    arquivo excel chamado 'Turnos.xlsx' os dados do plantão montado'''

    lista_turnos = []
    while len(lista_turnos) < shift_quantity:
        div = '='
        print(f'\n\n {50*div} Turnos de {shift.nome}, em {shift.local}, opção {len(lista_turnos) + 1} {50*div}\n')
        turno, desvio = shift.best_shift(1000)
        lista_turnos.append(turno)
        if len(lista_turnos) == 1:
            engine = 'xlsxwriter'
            mode = 'w'
        else:
            engine = 'openpyxl'
            mode = 'a'
        aux_df = pd.DataFrame(['Distribuição de turnos:'])

        df_final = pd.concat([turno, aux_df, desvio], axis=1)

        with pd.ExcelWriter('Turnos.xlsx', engine=engine, mode=mode) as writer:
            df_final.to_excel(writer, sheet_name=f'Turno {len(lista_turnos)}', index=False)
