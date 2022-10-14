
import random as rnd
import statistics as stt
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
            doctor._priority_factor = 1/(shifts_left/2 + doctor.shift_count)

            if doctor.shift_count >= ideal_shifts:
                doctor._priority_factor = doctor.priority_factor * 0.01

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
                        doctor.is_valid(priority_factor, selected, self.accuracy_factor)):
                        
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

    def create_shift_list(self, number_of_iteractions):
        '''Metodo interno da classe, que, dada o numero de iterações, gera uma lista de n turnos, e retorna uma lista
        de turnos, no formato de dicionarios, com dados como o turno bruto, contagem de plantoes vazios e outros, retorna
        a distribuicao minima do conjunto (menor desvio padrao), e os turnos com maior numero de plantoes preenchidos.'''

        shift_list = []
        std_list = []
        empty_shifts_list = []
        graduated_list = []
        pontuation_list = []

        for i in range(number_of_iteractions):
            shift_count_list = []
            shift = self.create_shift()

            empty_shifts = []
            for day in shift:
                empty_shifts.append(day.count('Plantonistas Insuficientes'))

            docs_dict = {}
            for doctor in self.doctors:

                shift_count_list.append(doctor.shift_count)
                graduated_list.append(doctor.graduated_from)
                docs_dict[doctor.name] = doctor.shift_count

            pontuation = self.shift_pontuator(graduated_list, docs_dict)
            if sum(empty_shifts) != 0:
                pontuation = pontuation/sum(empty_shifts)

            pontuation_list.append(pontuation)

            shift_dict = {
                'shift': shift,
                'std': stt.pstdev(shift_count_list),
                'shift_count': docs_dict,
                'empty_shifts': sum(empty_shifts),
                'pontuation': pontuation
            }
            shift_list.append(shift_dict)
            empty_shifts_list.append(shift_dict['empty_shifts'])
            std_list.append(shift_dict['std'])

        empty_shifts_min = min(empty_shifts_list)
        std_min = min(std_list)
        max_pontuation = max(pontuation_list)
        
        return (shift_list, empty_shifts_min, std_min, max_pontuation)

    def shift_pontuator(self, graduated_list, docs_dict):
        '''Metodo interno, que calcula a pontuacao do turno, com base no numero de turno dos medicos mais prestigiados, como os com
        mais tempo de formado, o fato de o medico ser ou nao do hospital, e dele ser ou nao especialista, por exemplo'''

        graduated_list.sort()
        sorted_list = list(set(graduated_list))
        pontuation = 0

        for doctor in self.doctors:
            if doctor.is_from_hospital == True:
                pontuation += 100 * docs_dict[doctor.name]

            for i in range(len(sorted_list)):

                if doctor.graduated_from == sorted_list[-1 -(1 * i)]:
                    pontuation += 150/(i+1) * (len(sorted_list) - i) * docs_dict[doctor.name]

        return pontuation

    def best_shift(self, number_of_iteractions):
        '''Metodo externo da classe, que define o numero n de iterações desejadas, compara os turnos de uma dada lista
        entre si para retornar a, ou uma das melhores combinações, geradas combinadas com a aleatoriedade, priorizando
        primeiramente os turnos com menos dias sem plantonistas, e depois os turnos com uma melhor distribuição 
        (menor desvio padrão) de turnos entre os médicos, e então o imprime e retorna'''

        shift_list, empty_shifts_min, std_min, max_pontuation = self.create_shift_list(number_of_iteractions)

        for shift in range(len(shift_list)-1, -1, -1):

            if shift_list[shift]['empty_shifts'] != empty_shifts_min:
                shift_list.pop(shift)
            elif shift_list[shift]['std'] != std_min:
                shift_list.pop(shift)
            elif shift_list[shift]['pontuation'] != max_pontuation:
                shift_list.pop(shift)

        for shift in shift_list:

            name_list = ['Desvio Padrao', 'Pontuação']
            count_list = [shift['std'], shift['pontuation']]
            shift_df = self.print_shift(shift['shift'])

            for doctor in shift['shift_count'].keys():
                name_list.append(doctor)
                count_list.append(shift['shift_count'][doctor])

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