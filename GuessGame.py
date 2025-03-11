#libraries
import random
import time


#//Variables//
difficulty = 0
attempts = 0
choosen_number = -1
random_number = None
tries = None
hints = 2

def game(): #here we initialize the first part of the game, asking for difficulty, explaining it, etc.
    global difficulty, attempts, tries, random_number, hints #we need them global since we are dealing with functions.

    print("Welcome to the Number Guessing Game!")
    time.sleep(1)
    print("The game is simple: I choose a random number between 1 and 100...")
    time.sleep(1)
    print("And you'll have to guess the one I choosed!")
    time.sleep(1)
    print("Please select the difficulty, it will change how many tries you'll have:")
    print("1. Easy (10 chances)")
    print("2. Medium (5 chances)")
    print("3. Hard (3 chances)")

    difficulty_values = {
        1: "Easy",
        2: "Medium",
        3: "Hard"
    }

    while True: #if the input is not valid, an error wil be thrown until the input is correct.
        try:
            difficulty = int(input("Choose the difficulty by tiping 1,2 or 3: "))
            if difficulty in difficulty_values.keys():
                break
            else:
                print("You can choose only between 1,2 and 3!")
        except ValueError:
            print("Please insert a valid number!")

    difficulty = difficulty_values.get(difficulty) #we convert the input given by the user into a string with the corrispondent difficulty.

    print(f"Great, you have selected the {difficulty} difficulty level.")
    time.sleep(1)
    print("You will always have 2 hints, if you are running out of tries!")
    time.sleep(1)
    print("OK. Let's start the game!")


    tries_system = {
        "Easy": 10,
        "Medium": 5,
        "Hard": 3
    }

    tries = tries_system.get(difficulty) #we give to tries the value corresponding to the difficulty choosen before.
    attempts = 0  
    hints = 2  
    random_number = random.randint(1, 100)  
    game2()

def game2(): #This is the second part of the game. We splitted it because when we go to the hint function, we can go back to the game without cycling from the start again.
    global choosen_number, tries, random_number, attempts

    while choosen_number != random_number and tries > 0: #OK. this basically checks in a loop if the input given by the user is equal to the one choosen by the machine.
        while True:
            user_input = input("Enter your guess (or type -1 for a hint): ")

            if user_input == "-1":  
                Hint()
                continue   #we first check if the user wants an input, if not we can go on.
            
            try:
                choosen_number = int(user_input)  
                if choosen_number < 1 or choosen_number > 100:
                    print("You can choose only between 1 and 100!")
                    continue 
                else:
                    break  
            except ValueError:
                print("Invalid input, please enter a number.")
                continue  #we checked whether the input was between 1 and 100.

        if choosen_number > random_number:
            print(f"Wrong! The number is less than {choosen_number}")
        elif choosen_number < random_number:
            print(f"Wrong! The number is greater than {choosen_number}") #we control if the user got it or not.

        attempts += 1
        tries -= 1

        print(f"You have {tries} tries left!")

    if tries == 0 and random_number != choosen_number: #the 2nd condition is necessarily because if the user guesses it on the last tries, it will go to 0 and therefore considering it as a lose.
        print(f"Your tries have reached 0..., you lose! The number was {random_number}")
    else:
        print(f"Congratulations! You won in {attempts} attempts!")
        ScoreSaver(difficulty, attempts)

def ScoreSaver(difficulty, attempts): #this function saves the score into a file, so that it will be saved forever.
    file_name = "Scores.txt"

    try:
        with open(file_name, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = [] #if the file is not found, the lines will be empty.

    updated = False  
    new_data = []  

    for line in lines:
        if line.startswith(difficulty): #if we find an existing line with that difficulty, we check by double splitting the line if the actual score is better than the one saved.
            current_attempts = int(line.split(":")[1].split()[0])  
            if attempts < current_attempts:  
                new_data.append(f"{difficulty}: {attempts} attempts\n")  
                updated = True  #if it is, we will save the new line to write in new_data.
            else:
                new_data.append(line)  #if the new score is not the best, we are going to re-append the already existing best score.
                updated = True  
        else:
            new_data.append(line) #if we do not find a match, we are going to append the original line.

    if not updated: 
        new_data.append(f"{difficulty}: {attempts} attempts\n") #here it adds the new difficulty, in case it was not present before. We are not adding two times the same line, as it was not present in lines.

    with open(file_name, "w") as file:
        file.writelines(new_data) #we overwrite the file with all the new info.

def Hint(): #this function gives to the user hints.
    global hints
    if hints > 0:
        print("Mhhh...")
        time.sleep(1)
        print("Seems like you wanna an hint...")
        time.sleep(1)

        if hints == 2:
            if len(str(random_number)) > 1:  
                print(f"OK. Your number starts with {str(random_number)[0]}")
            else:
                print("OK. Your number is less than 10!")
            print("You now have only 1 hint left!")

        elif hints == 1:
            print("Again?!")
            time.sleep(1)
            if len(str(random_number)) > 1:  
                last_digit = int(str(random_number)[-1])  #we take the last digit of the number if it has two digits.
                if last_digit % 2 == 0:
                    print("Fine, the last digit of your number is divisible by 2!")
                else:
                    print("Fine, the last digit of your number is NOT divisible by 2!")
            else:
                print("I can't give you a hint! Your number has only one digit!")
            print("You now have only 0 hint left!")

        hints -=1
    else:
        print("Sorry. You have run out of hints!")
    
    #well, it is pretty self-explanatory.

def ask_to_play_again(): #we check if the user wants to play another round.
    while True:
        file_name = "Scores.txt"

        try:
            with open(file_name, "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
                lines = []
        
        with open(file_name, "r") as file:  
            print(f"Your best scores are:")
            print(*lines, sep="") #we give to the user its best results.


        wanna_play_again = input("Want to make a new round? (Y/N): ")

        if wanna_play_again == "Y":
            print("Good!")
            time.sleep(2)
            break 
        elif wanna_play_again == "N":
            print("OK. Thank you for playing!")
            time.sleep(2)
            exit() 
        else:
            print("Please type only 'Y' for yes or 'N' for no!")
            time.sleep(1)

while True: #the main loop of the app.
    game()
    ask_to_play_again()