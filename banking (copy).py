import random


def generate_password():
    password = random.choices("0123456789", k=4)
    password = "".join(password)
    return password


def generate_card():
    iin = ["4", "0", "0", "0", "0", "0"]
    left = random.choices("0123456789", k=9)
    combine = iin+left
    for i in range(len(combine)):
        if i % 2 == 0:
            combine[i] = int(combine[i])*2
        else:
            combine[i] = int(combine[i])
    combine = [i-9 if i > 9 else i for i in combine]
    sum = 0
    for i in combine:
        sum += i
    checksum = str(10 - sum % 10)
    left.append(checksum)
    return "".join(iin+left)


cards = {}
while True:
    choose = int(input("1. Create an account\n2. Log into account\n0. Exit\n"))
    if choose == 0:
        print("\nBye!")
        break
    elif choose == 1:
        card = {"password": generate_password(),
                "balance": 0}
        number = generate_card()
        cards[number] = card
        print(
            f"\nYour card has been created\nYour card number:\n{number}\nYour card PIN:\n{card['password']}\n")
    elif choose == 2:
        card = input("Enter your card number:\n")
        password = input("Enter your PIN:\n")
        if cards.get(card) and cards[card]['password'] == password:
            print("\nYou have successfully logged in!\n")
            while True:
                next = int(input("1. Balance\n2. Log out\n0. Exit\n"))
                if next == 1:
                    print(f"\nBalance: {cards[card]['balance']}\n")
                if next == 2:
                    print("\nYou have successfully logged out!\n")
                    break
                if next == 0:
                    exit()
        else:
            print("\nWrong card number or PIN!\n")
