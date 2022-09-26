
from entities.shift import Shift
from business.doctors_list_generator import list_generator, default_list, random_list

# doctors = list_generator(16, 10) ## lista que pergunta nomes/disponibilidade
# doctors = random_list(2, 10, 7, 7) ## lista com nomes padrao e disponibilidade aleatoria para testes 
doctors = default_list() ## Lista com nomes e disponibilidade padrao para aprimoramento

outubro = Shift('Outubro', 10, doctors, 4, 1)

outubro.best_shift(1000)
