import tkinter as tk
from tkinter import messagebox
import math
import re

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.is_degrees = True

        self.create_widgets()

    def create_widgets(self):
        self.mode_label = tk.Label(self.root, text="Mode: Degrees", font=("Arial", 12))
        self.mode_label.grid(row=0, column=0, columnspan=4, pady=5)

        self.entry = tk.Entry(self.root, font=("Arial", 18), bd=10, relief=tk.GROOVE, justify='right')
        self.entry.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

        buttons = [
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
            ('0', 5, 0), ('.', 5, 1), ('+', 5, 2), ('=', 5, 3),
            ('C', 6, 0), ('sin(', 6, 1), ('cos(', 6, 2), ('tan(', 6, 3),
            ('(', 7, 0), (')', 7, 1), ('log(', 7, 2), ('Toggle Mode', 7, 3)
        ]

        for (text, row, col) in buttons:
            if text == "=":
                btn = tk.Button(self.root, text=text, width=10, height=2, command=self.calculate)
            elif text == "C":
                btn = tk.Button(self.root, text=text, width=10, height=2, command=self.clear)
            elif text == "Toggle Mode":
                btn = tk.Button(self.root, text=text, width=15, height=2, command=self.toggle_mode)
            else:
                btn = tk.Button(self.root, text=text, width=10, height=2,
                                command=lambda t=text: self.insert_value(t))

            btn.grid(row=row, column=col, padx=5, pady=5,
                     columnspan=(2 if text == "Toggle Mode" else 1))

    def toggle_mode(self):
        self.is_degrees = not self.is_degrees
        self.mode_label.config(text=f"Mode: {'Degrees' if self.is_degrees else 'Radians'}")

    def evaluate_expression(self, expression):
        try:
            while "log(" in expression:
                start = expression.find("log(")
                end = expression.find(")", start)
                if end == -1:
                    raise ValueError("Unmatched parentheses in log function")

                log_content = expression[start + 4:end]
                parts = log_content.split(",")
                if len(parts) == 1:
                    log_result = math.log10(float(parts[0]))
                elif len(parts) == 2:
                    log_result = math.log(float(parts[0]), float(parts[1]))
                else:
                    raise ValueError("Invalid log format. Use log(value) or log(value, base)")

                expression = expression[:start] + str(log_result) + expression[end + 1:]

            def replace_trig(match):
                func = match.group(1)
                value = float(match.group(2))
                if self.is_degrees:
                    value = math.radians(value)
                return str(getattr(math, func)(value))

            expression = re.sub(r"(sin|cos|tan)\((-?\d+(\.\d*)?)\)", replace_trig, expression)

            result = eval(expression, {"__builtins__": None}, math.__dict__)
            return result

        except Exception as e:
            return f"Error: {e}"