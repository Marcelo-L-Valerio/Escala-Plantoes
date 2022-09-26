
class Doctor():

    def __init__(self, name: str, avaible_days: list, avaible_nights: list) -> None:
        self.name: str = name
        self.__availability: list = avaible_days
        self.__night_availability= avaible_nights
        self.__shift_count: int = 0
        self._priority_factor: int = 0
        self.__history: list = []
        self.__consecutive_shifts: int = 0

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