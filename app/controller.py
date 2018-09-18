import _tkinter as _tk
import datetime

from app.model import DBConnection
from app.view_main import MainWindow
from app.view_top_level import (TopLevelAddingAmount, TopLevelShowingInfo,
                                TopLevelSubtractingAmount,
                                TopLevelEditArchiveItem)
from app.view_validation import TopLevelValidation


class FamilyBudgetController(object):
    def __init__(self, parent):
        self.all_currency_values = {"UAH": "uk_UA.UTF-8",
                                    "USD": "en_US.UTF-8",
                                    "EUR": "eu_ES.UTF-8"}
        self.wins = [parent]
        self.model = DBConnection(self)
        self.view = MainWindow(self)

        self.validation_win = None
        self.center_main_window(parent)

        self.datetime_now = datetime.datetime.now().strftime("%d/%m/%Y")


    @staticmethod
    def center_main_window(obj, width=200, height=155):
        screen_width = obj.winfo_screenwidth()
        screen_height = obj.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        obj.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def open_incomes(self):
        self.wins.append(TopLevelAddingAmount(self))
        self.wins[-2].withdraw()
        self._set_initial_values()
        self.wins[-1].wait_window()

    def open_expenses(self):
        self.wins.append(TopLevelSubtractingAmount(self))
        self.wins[-2].withdraw()
        self._set_initial_values()
        self.wins[-1].wait_window()

    def open_archive(self):
        self.wins.append(TopLevelShowingInfo(self))
        self.wins[-2].withdraw()
        self.show_stored_data()
        self.wins[-1].wait_window()

    def on_closing(self):
        self.wins[-2].deiconify()
        self.wins[-1].destroy()
        self.wins.pop()

    def on_closing_validation(self, event=None):
        self.wins[-1].deiconify()
        if event is None:
            self.validation_win.destroy()

    def _validate_entry(self, msg):
        self.wins[-1].withdraw()
        self.validation_win = TopLevelValidation(self)
        self.validation_win.validation_message.set(msg)
        self.validation_win.wait_window()

    def _set_initial_values(self):
        self.wins[-1].set_total_amount(self.model.last_total_amount)
        self.wins[-1].date_content.set(self.datetime_now)
        self.wins[-1].sum_content.set(0)
        self.wins[-1].comment_content.set("")

    def add_new_record(self):
        try:
            date = self.wins[-1].date_content.get()
            datetime.datetime.strptime(date, "%d/%m/%Y")
        except (ValueError, _tk.TclError):
            self._validate_entry(msg='Date must be in "dd/mm/year" format')
            return

        try:
            amount = self.wins[-1].amount
            if abs(amount) <= 0.0:
                raise ValueError
        except (ValueError, _tk.TclError):
            self._validate_entry(
                msg='Sum must be a number that is greater than 0')
            return

        comment = self.wins[-1].comment_content.get()
        if comment == "":
            self._validate_entry(msg='You must type a comment')
            return

        last_total_amount = self.model.last_total_amount + amount

        self.model.add_record(date, amount, comment, last_total_amount)

        self._set_initial_values()

    def show_stored_data(self):
        self.wins[-1].set_total_amount(self.model.last_total_amount)
        rows = self.model.get_all_rows()
        current_id = len(rows)
        for r in reversed(rows):
            self.wins[-1].insert_data_to_tree(current_id, r)
            current_id -= 1

    def open_editing(self, event):
        self.wins.append(TopLevelEditArchiveItem(self))
        selected_item = self.wins[-2].data_tree.selection()[0]
        item_data = self.wins[-2].data_tree.item(selected_item, "values")
        item_date = item_data[0]
        item_amount = item_data[1]
        item_comment = item_data[2]
        self.wins[-1].date_content.set(item_date)
        self.wins[-1].sum_content.set(item_amount)
        self.wins[-1].comment_content.set(item_comment)
        self.wins[-1].wait_window()

    def edit_data(self):
        selected_item = self.wins[-2].data_tree.selection()[0]
        item_id = self.wins[-2].data_tree.item(selected_item, "text")
        item_amount_before = float(
            self.wins[-2].data_tree.item(selected_item, "values")[1])
        try:
            date = self.wins[-1].date_content.get()
            datetime.datetime.strptime(date, "%d/%m/%Y")
        except (ValueError, _tk.TclError):
            self._validate_entry(msg='Date must be in "dd/mm/year" format')
            return

        try:
            amount = self.wins[-1].sum_content.get()
            if abs(amount) <= 0.0:
                raise ValueError
        except (ValueError, _tk.TclError):
            self._validate_entry(
                msg='Sum must be a number that is greater than 0')
            return

        comment = self.wins[-1].comment_content.get()
        if comment == "":
            self._validate_entry(msg='You must type a comment')
            return

        new_total_amount = (
                self.model.last_total_amount - item_amount_before + amount)

        self.model.update_record(item_id, date, amount, comment,
                                 new_total_amount)

        self.on_closing()

        self.wins[-1].data_tree.delete(*self.wins[-1].data_tree.get_children())
        self.show_stored_data()

    def change_currency(self, *args):
        chosen_currency = self.view.currency_value.get()
        self.model.connect_to_db(chosen_currency)

    @property
    def locale_value(self):
        chosen_currency = self.view.currency_value.get()
        locale_value = self.all_currency_values[chosen_currency]
        return locale_value
