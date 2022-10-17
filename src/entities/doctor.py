
class Doctor():

    def __init__(self, name: str, avaible_days: list, avaible_nights: list, is_from_hospital: bool, graduated_from: int, is_spceialist: bool) -> None:
        self.name: str = name
        self.__availability: list = avaible_days
        self.__night_availability= avaible_nights
        self.__shift_count: int = 0
        self._priority_factor: int = 0
        self.__history: list = []
        self.__consecutive_shifts: int = 0
        self.__is_from_hospital: bool = is_from_hospital
        self.__graduated_from: int = graduated_from
        self.__is_spceialist: bool = is_spceialist

    @property
    def shift_count(self) -> str:
        return self.__shift_count

    @property
    def availability(self) -> str:
        return self.__availability
    
    @property
    def night_availability(self) -> str:
        return self.__night_availability

    @property
    def priority_factor(self) -> str:
        return self._priority_factor

    @property
    def history(self) -> str:
        return self.__history

    @property
    def consecutive_shifts(self) -> str:
        return self.__consecutive_shifts

    @property
    def is_from_hospital(self) -> str:
        return self.__is_from_hospital

    @property
    def graduated_from(self) -> str:
        return self.__graduated_from

    @property
    def is_spceialist(self) -> str:
        return self.__is_spceialist

    def increment(self):
        self.__shift_count += 1

    def add_day(self):
        self.__consecutive_shifts += 1

    def zero_consec(self):
        self.__consecutive_shifts = 0
    
    def history_add(self, day):
        self.__history.append(day)

    def setup(self):
        self.__consecutive_shifts = 0
        self.__history = []
        self.__shift_count = 0

    def is_valid(self, priority_factor, selected, accuracy_factor):
        if self.__consecutive_shifts < 2 and (
            priority_factor * accuracy_factor <= self._priority_factor <= priority_factor):
            if self not in selected:
                return True
        else:
            return False

    def pontuation(self, graduated_years_list, pontuation):

        if self.is_from_hospital == True:
            pontuation += 200 * self.shift_count

        if self.is_spceialist == True:
            pontuation += 100 * self.shift_count

        for i in range(len(graduated_years_list)):

            if self.graduated_from == graduated_years_list[-1 -(1 * i)]:
                pontuation += 100/(i+1) * self.shift_count
                return pontuation
