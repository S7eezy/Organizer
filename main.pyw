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

    window = MainWindow(Organizer=Organizer)
    window.show()

    # Create and show the overlay
    overlay = OverlayWidget(
        characters=Organizer.Characters,
        characters_icons=Organizer.CharactersIcons,
        current_index=Organizer.ProcessIndex
    )
    overlay.show()

    # Pass the overlay to the main window
    window.overlay = overlay

    # Connect the signal
    Organizer.current_index_changed.connect(overlay.set_current_index)

    sys.exit(app.exec())
