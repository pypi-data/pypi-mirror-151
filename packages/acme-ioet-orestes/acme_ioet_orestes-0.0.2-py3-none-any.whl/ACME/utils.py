from datetime import datetime
import re
from  ACME.errors import EmptyFileError, ErrorFileType, bcolors
import os

############--------START OF CANCATENATION FUNCTIONS--------#################

def check_file_extesion(path: str) -> str:
        """
        First function to check if the file
        extension is a .txt: if so, call the next
        function
        """
        if not path.endswith('.txt'):
                raise ErrorFileType()
        return read_file_lines(path)  


def read_file_lines(path: str) -> str:
        """
        Check if the file exist, read it and pass it
        as a list to the next function. 
        """
        lines = []
        try:
                with open(path) as file:
                        lines = file.readlines()
                if not lines:
                        raise EmptyFileError()
        except FileNotFoundError:
                print(bcolors.FAIL + 'File not found. Make sure to submit the complete path to the file.')
        return read_lines(lines)

def read_lines(lines_input: list) -> list:
        """
        Check for input errors in the file.
        If there's error print it.
        Lines with no problem are appended to the cleared_lines list 
        and returned to the main Class AcmeEmployee.
        """
        cleared_lines = []
        nro_lines = 1
        for line in lines_input:
            if not check_line(line):
                print(f"{bcolors.FAIL}Error in line {bcolors.OKBLUE}{nro_lines}{bcolors.ENDC}{bcolors.FAIL} please make sure to use the standar format. This line will not be computed{bcolors.ENDC}")
            else:
                cleared_lines.append(get_name_and_days__hours(line))
            nro_lines += 1
       
        return cleared_lines

############--------END OF CANCATENATION FUNCTIONS--------#################


def check_line(line):
        """
        Function to check if the complete line meets the 
        requirements.
        """
        string_ok = re.search(r"""
                                ^(([A-Za-z]+[=]+
                                [A-Z]{2}[0-9][0-9]:[0-9][0-9]-[0-9][0-9]:[0-9][0-9]){1},
                                *([A-Z]{2}[0-9][0-9]:[0-9][0-9]-[0-9][0-9]:[0-9][0-9],)*
                                ([A-Z]{2}[0-9][0-9]:[0-9][0-9]-[0-9][0-9]:[0-9][0-9])($|\s)*)$
                                """,line, re.VERBOSE)
        return bool(string_ok)

def get_name_and_days__hours(string):
        """
        Function to separate the name and working 
        hours from the input text.
        """
        #Get the name of the employee.
        employee_name = re.search(r"([A-Za-z]+)([=]+)", string).group(1)
        #Get the worked days and hours as a list of tuples.
        worked_days_and_hours = re.findall(r"""
                                             ([A-Z]{2})([0-9][0-9]:[0-9][0-9])-([0-9][0-9]:[0-9][0-9])
                                             """, string, re.VERBOSE)

        return employee_name, worked_days_and_hours



def string_to_time(time_string):
        """
        Function to transform the str data to
        time data.
        """
        now = datetime.now()
        hours, minutes = time_string.split(":")[0],  time_string.split(":")[1]
        if hours == '00' and minutes == '00':
                hours,minutes = '23', '59'
        total_time = now.replace(hour=int(hours), minute=int(minutes), second=0, microsecond=0)
        return total_time

def string_to_time_employee(time_string):
        """
        Function to transform the str data to
        time data.
        """
        now = datetime.now()
        hours, minutes = time_string.split(":")[0],  time_string.split(":")[1]
        total_time = now.replace(hour=int(hours), minute=int(minutes), second=0, microsecond=0)
        return total_time


def open_files(file_name, example=False):
        """
        Function to open the data files of the program
        """
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, file_name), 'r') as f:
                info = f.read()
        if example:
                return os.path.join(__location__, file_name)
        else:
                return info


def example(output):
        info = open_files('acme.txt')
        
        text = f"""
The .txt contains this lines:

{bcolors.OKBLUE}{info}
The output will be:

{bcolors.OKGREEN}{output}
        """
        print(text)



def help():
        text = f"""
{bcolors.OKBLUE}
    _    ____ __  __ _____   _______  _______ ____  ____ ___ ____ _____
   / \  / ___|  \/  | ____| | ____\ \/ / ____|  _ \/ ___|_ _/ ___| ____|
  / _ \| |   | |\/| |  _|   |  _|  \  /|  _| | |_) \___ \| | |   |  _|
 / ___ \ |___| |  | | |___  | |___ /  \| |___|  _ < ___) | | |___| |___
/_/   \_\____|_|  |_|_____| |_____/_/\_\_____|_| \_\____/___\____|_____|

.......................................................................
                         ___ ___  _____ _____
                        |_ _/ _ \| ____|_   _|
                         | | | | |  _|   | |
                         | | |_| | |___  | |
                        |___\___/|_____| |_|
........................................................................
{bcolors.ENDC}
This program is designed to obtain the total amount for the employees of ACME. 
The info has to be submit in a .txt file with this format:

RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00

You can use as many lines as you want. The output will be the total amount that each employeee has earned. 
To proccess the data type in the terminal use this commands:
ACME <path to the file>
The path to the .txt file has to be explicit, 
example: "C:/User/Desktop/acme_may_payroll.txt" 
or you can put the file in the same directory of the project and simple run it:
python ACME acme_may_payroll.txt
######################################################

OPTIONS
---------------
To save the output in a .txt file in the same directory of the project use -sc (save copy) before the path to the file,
example:
ACME -sc <path to the file> 

To see and example user the -example command:
ACME -example

NOTES
-----------
If you have typo errors that doesn't match the require format in the lines of the .txt file, 
those lines will not be proccessed but the program will still run the next one. 
        """

        print(text)