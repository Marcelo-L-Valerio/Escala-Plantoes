
from entities.doctor import Doctor
import pandas as pd

def excel_list(nome_planilha:str) -> tuple[list, int]:
    '''Dado o nome da planilha, importa os dias e noites disponíveis de cada médico, formata os dados, e cria uma
    lista de médicos a partir deles, retorna a lista de médicos, e os dias do mês que terá plantões'''

    medicos = pd.read_excel(nome_planilha, sheet_name="Medicos_diarista")
    noturnos = pd.read_excel(nome_planilha, sheet_name="Medicos_noturno")
    dados_medicos = pd.read_excel(nome_planilha, sheet_name="Dados_medicos")
    tamanho = medicos.shape

    dias = []
    lista_medicos = []
    for i in range(1, len(medicos.columns)):
        dias.append(int(medicos.columns[i]))

    for medico in range(tamanho[0]):
        nome = str(medicos['Nome'][medico])
        dias_disponivel = []
        noites_disponivel = []
        do_hospital = bool(dados_medicos['é do hospital'][medico] == 'Sim') 
        graduado_a = int(dados_medicos['graduado há'][medico])
        eh_especialista = bool(dados_medicos['é especialista'][medico] == 'Sim')
        so_diarista = bool(dados_medicos['só diarista'][medico] == 'Sim')

        for dia in dias:
            if medicos[f'{dia}'][medico] == 'D':
                dias_disponivel.append(dia)
            if noturnos[f'{dia}'][medico] == 'D':
                noites_disponivel.append(dia)
            
        lista_medicos.append(Doctor(nome, dias_disponivel, noites_disponivel, do_hospital, graduado_a, eh_especialista, so_diarista))

    return lista_medicos, dias
