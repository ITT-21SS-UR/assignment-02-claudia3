import sys

from PyQt5 import uic, Qt, QtCore
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QKeyEvent

"""
    The model saves and processes relevant data for the calculator UI.
"""


class CalculatorModel(QObject):
    data_changed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.equation = ""
        self.current_number = ""

    @staticmethod
    def convert_to_key_code(text: str):  # TODO maybe for logging in reverse or with dictionary
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

    def is_operator(self, key_code):
        operators = [QtCore.Qt.Key_Plus, QtCore.Qt.Key_Minus, QtCore.Qt.Key_Asterisk, QtCore.Qt.Key_Slash]

        if self.convert_to_key_code(key_code) in operators:
            return True

        return False

    @staticmethod
    def is_digit(key_code):
        digits = [QtCore.Qt.Key_0, QtCore.Qt.Key_1, QtCore.Qt.Key_2, QtCore.Qt.Key_3, QtCore.Qt.Key_4,
                  QtCore.Qt.Key_5, QtCore.Qt.Key_6, QtCore.Qt.Key_7, QtCore.Qt.Key_8, QtCore.Qt.Key_9]

        if key_code in digits:
            return True

        return False

    @staticmethod
    def is_decimal_point(key_code):
        return key_code == QtCore.Qt.Key_Period

    # TODO accepts keyCode
    def accept_key_code(self, key_code):
        return self.is_digit(key_code) or self.is_operator(key_code) or self.is_decimal_point(key_code)

    # TODO maybe separate button and key messages logs
    def log_message(message):  # log all button clicks with one parameter
        def log_decorator(function):
            def log_function(self, data):
                # if isinstance(data, QKeyEvent):  # TODO
                #     data = data.text()

                sys.stdout.write(message + " " + str(data) + "\n")
                # print("test: " + str(self.equation))  # TODO
                function(self, data)

            return log_function

        return log_decorator

    # TODO decorator logging
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
            return False  # TODO die bedingung geht nicht, da verschiedene operatoren aneinander gehängt werden können nur der gleiche ned

        if self.is_decimal_point(key_code) and (self.current_number.__contains__(".")):
            return False  # TODO use sth other than contains in python this is not good

        return True

    @log_message("Button clicked: ")
    def button_clicked(self, value: str):
        self.handle_key(value)

    def get_current_number(self):
        if not self.current_number:
            return "0"

        return self.current_number

    def get_equation(self):
        return self.equation

    def calculate_result(self):
        try:
            self.current_number = str(eval(self.equation))
        except SyntaxError:  # TODO after calculating one result I always get a syntax error
            self.current_number = "Err"

        sys.stdout.write(self.current_number)  # TODO with logging

        self.data_changed.emit()

        self.equation = ""  # TODO
        self.current_number = ""

        # log all button clicks with no parameter except self

    def log_message_no_parameter(message):
        # TODO better because no there are nearly to identical decorators
        def log_decorator(function):
            def log_function(self):
                sys.stdout.write(message + "\n")
                function(self)

            return log_function

        return log_decorator

    @log_message_no_parameter("Clear last digit ")
    def clear(self):
        if self.current_number:  # len(self.current_number) and len(self.equation) > 1 is redundant
            self.equation = self.equation[:-1]  # TODO current_number remove only when real number
            self.current_number = self.current_number[:-1]

        self.data_changed.emit()

    @log_message_no_parameter("Calculate result")
    def calculate_result(self):
        try:
            self.current_number = str(eval(self.equation))
        except SyntaxError:
            self.current_number = "Err"

        sys.stdout.write(self.current_number)  # TODO logging

        self.data_changed.emit()

        self.equation = ""
        self.current_number = ""

    @log_message_no_parameter("AC clicked (Clear all)")
    def clear_all(self):
        self.equation = ""
        self.current_number = ""

        self.data_changed.emit()

    @log_message("Key pressed: ")  # TODO log after processing possible? keyPressed
    def keyPressEvent(self, key_pressed):
        self.handle_input(key_pressed)
        # print(pressed_key.text())
        # pressed_key = pressed_key.key()
        # pressed_key_text = pressed_key.text()
        # pressed_key_key = pressed_key.key()  # TODO
        # if pressed_key in self.NUMBERS:
        #     self.model.handle_number(pressed_key)
        #
        # elif pressed_key in self.OPERATORS:
        #     self.model.handle_operator(pressed_key)
        #
        # elif pressed_key == self.DECIMAL_POINT:
        #     self.model.handle_decimal_point()
        #
        # elif pressed_key == QtCore.Qt.Key_Return or pressed_key == QtCore.Qt.Key_Enter:
        #     self.model.calculate_result()
        #
        # elif pressed_key == QtCore.Qt.Key_Delete or pressed_key == QtCore.Qt.Key_Backspace:
        #     self.model.handle_c()
