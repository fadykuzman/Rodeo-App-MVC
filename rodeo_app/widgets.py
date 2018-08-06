import tkinter as tk
from tkinter import ttk

class LabelInput(tk.Frame):

    def __init__(self, parent, label='', input_class=ttk.Entry,
        input_var=None, input_args=None, label_args=None,
        **kwargs):
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        self.variables = input_var
        if input_class in (ttk.Checkbutton, ttk.Button,
        ttk.Radiobutton):
            input_args['text'] = label
            input_args['textvariable'] = input_var
        else:
            self.label = ttk.Label(
                self, text=label, **label_args).grid(
                    row=0, column=0, sticky=(tk.W))
            input_args['textvariable'] = input_var
        self.input = input_class(
            self, **input_args).grid(
                row=0, column=1, sticky=(tk.W))
        self.columnconfigure(0, weight=1)

        self.error = getattr(self.input, 'error', tk.StringVar())
        self.error_label = ttk.Label(self, textvariable=self.error)
        self.error_label.grid(row=2, column=0, sticky=(tk.W + tk.E))

    def grid(self, sticky=(tk.W, tk.E), **kwargs):
        super().grid(sticky=sticky, **kwargs)

    def get(self):
        try:
            if self.variables:
                return self.variables.get()
            elif type(self.input) == tk.Text:
                return self.input.get('1.0', tk.END)
            else:
                return self.input.get()
        except (TypeError, tk.TclError):
            return ''
