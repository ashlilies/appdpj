# Account login tester... Meant to be run standalone
from application.Models.Account import *


def main():
    print("1-Register")
    print("2-Login")

    choice = input("Enter choice: ")
    if choice == '1':
        print("REGISTER")
        Account(input("Email: "), input("Password: "))

    elif choice == '2':
        print("LOGIN")
        if Account.login_user(input("Enter email: "),
                              input("Enter password: ")):
            print("Success")
        else:
            print("Failure")

    main()

main()