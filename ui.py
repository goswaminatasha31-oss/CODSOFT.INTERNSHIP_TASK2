import tkinter as tk
class CalculatorUI:
    def __init__(self, root, calculate_function):
        self.root = root
        self.calculate_function = calculate_function
        self.root.title("Smart Calculator")
        self.root.geometry("360x540")
        self.root.resizable(False, False)
        self.root.configure(bg="#101426")
        self.display_text = tk.StringVar()
        self.display = tk.Entry(
            root,
            textvariable=self.display_text,
            font=("times new roman", 26),
            bg="#1B2038",
            fg="white",
            insertbackground="white",
            justify="right",
            bd=0
        )
        self.display.pack(fill="x", padx=18, pady=25, ipady=18)
        self.button_frame = tk.Frame(root, bg="#101426")
        self.button_frame.pack(expand=True, fill="both", padx=12, pady=10)
        buttons = [
            ["C", "DEL", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "(", ")"],
            ["="]
        ]
        for row_number, row in enumerate(buttons):
            for column_number, text in enumerate(row):
                column_span = 4 if text == "=" else 1
                button = tk.Button(
                    self.button_frame,
                    text=text,
                    font=("times new roman", 16, "bold"),
                    bg="#252B49" if text not in ["=", "C"] else
                       "#7655D9" if text == "=" else "#B84B63",
                    fg="white",
                    activebackground="#9575E8",
                    activeforeground="white",
                    bd=0,
                    command=lambda value=text: self.button_click(value)
                )
                button.grid(
                    row=row_number,
                    column=column_number,
                    columnspan=column_span,
                    sticky="nsew",
                    padx=5,
                    pady=5,
                    ipady=12
                )
        for i in range(6):
            self.button_frame.rowconfigure(i, weight=1)
        for i in range(4):
            self.button_frame.columnconfigure(i, weight=1)
        self.root.bind("<Key>", self.keyboard_input)
    def button_click(self, value):
        if value == "C":
            self.display_text.set("")
        elif value == "DEL":
            current = self.display_text.get()
            self.display_text.set(current[:-1])
        elif value == "%":
            current = self.display_text.get()
            if current:
                self.display_text.set("(" + current + ")/100")
        elif value == "=":
            self.calculate_answer()
        else:
            self.display_text.set(self.display_text.get() + value)
    def calculate_answer(self):
        expression = self.display_text.get()
        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")
        try:
            answer = self.calculate_function(expression)
            if isinstance(answer, float) and answer.is_integer():
                answer = int(answer)
            self.display_text.set(str(answer))
        except ZeroDivisionError:
            self.display_text.set("Cannot divide by zero")
        except Exception:
            self.display_text.set("Error")
    def keyboard_input(self, event):
        key = event.char
        if event.keysym == "Return":
            self.calculate_answer()
        elif event.keysym == "Escape":
            self.display_text.set("")
        elif event.keysym == "BackSpace":
            current = self.display_text.get()
            self.display_text.set(current[:-1])
        elif key in "0123456789.+-()%":
            self.display_text.set(self.display_text.get() + key)
        elif key == "*":
            self.display_text.set(self.display_text.get() + "×")
        elif key == "/":
            self.display_text.set(self.display_text.get() + "÷")
