from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QLabel, QSizePolicy
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont, QFontMetrics
import sys

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rechner")
        self.setMinimumSize(QSize(320, 500))
        self.setStyleSheet("background-color: #1e1e1e;")

        # Main-Widget & Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # History Label (smaller and grey)
        self.previous_input_label = QLabel("")
        self.previous_input_label.setStyleSheet("""
            font-size: 18px;
            font-family: Arial, Sans-Serif;
            color: #888888;
        """)
        self.previous_input_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Display
        self.display = QLineEdit("0")
        self.display.setReadOnly(True)
        self.display.setFixedHeight(80)
        self.display.setStyleSheet("""
            font-weight: bold;
            font-family: Arial, Sans-Serif;
            padding: 15px;
            border: none;
            background: transparent;
            color: white;
        """)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setFont(QFont("Arial", 36))  # Standard-Font-Size

        layout.addWidget(self.previous_input_label)
        layout.addWidget(self.display)

        self.current_input = ""
        self.last_number = ""
        self.operator = ""
        self.reset_next = False

        # Buttons
        self.create_buttons(layout)

    def create_buttons(self, layout):
        grid_layout = QGridLayout()
        grid_layout.setSpacing(4)
        layout.addLayout(grid_layout)

        buttons = [
            ('%', 0, 0), ('CE', 0, 1), ('C', 0, 2), ('⌫', 0, 3),
            ('1/x', 1, 0), ('x²', 1, 1), ('√x', 1, 2), ('+', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
            ('+/-', 5, 0), ('0', 5, 1), ('.', 5, 2), ('=', 5, 3)
        ]

        for text, row, col in buttons:
            button = QPushButton(text)
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            button.setStyleSheet(f"""
                font-size: 20px;
                font-weight: bold;
                font-family: Arial, Sans-Serif;
                border-radius: 10px;
                background-color: {'#0078D7' if text == '=' else '#2D2D2D'};
                color: white;
            """)
            button.clicked.connect(lambda checked, t=text: self.on_button_click(t))
            grid_layout.addWidget(button, row, col)

    def adjust_font_size(self):
        text = self.display.text()
        font = self.display.font()
        font_metrics = QFontMetrics(font)

        max_width = self.display.width() - 20  # Place for Padding
        min_font_size = 10
        max_font_size = 36  # Standard size
        font_size = max_font_size

        # Make font smaller, if text is too big
        while font_size > min_font_size and font_metrics.horizontalAdvance(text) > max_width:
            font_size -= 2
            font.setPointSize(font_size)
            font_metrics = QFontMetrics(font)

        # Make font bigger, if Text is smaller than available place
        while font_size < max_font_size and font_metrics.horizontalAdvance(text) < max_width:
            font_size += 2
            font.setPointSize(font_size)
            font_metrics = QFontMetrics(font)
            
            if font_metrics.horizontalAdvance(text) > max_width:
                font_size -= 2
                break

        font.setPointSize(font_size)
        self.display.setFont(font)

    def on_button_click(self, text):
        if text.isdigit() or text == ".":
            if self.reset_next:
                self.current_input = text
                self.reset_next = False
            else:
                self.current_input += text
            self.display.setText(self.current_input)
            self.adjust_font_size()

        elif text in ["+", "-", "*", "/"]:
            if self.current_input:
                self.last_number = self.current_input
                self.operator = text
                self.previous_input_label.setText(f"{self.last_number} {self.operator}")
                self.reset_next = True
            self.display.setText("0")
            self.adjust_font_size()

        elif text == "=":
            if self.last_number and self.operator and self.current_input:
                try:
                    result = str(eval(self.last_number + self.operator + self.current_input))
                    self.previous_input_label.setText(f"{self.last_number} {self.operator} {self.current_input} =")
                    self.display.setText(result)
                    self.current_input = result
                    self.last_number = ""
                    self.operator = ""
                except Exception:
                    self.display.setText("Error")
                    self.current_input = ""
            self.adjust_font_size()

        elif text == "C":
            self.current_input = ""
            self.last_number = ""
            self.operator = ""
            self.previous_input_label.setText("")
            self.display.setText("0")
            self.adjust_font_size()

        elif text == "CE":
            self.current_input = ""
            self.display.setText("0")
            self.adjust_font_size()

        elif text == "⌫":
            self.current_input = self.current_input[:-1] if self.current_input else "0"
            self.display.setText(self.current_input)
            self.adjust_font_size()

        elif text == "+/-":
            if self.current_input:
                if self.current_input.startswith("-"):
                    self.current_input = self.current_input[1:]
                else:
                    self.current_input = "-" + self.current_input
                self.display.setText(self.current_input)
            self.adjust_font_size()

        elif text == "%":
            try:
                if self.operator and self.last_number:
                    percentage_value = float(self.last_number) * (float(self.current_input) / 100)
                    self.current_input = str(percentage_value)
                else:
                    self.current_input = str(float(self.current_input) / 100)
                self.display.setText(self.current_input)
            except Exception:
                self.display.setText("Error")
                self.current_input = ""
            self.adjust_font_size()

        elif text == "1/x":
            try:
                result = str(1 / float(self.current_input))
                self.display.setText(result)
                self.current_input = result
            except Exception:
                self.display.setText("Error")
                self.current_input = ""
            self.adjust_font_size()

        elif text == "x²":
            try:
                result = str(float(self.current_input) ** 2)
                self.display.setText(result)
                self.current_input = result
            except Exception:
                self.display.setText("Error")
                self.current_input = ""
            self.adjust_font_size()

        elif text == "√x":
            try:
                result = str(float(self.current_input) ** 0.5)
                self.display.setText(result)
                self.current_input = result
            except Exception:
                self.display.setText("Error")
                self.current_input = ""
            self.adjust_font_size()

# start App
app = QApplication(sys.argv)
window = Calculator()
window.show()
app.exec()
