
from common import *
from database import *

__all__ = ['test_options']

def test_options():
    tests_available = get_tests_avail()
    if(len(tests_available) == 0):
        print("\nThere are no tests available currently!\n")
    else:
        while(1):
            i = 1
            print("\nTESTS AVAILABLE ON:\n")
            for test in tests_available:
                print("{}.".format(i), test) 
                i += 1
            print("{}. Exit".format(i))
            testChoice = get_int_input("Please choose the topic or exit: ", len(tests_available) + 1)
            if(testChoice != len(tests_available) + 1):
                take_test(tests_available[testChoice-1])
            else:
                break
    return None

def take_test(testName):
    print("\n1. START TEST \n2. GO BACK")
    userChoice = get_int_input("Enter your Choice : ", 2)

    if(userChoice == 1):
        UserScore = 0
        TotalScore = 0
        
        test = get_test(testName)

        i = 1
        print()
        for row in test:
            print('{}.'.format(i), '[{} mark(s)]'.format(row[6]), row[0], '\n')
            print("    A) ", row[1])
            print("    B) ", row[2])
            print("    C) ", row[3])
            print("    D) ", row[4], "\n")
            i += 1

            while(1):
                UserAnswer = input("Enter your Answer(A/B/C/D): ",)
                if(UserAnswer.upper() not in ['A', 'B', 'C', 'D']):
                    print("Please enter a valid answer.")
                else:
                    break

            if(UserAnswer.upper() == row[5].upper()):
                print("That's Correct!")
                UserScore += row[6]
            else:
                print("Incorrect. The right answer is", row[5].upper())

            print(row[7], '\n')
            TotalScore += row[6]
        if(i == 1):
            print("No Questions available in this test!")
        else:
            print("\nYour Score: {0:d}/{1:d}({2:.2f}%)".format(UserScore, TotalScore, float(UserScore*100)/TotalScore))
    return None

    

