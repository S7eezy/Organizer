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

from src.core.organizer import Organizer
from src.core.utils.resources import resource_path
from PySide6.QtWidgets import QApplication
from src.gui.tool import Tool
from src.gui.overlay import OverlayWidget
import sys

if __name__ == '__main__':
    Organizer = Organizer()

    app = QApplication(sys.argv)

    with open(resource_path('src/gui/style/stylesheet.qss'), 'r') as f:
        style = f.read()

    app.setStyleSheet(style)

    overlay = OverlayWidget(
        characters=Organizer.Characters,
        characters_icons=Organizer.CharactersIcons,
        current_index=Organizer.ProcessIndex
    )

    Organizer.current_index_changed.connect(overlay.set_current_index)

    window = Tool(organizer=Organizer, overlay=overlay)
    window.show()

    sys.exit(app.exec())
