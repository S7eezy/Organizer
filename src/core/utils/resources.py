import sys
import os


def get_user_data_dir():
    """Return the path to the user data directory."""
    if sys.platform == 'win32':
        # On Windows, use %APPDATA%\Organizer
        return os.path.join(os.getenv('APPDATA'), 'Organizer').replace('\\', '/')
    else:
        # On other platforms, use the home directory
        return os.path.join(os.path.expanduser('~'), '.organizer').replace('\\', '/')


def resource_path(relative_path):
    """Get the absolute path to a resource."""
    if getattr(sys, 'frozen', False):
        # Running in a PyInstaller bundle
        base_path = os.path.join(os.path.dirname(sys.executable), 'src')
    else:
        # Running in a normal Python environment
        base_path = os.path.join(os.path.abspath("."), 'src')
    return os.path.join(base_path, relative_path).replace('\\', '/')


def get_icons_dir():
    """Get the path to the characterIcons directory."""
    base_path = os.path.join(os.path.dirname(sys.executable), 'src') if getattr(sys, 'frozen', False) else os.path.join(os.path.abspath("."), 'src')
    icons_dir = os.path.join(base_path, 'gui', 'assets', 'characterIcons')
    # Ensure the directory exists
    if not os.path.exists(icons_dir):
        os.makedirs(icons_dir, exist_ok=True)
    return icons_dir.replace('\\', '/')
