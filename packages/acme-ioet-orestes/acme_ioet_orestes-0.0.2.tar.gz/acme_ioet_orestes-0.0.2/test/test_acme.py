import os
import unittest
from ACME.utils import *
from ACME.__main__ import AcmeEmployee
from ACME.errors import ErrorFileType

class TestStringMethods(unittest.TestCase):
    if os.name == 'nt':
        txt_file = 'test\\data\\test_acme.txt'
        five_employees = 'test\\data\\test_acme_five_employees.txt'
        wrong_extension = 'test\\data\\wrong_extension.jpg'
        empty_file = 'test\\data\\empty_file.txt'
    else:
        txt_file = 'test//data//test_acme.txt'
        five_employees = 'test//data//test_acme_five_employees.txt'
        wrong_extension = 'test//data//wrong_extension.jpg'
        empty_file = 'test//data//empty_file.txt'

    def test_check_file_extesion(self):
        self.assertEqual(check_file_extesion(TestStringMethods.txt_file), [('ASTRID', [('MO', '10:00', '12:00'), ('TH', '12:00', '14:00'), ('SU', '20:00',\
                                                           '21:00')]), ('RENE', [('MO', '10:00', '12:00'), ('TU', '10:00', '12:00'), ('TH'\
,                                                           '01:00', '03:00'), ('SA', '14:00', '18:00'), ('SU', '20:00', '21:00')])])
        
        "Next lines replicates the use of the program in test"
        employees = check_file_extesion(TestStringMethods.txt_file)
        for employee in employees:
            AcmeEmployee(employee)
        self.assertEqual(str(AcmeEmployee.output), "The amount to pay ASTRID is: 85 USD\nThe amount to pay RENE is: 215 USD\n")

        AcmeEmployee.output = ""
        five_employees_file = check_file_extesion(TestStringMethods.five_employees)
        for employee_ in five_employees_file:
            AcmeEmployee(employee_)
        self.assertEqual(str(AcmeEmployee.output), "The amount to pay ASTRID is: 85 USD\nThe amount to pay RENE is: 215 USD\nThe amount to pay ABBY is: 380 USD\nThe amount to pay MATILDA is: 705 USD\n")

    def test_wron_extesion(self):
      with self.assertRaises(SystemExit):
         check_file_extesion(TestStringMethods.wrong_extension)


    def test_empty_file(self):
      with self.assertRaises(SystemExit):
         check_file_extesion(TestStringMethods.empty_file)  



if __name__ == '__main__':
    unittest.main()


    
                