import sys

from PyQt5.QtWidgets import QApplication

from .database import connection
from .view import Window

def main():
    app:QApplication = QApplication(sys.argv)
    if not connection("agenda.sqlite"):
        sys.exit(1)
        
    win:Window = Window()
    win.show()
    sys.exit(app.exec_())