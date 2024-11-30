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

import sys
import os

# Add the directory containing main.pyw to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from core.organizer import Organizer
from core.utils.resources import resource_path, get_user_data_dir, get_icons_dir
from gui.tool import Tool
from gui.overlay import OverlayWidget


if __name__ == '__main__':
    Organizer = Organizer()

    app = QApplication(sys.argv)

    with open(resource_path('gui/style/stylesheet.qss'), 'r') as f:
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
