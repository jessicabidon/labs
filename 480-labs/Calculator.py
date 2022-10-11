# -*- coding: utf-8 -*-
"""
Updated on Tues Oct 11 1:17:20 2022

@author: Jessica Bidon
"""

"""
    Priority Fixes:
        - create methods for utitilty buttons:
            - clear
            - back
        - disable buttons depending on value of last symbol added
            - ex. parentheses only following an operator of priority 3 or lower
            - operators only after operands
        - disable window resizing (until we add dynamic resizing) 
        - entry box doesn't side scroll as the input exceeds size of frame
        
    Possible Features: 
        - dynamic resizing
        - icons instead of text for button labels
        - New operators: 
            - square root
            - multiplicative inverse
            - percent
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
             '.': Operator('.',     4,      True,       '.',            '.',        lambda x: x), # use for infix only
             '(': Operator('(',     4,      False,      '(',            '(',        lambda x: x), # use for infix only
             ')': Operator(')',     4,      False,      ')',            ')',        lambda x: x) # use for infix only
            }

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
                 '.': Operator('.',     4,      True,       '.',            '.',        lambda x: x), # use for infix only
                 '(': Operator('(',     4,      False,      '(',            '(',        lambda x: x), # use for infix only
                 ')': Operator(')',     4,      False,      ')',            ')',        lambda x: x) # use for infix only
                } 
    
    # TODO converts an expression from infix to postfix
    @staticmethod
    def convert_to_postfix(infix_expression: str) -> Stack:
        
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
            elif symbol not in operators:
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
                    while (operators[operator_stack.peek()].priority < 4):
                        postfix_stack.push(operator_stack.pop())
                    # if the new top element of operator_stack is parentheses, discard
                    if operator_stack.peek() == '(':
                        operator_stack.pop()
                    # otherwise, the new top element of operator_stack is a trig/log function,
                    # pop and push to postfix_stack
                    else: 
                        postfix_stack.push(operator_stack.pop())
                
                # if top of operator stack is (, s, c, t, or l, just ignore priority and push operator to stack
                elif (not operator_stack.isEmpty() and operators[operator_stack.peek()].priority == 4):
                    operator_stack.push(symbol)
                                        
                else: 
                    # if this symbol's priority is less than/equal the priority
                    #  of the top operator on the stack, pop from operator_stack    
                    #  and push to postfix_stack until the symbol priority is greater than top element
                    while (not operator_stack.isEmpty() and operators[symbol].priority <= operators[operator_stack.peek()].priority):
                        # stop popping if we hit a (, s, t, c, or l
                        if operators[operator_stack.peek()].priority == 4:
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
    @staticmethod
    def evaluate(postfix_expression: Stack) -> float:
        
        # temporary stack to keep track of operands during evaluation
        operand_stack = Stack()
            
        for symbol in postfix_expression.array:
            
            # if digit, push to stack
            if type(symbol) == int or type(symbol) == float:
                operand_stack.push(symbol)
                               
            # check if its a valid operator
            elif symbol not in operators:
                # TODO: throw error
                print("invalid operator: postfix evaluation")
                            
            # handle parentheses (this shouldn't happen)
            elif symbol == '(' or symbol == ')':
                # do nothing: there may be extra parentheses if closing parentheses are missing
                continue
                            
            # handle unary operators
            elif operators[symbol].is_unary:
                # pop the sole operand
                sole_operand = operand_stack.pop()
                # apply funciton assigned to that operator
                result = operators[symbol].func(sole_operand)
                # push result back to operand stack
                operand_stack.push(result)
            
            # handle binary operators
            else:
                # pop two operands
                second_operand = operand_stack.pop()
                first_operand = operand_stack.pop()
                # apply function assigned to that operator
                result = operators[symbol].func(first_operand, second_operand)
                # push result back to operand stack
                operand_stack.push(result)
                
        # the result should be the one remaining element of this stack
        if operand_stack.top != 0:
            # TODO: throw error
            print("postfix evaluation exception: operands remaining")
            
        result = operand_stack.pop()
        
        # return as an integer, if possible
        if result.is_integer():
            return int(result)
        else: 
            return result

    # gets the string representation of an infix expression
    @classmethod
    def to_string(cls, infix_expression: str):
        
        result = ''
        
        for symbol in infix_expression:
            
            if symbol in operators:
                result += operators[symbol].output_str
            
            else:
                result += symbol

        return result

class GUI():
        
    BUTTON_WIDTH = 10
    BUTTON_PADY = 20

    clear_flag = False # what is this for?
    current_num = 0 # what is this for?
    math = '' # what is this for?

    def __init__(self):
                
        self.expression = ''
        self.output_string = ''
        
        # create frame
        self.root = tk.Tk()
        self.root.title("Calculator")
        
        # create terminal entry (disabled for typing)
        self.terminal = tk.Entry(self.root, width=35, borderwidth=5, font=('Arial 14'), state='disabled')
        self.terminal.grid(row=0, column=0, columnspan=5)
        
        # create the gui
        self.create_gui()
        
        # main loop
        self.root.mainloop()
        
    def create_gui(self):
        
        # create number buttons and add to grid
        self.create_number_buttons()
        
        # create operator buttons and add to grid
        self.create_operator_buttons()
        
        # create utitilty buttons (enter, clear, etc) and add to grid
        self.create_utility_buttons()
        
    def create_number_buttons(self):
        
        buttons = []
        
        # create number buttons
        for i in range(10):
            buttons.append(tk.Button(self.root, text=str(i), width=self.BUTTON_WIDTH, pady=self.BUTTON_PADY, command=lambda i=i: self.button_click(str(i))))
            
        # add number buttons to grid
        buttons[7].grid(row=3, column=1)
        buttons[8].grid(row=3, column=2)
        buttons[9].grid(row=3, column=3)
        buttons[4].grid(row=4, column=1)
        buttons[5].grid(row=4, column=2)
        buttons[6].grid(row=4, column=3)
        buttons[1].grid(row=5, column=1)
        buttons[2].grid(row=5, column=2)
        buttons[3].grid(row=5, column=3)
        buttons[0].grid(row=6, column=1)
        
    def create_operator_buttons(self):
        
        # decimal "."
        decimal_button = tk.Button(self.root, text=operators["."].button_str, width=self.BUTTON_WIDTH, pady=self.BUTTON_PADY, command=lambda: self.button_click("."))
        decimal_button.grid(row=6, column=2)
        # negation "~"
        negation_button = tk.Button(self.root, text=operators['~'].button_str, width=self.BUTTON_WIDTH, pady=self.BUTTON_PADY, command=lambda: self.button_click('~'))
        negation_button.grid(row=6, column=3)
        # divide "/"
        divide_button = tk.Button(self.root, text=operators['/'].button_str, width=self.BUTTON_WIDTH, pady=self.BUTTON_PADY, command=lambda: self.button_click('/'))
        divide_button.grid(row=2, column=1)
        # multiply "*"
        multiply_button = tk.Button(self.root, text=operators['*'].button_str, width=self.BUTTON_WIDTH, pady=self.BUTTON_PADY, command=lambda: self.button_click('*'))
        multiply_button.grid(row=2, column=2)
        # addition "+"
        addition_button = tk.Button(self.root, text=operators['+'].button_str, width=self.BUTTON_WIDTH, pady=self.BUTTON_PADY, command=lambda: self.button_click('+'))
        addition_button.grid(row=2, column=3)
        # subtraction "-"
        subtraction_button = tk.Button(self.root, text=operators['-'].button_str, width=self.BUTTON_WIDTH, pady=self.BUTTON_PADY, command=lambda: self.button_click('-'))
        subtraction_button.grid(row=2, column=4)
        # natural log "n"
        natural_log_button = tk.Button(self.root, text=operators['n'].button_str, width=self.BUTTON_WIDTH, pady=self.BUTTON_PADY, command=lambda: self.button_click('n'))
        natural_log_button.grid(row=6, column=0)
        # base-10 log "l"
        log10_button = tk.Button(self.root, text=operators['l'].button_str, width=self.BUTTON_WIDTH, pady=self.BUTTON_PADY, command=lambda: self.button_click('l'))
        log10_button.grid(row=5, column=0)
        # sin "s"
        sin_button = tk.Button(self.root, text=operators['s'].button_str, width=self.BUTTON_WIDTH, pady=self.BUTTON_PADY, command=lambda: self.button_click('s'))
        sin_button.grid(row=4, column=0)
        # cos "c"
        cos_button = tk.Button(self.root, text=operators['c'].button_str, width=self.BUTTON_WIDTH, pady=self.BUTTON_PADY, command=lambda: self.button_click('c'))
        cos_button.grid(row=3, column=0)
        # tan "t"
        tan_button = tk.Button(self.root, text=operators['t'].button_str, width=self.BUTTON_WIDTH, pady=self.BUTTON_PADY, command=lambda: self.button_click('c'))
        tan_button.grid(row=2, column=0)
        # exponent "^"
        exponent_button = tk.Button(self.root, text=operators['^'].button_str, width=self.BUTTON_WIDTH, pady=self.BUTTON_PADY, command=lambda: self.button_click('^'))
        exponent_button.grid(row=1, column=2)
        # open parentheses "("
        open_paren_button = tk.Button(self.root, text=operators['('].button_str, width=self.BUTTON_WIDTH, pady=self.BUTTON_PADY, command=lambda: self.button_click('('))
        open_paren_button.grid(row=1, column=3)
        # close parentheses ")"
        close_paren_button = tk.Button(self.root, text=operators[')'].button_str, width=self.BUTTON_WIDTH, pady=self.BUTTON_PADY, command=lambda: self.button_click(')'))
        close_paren_button.grid(row=1, column=4)
   
    def create_utility_buttons(self):
        
        # enter button
        enter_button = tk.Button(self.root, text='-->', width=self.BUTTON_WIDTH, pady=self.BUTTON_PADY, command=lambda: self.enter_command())
        enter_button.grid(row=5, column=4, rowspan=2, sticky='ns')
    
    # button commands
    def button_click(self, symbol):
        
        self.expression += symbol
        symbol_as_output = Evaluate.to_string(symbol)
        self.output_string += symbol_as_output
        
        self.terminal.config(state='normal') 
        self.terminal.insert('end', symbol_as_output)
        self.terminal.config(state='disabled') # re-disable input for typing
        
    def enter_command(self):
        
        if self.terminal.get(): # enter only if non-empty
            postfix = Evaluate.convert_to_postfix(self.expression)
            result = Evaluate.evaluate(postfix)
            
            self.terminal.config(state='normal')
            self.terminal.delete(0, "end")
            self.terminal.insert(0, result)
            self.terminal.config(state='disabled')


def main():
    
    GUI() 
    
    """string = "~5.78+~(4-2.23)+s0)*c1)/(1+t2*n~3+2*(1.23+99.111"
    string1 = "1+s~3+8*l9/6)-(6+9/2))"
    stack = Evaluate.convert_to_postfix(string)
    print(stack.array)
    print(Evaluate.to_string(string))
    print(Evaluate.evaluate(stack))"""

if __name__ == '__main__':
    main()
