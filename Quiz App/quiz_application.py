
''' Quiz Application

This is a standard quiz application that presents a set of carefully curated
questions to the users (a questionnaire), allows them to answer the same, and
displays the correct answer if they are wrong. Each test displays the 
final score of the user. 

The application has an account creation option for Admins.These Admins can create 
tests for other users, update or delete the tests they have created. 
'''

from common import get_int_input
from account import create_account
from admin import admin_login
from student import *
from database import start_db, close_db

print("Welcome to the Quiz App!")

start_db()

while(1):
    print("\n1. TAKE TEST\n"\
          "2. LOGIN AS ADMIN\n"\
          "3. CREATE ACCOUNT\n"\
          "4. EXIT")
    
    UserAction = get_int_input("Please enter your choice: ", 4)

    if(UserAction == 1):
        test_options()
    elif(UserAction == 2):
        admin_login()
    elif(UserAction == 3):
        create_account()
    else:
        print("\nClosing App...")
        break

close_db()