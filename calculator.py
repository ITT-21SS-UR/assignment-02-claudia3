import sys

from PyQt5 import uic, Qt
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
        self.__setup_button_extra()
        self.__setup_key_press()
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

    def __setup_button_extra(self):
        self.window.buttonAC.clicked.connect(self.model.clear_all)
        self.window.buttonC.clicked.connect(self.model.clear)
        self.window.buttonEquals.clicked.connect(self.model.calculate_result)

    # TODO handle key input event it is not working with model before it worked
    def __setup_key_press(self):
        pass  # TODO

    def __data_changed(self):
        self.window.lcdNumber.display(self.model.get_current_number())
        self.window.labelEquation.setText(self.model.get_equation())

    def __setup_display(self):
        self.model.data_changed.connect(self.__data_changed)


# https://pythonpyqt.com/pyqt-events/
# used for the base class structure
if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    calculator = Calculator()
    app.exec()
