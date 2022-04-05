# ░██████╗████████╗███████╗███████╗███████╗██╗░░░██╗
# ██╔════╝╚══██╔══╝██╔════╝██╔════╝╚════██║╚██╗░██╔╝
# ╚█████╗░░░░██║░░░█████╗░░█████╗░░░░███╔═╝░╚████╔╝░
# ░╚═══██╗░░░██║░░░██╔══╝░░██╔══╝░░██╔══╝░░░░╚██╔╝░░
# ██████╔╝░░░██║░░░███████╗███████╗███████╗░░░██║░░░
# ╚═════╝░░░░╚═╝░░░╚══════╝╚══════╝╚══════╝░░░╚═╝░░░

# ░█████╗░██████╗░░██████╗░░█████╗░███╗░░██╗██╗███████╗███████╗██████╗░
# ██╔══██╗██╔══██╗██╔════╝░██╔══██╗████╗░██║██║╚════██║██╔════╝██╔══██╗
# ██║░░██║██████╔╝██║░░██╗░███████║██╔██╗██║██║░░███╔═╝█████╗░░██████╔╝
# ██║░░██║██╔══██╗██║░░╚██╗██╔══██║██║╚████║██║██╔══╝░░██╔══╝░░██╔══██╗
# ╚█████╔╝██║░░██║╚██████╔╝██║░░██║██║░╚███║██║███████╗███████╗██║░░██║
# ░╚════╝░╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝╚═╝░░╚══╝╚═╝╚══════╝╚══════╝╚═╝░░╚═╝


from app.Organizer.main import Organizer
from PySide6.QtWidgets import QApplication
from gui.main import MainWindow
import sys

if __name__ == '__main__':
    Organizer = Organizer()

    app = QApplication(sys.argv)

    with open('gui/style/stylesheet.qss', 'r') as f:
        style = f.read()

    app.setStyleSheet(style)

    window = MainWindow(Organizer=Organizer)
    window.show()

    sys.exit(app.exec())
