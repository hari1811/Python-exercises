
import getpass 

from common import *
from account import delete_account
from database import *

__all__ = ['admin_login']

def admin_login():
    username = input("Please enter your username: ")
    password = getpass.getpass(prompt="Please enter your password: ") 
    if password == get_password(username): 
        print('\nWelcome', username, '..!!!') 
        admin_options(username)
    else: 
        print('Incorrect login credentials..!!!') 
    return None

def admin_options(username):
    while(1):
        print("\n1. CREATE NEW TEST\n"\
              "2. DISPLAY EXISTING TEST\n"
              "3. MODIFY EXISTING TEST\n"\
              "4. REMOVE/DELETE TEST\n"\
              "5. LOGOUT\n"\
              "6. DELETE ACCOUNT")
        userChoice = get_int_input("Enter your choice: ", 6)

        if(userChoice == 1):
            create_test(username)

        elif(userChoice == 2):
            test_list = display_tests(username, 1)
            if(test_list):
                test = get_int_input("Enter the test to be displayed: ", len(test_list))
                display_test(test_list[test-1])

        elif(userChoice == 3):
            test_list = display_tests(username, 1)
            if(test_list):
                test = get_int_input("Enter the test to be modified: ", len(test_list))
                modify_test(test_list[test-1])

        elif(userChoice == 4):
            test_list = display_tests(username, 1)
            if(test_list):
                test = get_int_input("Enter the test to be deleted: ", len(test_list))
                conf = get_yes_no_input("Confirm delete test {} (y/n)".format(test_list[test-1]))
                if(conf):
                    remove_test(username, test_list[test-1])

        elif(userChoice == 5):
            break
        else:
            confirm = get_yes_no_input("Confirm delete account?(y/n): ")
            if(confirm):
                delete_account(username)
                print("Account deleted.")
                break

    return None

def create_test(user):
    while(1):
        TestName = input("Enter the test name: ")
        if(create_test_table(TestName) == 0):
            break
    insert_test(user, TestName)
    modify_test(TestName)

def modify_test(TestName):
    while(1):
        print("\n1. ADD QUESTION\n"\
              "2. DELETE QUESTION\n"\
              "3. DISPLAY TEST\n"\
              "4. SUBMIT")

        adminChoice = get_int_input("Please enter your choice: ", 4)

        if(adminChoice == 1):
            add_ques(TestName)
        elif(adminChoice == 2):
            delete_ques(TestName)
        elif(adminChoice == 3):
            display_test(TestName)
        else:
            break
    return None
