
from entities.doctor import Doctor
from random import choices
import pandas as pd

def random_list(number_of_doctors, days, days_avaible, nights_avaible):
    '''Gera uma lista aleatoria de médicos, tendo como parâmetros a quantidade de médicos desejada, a lista
    de dias, quantos dias cada médico terá disponivel, e quantas noites disponíveis (dias selecionados
    aleatoriamente da lista de dias fornecida, diferente para cada médico)'''

    doctors = []
    name_list = ['Marcelo', 'Renan', 'Eduardo', 'Bruno', 'Barbara', 'Jonas', 'Joao', 'Andre', 'Julia', 'Ronaldo', 'Ricardo', 'Ana', 'Isa', 'Carlos', 'Paula', 'Maria', 'Roberto', 'Zoro', 'Mateus', 'Jorge', 'Marilia', 'Simone', 'Jonathan', 'Giovana', 'Bia']

    for i in range(number_of_doctors):
        name = name_list[i]
        availability = choices(days, k=days_avaible)
        night_availability = choices(days, k=nights_avaible)
        i = Doctor(name, availability, night_availability)
        doctors.append(i)

    return doctors

def excel_list(nome_planilha:str):
    '''Dado o nome da planilha, importa os dias e noites disponíveis de cada médico, formata os dados, e cria uma
    lista de médicos a partir deles, retorna a lista de médicos, e os dias do mês que terá plantões'''

    medicos = pd.read_excel(nome_planilha, sheet_name="Medicos_diarista")
    noturnos = pd.read_excel(nome_planilha, sheet_name="Medicos_noturno")
    tamanho = medicos.shape

    dias = []
    lista_medicos = []
    for i in range(1, len(medicos.columns) - 2):
        dias.append(int(medicos.columns[i]))

    for medico in range(tamanho[0]):
        nome = str(medicos['Nome'][medico])
        dias_disponivel = []
        noites_disponivel = []
        do_hospital = bool(medicos['é do hospital'][medico] == 'Sim') 
        graduado_a = int(medicos['graduado há'][medico])

        for dia in dias:
            if medicos[f'{dia}'][medico] == 'D':
                dias_disponivel.append(dia)
            if noturnos[f'{dia}'][medico] == 'D':
                noites_disponivel.append(dia)
            
        lista_medicos.append(Doctor(nome, dias_disponivel, noites_disponivel, do_hospital, graduado_a))

    return lista_medicos, dias
