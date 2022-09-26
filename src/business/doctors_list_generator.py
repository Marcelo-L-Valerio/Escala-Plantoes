
from entities.doctor import Doctor
from random import choices

def list_generator(number_of_doctors, days):
    doctors = []
    month_days = []
    aux = 1
    for i in range(days):
        month_days.append(aux)
        aux += 1
    for i in range(number_of_doctors):
        name = str(input(f"{i + 1} - Nome do plantonista: "))
        availability_list = []
        type_list = ['dia', 'noite']
        for dia in type_list:
            aux = int(input(f"Você prefere informar os dias que pode de {dia}: \n 1 - pode; \n 2 - nao pode; \n 3- posso todos os dias \n    "))
            if aux == 1:
                availability = eval(input("Insira os dias que pode, no seguinte formato: [1, 2, 3, etc]: "))
                availability_list.append(availability)
            elif aux == 2: 
                inavailability = eval(input("Insira os dias que NAO pode, no seguinte formato: [1, 2, 3, etc]: "))
                availability = []
                set_inavailability = set(inavailability)
                set_days = set(month_days)
                availability = list(set_days - set_inavailability)
                availability_list.append(availability)
            else:
                availability = month_days
                availability_list.append(availability)
        i = Doctor(name, availability_list[0], availability_list[1])
        doctors.append(i)
    return doctors

def random_list(number_of_doctors, days, days_avaible, nights_avaible):
    doctors = []
    name_list = ['Marcelo', 'Renan', 'Eduardo', 'Bruno', 'Barbara', 'Jonas', 'Joao', 'Andre', 'Julia', 'Ronaldo', 'Ricardo', 'Ana', 'Isa', 'Carlos', 'Paula', 'Maria', 'Roberto', 'Zoro', 'Mateus', 'Jorge', 'Marilia', 'Simone', 'Jonathan', 'Giovana', 'Bia']
    month_days = []
    aux = 1
    for i in range(days):
        month_days.append(aux)
        aux += 1
    for i in range(number_of_doctors):
        name = name_list[i]
        availability = choices(month_days, k=days_avaible)
        night_availability = choices(month_days, k=nights_avaible)
        i = Doctor(name, availability, night_availability)
        doctors.append(i)
    return doctors

def default_list():
    doctors = [Doctor('Marcelo', [1, 2, 4, 10], []), Doctor('Renan', [5, 6, 7, 8, 9], [5, 6, 7, 8, 9]), Doctor('Eduardo', [2, 3, 4, 5, 6, 7, 8, 9], 
    [2, 3, 4, 5, 6, 7, 8, 9]), Doctor('Bruno', [2, 3, 4, 5, 6, 7, 8, 9], [2, 3, 4, 5, 6, 7, 8, 9]), 
    Doctor('Barbara', [2, 6, 10], [1, 6, 10]), Doctor('Jonas', [1, 2, 3, 6, 7, 8, 9, 10], [1, 2, 3, 6, 7, 8, 9, 10]), 
    Doctor('Joao', [2], [1, 3, 5, 9]), Doctor('Andre', [4, 6, 7, 8, 9, 10], [4, 6, 7, 8, 9, 10]), 
    Doctor('Julia', [2, 3, 4, 6, 7, 10], [2, 3, 4, 6, 7, 10]), Doctor('Ronaldo', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 3, 5, 7, 9]), 
    Doctor('Ricardo', [4, 5, 6, 7, 8, 9, 10], [4, 5, 6, 7, 8, 9, 10]), Doctor('Ana', [5, 6, 7, 8, 9, 10], [5, 6, 7, 8, 9, 10]), 
    Doctor('Isa', [3, 6, 7, 8, 10], [3, 6]), Doctor('Carlos', [3, 4, 5, 6, 7, 8, 9, 10], [3, 4, 5, 6, 7, 8, 9, 10]), 
    Doctor('Paula', [2, 4, 6, 8, 10], []), Doctor('Maria', [7, 8, 9, 10], []), ]
    return doctors