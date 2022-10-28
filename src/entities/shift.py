
import random as rnd
import pandas as pd
from tabulate import tabulate

class Shift():

    def __init__(self, nome: str, month_days: list, doctors: list, doctors_per_day: int, doctors_per_night: int, local: str, accuracy: float = 1) -> None:
        self.nome: str = nome
        self.days: list = month_days
        self.doctors: list = doctors
        self.doctors_per_day: int = doctors_per_day
        self.doctors_per_night: int = doctors_per_night
        self.local: str = local
        self.accuracy_factor:float = accuracy
        self.pontuation: int = 0

    def availability_filter(self, day: int, shift_type: str) -> list:
        '''Metodo interno que, tendo o dia pedido, filtra na lista de médicos
        da classe apenas os que tenham o dia disponível'''

        if shift_type == "daily":
            available = list(filter(lambda doctor: day in doctor.availability, self.doctors))
            return available
        
        else:
            night_available = list(filter(lambda doctor: day in doctor.night_availability, self.doctors))
            return night_available
        


    def priorizer(self, available: list, current_day: int) -> tuple[int, list]:
        '''Metodo interno que, tendo a lista de medicos disponiveis e o dia, manipula dados
        dos medicos para definir qual/quais médicos são prioridade, de acordo com o numero de plantões
        de cada um, os dias disponiveis restantes, e o numero ideal de turnos para a lista, e salva 
        essa prioridade no atributo .priority_factor de cada medico'''

        priority_list = []
        ideal_shifts = (len(self.days)*(self.doctors_per_day+self.doctors_per_night))/len(self.doctors)

        for doctor in available:

            days_left = len(list(filter(lambda day: day >= current_day, doctor.availability)))

            if self.doctors_per_night == 0:
                nights_left = 0
            else:
                nights_left = len(list(filter(lambda day: day >= current_day, doctor.night_availability)))

            shifts_left = days_left+nights_left
            doctor._priority_factor = 1/(shifts_left/2 + doctor.shift_count)

            if doctor.shift_count >= ideal_shifts:
                doctor._priority_factor = doctor.priority_factor * 0.01

            priority_list.append(doctor.priority_factor)
        
        if len(priority_list) > 0:
            priority_factor = max(priority_list)
                    
        else:
            priority_factor = 0

        return priority_factor, priority_list

    def selector(self, day: int, shift_type: str) -> list:
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
                        doctor.is_valid(priority_factor, selected, self.accuracy_factor)):
                        
                        selected.append(doctor)
                        doctor.add_day()
                        doctor.history_add(day) 
                        doctor.increment()

                if len(selected) == doctors_qtd:
                    return selected

                else:
                    priority_list = list(filter(lambda x: x !=  priority_factor, priority_list))

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

    def create_shift(self) -> list:
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
                if shift_types[1] == []:
                    doctor.zero_consec()
        return shift

    def print_shift(self, shift: list) -> pd.DataFrame:
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
