from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QTextEdit, QVBoxLayout, QHBoxLayout,
    QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt6.QtGui import QPixmap, QTextDocument
from PyQt6.QtCore import Qt
from PyQt6.QtPrintSupport import QPrinter
from expression import parse_expression
from logic import simplify_with_steps

class BooleanSimplifierWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simplificador de Booleanos")
        self.setStyleSheet("background-color: #000000;")
        self.showMaximized()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Encabezado con logo y título
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

        # Campo de entrada
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

        instrucciones = QLabel(
            "Usa letras A-Z para variables. Operadores permitidos: + (OR), * (AND), ' o ´ (NOT), paréntesis (). Ejemplos válidos: A + B*C', (A+B)'*C")
        instrucciones.setStyleSheet("""
            color: #ffffff;
            font-size: 16px;
            font-family: 'Poppins';
            padding: 6px;
        """)
        instrucciones.setWordWrap(True)
        main_layout.addWidget(instrucciones)

        # Botón de simplificación
        simplify_btn = QPushButton("Simplificar paso a paso")
        simplify_btn.setStyleSheet("""
            background-color: #d0f0c0;
            color: #000000;
            border-radius: 10px;
            padding: 8px;
            font-size: 15px;
            font-family: 'Poppins';
        """)
        simplify_btn.setFixedSize(220, 35)
        simplify_btn.clicked.connect(self.simplify_expression)
        main_layout.addWidget(simplify_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Área de salida
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

        # Botones extra: limpiar y guardar
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

    def simplify_expression(self):
        texto = self.input_field.text()
        if not texto.strip():
            QMessageBox.warning(self, "Error", "Debes ingresar una expresión booleana.")
            return

        try:
            expr = parse_expression(texto)
            pasos, resultado = simplify_with_steps(expr)

            self.output_area.clear()

            html = f"""
            <div style='color:#ffd700; font-weight:bold; font-size:17px;'>Expresión ingresada:</div>
            <div style='color:#ffffff; font-size:16px; margin-bottom:12px;'><code>{texto}</code></div>
            """

            if not pasos or len(pasos) == 1:
                html += "<div style='color:#90ee90; font-size:16px;'>Expresión simplificada al mínimo.</div>"
            else:
                html += "<div style='color:#00ced1; font-weight:bold; font-size:17px;'>Pasos de simplificación:</div><br>"
                for i, (regla, paso) in enumerate(pasos[1:], start=1):
                    html += f"""
                    <div style='margin-bottom:10px;'>
                        <span style='color:#ffd700; font-weight:bold;'>Paso {i}:</span>
                        <span style='color:#ffffff;'> <code>{paso}</code></span><br>
                        <span style='color:#cccccc;'>Regla aplicada: {regla}</span>
                    </div>
                    """

            html += f"""
            <br><div style='color:#ffb6c1; font-weight:bold; font-size:17px;'>Resultado final:</div>
            <div style='color:#ffffff; font-size:16px;'><code>{resultado}</code></div>
            """

            self.output_area.setHtml(html)

        except Exception as e:
            QMessageBox.critical(self, "Error de análisis", f"Ocurrió un error:\n{str(e)}")

    def clear_all(self):
        self.input_field.clear()
        self.output_area.clear()

    def save_to_pdf(self):
        printer = QPrinter()
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName("resultado_booleano.pdf")

        doc = QTextDocument()
        contenido = f"Expresión ingresada:\n{self.input_field.text()}\n\n"
        contenido += self.output_area.toPlainText()
        doc.setPlainText(contenido)
        doc.print(printer)

        QMessageBox.information(self, "PDF guardado", "El resultado se ha guardado como 'resultado_booleano.pdf'.")
