# imports necesarry for the program

# here we import the classes from the pizza_order.py file
from pizza_order import Order, DeliveryOrder

# import the UI library
import tkinter as tk

# here we import the calander to select dates and see the dates in that format
from tkcalendar import Calendar

# boxes to display info like errors, and ttk for some widgets used throughout
from tkinter import messagebox, ttk

# handing and getting dates
import datetime


# here a function is made to add items to the order
def add_item():
    # make the selection the one the user selected from the listox
    selection = menu_listbox.curselection()

    if not selection:  # if no items are selected, user is instructed to select an item
        messagebox.showerror("Error", "Please select an item first!")
        return

    try:
        # get the name of the selected item
        selected = menu_listbox.get(selection)
        # add the item to the order and make sure the display also shows selection
        if current_order.add_item(selected):
            update_display()

        # to catch any possible edge cases is exception is included here
        # for some reason my editor would have warning if i just used except so fixed by adding Exception as e
    except Exception as e:
        messagebox.showerror("Error", str(e))


# funciton to update the info and ui to user
def update_display():
    # here we clear display, from line 1 character 0 to the end so the order the user adds is correct
    order_display.delete(1.0, tk.END)

    # with this for loop we can build the order, with both its name and price
    for item in current_order.items:
        text = str(item[1]) + "x " + item[0] + " - $" + str(item[2]) + "\n"
        order_display.insert(tk.END, text)

    # here we can calculate the total price, if delivery, then calculate accordingly
    if isinstance(current_order, DeliveryOrder):
        total = current_order.calculate_total()
    else:
        total = sum(item[1] * item[2] for item in current_order.items)
        # we can show the updated total to the user
    total_label.config(text="Total: $" + "%.2f" % total)

    # function for saving the order to the file


def save_order():
    # validate inputs, make sure name and at least one item are inputted and selected
    if not name_entry.get():
        messagebox.showerror("Error", "Enter your name!")
        return
    if not current_order.items:
        messagebox.showerror("Error", "Add items first!")
        return
    # Write to the file, all info from user
    with open("order.txt", "w") as f:
        f.write("Name: " + name_entry.get() + "\n")
        f.write("Date: " + str(datetime.date.today()) + "\n")
        f.write("Delivery: " + ("Yes" if delivery_var.get() else "No") + "\n")
        f.write("Items:\n")
        # write all items in file
        for item in current_order.items:
            line = (
                "- " + item[0] + ": " + str(item[1]) + "x $" + "%.2f" % item[2] + "\n"
            )
            f.write(line)
        f.write(total_label.cget("text"))
    # show message to user saying their order has been placed
    messagebox.showinfo("Saved", "Order saved!")


# function to change between order type
def toggle_delivery():
    global current_order
    # save items when changing order type
    items = current_order.items

    # change the order type depending on whats selected
    if delivery_var.get():
        current_order = DeliveryOrder()
    else:
        current_order = Order()
    # make sure the current items are actually the ones the user selected
    current_order.items = items
    # update the display with the new info
    update_display()


# create the ui window, and title
root = tk.Tk()
root.title("Pizza Order")

# label for the name
tk.Label(root, text="Customer Name:").pack()

# name imput for the user
name_entry = tk.Entry(root)
name_entry.pack()

# calendar for picking the date
cal = Calendar(root)
cal.pack()

# list of the menu items shown with the listbox
menu_listbox = tk.Listbox(root, height=4)
for item in ["Cheese Pizza", "Pepperoni Pizza", "Salad", "Soda"]:
    menu_listbox.insert(tk.END, item)
menu_listbox.pack()

# add a button for user to add seleted menu items to their order
tk.Button(root, text="Add to Order", command=add_item).pack()

# show the order selected by the user
order_display = tk.Text(root, height=5, width=40)
order_display.pack()

# checkbox for the delivery
delivery_var = tk.BooleanVar()
ttk.Checkbutton(
    root, text="Delivery (+$4.99)", variable=delivery_var, command=toggle_delivery
).pack()

# label to show total to the user
total_label = tk.Label(root, text="Total: $0.00")
total_label.pack()
tk.Button(root, text="Save Order", command=save_order).pack()

# initalizing the current order of the user
current_order = Order()

# starting the UI
root.mainloop()
