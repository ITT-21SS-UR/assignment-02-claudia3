import sys

from PyQt5 import uic, Qt
from PyQt5.QtWidgets import QMainWindow
from calculator_model import CalculatorModel


class Calculator(QMainWindow):

    def __init__(self):
        super().__init__()

        self.__model = CalculatorModel()
        self.__window = uic.loadUi("calculator.ui", self)
        self.__setup_ui()
        self.__window.show()

    def __setup_ui(self):
        self.__setup_button_numbers()
        self.__setup_button_operators()
        self.__setup_button_special()
        self.__setup_display()

    def __setup_button_numbers(self):
        self.__window.button0.clicked.connect(lambda: self.__model.button_clicked("0"))
        self.__window.button1.clicked.connect(lambda: self.__model.button_clicked("1"))
        self.__window.button2.clicked.connect(lambda: self.__model.button_clicked("2"))
        self.__window.button3.clicked.connect(lambda: self.__model.button_clicked("3"))
        self.__window.button4.clicked.connect(lambda: self.__model.button_clicked("4"))
        self.__window.button5.clicked.connect(lambda: self.__model.button_clicked("5"))
        self.__window.button6.clicked.connect(lambda: self.__model.button_clicked("6"))
        self.__window.button7.clicked.connect(lambda: self.__model.button_clicked("7"))
        self.__window.button8.clicked.connect(lambda: self.__model.button_clicked("8"))
        self.__window.button9.clicked.connect(lambda: self.__model.button_clicked("9"))

        self.__window.buttonDecimalPoint.clicked.connect(lambda: self.__model.button_clicked("."))

    def __setup_button_operators(self):
        self.__window.buttonAddition.clicked.connect(lambda: self.__model.button_clicked("+"))
        self.__window.buttonSubtraction.clicked.connect(lambda: self.__model.button_clicked("-"))
        self.__window.buttonMultiplication.clicked.connect(lambda: self.__model.button_clicked("*"))
        self.__window.buttonDivision.clicked.connect(lambda: self.__model.button_clicked("/"))

    def __setup_button_special(self):
        self.__window.buttonC.clicked.connect(lambda: self.__model.button_clicked(self.__model.CLEAR))
        self.__window.buttonDel.clicked.connect(lambda: self.__model.button_clicked(self.__model.DELETE))
        self.__window.buttonEquals.clicked.connect(lambda: self.__model.button_clicked(self.__model.CALCULATE))

    def __data_changed(self):
        self.__window.lcdNumber.display(self.__model.get_current_number())
        self.__window.labelEquation.setText(self.__model.get_equation())

    def __setup_display(self):
        self.__model.data_changed.connect(self.__data_changed)

    def keyPressEvent(self, pressed_key):
        pressed_key_code = pressed_key.key()

        if self.__model.is_accepted_key_code(pressed_key_code):
            self.__model.key_pressed_event(pressed_key.text())
        elif self.__model.is_accepted_key_code_special(pressed_key_code):
            # special key codes that have no value when using pressed_key.text()
            pressed_key_code = self.__model.convert_to_text(pressed_key_code)
            self.__model.key_pressed_event(pressed_key_code)


if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    calculator = Calculator()
    app.exec()
