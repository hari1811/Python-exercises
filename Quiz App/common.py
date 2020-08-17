

def get_int_input(prompt, high):
    while(1):
        print()
        try:
            UserChoice = int(input(prompt))
        except(ValueError):
            print("Error: Expected an integer input!")
            continue
        if(UserChoice > high or UserChoice < 1):
            print("Error: Please enter a valid choice!")
        else:
            break
    return UserChoice

def get_yes_no_input(prompt):
    while(1):
        print()
        UserChoice = input(prompt).lower()
        if(UserChoice == 'y'):
            return 1
        elif(UserChoice == 'n'):
            return 0
        else:
            print("Error: Please enter y or n!")
