
import pandas as pd
from business.doctors_list_generator import excel_list


def import_data(nome_da_planilha: str) -> list:
    '''Dado o nome da planilha, importa todos os dados sobre o turno e os médicos, e retorna no formato de uma
    lista de resultados'''
    dados = pd.read_excel(nome_da_planilha, sheet_name="Dados_gerais")

    lista_medicos, dias = excel_list(nome_da_planilha)

    nome = str(dados['Mês'][0])
    diaristas = int(dados['Diaristas'][0])
    plantonistas_dia = int(dados['Plantonistas dia'][0])
    plantonistas_noite = int(dados['Plantonistas noite'][0])
    n_opcoes = int(dados['N de opções'][0])
    local = str(dados['Local'][0])
    n_iteracoes = int(dados['N de iterações'][0])

    results = [nome, dias, lista_medicos, diaristas, plantonistas_dia, plantonistas_noite, local, n_iteracoes, n_opcoes]

    return results
