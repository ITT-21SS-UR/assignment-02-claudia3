import sys

from PyQt5 import uic, Qt, QtCore
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QKeyEvent


# The model saves and processes relevant data for the calculator.

class CalculatorModel(QObject):
    # https://www.pythoncentral.io/pysidepyqt-tutorial-creating-your-own-signals-and-slots/
    # nice tutorial for custom signals and slots
    data_changed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.DELETE = "Delete"
        self.CLEAR = "Clear"
        self.CALCULATE = "Calculate"

        self.__equation = ""
        self.__current_number = ""

    @staticmethod
    def __convert_to_key_code(value: str):
        if value == "+":
            return QtCore.Qt.Key_Plus

        if value == "-":
            return QtCore.Qt.Key_Minus

        if value == "/":
            return QtCore.Qt.Key_Slash

        if value == "*":
            return QtCore.Qt.Key_Asterisk

        if value == ".":
            return QtCore.Qt.Key_Period

        return value

    @staticmethod
    def __is_digit(key_code):
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
    def __is_decimal_point(key_code):
        return key_code == QtCore.Qt.Key_Period

    def __is_operator(self, value: str):
        operators = [
            QtCore.Qt.Key_Plus,
            QtCore.Qt.Key_Minus,
            QtCore.Qt.Key_Asterisk,
            QtCore.Qt.Key_Slash
        ]

        if self.__convert_to_key_code(value) in operators:
            return True

        return False

    def __is_key_allowed(self, value: str):
        key_code = self.__convert_to_key_code(value)

        if self.__is_decimal_point(key_code) \
                and (self.__current_number.__contains__(".")):

            return False

        return True

    def __handle_input(self, value: str):
        if value == self.CLEAR:
            self.__clear_all()

        elif value == self.DELETE:
            self.__delete()

        elif value == self.CALCULATE:
            self.__calculate_result()

        else:
            self.__handle_key(value)

    def __handle_key(self, value: str):
        if not self.__is_key_allowed(value):
            return

        if self.__is_operator(value):
            if self.__equation and self.__is_operator(self.__equation[-1]):
                # if the last character of equation is an operator: replace it with the new operator
                self.__equation = self.__equation[:-1]

            self.__current_number = ""
        else:
            self.__current_number += value

        self.__equation += value

        self.data_changed.emit()

    def __delete(self):
        if self.__current_number:
            self.__equation = self.__equation[:-1]
            self.__current_number = self.__current_number[:-1]

        self.data_changed.emit()

    def __clear_all(self):
        self.__equation = ""
        self.__current_number = ""

        self.data_changed.emit()

    def __calculate_result(self):
        try:
            self.__current_number = str(round(eval(self.__equation), 14))
            # without round eval cannot calculate correctly: 0.3+0.3+0.3=0.8999999...1
            # also without string conversion the result looks weird
            # LCD Display only shows 20 digits
        except SyntaxError:
            self.__current_number = "Err"

        self.__handle_result(self.__current_number)

    def log_message(message):
        def log_decorator(function):
            def log_function(self, data):
                sys.stdout.write(message + " " + str(data) + "\n")
                function(self, data)

            return log_function

        return log_decorator

    @log_message("Result: ")
    def __handle_result(self, result: str):
        self.data_changed.emit()

        self.__equation = ""
        self.__current_number = ""

    @staticmethod
    def is_accepted_key_code_special(key_code):

        special_keys = [
            QtCore.Qt.Key_Delete,
            QtCore.Qt.Key_Backspace,
            QtCore.Qt.Key_Escape,
            QtCore.Qt.Key_Return,
            QtCore.Qt.Key_Enter,
            QtCore.Qt.Key_Equal
        ]

        if key_code in special_keys:
            return True

        return False

    def is_accepted_key_code(self, key_code):
        return self.__is_digit(key_code) \
               or self.__is_operator(key_code) \
               or self.__is_decimal_point(key_code)

    def convert_to_text(self, key_code):
        if key_code == QtCore.Qt.Key_Delete \
                or key_code == QtCore.Qt.Key_Backspace:

            return self.DELETE

        if key_code == QtCore.Qt.Key_Escape:
            return self.CLEAR

        if key_code == QtCore.Qt.Key_Return \
                or key_code == QtCore.Qt.Key_Enter:

            return self.CALCULATE

    @log_message("Button clicked: ")
    def button_clicked(self, value):
        self.__handle_input(value)

    @log_message("Key pressed: ")
    def key_pressed_event(self, key_pressed):
        self.__handle_input(str(key_pressed))

    def get_current_number(self):
        if not self.__current_number:
            return "0"

        return self.__current_number

    def get_equation(self):
        return self.__equation
