import tkinter as tk
from tkinter import ttk
from datetime import datetime
from . import views as v
from . import model as m


class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Rodeo Potentiostat App')

        ttk.Label(self, text='SKAN Rodeo Potentiostat Application',
            font=('TkDefault', 16)).grid(row=0)

        self.testform = v.TestForm(self)
        self.testform.grid(
            row=1, column=0, padx=10, pady=10)
