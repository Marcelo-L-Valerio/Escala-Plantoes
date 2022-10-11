
import random as rnd
import statistics as stt
import pandas as pd
from tabulate import tabulate

class Shift():

    def __init__(self, nome: str, month_days: list, doctors: list, doctors_per_day: int, doctors_per_night: int, local: str) -> None:
        self.nome: str = nome
        self.days: list = month_days
        self.doctors: list = doctors
        self.doctors_per_day: int = doctors_per_day
        self.doctors_per_night: int = doctors_per_night
        self.local: str = local

    def availability_filter(self, day, shift_type):
        '''Metodo interno que, tendo o dia pedido, filtra na lista de médicos
        da classe apenas os que tenham o dia disponível'''

        available = [doctor for doctor in self.doctors if day in doctor.availability]

        night_available = [doctor for doctor in self.doctors if day in doctor.night_availability]

        if shift_type == "daily":
            return available
        else:
            return night_available

    def priorizer(self, available, current_day):
        '''Metodo interno que, tendo a lista de medicos disponiveis e o dia, manipula dados
        dos medicos para definir qual/quais médicos são prioridade, de acordo com o numero de plantões
        de cada um, os dias disponiveis restantes, e o numero ideal de turnos para a lista, e salva 
        essa prioridade no atributo .priority_factor de cada medico'''

        priority_list = []
        ideal_shifts = (len(self.days)*(self.doctors_per_day+self.doctors_per_night))/len(self.doctors)

        for doctor in available:
            days_left = len([day for day in doctor.availability if day >= current_day])
            if self.doctors_per_night == 0:
                nights_left = 0
            else:
                nights_left = len([day for day in doctor.night_availability if day >= current_day])
            shifts_left = days_left+nights_left
            doctor._priority_factor = 1/(shifts_left + doctor.shift_count)

            if doctor.shift_count >= ideal_shifts:
                doctor._priority_factor = doctor.priority_factor * 0.0001

            priority_list.append(doctor.priority_factor)
        
        if len(priority_list) > 0:
            priority_factor = max(priority_list)
                    
        else:
            priority_factor = 0

        return([priority_factor, priority_list])

    def selector(self, day, shift_type):
        '''Metodo interno que, tendo a disponibilidade, numero de turnos do dia, fator de prioridade da
        rodada, e a lista com os fatores de prioridade dos medicos disponiveis, embaralha a lista de
        disponibilidade para garantir resultados diferentes a cada iteração, e seleciona os medicos
        que tenham prioridade igual ao maximo da lista'''

        available = self.availability_filter(day, shift_type)

        if shift_type == "daily":
            doctors_qtd = self.doctors_per_day
        else:
            doctors_qtd = self.doctors_per_night
        priority_factor, priority_list = self.priorizer(available, day)

        selected = []
        if available != [] and doctors_qtd != 0:
            rnd.shuffle(available)

            while len(selected) != doctors_qtd:

                for doctor in available:
                    if doctors_qtd != len(selected) and (
                        doctor.is_valid(priority_factor, selected)):
                        
                        selected.append(doctor)
                        doctor.add_day()
                        doctor.history_add(day) 
                        doctor.increment()

                if len(selected) == doctors_qtd:
                    return selected

                else:
                    priority_list = list(
                        filter(lambda x: x !=  priority_factor, priority_list)
                        )

                    if len(priority_list) != 0:
                        priority_factor = max(priority_list)
                    else:
                        selected.append('Plantonistas Insuficientes')

                        if len(selected) == doctors_qtd:
                            return selected
        else:
            
            while len(selected) != doctors_qtd:

                selected.append('Plantonistas Insuficientes')
            return selected

    def create_shift(self):
        '''Metodo interno que liga os outros metodos da classe, para calcular um plantao aleatorio que atenda
        aos requisitos de disponibilidade e priorização dos medicos, fazendo cada dia como se fosse uma rodada
        de um loop'''

        for doctor in self.doctors:
            doctor.setup()

        shift = []

        for day in self.days:
            if self.days[self.days.index(day)-1] != day-1:
                for doctor in self.doctors:
                    doctor.zero_consec()

            shift_selected = self.selector(day, "daily")
            if self.doctors_per_night >= 0:
                night_shift_selected = self.selector(day, "night")
            shift_types = [shift_selected, night_shift_selected]

            day_shift = [day]

            for i in shift_types:
                for doctor in i:
                    if hasattr(doctor, 'name'):
                        aux = doctor.name
                    else:
                        aux = doctor
                    day_shift.append(aux)

            shift.append(day_shift)
            for doctor in self.doctors:

                if shift_types[1] != [] and doctor not in shift_types[1]:
                    doctor.zero_consec()
                else:
                    doctor.zero_consec()
        return shift

    def best_shift(self, number_of_iteractions):
        '''Metodo externo da classe, que define o numero n de iterações desejadas, gera n turnos, e depois compara
        esses turnos entre si para retornar a, ou uma das melhores combinações, geradas combinadas com a 
        aleatoriedade, priorizando primeiramente os turnos com menos dias sem plantonistas, e depois os turnos
        com uma melhor distribuição (menor desvio padrão) de turnos entre os médicos, e então o imprime e retorna'''

        shift_list = []
        std_list = []
        empty_shifts_list = []

        for i in range(number_of_iteractions):
            shift_count_list = []
            shift = self.create_shift()

            for doctor in self.doctors:
                shift_count_list.append(doctor.shift_count)

            empty_shifts = []
            for day in shift:
                empty_shifts.append(day.count('Plantonistas Insuficientes'))

            empty_shifts_list.append(sum(empty_shifts))
            shift_list.append(shift)
            std_list.append(stt.pstdev(shift_count_list))
        empty_shifts_min = min(empty_shifts_list)
        useless_shifts = []

        for i in range(number_of_iteractions):

            if empty_shifts_list[i] != empty_shifts_min:
                useless_shifts.append(i)
        useless_shifts.reverse()

        for i in useless_shifts:
            shift_list.pop(i)
            std_list.pop(i)

        std_min = min(std_list)
        
        for i in range(len(shift_list)):

            if std_list[i] == std_min:

                name_list = ['Desvio Padrao']
                count_list = [std_list[i]]
                shift_df = self.print_shift(shift_list[i])

                for doctor in self.doctors:
                    name_list.append(doctor.name)
                    aux = []
                    for day in range(len(self.days)):
                        aux.append(shift_list[i][day].count(doctor.name))
                    count_list.append(sum(aux))

                final_list = [name_list, count_list]
                std_df = pd.DataFrame(final_list)
                print(tabulate(std_df, tablefmt='fancy_grid', showindex=False))

                return shift_df, std_df

    def print_shift(self, shift):
        '''Metodo interno utilizado para printar um turno de maneira organizada no terminal, cria um
        Pandas DataFrrame com o resultado e o retorna'''

        shift_data = {'Dia': self.days}
        
        for doctor in range(self.doctors_per_day):
            doctor_list = []
            for day in range(len(self.days)):
                try:
                    doctor_list.append(shift[day][doctor + 1])
                except:
                    doctor_list.append('Plantonistas Insuficientes')
            shift_data[f'{doctor+1}° Plantonista'] = doctor_list

        for doctor in range(self.doctors_per_night):
            doctor_list = []
            for day in range(len(self.days)):
                try:
                    doctor_list.append(shift[day][doctor + 1 + self.doctors_per_day])
                except:
                    doctor_list.append('Plantonistas Insuficientes')
            shift_data[f'{doctor+1}° Plantonista Noturno'] = doctor_list

        df = pd.DataFrame(shift_data)
        print(tabulate(df,  headers='keys', tablefmt='fancy_grid', showindex=False))

        return df