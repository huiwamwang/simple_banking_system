import random
import sqlite3


conn = sqlite3.connect('card.s3db')
c = conn.cursor()


def luhn_algorithm(digits):
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    double_odd = [i * 2 for i in odd_digits]
    new_odd = [i - 9 if i > 9 else i for i in double_odd]
    sum_odd = sum(new_odd)
    sum_even = sum(even_digits)
    checksum = (((sum_odd + sum_even) * 9) % 10)
    return checksum


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER);')
    conn.commit()


def adding_data(card_number, pin, balance=0):
    c.execute('INSERT INTO card (number, pin, balance) VALUES (?, ?, ?)', (card_number, pin, balance))
    conn.commit()


def add_income(card_number, balance):
    c.execute('UPDATE card SET balance=? WHERE number=?', (balance, card_number))
    conn.commit()


def reading_data(card_number):
    c.execute('SELECT number, pin, balance FROM card WHERE number = ?', (card_number,))
    conn.commit()
    data = c.fetchall()
    return data


def reading_balance(card_number):
    c.execute('SELECT balance FROM card WHERE number=?', (card_number,))
    data = c.fetchone()
    return data[0]


class Main:

    def __init__(self):
        self.first_choice = None
        self.card = None
        self.pin = None
        self.balance = None

    def start(self):
        inp = int(input("1. Create an account\n2. Log into account\n0. Exit\n"))
        if inp == 1:
            self.creating_account()
        elif inp == 2:
            self.login()
        elif inp == 0:
            exit()
        else:
            print("Please choose the action from the list")
            self.start()

    def creating_account(self):
        iin = 400000
        bin_ = random.randint(100000000, 999999999)
        first15digit_str = ''.join(map(str, [iin, bin_]))
        checksum = luhn_algorithm([int(_) for _ in first15digit_str])
        card_number = ''.join(map(str, [iin, bin_, checksum]))
        print('\nYour card has been created', 'Your card number:', card_number, sep='\n')
        pin = random.randint(1000, 9999)
        print('Your card PIN:', pin, sep='\n')
        adding_data(card_number, pin)
        self.start()

    def login(self):
        card = input("Enter your card number:\n")
        try:
            self.card, self.pin, self.balance = reading_data(card)[0]
        except IndexError:
            print("\nWrong card number or PIN!\n")
            self.start()
        if card == self.card:
            pin = input("Enter your PIN:\n")
            if pin == self.pin:
                print('\nYou have successfully logged in!')
                self.logged()
            else:
                print("\nWrong card number or PIN!\n")
                self.start()
        else:
            print("\nWrong card number or PIN!\n")
            self.start()

    def logged(self):
        print("\n1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n")
        inp = int(input())
        if inp == 1:
            print(self.balance)
            self.logged()
        elif inp == 2:
            income = int(input('Enter income:\n'))
            self.card, self.pin, self.balance = reading_data(self.card)[0]
            self.balance += income
            add_income(self.card, self.balance)
            self.logged()
        elif inp == 3:
            print('Transfer\nEnter card number:\n')
            transfer_card = input()
            last_digit = int(transfer_card[-1])
            checksum = luhn_algorithm([int(_) for _ in transfer_card[0:-1]])
            if checksum != last_digit:
                print('Probably you made a mistake in the card number. Please try again!')
                self.logged()
            try:
                balance2 = reading_balance(transfer_card)
                transfer = int(input('Enter how much money you want to transfer:\n'))
                if self.balance - transfer < 0:
                    print('Not enough money!')
                    self.logged()
                self.balance -= transfer
                balance2 += transfer
                add_income(self.card, self.balance)
                add_income(transfer_card, balance2)
                print('Success!')
                self.logged()
            except TypeError:
                print('Such a card does not exist.')
                self.logged()
        elif inp == 4:
            c.execute('DELETE FROM card WHERE number=?', (self.card,))
            conn.commit()
            print('\nThe account has been closed!\n')
            self.start()
        elif inp == 5:
            print("\nYou have successfully logged out!\n")
            self.start()
        elif inp == 0:
            print('Bye!')
            exit()
        else:
            return self.logged()


create_table()
go = Main()
go.start()
