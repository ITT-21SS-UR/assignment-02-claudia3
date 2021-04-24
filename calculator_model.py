import sys

from PyQt5 import uic, Qt, QtCore
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QKeyEvent

"""
    The model saves and processes relevant data for the calculator UI.
"""


class CalculatorModel(QObject):
    # https://www.pythoncentral.io/pysidepyqt-tutorial-creating-your-own-signals-and-slots/
    # nice tutorial for custom signals and slots
    data_changed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.equation = ""
        self.current_number = ""

    @staticmethod
    def convert_to_key_code(text: str):
        if text == "+":
            return QtCore.Qt.Key_Plus

        if text == "-":
            return QtCore.Qt.Key_Minus

        if text == "/":
            return QtCore.Qt.Key_Slash

        if text == "*":
            return QtCore.Qt.Key_Asterisk

        if text == ".":
            return QtCore.Qt.Key_Period

        return text

    def is_operator(self, key_code):
        operators = [
            QtCore.Qt.Key_Plus,
            QtCore.Qt.Key_Minus,
            QtCore.Qt.Key_Asterisk,
            QtCore.Qt.Key_Slash
        ]

        if self.convert_to_key_code(key_code) in operators:
            return True

        return False

    @staticmethod
    def is_digit(key_code):
        digits = [
            QtCore.Qt.Key_0,
            QtCore.Qt.Key_1,
            QtCore.Qt.Key_2,
            QtCore.Qt.Key_3,
            QtCore.Qt.Key_4,
            QtCore.Qt.Key_5,
            QtCore.Qt.Key_6,
            QtCore.Qt.Key_7,
            QtCore.Qt.Key_8,
            QtCore.Qt.Key_9
        ]

        if key_code in digits:
            return True

        return False

    @staticmethod
    def is_decimal_point(key_code):
        return key_code == QtCore.Qt.Key_Period

    @staticmethod
    def is_special_key(key_code):
        special_keys = [
            QtCore.Qt.Key_Return,
            QtCore.Qt.Key_Enter,
            QtCore.Qt.Key_Backspace,
            QtCore.Qt.Key_Delete
        ]

        if key_code in special_keys:
            return True

        return False

    def is_accepted_key_code(self, key_code):
        return self.is_digit(key_code) or self.is_operator(key_code) or self.is_decimal_point(key_code)

    def log_message(message):
        def log_decorator(function):
            def log_function(self, data):
                sys.stdout.write(message + " " + str(data) + "\n")
                function(self, data)

            return log_function

        return log_decorator

    def handle_key(self, value):
        if not self.is_key_allowed(value):
            return

        self.equation += value

        if self.is_operator(value):
            self.current_number = ""
        else:
            self.current_number += value

        self.data_changed.emit()

    def is_key_allowed(self, value):
        key_code = self.convert_to_key_code(value)

        # TODO maybe change last operator aber nicht in der aktuellen funktion, da sonst code smell
        if self.is_operator(key_code) and ((not self.current_number) or (self.equation[-1] == value)):
            # TODO Maybe with endswitch
            return False  # TODO die bedingung geht nicht, da verschiedene operatoren aneinander gehängt werden können nur der gleiche ned

        if self.is_decimal_point(key_code) and (self.current_number.__contains__(".")):
            return False  # TODO use sth other than contains in python this is not good

        return True

    @log_message("Button clicked: ")
    def button_clicked(self, value: str):
        self.handle_key(value)

    @log_message("Special Button clicked: ")
    def button_clicked_special(self, value: str):
        if value == "C":
            self.clear_all()
        elif value == "DEL":
            self.delete()
        elif value == "=":
            self.calculate_result()

    def get_current_number(self):
        if not self.current_number:
            return "0"

        return self.current_number

    def get_equation(self):
        return self.equation

    def delete(self):
        if self.current_number:  # len(self.current_number) and len(self.equation) > 1 is redundant
            self.equation = self.equation[:-1]  # TODO current_number remove only when real number
            self.current_number = self.current_number[:-1]

        self.data_changed.emit()

    @log_message("Calculated Result: ")
    def log_calculated_result(self, result):
        # This looks pretty ugly but we have to use logging like this so I did it like this
        return

    def calculate_result(self):
        try:
            self.current_number = str(eval(self.equation))
        except SyntaxError:
            self.current_number = "Err"

        self.log_calculated_result(self.current_number)

        self.data_changed.emit()

        self.equation = ""
        self.current_number = ""

    def clear_all(self):
        self.equation = ""
        self.current_number = ""

        self.data_changed.emit()

    @log_message("Key pressed: ")
    def key_pressed_event(self, key_pressed):
        self.handle_key(str(key_pressed))

    @log_message("Special key pressed: ")
    def key_pressed_event_special(self, key_pressed):
        if key_pressed == "Enter":
            self.calculate_result()

        elif key_pressed == "Delete":
            self.delete()
