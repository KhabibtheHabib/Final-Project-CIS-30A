# same imports from the main file to keep the imports consistent

from datetime import datetime
import tkinter as tk
from tkcalendar import Calendar
from tkinter import messagebox


# here we define the Order class to handle food orders
class Order:
    # constructor for the class
    def __init__(self):
        # starting with an empty list to fill with the user selected menu items
        self.items = []
        # a dictionary that maps the menu items to prices is created here
        self.menu = {
            "Cheese Pizza": 12.99,
            "Pepperoni Pizza": 14.99,
            "Salad": 6.99,
            "Soda": 2.99,
        }

    # here is a function to add items to the order
    def add_item(self, item, quantity=1):
        # check if the item is in the menu
        if item in self.menu:
            # now we make a tuple of the items the user chooses, making sure to store how many they selected, what they selected and the cost
            self.items.append((item, quantity, self.menu[item]))
            return True  # operation was a success
        return False  # fails if item not found


# class for devlivery orders, a subclass, that inherits from the Order class
class DeliveryOrder(Order):
    # constructor for the class
    def __init__(self):
        # the parent class constructor is called here
        super().__init__()
        self.delivery_fee = 4.99  # delivery fee
        # we now have a function to calculate the total, with the delivery fee=

    def calculate_total(self):
        # calculate the total for the items the user chooses
        subtotal = sum(item[1] * item[2] for item in self.items)
        # now we add the delivery fee
        return subtotal + self.delivery_fee
