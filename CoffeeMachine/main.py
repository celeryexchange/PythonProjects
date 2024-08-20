import os
import sys
from art import logo
import time

menu = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
    "money": 0,
}

resources_unit = {
    "water": "ml",
    "milk": "ml",
    "coffee": "g",
    "money": "$",
}


def print_report() -> None:
    """Prints a report that shows the current resource quantities, e.g.
    Water: 100ml, Milk: 50ml, Coffee: 25g, Money: $17.55. """
    for resource in resources.keys():
        resource_amount = resources[resource]
        resource_unit = resources_unit[resource]
        resource_and_unit = f"{resource_amount}{resource_unit}"
        if resource_unit == "$":
            resource_and_unit = f"{resource_unit}{resource_amount:.2f}"
        print(f"{resource.capitalize()}: {resource_and_unit}")


def is_resource_sufficient(drink: str):
    """Function which looks up how much of each ingredient is needed to
    prepare a given drink and checks if the coffee machine has sufficient
    ingredients to make the drink. """
    # Check if the requested drink is in the menu
    if drink not in menu:
        print(f"Sorry, {drink} is not in the menu.")
        return

    # Get the required ingredients for the selected drink from the menu
    required_ingredients = menu[drink]["ingredients"]

    # Check if the machine has sufficient ingredients
    for ingredient, amount in required_ingredients.items():
        if ingredient not in resources or resources[ingredient] < amount:
            print(f"Sorry, not enough {ingredient} to prepare {drink}.")
            return

    return True


def is_payment_enough(drink: str):
    price_of_drink = menu[drink]['cost']
    print(f"The price of a {drink} is ${price_of_drink:.2f}. Please insert your coins.")

    # get quantities of different coins
    quarters = int(input("Quarters: "))
    dimes = int(input("Dimes: "))
    nickles = int(input("Nickels: "))
    pennies = int(input("Pennies: "))

    # calculate the monetary value of inserted coins
    money_inserted = quarters * 0.25 + dimes * 0.1 + nickles * 0.05 + pennies * 0.01

    if money_inserted < price_of_drink:
        print(f"Sorry, ${money_inserted:.2f} is not enough to buy a {drink}. Money refunded.")
        return
    else:
        # if the user has inserted too much money, the machine should offer change.
        change_for_drink = money_inserted - price_of_drink
        if change_for_drink > 0:
            print(f"Here is your change: ${change_for_drink:.2f}.")
        return True


def prepare_drink(drink: str):
    # Get the required ingredients for the selected drink from the menu
    required_ingredients = menu[drink]["ingredients"]

    print(f"Preparing {drink}...")
    time.sleep(3)

    # Reduce the amount of ingredients in the machine
    for ingredient, amount in required_ingredients.items():
        resources[ingredient] -= amount

    # Add money to the machine
    resources["money"] += menu[drink]['cost']

    print(f"{drink.capitalize()} is ready! ☕ Enjoy.")


def start_coffee_machine():

    # clear terminal
    os.system('cls||clear')
    print(logo)

    while True:
        user_command = input("What would you like? (espresso/latte/cappuccino): ").lower()
        if user_command == "off":
            sys.exit()
        elif user_command == "report":
            print_report()
        else:
            if is_resource_sufficient(user_command):
                if is_payment_enough(user_command):
                    prepare_drink(user_command)


if __name__ == "__main__":
    start_coffee_machine()
