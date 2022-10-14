
class Doctor():

    def __init__(self, name: str, avaible_days: list, avaible_nights: list, is_from_hospital: bool, graduated_from: int) -> None:
        self.name: str = name
        self.__availability: list = avaible_days
        self.__night_availability= avaible_nights
        self.__shift_count: int = 0
        self._priority_factor: int = 0
        self.__history: list = []
        self.__consecutive_shifts: int = 0
        self.__is_from_hospital: bool = is_from_hospital
        self.__graduated_from: int = graduated_from

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
