
import unittest
from src.entities.doctor import Doctor

class test_create_shift(unittest.TestCase):
    
    def test_create_doctor(self):

        #given
        doctor = Doctor('Marcelo', [1, 2], [1, 3], True, 3, True)

        #then
        self.assertEqual(doctor.name, 'Marcelo')
        self.assertEqual(doctor.availability, [1, 2])
        self.assertEqual(doctor.night_availability, [1, 3])

    def test_class_count_methods(self):

        #given
        doctor = Doctor('Marcelo', [1, 2], [1, 3], True, 3, True)

        #when
        doctor.increment()
        doctor.add_day()
        doctor.history_add(2)

        #then
        self.assertEqual(doctor.shift_count, 1)
        self.assertEqual(doctor.consecutive_shifts, 1)
        self.assertEqual(doctor.history, [2])

    def test_class_setup_methods(self):

        #given
        doctor = Doctor('Marcelo', [1, 2], [1, 3], True, 3, True)
        doctor.increment()
        doctor.add_day()
        doctor.history_add(2)

        #when
        doctor.setup()

        #then
        self.assertEqual(doctor.shift_count, 0)
        self.assertEqual(doctor.consecutive_shifts, 0)
        self.assertEqual(doctor.history, [])

    def test_doctor_not_valid(self):

        #given
        doctor = Doctor('Marcelo', [1, 2], [1, 3], True, 3, True)
        doctor.add_day()
        doctor.add_day()
        doctor._priority_factor = 0.5

        #when
        response = doctor.is_valid(0.5, [], 1)

        #then
        self.assertEqual(response, False)

    def test_doctor_is_valid(self):

        #given
        doctor = Doctor('Marcelo', [1, 2], [1, 3], True, 3, True)
        doctor.add_day()
        doctor._priority_factor = 0.5

        #when
        response = doctor.is_valid(0.5, [], 1)

        #then
        self.assertEqual(response, True)
