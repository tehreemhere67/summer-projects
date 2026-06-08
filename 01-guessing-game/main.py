import random

def main():
    random_number = random.randint(1, 100)
    user_input = int(input("Enter your guessed number: "))
    attempt_count = 0

    while user_input != random_number:
        attempt_count += 1
        if user_input < random_number:
            print("Too low")
        elif user_input > random_number:
            print("Too high")
        user_input = int(input("Enter your guessed number: "))

    attempt_count += 1
    print(f"Correct! You got it in {attempt_count} attempts.")

    try:
        with open("highscore.txt", "r") as f:
            content = int(f.read())
        if attempt_count < content:
            with open("highscore.txt", "w") as f:
                f.write(str(attempt_count))
            print("New high score!")
        else:
            print(f"High score is still {content} attempts.")
    except FileNotFoundError:
        with open("highscore.txt", "w") as f:
            f.write(str(attempt_count))
        print("First game! Score saved.")

main()