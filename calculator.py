import sys

from PyQt5 import uic, Qt, QtCore
from PyQt5.QtWidgets import QMainWindow
from calculator_model import CalculatorModel


class Calculator(QMainWindow):

    def __init__(self):
        super().__init__()

        self.model = CalculatorModel()
        self.window = uic.loadUi("calculator.ui", self)

        self.__setup_ui()

        self.window.show()

    def __setup_ui(self):
        self.__setup_button_numbers()
        self.__setup_button_operators()
        self.__setup_button_special()
        self.__setup_display()

    def __setup_button_numbers(self):
        self.window.button0.clicked.connect(lambda: self.model.button_clicked("0"))
        self.window.button1.clicked.connect(lambda: self.model.button_clicked("1"))
        self.window.button2.clicked.connect(lambda: self.model.button_clicked("2"))
        self.window.button3.clicked.connect(lambda: self.model.button_clicked("3"))
        self.window.button4.clicked.connect(lambda: self.model.button_clicked("4"))
        self.window.button5.clicked.connect(lambda: self.model.button_clicked("5"))
        self.window.button6.clicked.connect(lambda: self.model.button_clicked("6"))
        self.window.button7.clicked.connect(lambda: self.model.button_clicked("7"))
        self.window.button8.clicked.connect(lambda: self.model.button_clicked("8"))
        self.window.button9.clicked.connect(lambda: self.model.button_clicked("9"))

        self.window.buttonDecimalPoint.clicked.connect(lambda: self.model.button_clicked("."))

    def __setup_button_operators(self):
        self.window.buttonSubtraction.clicked.connect(
            lambda: self.model.button_clicked("-"))
        self.window.buttonAddition.clicked.connect(
            lambda: self.model.button_clicked("+"))
        self.window.buttonDivision.clicked.connect(
            lambda: self.model.button_clicked("/"))
        self.window.buttonMultiplication.clicked.connect(
            lambda: self.model.button_clicked("*"))

    def __setup_button_special(self):
        self.window.buttonC.clicked.connect(lambda: self.model.button_clicked_special("C"))
        self.window.buttonDel.clicked.connect(lambda: self.model.button_clicked_special("DEL"))
        self.window.buttonEquals.clicked.connect(lambda: self.model.button_clicked_special("="))

    def __data_changed(self):
        self.window.lcdNumber.display(self.model.get_current_number())
        self.window.labelEquation.setText(self.model.get_equation())

    def __setup_display(self):
        self.model.data_changed.connect(self.__data_changed)

    def keyPressEvent(self, pressed_key):
        pressed_key_code = pressed_key.key()

        if self.model.is_accepted_key_code(pressed_key_code):
            self.model.key_pressed_event(pressed_key.text())
        elif self.model.is_special_key(pressed_key_code):
            if pressed_key_code == QtCore.Qt.Key_Return or pressed_key_code == QtCore.Qt.Key_Enter:
                pressed_key_code = "Enter"
            elif pressed_key_code == QtCore.Qt.Key_Delete or pressed_key_code == QtCore.Qt.Key_Backspace:
                pressed_key_code = "Delete"

            self.model.key_pressed_event_special(pressed_key_code)


if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    calculator = Calculator()
    app.exec()
