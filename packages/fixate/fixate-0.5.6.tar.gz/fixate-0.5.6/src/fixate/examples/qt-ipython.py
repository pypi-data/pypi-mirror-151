#!/usr/bin/env python
"""Example integrating an IPython kernel into a GUI App.
This trivial GUI application internally starts an IPython kernel, to which Qt
consoles can be connected either by the user at the command line or started
from the GUI itself, via a button.  The GUI can also manipulate one variable in
the kernel's namespace, and print the namespace to the console.
Play with it by running the script and then opening one or more consoles, and
pushing the 'Counter++' and 'Namespace' buttons.
Upon exit, it should automatically close all consoles opened from the GUI.
Consoles attached separately from a terminal will not be terminated, though
they will notice that their kernel died.
"""
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from PyQt5 import QtWidgets, QtCore

from internal_ipkernel import InternalIPKernel


# -----------------------------------------------------------------------------
# Functions and classes
# -----------------------------------------------------------------------------
class SimpleWindow(QtWidgets.QWidget, InternalIPKernel):
    def __init__(self, app):
        QtWidgets.QWidget.__init__(self)
        self.app = app
        self.add_widgets()
        self.init_ipkernel("qt")

    def add_widgets(self):
        self.setGeometry(300, 300, 400, 70)
        self.setWindowTitle("IPython in your app")

        # Add simple buttons:
        console = QtWidgets.QPushButton("Qt Console", self)
        console.setGeometry(10, 10, 100, 35)
        console.clicked.connect(self.new_qt_console)

        namespace = QtWidgets.QPushButton("Namespace", self)
        namespace.setGeometry(120, 10, 100, 35)
        namespace.clicked.connect(self.print_namespace)

        count = QtWidgets.QPushButton("Count++", self)
        count.setGeometry(230, 10, 80, 35)
        count.clicked.connect(self.count)

        # Quit and cleanup
        # quit = QtWidgets.QPushButton('Quit', self)
        # quit.setGeometry(320, 10, 60, 35)
        # quit.clicked.connect(self.quit)

        # self.app.connect(self.app, Qt.SIGNAL("lastWindowClosed()"),
        #                  self.app, Qt.SLOT("quit()"))

        self.app.aboutToQuit.connect(self.cleanup_consoles)


# -----------------------------------------------------------------------------
# Main script
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    # Create our window
    win = SimpleWindow(app)
    win.show()

    # Very important, IPython-specific step: this gets GUI event loop
    # integration going, and it replaces calling app.exec_()
    win.ipkernel.start()
