
import getpass
from common import *
from database import *

def create_account():

    userList = get_admin_List()
    while(1):
        username = input("\nPlease give your username: ")
        if username in userList:
            print("\nUsername not available, please choose another one.", end = '')
        else:
            while(1):
                password1 = getpass.getpass(prompt="\nPlease enter your password: ")
                password2 = getpass.getpass(prompt="\nPlease re-enter your password: ")
                if(password1 != password2):
                    print("\nPasswords don,t match!")
                    continue
                else:
                    break
            break

    insert_adm_list(username, password1)
    create_user_table(username)
    print("\nAccount created successfully.")
    return None

def delete_account(username):
    test_list = display_tests(username, 1)
    for test in test_list:        
        remove_test(username, test)
    delete_user_table(username)
    remove_adm_list(username)