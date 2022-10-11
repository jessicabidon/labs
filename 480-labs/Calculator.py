# -*- coding: utf-8 -*-
"""
Updated on Tues Oct 11 11:16:32 2022

@author: Jessica Bidon
"""

import tkinter as tk
import math as m

class Operator:
    
    def __init__(self, symbol, priority, is_unary, output_string, button_string, func):
        self.symbol = symbol
        self.priority = priority
        self.is_unary = is_unary
        self.output_str = output_string
        self.button_str = button_string
        self.func = func

class Stack:
    
    # Constructor
    def __init__(self):
        self.top = -1
        self.array = []
        
    # check if stack is empty
    def isEmpty(self):
        return True if self.top == -1 else False
    
    # return top of stack
    def peek(self):
        return self.array[-1]
    
    # pop top of stack (returns ? if empty)
    def pop(self):
        if not self.isEmpty():
            self.top -= 1
            return self.array.pop()
        else:
            return "?"
        
    # push element to stack
    def push(self, element):
        self.top += 1
        self.array.append(element)
        
    # modify top element of stack
    # add element if empty
    def modify(self, element):
        if self.isEmpty():
            self.push(element)
        else:
            self.array[-1] = element
        
class Evaluate:
    
    # operator attributes:   symbol, priority, is_unary, output_string, button_string, and func (function to execute)
    operators = {'+': Operator('+',     1,      False,      '+',            '+',        lambda x, y: x + y),
                 '-': Operator('-',     1,      False,      '-',            '-',        lambda x, y: x - y),
                 '*': Operator('*',     2,      False,      '*',            'x',        lambda x, y: x * y), # TODO: change to unicode multiply
                 '/': Operator('/',     2,      False,      '/',            '/',        lambda x, y: x / y), # TODO: change to unicode divide
                 '~': Operator('~',     2,      True,       '-',            '(-)',      lambda x: x * -1),
                 '^': Operator('^',     3,      False,      '^',            '^',        lambda x, y: x ** y), 
                 's': Operator('s',     4,      True,       'SIN(',         'SIN',      lambda x: m.sin(x)),
                 'c': Operator('c',     4,      True,       'COS(',         'COS',      lambda x: m.cos(x)),
                 't': Operator('t',     4,      True,       'TAN(',         'TAN',      lambda x: m.tan(x)),
                 'l': Operator('l',     4,      True,       'LOG(',         'LOG',      lambda x: m.log10(x)),
                 'n': Operator('n',     4,      True,       'LN(',          'LN',       lambda x: m.log(x)), 
                 '.': Operator('.',     4,      True,       '.',            '.',        lambda x: x),
                 '(': Operator('(',     4,      False,      '(',            '(',        lambda x: x), # use for infix only
                 ')': Operator(')',     4,      False,      ')',            ')',        lambda x: x) # use for infix only# use for infix only
                } 
    
    # TODO converts an expression from infix to postfix
    @classmethod
    def convert_to_postfix(cls, infix_expression: str) -> Stack:
        
        # keeps track of the operators before pushing to postfix
        operator_stack = Stack()
        
        # will be the final postfix representation
        postfix_stack = Stack()
        
        # use to get a full number before pushing to postfix
        current_number = ''
        decimal = False
        
        for symbol in infix_expression:
           
            # operands go straight to postfix, 
            # but we have to get the full number first
            if symbol.isdigit():
                current_number += symbol
            
            # append decimal to number, unless there is already a decimal somehow 
            elif symbol == '.':
                if decimal: 
                    # TODO: throw error
                    print("there are two decimals in this number!")
                    continue
                current_number += '.'
                decimal = True
            
            # check if its a valid operator
            elif symbol not in cls.operators:
                # TODO: throw error
                print("invalid operator: infix conversion")
                  
            # it's definitely an operator          
            else: 
                
                # first, clear current_number and add full number to postfix_stack
                if current_number:
                    postfix_stack.push(float(current_number))
                    current_number = ''
                    decimal = False
                
                # if the symbol is a close parentheses, pop from operator_stack
                #  and push to postfix_stack until we reach a (, s, t, c, or l (priority 4)
                if symbol == ')':
                    while (cls.operators[operator_stack.peek()].priority < 4):
                        postfix_stack.push(operator_stack.pop())
                    # if the new top element of operator_stack is parentheses, discard
                    if operator_stack.peek() == '(':
                        operator_stack.pop()
                    # otherwise, the new top element of operator_stack is a trig/log function,
                    # pop and push to postfix_stack
                    else: 
                        postfix_stack.push(operator_stack.pop())
                
                # if top of operator stack is (, s, c, t, or l, just ignore priority and push operator to stack
                elif (not operator_stack.isEmpty() and cls.operators[operator_stack.peek()].priority == 4):
                    operator_stack.push(symbol)
                                        
                else: 
                    # if this symbol's priority is less than/equal the priority
                    #  of the top operator on the stack, pop from operator_stack    
                    #  and push to postfix_stack until the symbol priority is greater than top element
                    while (not operator_stack.isEmpty() and cls.operators[symbol].priority <= cls.operators[operator_stack.peek()].priority):
                        # stop popping if we hit a (, s, t, c, or l
                        if cls.operators[operator_stack.peek()].priority == 4:
                            break
                        postfix_stack.push(operator_stack.pop())
                    
                    # then push operator to stack
                    operator_stack.push(symbol)           
                             
        # end for loop: each symbol in infix expression
        
        # if there is something in current_number, push to postfix_stack
        if current_number:
            postfix_stack.push(float(current_number))
        
        # if there are remaining elements in the operator_stack,
        #  pop and push to postfix_stack until empty
        while (not operator_stack.isEmpty()):
            postfix_stack.push(operator_stack.pop())               
        
        return postfix_stack
    
    # evaluates a postfix expression
    @classmethod
    def evaluate(cls, postfix_expression: Stack) -> float:
        
        # temporary stack to keep track of operands during evaluation
        operand_stack = Stack()
            
        for symbol in postfix_expression.array:
            
            # if digit, push to stack
            if type(symbol) == int or type(symbol) == float:
                operand_stack.push(symbol)
                               
            # check if its a valid operator
            elif symbol not in cls.operators:
                # TODO: throw error
                print("invalid operator: postfix evaluation")
                            
            # handle parentheses (this shouldn't happen)
            elif symbol == '(' or symbol == ')':
                # do nothing: there may be extra parentheses if closing parentheses are missing
                continue
                            
            # handle unary operators
            elif cls.operators[symbol].is_unary:
                # pop the sole operand
                sole_operand = operand_stack.pop()
                # apply funciton assigned to that operator
                result = cls.operators[symbol].func(sole_operand)
                # push result back to operand stack
                operand_stack.push(result)
            
            # handle binary operators
            else:
                # pop two operands
                second_operand = operand_stack.pop()
                first_operand = operand_stack.pop()
                # apply function assigned to that operator
                result = cls.operators[symbol].func(first_operand, second_operand)
                # push result back to operand stack
                operand_stack.push(result)
                
        # the result should be the one remaining element of this stack
        if operand_stack.top != 0:
            # TODO: throw error
            print("postfix evaluation exception: operands remaining")
            
        return operand_stack.pop()

    # gets the string representation of an infix expression
    @classmethod
    def to_string(cls, infix_expression: str):
        
        result = ''
        
        for symbol in infix_expression:
            
            if symbol in cls.operators:
                result += cls.operators[symbol].output_str
            
            else:
                result += symbol

        return result


# string = "~5.78+~(4-2.23)+s0)*c1)/(1+t2*n~3+2*(1.23+99.111"
# string1 = "1+s~3+8*l9/6)-(6+9/2))"
# stack = Evaluate.convert_to_postfix(string)
# print(stack.array)
# print(Evaluate.to_string(string))
# print(Evaluate.evaluate(stack))

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
