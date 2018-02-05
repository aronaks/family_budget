import tkinter as tk

from app.controller import FamilyBudgetController


def main():
    root = tk.Tk()
    root.title('Main')
    root.resizable(width=False, height=False)
    FamilyBudgetController(root)
    root.mainloop()


if __name__ == '__main__':
    main()
