# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 17:47:36 2021

@author: Jessica Bidon
"""

import tkinter as tk
import math as m


# create frame
root = tk.Tk()
root.title("Simple Calculator")


# create entry box
e = tk.Entry(root, width=35, borderwidth=5)
# columnspan=x makes the entry box the width of x columns
e.grid(row=0, column=0, columnspan=4)

BUTTON_WIDTH = 10

clear_flag = False
current_num = 0
math = ""

# button/click functions
def button_click(number):
    global clear_flag
    if clear_flag:
        button_clear_entry()
        clear_flag = False
    current = e.get()
    button_clear_entry()
    e.insert(0, current + number)
   
def display_current():
    global clear_flag
    button_clear_entry()
    e.insert(0, current_num)
    clear_flag = True
   
def button_c():
    global current_num
    current_num = 0
    button_clear_entry()
   
def button_clear_entry():
    e.delete(0, tk.END)
   
def button_equals():
    global math
    global current_num
    second_num = float(e.get())
    button_clear_entry()
    if math == "addition":
        e.insert(0, float(current_num) + second_num)
    elif math == "subtraction":
        e.insert(0, float(current_num) - second_num)
    elif math == "multiplication":
        e.insert(0, float(current_num) * second_num)
    elif math == "division":
        e.insert(0, float(current_num) / second_num)
    elif math == "apercent":
        e.insert(0, float(current_num) + (float(current_num) * (second_num)/100))
    elif math == "spercent":
        e.insert(0, float(current_num) - (float(current_num) * (second_num)/100))
    elif math == "exponent":
        e.insert(0, float(current_num) ** second_num)
    else:
        current_num = second_num
    math = ""

def button_add():
    global current_num
    global math
    if math != "":
        button_equals()    
    math = "addition"
    current_num = float(e.get())
    display_current()
   
def button_subtract():
    global current_num
    global math
    if math != "":
        button_equals()
    math = "subtraction"
    current_num = float(e.get())
    display_current()

def button_multiply():
    global current_num
    global math
    if math != "":
        button_equals()
    math = "multiplication"
    current_num = float(e.get())
    display_current()
   
def button_divide():
    global current_num
    global math
    if math != "":
        button_equals()
    math = "division"
    current_num = float(e.get())
    display_current()
   
# current bugs: only works when used with + and -    
def button_percent():
    global current_num
    global math
    if math == "addition":
        math = "apercent"    
        button_equals()
        current_num = float(e.get())
    elif math == "subtraction":
        math = "spercent"
        button_equals()
        current_num = float(e.get())
    else:
        current_num = 0
    display_current()
   
# current bugs: can still backspace on resulting value
def button_back():
    current = e.get()[:-1]
    button_clear_entry()
    e.insert(0, current)
   
def button_mult_inv():
    current = float(e.get())
    current = 1 / current
    button_clear_entry()
    e.insert(0, current)

def button_power():
    global current_num
    global math
    if math != "":
        button_equals()
    math = "exponent"
    current_num = float(e.get())
    display_current()
   
def button_root():
    current = float(e.get())
    current = m.sqrt(current)
    button_clear_entry()
    e.insert(0, current)
   
def button_pos_neg():
    current = float(e.get())
    current = current - (2 * current)
    button_clear_entry()
    e.insert(0, current)
   

# create number buttons
buttons = []

for i in range(10):
    # usually we can't pass arguments into method used in command,
    # so instead we need to use a lambda function to pass the value of button into button_click()
    # if we weren't in a for loop, we could say lambda: button_click(str(i)),
    # but lambda functions are wonky in for loops so you must bind lambda to i
    buttons.append(tk.Button(root, text=str(i), width=BUTTON_WIDTH, pady=20, command=lambda i=i: button_click(str(i))))

# create function buttons
percent_button = tk.Button(root, text="%", width=BUTTON_WIDTH, pady=20, command=button_percent)
ce_button = tk.Button(root, text="CE", width=BUTTON_WIDTH, pady=20, command=button_clear_entry)
c_button = tk.Button(root, text="C", width=BUTTON_WIDTH, pady=20, command=button_c)
back_button = tk.Button(root, text="<--", width=BUTTON_WIDTH, pady=20, command=button_back)
multiplicative_inverse_button = tk.Button(root, text="1/x", width=BUTTON_WIDTH, pady=20, command=button_mult_inv)
power_button = tk.Button(root, text="^", width=BUTTON_WIDTH, pady=20, command=button_power)
root_button = tk.Button(root, text="sqrt", width=BUTTON_WIDTH, pady=20, command=button_root)
divide_button = tk.Button(root, text="/", width=BUTTON_WIDTH, pady=20, command=button_divide)
multiply_button = tk.Button(root, text="x", width=BUTTON_WIDTH, pady=20, command=button_multiply)
subtract_button = tk.Button(root, text="-", width=BUTTON_WIDTH, pady=20, command=button_subtract)
add_button = tk.Button(root, text="+", width=BUTTON_WIDTH, pady=20, command=button_add)
pos_neg_button = tk.Button(root, text="+/-", width=BUTTON_WIDTH, pady=20, command=button_pos_neg)
decimal_button = tk.Button(root, text=".", width=BUTTON_WIDTH, pady=20, command=lambda i=i: button_click("."))
equal_button = tk.Button(root, text="=", width=BUTTON_WIDTH, pady=20, command=button_equals)

# add buttons to calculator
percent_button.grid(row=1, column=0)
ce_button.grid(row=1, column=1)
c_button.grid(row=1, column=2)
back_button.grid(row=1, column=3)
multiplicative_inverse_button.grid(row=2, column=0)
power_button.grid(row=2, column=1)
root_button.grid(row=2, column=2)
divide_button.grid(row=2, column=3)
multiply_button.grid(row=3, column=3)
subtract_button.grid(row=4, column=3)
add_button.grid(row=5, column=3)
pos_neg_button.grid(row=6, column=0)
decimal_button.grid(row=6, column=2)
equal_button.grid(row=6, column=3)
buttons[7].grid(row=3, column=0)
buttons[8].grid(row=3, column=1)
buttons[9].grid(row=3, column=2)
buttons[4].grid(row=4, column=0)
buttons[5].grid(row=4, column=1)
buttons[6].grid(row=4, column=2)
buttons[1].grid(row=5, column=0)
buttons[2].grid(row=5, column=1)
buttons[3].grid(row=5, column=2)
buttons[0].grid(row=6, column=1)

root.mainloop()
