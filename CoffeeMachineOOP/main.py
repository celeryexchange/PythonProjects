from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine
import os
import sys


# instantiate all objects
my_coffee_machine = CoffeeMaker()
my_menu = Menu()
my_money_machine = MoneyMachine()

# clear the terminal
os.system("cls||clear")

# start the coffee machine
while True:
    command = input(f"What would you like? ({my_menu.get_items()}): ").lower()
    if command == "off":
        sys.exit()
    elif command == "report":
        my_coffee_machine.report()
    elif command == "money":
        my_money_machine.report()
    else:
        # check if the command is a known drink on the menu
        drink_item = my_menu.find_drink(command)
        # check if we have enough ingredients
        if drink_item:
            if my_coffee_machine.is_resource_sufficient(drink_item):
                # if payment is accepted then go ahead and make the drink
                if my_money_machine.make_payment(drink_item.cost):
                    my_coffee_machine.make_coffee(drink_item)
