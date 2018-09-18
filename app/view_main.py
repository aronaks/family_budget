import tkinter as tk


class MainWindow(tk.Frame):
    def __init__(self, vc, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.pack()

        self.vc = vc

        self.currency_value = tk.StringVar(self)
        self.make_widgets()

    def make_widgets(self):
        tk.Button(self, text='Incomes', command=self.vc.open_incomes).pack(
            fill=tk.X, pady=5)
        tk.Button(self, text='Expenses', command=self.vc.open_expenses).pack(
            fill=tk.X, pady=5)
        tk.Button(self, text='Archive', command=self.vc.open_archive).pack(
            fill=tk.X, pady=5)

        self.currency_value.set(list(self.vc.all_currency_values.keys())[0])
        w = tk.OptionMenu(self, self.currency_value,
                          *self.vc.all_currency_values.keys())
        w.pack(fill=tk.X, pady=5)
        self.currency_value.trace('w', self.vc.change_currency)
