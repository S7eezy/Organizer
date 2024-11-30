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
from gui.overlay import OverlayWidget
import sys

if __name__ == '__main__':
    Organizer = Organizer()

    app = QApplication(sys.argv)

    with open('gui/style/stylesheet.qss', 'r') as f:
        style = f.read()

    app.setStyleSheet(style)

    overlay = OverlayWidget(
        characters=Organizer.Characters,
        characters_icons=Organizer.CharactersIcons,
        current_index=Organizer.ProcessIndex
    )

    Organizer.current_index_changed.connect(overlay.set_current_index)

    window = MainWindow(Organizer=Organizer, overlay=overlay)
    window.show()

    sys.exit(app.exec())
