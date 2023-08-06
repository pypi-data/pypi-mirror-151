"""
Entry point for the BoxJelly application.
"""

import sys

from PyQt5 import QtWidgets, QtGui

from boxjelly.lib.constants import APP_NAME, APP_ORGANIZATION, APP_VERSION
from boxjelly.ui.MainWindow import MainWindow


def start(argv):
    """Start the application"""
    # Create the application
    app = QtWidgets.QApplication(argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName(APP_ORGANIZATION)
    
    # Create the splash screen
    splash_logo = QtGui.QIcon(':icons/boxjelly_logo.svg').pixmap(256, 256)
    splash = QtWidgets.QSplashScreen(splash_logo)
    splash.show()
    
    # Create the main window
    window = MainWindow()
    window.show()
    splash.finish(window)
    
    # Start the application
    app.exec_()


def main():
    """Parse command line arguments and start"""
    start(sys.argv)


if __name__ == "__main__":
    main()
