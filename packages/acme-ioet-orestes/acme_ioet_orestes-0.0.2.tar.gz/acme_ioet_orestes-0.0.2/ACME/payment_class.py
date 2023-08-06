import json
from datetime import timedelta
import os
from ACME.utils import string_to_time, string_to_time_employee, open_files

class AcmeEmployee():
    output = ''
    def __init__(self, cleared_data, json_file=open_files('payment.json')):
        self.json_file = json_file
        self.cleared_data = cleared_data
        #Open the json file and read the data
        company_payment_data = json.loads(self.json_file)
        self.company_payment_data = company_payment_data
        #Load the days and weekend days
        self.week_days = company_payment_data["week"]
        self.weekend_days = company_payment_data["weekend"]
        #Make the string data to time data (worked time) and int data (pay per hour).
        self.week_payment = [ [string_to_time(i[0]), string_to_time(i[1]), int(i[2])] for i in company_payment_data["week_pay"]]
        self.weekend_payment = [ [string_to_time(i[0]), string_to_time(i[1]), int(i[2])] for i in company_payment_data["weekend_pay"]]
        #After receive the data, procces the payment
        self.procces_payment()
     
        
    def procces_payment(self: list) -> list:
        """
        This function is the core of the app. Here the computation of 
        the total salary is made
        """
        total_payment = 0
        #Extract from the list the employee name and
        #working hours
        employee = self.cleared_data[0]
        working_hours = self.cleared_data[1]
        for data in working_hours:
            day, start_time, end_time = data[0], string_to_time_employee(data[1]), string_to_time_employee(data[2])
            current_hour = start_time
            while current_hour < end_time:
                current_hour +=  timedelta(hours=1)
                if day in self.week_days:
                    for hour in self.week_payment:
                        if  hour[0] <= current_hour <= hour[1]:
                            total_payment += hour[2]       
                else:
                    for hour in self.weekend_payment:
                        if hour[0] <= current_hour <= hour[1]:
                            total_payment += hour[2]
    
        AcmeEmployee.output += f"The amount to pay {employee} is: {total_payment} USD\n"

    @staticmethod
    def save_output():
        """
        Save the output to a .txt file
        """
        ROOT_DIR = os.path.abspath(os.curdir)
        joined_path = os.path.join(ROOT_DIR, "acme_employee_payment_roll.txt") 
        with open(joined_path, "w+") as wf:
            wf.writelines(AcmeEmployee.output)
        print(f'File saved in {joined_path}!')
        


    def __str__(self) -> str:
        return AcmeEmployee.output
