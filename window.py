from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QTextEdit, QVBoxLayout, QHBoxLayout, QGridLayout,
    QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt6.QtGui import QPixmap, QTextDocument
from PyQt6.QtCore import Qt
from PyQt6.QtPrintSupport import QPrinter
from expression import Expression
from logic import Logic

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simplificador de Booleanos")
        self.setStyleSheet("background-color: #000000;")
        self.showMaximized()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        header_layout = QHBoxLayout()

        logo = QLabel()
        pixmap = QPixmap("Aditional_Files/Boolean_Simplifier_Logo.png").scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio)
        logo.setPixmap(pixmap)
        logo.setStyleSheet("border-radius: 30px;")
        logo.setFixedSize(60, 60)

        title = QLabel("Simplificador de Booleanos")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            color: white;
            font-size: 32px;
            font-weight: bold;
            font-family: 'Poppins';
        """)

        header_layout.addWidget(logo)
        header_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        header_layout.addWidget(title)
        main_layout.addLayout(header_layout)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ejemplo: A + B · C'")
        self.input_field.setStyleSheet("""
            background-color: #ffffff;
            color: #000000;
            border: 2px solid #5c5c5c;
            border-radius: 10px;
            padding: 8px;
            font-size: 18px;
            font-family: 'Poppins';
        """)
        main_layout.addWidget(self.input_field)


        var_layout = QHBoxLayout()
        variables = ['A', 'B', 'C', 'D', 'E', 'F']
        pastel_colors = ['#fffacd', '#d0f0c0', '#add8e6', '#e6e6fa', '#ffc0cb']

        for i, symbol in enumerate(variables):
            btn = QPushButton(symbol)
            btn.setFixedSize(50, 35)
            color = pastel_colors[i % len(pastel_colors)]
            btn.setStyleSheet(f"""
                background-color: {color};
                color: #000000;
                border-radius: 8px;
                font-size: 14px;
                font-family: 'Poppins';
            """)
            btn.clicked.connect(lambda _, s=symbol: self.input_field.insert(s))
            var_layout.addWidget(btn)
        main_layout.addLayout(var_layout)

        op_layout = QGridLayout()
        operators = ['+', '·', "'", '(', ')', '0', '1']

        for i, symbol in enumerate(operators):
            btn = QPushButton(symbol)
            btn.setFixedSize(50, 35)
            color = pastel_colors[i % len(pastel_colors)]
            btn.setStyleSheet(f"""
                background-color: {color};
                color: #000000;
                border-radius: 8px;
                font-size: 14px;
                font-family: 'Poppins';
            """)
            btn.clicked.connect(lambda _, s=symbol: self.input_field.insert(s))
            op_layout.addWidget(btn, i // 7, i % 7)
        main_layout.addLayout(op_layout)

        eval_btn = QPushButton("Evaluar expresión")
        eval_btn.setStyleSheet("""
            background-color: #d0f0c0;
            color: #000000;
            border-radius: 10px;
            padding: 8px;
            font-size: 15px;
            font-family: 'Poppins';
        """)
        eval_btn.setFixedSize(180, 35)
        eval_btn.clicked.connect(self.evaluate_expression)
        main_layout.addWidget(eval_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setStyleSheet("""
            background-color: #4d4d4d;
            color: #ffffff;
            border: 2px solid #5c5c5c;
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
            font-family: 'Consolas';
        """)
        main_layout.addWidget(self.output_area)

        extra_layout = QHBoxLayout()

        clear_btn = QPushButton("Limpiar")
        clear_btn.setStyleSheet("""
            background-color: #fffacd;
            color: #000000;
            border-radius: 10px;
            padding: 8px;
            font-size: 15px;
            font-family: 'Poppins';
        """)
        clear_btn.setFixedSize(120, 35)
        clear_btn.clicked.connect(self.clear_all)
        extra_layout.addWidget(clear_btn)

        save_btn = QPushButton("Guardar en PDF")
        save_btn.setStyleSheet("""
            background-color: #add8e6;
            color: #000000;
            border-radius: 10px;
            padding: 8px;
            font-size: 15px;
            font-family: 'Poppins';
        """)
        save_btn.setFixedSize(140, 35)
        save_btn.clicked.connect(self.save_to_pdf)
        extra_layout.addWidget(save_btn)

        main_layout.addLayout(extra_layout)
        self.setLayout(main_layout)

    def evaluate_expression(self):
        expr = Expression(self.input_field.text())
        if not expr.validate():
            QMessageBox.warning(self, "Error", "Expresión inválida. Verifica paréntesis y símbolos.")
            return

        logic = Logic(expr.get())
        result = logic.apply_laws()
        steps = logic.get_steps()

        self.output_area.clear()
        if not steps:
            self.output_area.append("Expresión simplificada al mínimo.\n")
        else:
            self.output_area.append("Pasos de simplificación:\n")
            for i, (before, law, after) in enumerate(steps, start=1):
                self.output_area.append(f"Paso {i}: {before}  →  {law}  →  {after}")
        self.output_area.append(f"\nResultado final:\n{result}")

    def clear_all(self):
        self.input_field.clear()
        self.output_area.clear()

    def save_to_pdf(self):
        printer = QPrinter()
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName("resultado_booleano.pdf")

        doc = QTextDocument()
        doc.setPlainText(self.output_area.toPlainText())
        doc.print(printer)

        QMessageBox.information(self, "PDF guardado", "El resultado se ha guardado como 'resultado_booleano.pdf'.")
