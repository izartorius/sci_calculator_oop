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