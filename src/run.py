import tkinter as tk

from src.controller import FamilyBudgetController


def main():
    root = tk.Tk()
    root.title('Main')
    root.resizable(width=False, height=False)
    FamilyBudgetController(root)
    root.mainloop()


if __name__ == '__main__':
    main()
