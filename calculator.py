
import tkinter as tk
import ast
import operator
# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Calculator")
root.geometry("390x650")
root.resizable(False, False)
root.configure(bg="#0C0D0F")
# ---------------- COLORS ----------------
BG = "#10131C"
PANEL = "#191E2B"
DISPLAY_BG = "#202738"
NUMBER = "#293246"
OPERATOR = "#343D59"
ACCENT = "#795BFF"
ACCENT_HOVER = "#917BFF"
DANGER = "#E65370"
TEXT = "#FFFFFF"
MUTED = "#8993AA"
expression = ""
last_result = ""
# ---------------- SAFE CALCULATION ----------------
def safe_calculate(expr):
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow
    }
    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant):
            if type(node.value) in (int, float):
                return node.value
            raise ValueError("Invalid input")
        if isinstance(node, ast.BinOp):
            op = type(node.op)
            if op not in allowed_operators:
                raise ValueError("Invalid operation")
            return allowed_operators[op](
                evaluate(node.left),
                evaluate(node.right)
            )
        if isinstance(node, ast.UnaryOp):
            value = evaluate(node.operand)
            if isinstance(node.op, ast.UAdd):
                return value
            if isinstance(node.op, ast.USub):
                return -value
        raise ValueError("Invalid expression")
    tree = ast.parse(expr, mode="eval")
    return evaluate(tree)
# ---------------- DISPLAY ----------------
header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=25, pady=(22, 10))
tk.Label(
    header,
    font=("times new roman", 18, "bold"),
    bg=BG,
    fg=ACCENT
).pack(side="left")
tk.Label(
    header,
    text="CALCULATOR",
    font=("times new roman", 9, "bold"),
    bg=BG,
    fg=MUTED
).pack(side="right", pady=7)
display_frame = tk.Frame(
    root,
    bg=DISPLAY_BG,
    padx=18,
    pady=20
)
display_frame.pack(fill="x", padx=20, pady=15)
history = tk.Label(
    display_frame,
    text="Ready to calculate",
    font=("times new roman", 10),
    bg=DISPLAY_BG,
    fg=MUTED,
    anchor="e"
)
history.pack(fill="x")
display = tk.Label(
    display_frame,
    text="0",
    font=("times new roman", 34, "bold"),
    bg=DISPLAY_BG,
    fg=TEXT,
    anchor="e"
)
display.pack(fill="x", pady=(12, 4))
# ---------------- FUNCTIONS ----------------
def update_display():
    display.config(text=expression if expression else "0")
def press(value):
    global expression
    if expression == "Error":
        expression = ""
    if value == "×":
        value = "*"
    elif value == "÷":
        value = "/"
    expression += value
    update_display()
def clear():
    global expression
    expression = ""
    history.config(text="Ready to calculate")
    update_display()
def delete():
    global expression
    if expression != "Error":
        expression = expression[:-1]
    else:
        expression = ""
    update_display()
def calculate():
    global expression, last_result
    if not expression:
        return
    try:
        result = safe_calculate(expression)
        if isinstance(result, float):
            result = round(result, 10)
            if result.is_integer():
                result = int(result)
        history.config(text=expression + " =")
        expression = str(result)
        last_result = expression
        update_display()
    except ZeroDivisionError:
        expression = "Error"
        history.config(text="Cannot divide by zero")
        update_display()
    except Exception:
        expression = "Error"
        history.config(text="Invalid calculation")
        update_display()
def percentage():
    global expression
    if not expression or expression == "Error":
        return
    try:
        result = float(expression) / 100
        expression = str(result)
        update_display()
        history.config(text="Percentage")
    except ValueError:
        history.config(text="Use % in expressions")
# ---------------- BUTTONS ----------------
button_frame = tk.Frame(root, bg=BG)
button_frame.pack(fill="both", expand=True, padx=18, pady=10)
buttons = [
    ["AC", "DEL", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["00", "0", ".", "="]
]
def button_action(value):
    if value == "AC":
        clear()
    elif value == "DEL":
        delete()
    elif value == "=":
        calculate()
    elif value == "%":
        percentage()
    else:
        press(value)
def on_enter(event):
    event.widget.config(bg=ACCENT_HOVER)
def on_leave(event):
    event.widget.config(bg=event.widget.default_color)
for r, row in enumerate(buttons):
    for c, value in enumerate(row):
        if value == "=":
            color = ACCENT
        elif value in ["+", "-", "×", "÷", "%"]:
            color = OPERATOR
        elif value in ["AC", "DEL"]:
            color = "#512C40"
        else:
            color = NUMBER
        btn = tk.Button(
            button_frame,
            text=value,
            font=("times new roman", 17, "bold"),
            bg=color,
            fg=TEXT,
            activebackground=ACCENT_HOVER,
            activeforeground=TEXT,
            bd=0,
            relief="flat",
            cursor="hand2",
            command=lambda v=value: button_action(v)
        )
        btn.default_color = color
        btn.grid(
            row=r,
            column=c,
            padx=5,
            pady=6,
            sticky="nsew"
        )
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
for i in range(4):
    button_frame.grid_columnconfigure(i, weight=1)
for i in range(5):
    button_frame.grid_rowconfigure(i, weight=1)
# ---------------- KEYBOARD SUPPORT ----------------
def keyboard_input(event):
    key = event.char
    if key in "0123456789.+-*/%":
        press(key)
    elif event.keysym == "Return":
        calculate()
    elif event.keysym == "BackSpace":
        delete()
    elif event.keysym == "Escape":
        clear()
root.bind("<Key>", keyboard_input)
# ---------------- FOOTER ----------------
tk.Label(
    root,
    text="CALCULATOR DESIGNED WITH PYTHON BY NATASHA GOSWAMI ",
    font=("times new roman", 8, "bold"),
    bg=BG,
    fg=MUTED
).pack(pady=12)
root.mainloop()