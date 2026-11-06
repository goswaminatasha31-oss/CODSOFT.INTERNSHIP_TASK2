
from tkinter import Tk

from calculator_logic import safe_calculate
from ui import CalculatorUI


# This function connects the interface to the calculation logic
def calculate_expression(expression):
    return safe_calculate(expression)


# Create the main application window
root = Tk()

app = CalculatorUI(root, calculate_expression)
root.mainloop()