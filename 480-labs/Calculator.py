# -*- coding: utf-8 -*-
"""
Updated on Tues Oct 13 12:51:10 2022

@author: Jessica Bidon
"""

"""
    Known Bugs: 
        - entry box doesn't side scroll as the input exceeds size of frame
        - if result is too big, it might extend beyond frame
        
    Possible Features: 
        - icons instead of text for button labels
        - New operators: 
            - square root
            - multiplicative inverse
            - percent
        - Better design
            - colors!
            - rounded buttons
            
    Software Design Improvements:
        - separate operator_command into multiple methods to handle outliers
            - close_paren_command
            - negation_command
            - decimal_command
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

# operator attributes:   symbol, priority, is_unary, output_string, button_string, and func (function to execute)
operators = {'+': Operator('+',     1,      False,      '+',            '+',        lambda x, y: x + y),
             '-': Operator('-',     1,      False,      '-',            '-',        lambda x, y: x - y),
             '*': Operator('*',     2,      False,      '*',            'x',        lambda x, y: x * y), # TODO: change to unicode multiply
             '/': Operator('/',     2,      False,      '/',            '/',        lambda x, y: x / y), # TODO: change to unicode divide
             '^': Operator('^',     3,      False,      '^',            '^',        lambda x, y: x ** y), 
             '~': Operator('~',     4,      True,       '-',            '(-)',      lambda x: x * -1),
             's': Operator('s',     4,      True,       'SIN(',         'SIN',      lambda x: m.sin(x)),
             'c': Operator('c',     4,      True,       'COS(',         'COS',      lambda x: m.cos(x)),
             't': Operator('t',     4,      True,       'TAN(',         'TAN',      lambda x: m.tan(x)),
             'l': Operator('l',     4,      True,       'LOG(',         'LOG',      lambda x: m.log10(x)),
             'n': Operator('n',     4,      True,       'LN(',          'LN',       lambda x: m.log(x)), 
             '(': Operator('(',     4,      True,       '(',            '(',        lambda x: x), # use for infix only
             ')': Operator(')',     4,      True,       ')',            ')',        lambda x: x), # use for infix only
             '.': Operator('.',     5,      True,       '.',            '.',        lambda x: x), # use for infix only
             'i': Operator('i',     5,      True,       '^-1',          '1/x',      lambda x: x), # not yet implemented
             'q': Operator('q',     5,      True,       'sqrt(',        'sqrt',     lambda x: x)  # not yet implemented
            }

class Evaluate:
    
    # converts a string infix expression to a postfix stack
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
            
            # append decimal to number
            elif symbol == '.':
                if decimal: 
                    raise Exception("Error: two decimals in this number!")
                    continue
                current_number += '.'
                decimal = True
            
            # check if its a valid operator
            elif symbol not in operators:
                # TODO: throw error
                raise Exception("invalid operator: infix conversion")
                  
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
                raise Exception("invalid operator: postfix evaluation")
                            
            # handle parentheses (this shouldn't happen)
            elif symbol == '(' or symbol == ')':
                # do nothing: there may be extra parentheses if closing parentheses are missing
                continue
                            
            # handle unary operators
            elif operators[symbol].is_unary:
                
                # pop the sole operand
                sole_operand = operand_stack.pop()
                
                # don't allow log or square root of negative
                if sole_operand < 0 and symbol in ('l', 'q'):
                    return f"Domain Error: {operators[symbol].button_str}"
                
                # apply funciton assigned to that operator
                result = operators[symbol].func(sole_operand)
                
                # push result back to operand stack
                operand_stack.push(result)
            
            # handle binary operators
            else:
                
                # pop two operands
                second_operand = operand_stack.pop()
                first_operand = operand_stack.pop()
                
                # don't allow divide by zero
                if symbol == '/' and second_operand == 0:
                    return "Error: Div by 0"
                
                # apply function assigned to that operator
                result = operators[symbol].func(first_operand, second_operand)
                
                # push result back to operand stack
                operand_stack.push(result)
                
        # the result should be the one remaining element of this stack
        if operand_stack.top != 0:
            # TODO: throw error
            raise Exception("postfix evaluation exception: operands remaining")
            
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

    def __init__(self):
            
        self.font = 'Arial '
        self.terminal_fontsize = '20'
        self.button_fontsize = '16'
        
        self.expression = ''
        self.output_string = ''
        self.is_result = False
        
        self.buttons = []
        
        # create frame
        self.root = tk.Tk()
        self.root.title("Calculator")
        self.root.geometry("400x500")
        
        # configure grid for dynamic resizing
        for i in range(7):
            tk.Grid.rowconfigure(self.root, i, weight=1)
        for i in range(5):
            tk.Grid.columnconfigure(self.root, i, weight=1)
        
        # create terminal entry (disabled for typing)
        self.terminal = tk.Entry(self.root, borderwidth=5, font=self.font + self.terminal_fontsize, state='disabled')
        self.terminal.grid(row=0, column=0, columnspan=5, sticky='nesw')
        
        # create the gui
        self.create_gui()

        # bind resize function to window resizing
        self.root.bind('<Configure>', self.resize_text)
        
        # main loop
        self.root.mainloop()
        
    def create_gui(self):
        
        # create number buttons and add to grid
        self.create_number_buttons()
        
        # create operator buttons and add to grid
        self.create_operator_buttons()
        
        # create utitilty buttons (enter, clear, etc) and add to grid
        self.create_utility_buttons()
        
        # update all button fonts
        for button in self.buttons:
            button.config(font = self.font + self.button_fontsize)
        
    def create_number_buttons(self):
        
        # create number buttons
        for i in range(10):
            self.buttons.append(tk.Button(self.root, text=str(i), command=lambda i=i: self.number_command(str(i))))
            
        # add number buttons to grid
        self.buttons[7].grid(row=3, column=1, sticky='nesw')
        self.buttons[8].grid(row=3, column=2, sticky='nesw')
        self.buttons[9].grid(row=3, column=3, sticky='nesw')
        self.buttons[4].grid(row=4, column=1, sticky='nesw')
        self.buttons[5].grid(row=4, column=2, sticky='nesw')
        self.buttons[6].grid(row=4, column=3, sticky='nesw')
        self.buttons[1].grid(row=5, column=1, sticky='nesw')
        self.buttons[2].grid(row=5, column=2, sticky='nesw')
        self.buttons[3].grid(row=5, column=3, sticky='nesw')
        self.buttons[0].grid(row=6, column=1, sticky='nesw')
        
    def create_operator_buttons(self):
        
        # decimal "."
        decimal_button = tk.Button(self.root, text=operators["."].button_str, command=lambda: self.operator_command("."))
        decimal_button.grid(row=6, column=2, sticky='nesw')
        self.buttons.append(decimal_button)
        
        # negation "~"
        negation_button = tk.Button(self.root, text=operators['~'].button_str, command=lambda: self.operator_command('~'))
        negation_button.grid(row=6, column=3, sticky='nesw')
        self.buttons.append(negation_button)
        
        # divide "/"
        divide_button = tk.Button(self.root, text=operators['/'].button_str, command=lambda: self.operator_command('/'))
        divide_button.grid(row=2, column=1, sticky='nesw')
        self.buttons.append(divide_button)
        
        # multiply "*"
        multiply_button = tk.Button(self.root, text=operators['*'].button_str, command=lambda: self.operator_command('*'))
        multiply_button.grid(row=2, column=2, sticky='nesw')
        self.buttons.append(multiply_button)
        
        # addition "+"
        addition_button = tk.Button(self.root, text=operators['+'].button_str, command=lambda: self.operator_command('+'))
        addition_button.grid(row=2, column=3, sticky='nesw')
        self.buttons.append(addition_button)
        
        # subtraction "-"
        subtraction_button = tk.Button(self.root, text=operators['-'].button_str, command=lambda: self.operator_command('-'))
        subtraction_button.grid(row=2, column=4, sticky='nesw')
        self.buttons.append(subtraction_button)
        
        # natural log "n"
        natural_log_button = tk.Button(self.root, text=operators['n'].button_str, command=lambda: self.operator_command('n'))
        natural_log_button.grid(row=6, column=0, sticky='nesw')
        self.buttons.append(natural_log_button)
        
        # base-10 log "l"
        log10_button = tk.Button(self.root, text=operators['l'].button_str, command=lambda: self.operator_command('l'))
        log10_button.grid(row=5, column=0, sticky='nesw')
        self.buttons.append(log10_button)
        
        # sin "s"
        sin_button = tk.Button(self.root, text=operators['s'].button_str, command=lambda: self.operator_command('s'))
        sin_button.grid(row=4, column=0, sticky='nesw')
        self.buttons.append(sin_button)
        
        # cos "c"
        cos_button = tk.Button(self.root, text=operators['c'].button_str, command=lambda: self.operator_command('c'))
        cos_button.grid(row=3, column=0, sticky='nesw')
        self.buttons.append(cos_button)
        
        # tan "t"
        tan_button = tk.Button(self.root, text=operators['t'].button_str, command=lambda: self.operator_command('t'))
        tan_button.grid(row=2, column=0, sticky='nesw')
        self.buttons.append(tan_button)
        
        # exponent "^"
        exponent_button = tk.Button(self.root, text=operators['^'].button_str, command=lambda: self.operator_command('^'))
        exponent_button.grid(row=1, column=2, sticky='nesw')
        self.buttons.append(exponent_button)
        
        # open parentheses "("
        open_paren_button = tk.Button(self.root, text=operators['('].button_str, command=lambda: self.operator_command('('))
        open_paren_button.grid(row=1, column=3, sticky='nesw')
        self.buttons.append(open_paren_button)
        
        # close parentheses ")"
        close_paren_button = tk.Button(self.root, text=operators[')'].button_str, command=lambda: self.operator_command(')'))
        close_paren_button.grid(row=1, column=4, sticky='nesw')
        self.buttons.append(close_paren_button)
        
        # square root 'q'
        square_root_button = tk.Button(self.root, text=operators['q'].button_str, command=None)
        square_root_button.grid(row=1, column=0, sticky='nesw')
        square_root_button["state"] = tk.DISABLED
        self.buttons.append(square_root_button)
        
        # multiplicative inverse
        mult_inverse_button = tk.Button(self.root, text=operators['i'].button_str, command=None)
        mult_inverse_button.grid(row=1, column=1, sticky='nesw')
        mult_inverse_button["state"] = tk.DISABLED
        self.buttons.append(mult_inverse_button)
        
    def create_utility_buttons(self):
        
        # enter button
        enter_button = tk.Button(self.root, text='-->', command=lambda: self.enter_command())
        enter_button.grid(row=5, column=4, rowspan=2, sticky='nesw')
        self.buttons.append(enter_button)
                
        # clear button
        clear_button = tk.Button(self.root, text='clr', command=lambda: self.clear_command())
        clear_button.grid(row=4, column=4, sticky='nesw')
        self.buttons.append(clear_button)
                
        # back button
        back_button = tk.Button(self.root, text='<--', command=lambda: self.back_command())
        back_button.grid(row=3, column=4, sticky='nesw')
        self.buttons.append(back_button)
    
    # button commands
    def number_command(self, symbol):
        
        # if it's a result, don't add another digit to it
        # instead, clear and replace the result
        if self.is_result:
            self.is_result = False
            self.clear_command()
        
        # update expression and output strings
        self.expression += symbol
        symbol_as_output = Evaluate.to_string(symbol)
        self.output_string += symbol_as_output
        
        # update terminal with new symbol
        self.terminal.config(state='normal')
        self.terminal.insert('end', symbol_as_output)
        self.terminal.config(state='disabled')
            
    def operator_command(self, symbol):
        
        # if it's a result, that's fine, we can add an operator
        if self.is_result:
            self.is_result = False
                
        # if terminal is clear, don't allow binary operators, ')', or '.'
        if not self.expression:
            if symbol in (')', '.') or not operators[symbol].is_unary:
                return
        
        # handle close parentheses
        elif symbol == ')':
            # don't allow placement after operators (unless its ')')
            if self.expression[-1] != ')' and self.expression[-1] in operators:
                return
            
            # count open parentheses/trig/log functions
            open_paren_count = 0
            for char in self.expression:
                if char == ')': 
                    open_paren_count -= 1 # decrement for every closed
                elif char in operators and operators[char].priority == 4:
                    open_paren_count += 1 # increment for every open, trig/log
            
            # if there are no open parentheses, don't allow placement of )
            if open_paren_count <= 0:
                return
        
        # if priority 4 operators (parentheses and trig/log) 
        # follow an operand or '.', add a multiply first
        # (exclude close parentheses)
        elif symbol in operators and operators[symbol].priority == 4:
            if self.expression and (self.expression[-1].isdigit() or self.expression[-1] == '.'):
                symbol = '*' + symbol
        
        # negation operator cannot follow an operand
        elif symbol == '~':
            if self.expression[-1].isdigit():
                return
        
        # decimal must follow an operand, 
        # and if multiple, must be separated by operators
        elif symbol == '.':
            if not self.expression[-1].isdigit():
                return
            # check if last occurrence of decimal has been followed by operator
            last_decimal_index = self.expression.rfind('.')
            if last_decimal_index > 0:            
                operator_exists = False
                for char in self.expression[last_decimal_index+1:]:
                    if char in operators:
                        operator_exists = True
                if not operator_exists:
                    return          
        
        # all other operators cannot follow another operator (unless it's ')')
        elif symbol in operators and operators[symbol].priority < 4:
            if self.expression and not (self.expression[-1].isdigit() or self.expression[-1] == ')'):
                return
                
        # update expression and output strings
        self.expression += symbol
        symbol_as_output = Evaluate.to_string(symbol)
        self.output_string += symbol_as_output
        
        self.terminal.config(state='normal') 
        self.terminal.insert('end', symbol_as_output)
        self.terminal.config(state='disabled') # re-disable input for typing
        
    def enter_command(self):
        
        if not self.terminal.get(): # enter only if non-empty
            return 
        
        # make sure it ends with an operand (any ')' excluded)
        for char in reversed(self.expression):
            if char == ')':
                continue
            if char.isdigit() or char == '.':
                break
            else:
                # do nothing, need another operand
                return
        
        # this is a result (cannot be followed by backspace or operand)
        self.is_result = True
        
        # evaluate 
        postfix = Evaluate.convert_to_postfix(self.expression)
        result = Evaluate.evaluate(postfix)
        
        # if no error is passed, update expression and output strings
        if type(result) != str:
            
            # if negative, convert - to ~
            if result < 0:
                self.expression = "~" + str(result)[1:]
            else:
                self.expression = str(result)
            self.output_string = Evaluate.to_string(self.expression)
        
        else: # error has been passed
            self.output_string = result
            self.expression = ''
        
        # update terminal
        self.terminal.config(state='normal')
        self.terminal.delete(0, "end")
        self.terminal.insert(0, self.output_string)
        self.terminal.config(state='disabled')
        
    def clear_command(self):
        
        # if it was a result, it's not anymore
        if self.is_result:
            self.is_result = False
        
        # update expression and output strings
        self.expression = ''
        self.output_string = ''
        
        # update terminal
        self.terminal.config(state='normal')
        self.terminal.delete(0, "end")
        self.terminal.config(state='disabled')
        
    def back_command(self):
        
        # if expression is empty, do nothing
        if not self.expression:
            return
        
        # if expression is a result, just clear everything
        if self.is_result:
            self.clear_command()
            return
        
        # get last symbol from expression
        op_to_remove = self.expression[-1]
        
        # get the length of the output string for that symbol
        # (so we can remove the correct number of characters)
        if op_to_remove.isdigit():
            output_length = 1
        elif op_to_remove not in operators:
            # TODO: throw error
            raise Exception("how are you going to backspace an invalid operator?")
        else:
            output_length = len(operators[op_to_remove].output_str)
        
        # negate so we can get last x elements
        output_indices = output_length * -1
        
        # update expression and output strings
        self.expression = self.expression[:-1]
        self.output_string = self.output_string[:output_indices]
        
        # update terminal with new output string
        self.terminal.config(state='normal')
        self.terminal.delete(0, "end")
        self.terminal.insert(0, self.output_string)
        self.terminal.config(state='disabled')
        
    def resize_text(self, window):
        
        # size constraint is the smaller of width and height        
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        size = width if width < height else height
        
        # resize terminal font size according to width/height
        self.terminal_fontsize = str(size // 20)
        self.terminal.config(font = self.font + self.terminal_fontsize)
        
        # resize button font size according to width/height
        self.button_fontsize = str(size // 25)
        for button in self.buttons:
            button.config(font= self.font + self.button_fontsize)

def main():
    GUI() 

if __name__ == '__main__':
    main()
