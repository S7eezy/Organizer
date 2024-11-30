import sys
import ctypes
from PySide6.QtGui import QPainter, QPixmap, QColor
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QApplication
from PySide6.QtCore import Qt, QTimer, QSize, QPoint
from src.core.utils.resources import resource_path

class OverlayWidget(QWidget):
    def __init__(self, characters, characters_icons, current_index):
        super().__init__()
        self.characters = characters
        self.characters_icons = characters_icons
        self.current_index = current_index

        # Set window flags to remove decorations and keep on top
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool
        )

        # Make the window background transparent
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Create a horizontal layout for the characterIcons
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

        # Add characterIcons to the layout
        self.icons_labels = []
        for i, char in enumerate(self.characters):
            label = QLabel()
            pixmap = QPixmap(self.characters_icons.get(char, resource_path("src/gui/assets/icon_default.png")))
            pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(pixmap)
            self.layout.addWidget(label)
            self.icons_labels.append(label)

        # Adjust the opacity of the characterIcons
        self.adjust_icon_opacity(self.current_index)

        # Optionally make the window click-through
        QTimer.singleShot(0, self.make_click_through)

        # Position the overlay at the top center of the screen
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        overlay_width = self.sizeHint().width()
        x = (screen_geometry.width() - overlay_width) // 2
        y = 10  # 10 pixels from the top
        self.move(QPoint(x, y))

    def set_pixmap_opacity(self, pixmap, opacity):
        """Adjust the opacity of a pixmap."""
        # Create a transparent pixmap with the same size as the original
        transparent = QPixmap(pixmap.size())
        transparent.fill(Qt.transparent)

        # Create a QPainter to paint on the transparent pixmap
        painter = QPainter(transparent)
        painter.setOpacity(opacity)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        return transparent

    def adjust_icon_opacity(self, focused_index):
        """Adjust the opacity of characterIcons based on which one is focused."""
        for i, label in enumerate(self.icons_labels):
            opacity = 1.0 if i == focused_index else .5  # 0.2 for very low opacity
            # Get the original pixmap
            original_pixmap = QPixmap(self.characters_icons.get(self.characters[i], resource_path("src/gui/assets/icon_default.png")))
            original_pixmap = original_pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            # Adjust the pixmap opacity
            adjusted_pixmap = self.set_pixmap_opacity(original_pixmap, opacity)
            # Set the adjusted pixmap to the label
            label.setPixmap(adjusted_pixmap)

    def update_icons(self, characters, characters_icons):
        """Update the characterIcons displayed in the overlay."""
        self.characters = characters
        self.characters_icons = characters_icons
        # Clear existing widgets
        for label in self.icons_labels:
            self.layout.removeWidget(label)
            label.deleteLater()
        self.icons_labels.clear()
        # Add new characterIcons
        for i, char in enumerate(self.characters):
            label = QLabel()
            # Get the original pixmap
            original_pixmap = QPixmap(self.characters_icons.get(char, resource_path("src/gui/assets/icon_default.png")))
            original_pixmap = original_pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            # Adjust the pixmap opacity
            opacity = 1.0 if i == self.current_index else 0.5
            adjusted_pixmap = self.set_pixmap_opacity(original_pixmap, opacity)
            label.setPixmap(adjusted_pixmap)
            self.layout.addWidget(label)
            self.icons_labels.append(label)
        # Adjust size and reposition overlay
        self.adjustSize()
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        overlay_width = self.sizeHint().width()
        x = (screen_geometry.width() - overlay_width) // 2
        y = 10
        self.move(QPoint(x, y))

    def set_current_index(self, index):
        """Set the current focused character index."""
        self.current_index = index
        self.adjust_icon_opacity(self.current_index)

    def make_click_through(self):
        """Modify the window to be click-through."""
        hwnd = self.winId().__int__()
        extended_style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
        ctypes.windll.user32.SetWindowLongW(
            hwnd,
            -20,
            extended_style | 0x80000 | 0x20  # WS_EX_LAYERED | WS_EX_TRANSPARENT
        )
