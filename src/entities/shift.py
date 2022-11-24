
from random import shuffle
import pandas as pd
from tabulate import tabulate

class Shift():

    def __init__(self, name: str, month_days: list, doctors: list, diarists: int, plantonists: int, doctors_per_night: int, local: str) -> None:
        self.name: str = name
        self.days: list = month_days
        self.doctors: list = doctors
        self.plantonists: int = plantonists
        self.diarists: int = diarists
        self.doctors_per_day: int = plantonists + diarists
        self.doctors_per_night: int = doctors_per_night
        self.local: str = local
        
        self.pontuation: int = 0
        self.shift_data:list = []
        self.std:float = 0
        self.doctors_shift_count: dict = {}
        self.empty_shifts: int = 0
        self.pontuation: float = 0
        self.graduated_list: list = []

    def __str__(self) -> str:
        return self.name

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
            doctor._priority_factor = 1/(shifts_left/5 + doctor.shift_count)
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
            shuffle(available)

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
                    priority_list = list(filter(lambda x: x !=  priority_factor, priority_list))

                    if len(priority_list) != 0:
                        priority_factor = max(priority_list)
                    else:
                        continue
            
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
            aux = 0
            for i in shift:
                try:
                    i.index(day-1)
                    aux = 1
                    break
                except:
                    aux = 0
            if aux == 0:
                for doctor in self.doctors:
                    doctor.zero_consec()

            shift_selected = self.selector(day, "daily")
            if self.doctors_per_night >= 0:
                night_shift_selected = self.selector(day, "night")
            else: night_shift_selected = []
            shift_types = [shift_selected, night_shift_selected]

            day_shift = [day]

            for i in shift_types:
                for doctor in i:
                    day_shift.append(doctor)

            shift.append(day_shift)
            for doctor in self.doctors:

                if shift_types[1] != [] and doctor not in shift_types[1]:
                    doctor.zero_consec()
                if shift_types[1] == []:
                    doctor.zero_consec()
        self.shift_data = shift

        return None

    def shift_pontuator(self, shift: list = []) -> int:
        '''Metodo interno, que calcula a pontuacao do turno, com base no numero de turno dos medicos mais prestigiados, como os com
        mais tempo de formado, o fato de o medico ser ou nao do hospital, e dele ser ou nao especialista, por exemplo'''

        pontuation = 0

        for doctor in self.doctors:
            
            pontuation += doctor.pontuation(self.graduated_list)

        for day in shift:
            for doctor in range(1, self.diarists+1):
                if type(day[doctor]) != str and day[doctor].only_diarist == True:
                    pontuation += 300
                else:
                    pontuation -= 150
            for doctor in range(self.diarists+1, self.doctors_per_day+1):
                if type(day[doctor]) != str and day[doctor].only_diarist == False:
                    pontuation += 150
                else:
                    pontuation -= 300
        self.pontuation = pontuation   

        return None
    
    def diarist_selector(self):
        '''Método responsável por remanejar a ordem dos médicos que atuarao durante o dia, para que priorize os mais
        qualificados como diaristas, uma posição de maior prestigio, e coloque os menos qualificados como plantonistas
        normais'''

        for day in self.shift_data: #reorganiza a posição dos plantonistas para que os diaristas sejam mais qualificados
            doctor_list = day[1:self.doctors_per_day+1]

            for doctor in doctor_list:
                try:
                    doctor_list[doctor_list.index(doctor)] = {'doctor': doctor,
                    'priority': doctor.diarist_priority(self.graduated_list)}
                except:
                    doctor_list[doctor_list.index(doctor)] = {'doctor': doctor,
                    'priority': 0}
            doctor_list.sort(key=lambda doctor: doctor['priority'], reverse=True)

            for pos in range(1, len(day)):
                try:
                    day[pos] = doctor_list[pos-1]['doctor']
                except:
                    day[pos] = day[pos]

        self.shift_pontuator(shift=self.shift_data)

        for day in self.shift_data:
            for doctor in range(1, len(day)):
                try:
                    day[doctor] = day[doctor].name
                except:
                    continue

        return None

    def print_shift(self, shift: dict) -> pd.DataFrame:
        '''Metodo interno utilizado para printar um turno de maneira organizada no terminal, cria um
        Pandas DataFrame com o resultado e o retorna, além de printar os dados estatísticos mais importantes e salvar
        esses dados em outro dataframe'''

        self.days.sort()
        shift_data = {'Dia': self.days}
        shift_types_name = ['Diarista', 'Plantonista', 'Plantonista Noturno']
        shift_types_doctors = [self.diarists, self.plantonists, self.doctors_per_night]
        position_in_shift = [0, self.diarists, self.doctors_per_day] #posição do médico na lista "shift"
        
        for index, plantonist_type in enumerate(shift_types_doctors):
            for doctor in range(plantonist_type):
                doctor_list = []
                for day in range(len(self.days)):
                    try:
                        doctor_list.append(self.shift_data[day][doctor + 1 + position_in_shift[index]])
                    except:
                        doctor_list.append('Plantonistas Insuficientes')

                shift_data[f'{doctor+1}° {shift_types_name[index]}'] = doctor_list

        df = pd.DataFrame(shift_data)
        print(tabulate(df,  headers='keys', tablefmt='fancy_grid', showindex=False))

        self.shift_data.sort(key=lambda day: day[0]) ## reorganizando os dias embaralhados
        name_list = ['Desvio Padrao', 'Pontuação']
        count_list = [round(self.std, 6), self.pontuation]
    
        self.doctors.sort(key=lambda doctor: doctor.name)

        for doctor in self.doctors:
            name_list.append(doctor.name)
            count_list.append(self.doctors_shift_count[doctor.name])

        aditional_data_df = pd.DataFrame(count_list, index=name_list).T
        print(tabulate(aditional_data_df, headers='keys', tablefmt='fancy_grid', showindex=False))

        return df, aditional_data_df
