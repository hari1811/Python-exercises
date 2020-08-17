

import sqlite3
from common import *

conn = None

def connect():
    global conn
    conn = sqlite3.connect('quiz.db')

def create_adm_list():
    global conn
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS ADMINLIST
        (USERNAME       TEXT    NOT NULL,
         PASSWORD       TEXT    NOT NULL);''')

    conn.commit()

def insert_adm_list(user, passw):
    global conn
    conn.execute("INSERT INTO ADMINLIST (USERNAME,PASSWORD) \
      VALUES ('{}', '{}')".format(user, passw));
    conn.commit()

def remove_adm_list(user):
    global conn
    conn.execute("DELETE from ADMINLIST where USERNAME = '{}';".format(user))
    conn.commit()

def display_adm_list():
    global conn
    cursor = conn.execute("SELECT USERNAME from ADMINLIST")
    print("Admin list:\n")
    for row in cursor:
        print(row[0])

def get_admin_List():
    global conn
    cursor = conn.execute("SELECT USERNAME from ADMINLIST")
    userList = [row[0] for row in cursor] #row is a tuple: (username,)
    return userList

def get_password(user):
    global conn
    cursor = conn.execute("SELECT PASSWORD from ADMINLIST where USERNAME = '{}';".format(user))
    password = cursor.fetchone() # tuple (password,)
    if(password):
        return password[0]
    else:
        return None

def start_db():
    connect()
    create_adm_list()

def close_db():
    conn.close()

def create_user_table(user):
    global conn
    c = conn.cursor()
    c.execute('''CREATE TABLE {}
        (TESTS_BY_USER       TEXT    NOT NULL);'''.format(user.upper()))
    conn.commit()

def delete_user_table(user):
    global conn
    c = conn.cursor()
    c.execute("DROP TABLE {};".format(user.upper()))
    conn.commit()
    #print("User table for {} deleted.".format(user))

def insert_test(user, testName):
    global conn
    conn.execute("INSERT INTO {} VALUES ('{}')".format(user.upper(), testName));
    conn.commit()

def remove_test(user, testName):
    global conn
    conn.execute("DELETE from {} where TESTS_BY_USER = '{}';".format(user.upper(), testName))
    conn.execute("DROP TABLE {};".format(testName))
    conn.commit()
    print("Test {} deleted.".format(testName))

def display_tests(user, disp_flag):
    testList = []
    global conn
    cursor = conn.execute("SELECT TESTS_BY_USER  from {}".format(user.upper()))
    
    for row in cursor:
        testList.append(row[0])

    if(disp_flag):    
        if(testList):
            print("\nTests you have created:")
            i = 1
            for test in testList:
                print('{}.'.format(i),  test)
                i += 1
        else:
            print("\nYou have not created any test.")

    return testList

def get_tests_avail():
    testList = []
    adminList = get_admin_List()
    for admin in adminList:
        testList = testList + display_tests(admin, 0)
    return testList

def create_test_table(test):
    global conn
    c = conn.cursor()
    c.execute(''' SELECT count(name) FROM sqlite_master 
                     WHERE type='table' AND name='{}' '''.format(test)) #error for c++
    #if the count is 1, then table exists
    if(c.fetchone()[0]==1): 
        print("Test with the given name already exists!. Please give another name.")
        return -1

    else:
        c.execute('''CREATE TABLE {}
        (Question       TEXT    NOT NULL,
         Choice_A        TEXT    NOT NULL,
         Choice_B        TEXT    NOT NULL,
         Choice_C        TEXT    NOT NULL,
         Choice_D        TEXT    NOT NULL,
         Answer         TEXT    NOT NULL,
         Marks          INT,
         Explanation    TEXT);'''.format(test))
         
        conn.commit()
        return 0

def add_ques(TestName):

    Ques = input("Enter the question: ")

    ch = []
    ch.append(input("Enter choice A: "))
    ch.append(input("Enter choice B: "))
    ch.append(input("Enter choice C: "))
    ch.append(input("Enter choice D: "))

    while(1):
        Ans = input("Enter the right answer(A/B/C/D): ",)
        if(Ans.upper() not in ['A', 'B', 'C', 'D']):
            print("Please enter a valid answer.")
        else:
            break

    marks = get_int_input("Enter the marks for the question (positive integer, max = 10): ", 10)
    Exp = input("Enter explanation for the answer: ")

    global conn
    conn.execute("INSERT INTO {} VALUES ('{}', '{}', '{}', '{}', '{}', '{}',"\
                   " {}, '{}')".format(TestName, Ques, ch[0], ch[1], ch[2], 
                                       ch[3], Ans, marks, Exp))
    conn.commit()


def delete_ques(TestName):
    global conn
    cursor = conn.execute("SELECT Question from {}".format(TestName))
    QnsList = []
    i = 1
    print()
    for row in cursor:
        print('{}.'.format(i), row[0])
        QnsList.append(row[0])
        i += 1
    userInp = get_int_input("Enter the Question No. to be deleted: ", len(QnsList))
    conf = get_yes_no_input("Confirm delete question {} (y/n): ".format(userInp))
    if(conf):
        conn.execute("DELETE from {} where Question = '{}';".format(TestName, QnsList[userInp-1]))
        conn.commit()

def display_test(TestName):

    global conn
    cursor = conn.execute("SELECT Question, Choice_A, Choice_B, Choice_C, Choice_D, Marks" \
                          " from {}".format(TestName))
    i = 1
    print()
    for row in cursor:
        print('{}.'.format(i), '[{} mark(s)]'.format(row[5]), row[0], '\n')
        print("    A) ", row[1])
        print("    B) ", row[2])
        print("    C) ", row[3])
        print("    D) ", row[4], "\n")
        i += 1

def get_test(TestName):
    global conn
    cursor = conn.execute("SELECT Question, Choice_A, Choice_B, Choice_C, Choice_D,"\
                           " Answer, Marks, Explanation from {}".format(TestName))
    return cursor
