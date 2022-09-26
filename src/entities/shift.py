
import random as rnd
import statistics as stt

class Shift():

    def __init__(self, month: str, month_days: int, doctors: list, doctors_per_day: int, doctors_per_night) -> None:
        self.month: str = month
        self.days: int = month_days
        self.doctors: list = doctors
        self.doctors_per_day: int = doctors_per_day
        self.doctors_per_night: int = doctors_per_night

    def filtro(self, day):

        available = [doctor for doctor in self.doctors if day in doctor.availability]

        night_avaible = [doctor for doctor in self.doctors if day in doctor.night_availability]

        return available, night_avaible

    def priorizador(self, available, current_day):

        priority_list = []
        ideal_shifts = (self.days*(self.doctors_per_day+self.doctors_per_night))/len(self.doctors)
        for doctor in range(len(available)):
            days_left = len([day for day in available[doctor].availability if day >= current_day])

            available[doctor]._priority_factor = ideal_shifts/(days_left**2 * available[doctor].shift_count**3+1)

            if available[doctor].shift_count >= ideal_shifts:
                available[doctor]._priority_factor = available[doctor].priority_factor * 0.001
            priority_list.append(available[doctor].priority_factor)
        
        if len(priority_list) > 0:
            priority_factor = max(priority_list)
        else:
            priority_factor = 0

        return([priority_factor, priority_list])

    def seletor(self, available, doctors_per_day, priority_factor, priority_list):

        doctors_per_day = doctors_per_day
        selected = []

        if available != []:
            rnd.shuffle(available)

            while len(selected) != doctors_per_day:

                for doctor in range(len(available)):
                    if doctors_per_day != len(selected) and available[doctor] not in selected:
                            if priority_factor == available[doctor].priority_factor and available[doctor].consecutive_shifts != 2:
                                selected.append(available[doctor])
                                available[doctor].add_day()

                if len(selected) == doctors_per_day:

                    return selected

                else:
                    priority_list = list(filter(lambda x: x !=  priority_factor, priority_list))

                    if len(priority_list) != 0:
                        priority_factor = max(priority_list)
                    else:
                        selected.append('Faltam plantonistas para essa data')

                    if len(selected) == doctors_per_day:
                        return selected
        else:

            return ['Faltam plantonistas para essa data']

    def create_shift(self):

        for doctor in self.doctors:
            doctor.setup()

        shift = []
        for day in range(1, self.days + 1):

            available, night_avaible = self.filtro(day)

            priority, priority_list = self.priorizador(available, day)
            night_priority, night_priority_list = self.priorizador(night_avaible, day)

            selected = self.seletor(available, self.doctors_per_day, priority,priority_list)
            night_selected = self.seletor(night_avaible, self.doctors_per_night, night_priority, night_priority_list)

            shift.append(day)
            shift_types = [selected, night_selected]

            for i in shift_types:
                for doctor in i:
                    if hasattr(doctor, 'name'):
                        aux = doctor.name
                        doctor.history_add(day) 
                        doctor.increment()
                    else:
                        aux = doctor
                    shift.append(aux)

            for doctor in self.doctors:
                if doctor not in selected:
                    if doctor not in night_selected:
                        doctor.zero_consec()

        return shift
    
    def best_shift(self, number_of_interactions):

        shift_list = []
        std_list = []

        for i in range(number_of_interactions):
            shift_count_list = []
            shift = self.create_shift()

            for doctor in self.doctors:
                shift_count_list.append(doctor.shift_count)

            shift_list.append(shift)
            std_list.append(stt.pstdev(shift_count_list))

        std_min = min(std_list)
        aux = []
        aux_std = []

        for i in range(len(shift_list)):

            if 'Faltam plantonistas para essa data' not in shift_list[i]:
                aux.append(shift_list[i])
                aux_std.append(std_list[i])

                for j in range(len(aux)):
                    if aux_std[j] == std_min:
                        self.imprimir(aux[j])
                        print(f'\n Desvio Padrão: {aux_std[j]}')
                        final_list = []
                        
                        for doctor in self.doctors:
                            final_list.append(f'{doctor.name}: {aux[j].count(doctor.name)}')
                        print(f'\n Contagem de turnos: {final_list}')
                        return None

            else:
                if std_list[i] == std_min:
                    self.imprimir(shift_list[i])
                    print(f'\n Desvio Padrão: {std_list[i]}')
                    final_list = []
                    
                    for doctor in self.doctors:
                        final_list.append(f'{doctor.name}: {shift_list[i].count(doctor.name)}')
                    print(f'\n Contagem de turnos: {final_list}')
                    return None
            
    def imprimir(self, shift):

        if self.doctors_per_night != 0:
            for i in range(self.days):
                print(f'\n Dia {shift[(self.doctors_per_day + self.doctors_per_night+ 1) * i]}:') 

                for j in range(self.doctors_per_day):
                    print(f'{j + 1}° Plantonista - {shift[(self.doctors_per_day+self.doctors_per_night+1) * i + j+1]}')

                for k in range(self.doctors_per_night):
                    print(f'{k + 1}° Plantonista noturno - {shift[(self.doctors_per_day+self.doctors_per_night+1) *i+k+j+2]}')

        else:
            for i in range(self.days):
                print(f'\n Dia {shift[(self.doctors_per_day + 2) * i]}:') 

                for j in range(self.doctors_per_day):
                    print(f'{j + 1}° Plantonista - {shift[(self.doctors_per_day+2) * i + j+1]}')
                    