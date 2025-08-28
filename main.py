import sys
from PyQt6.QtWidgets import QApplication
from window import BooleanSimplifierWindow

def main():
    app = QApplication(sys.argv)
    ventana = BooleanSimplifierWindow()
    ventana.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
