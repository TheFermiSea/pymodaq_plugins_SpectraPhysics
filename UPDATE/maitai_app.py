import sys
from qtpy import QtWidgets
from pymodaq.utils.gui_utils import CustomApp, DockArea
from pymodaq_plugins_spectraphysics.daq_move_plugins.daq_move_MaiTai import DAQ_Move_MaiTai

class MaiTaiControlApp(CustomApp):
    """
    A standalone application for controlling the MaiTai laser.
    It uses the DAQ_Move_MaiTai plugin without the full PyMoDAQ Dashboard.
    """
    def __init__(self, dockarea):
        super().__init__(dockarea)
        self.setup_ui()

    def setup_docks(self):
        """Setup the docks inside the dockarea."""
        # Create a DAQ_Move instance programmatically. It will act as the backend.
        # It's important to set parent=None so it doesn't create its default UI elements.
        self.maitai_move = DAQ_Move_MaiTai(parent=None, title="MaiTai Control")

        # This is the key step: get the custom widget provided by the plugin
        self.maitai_widget, _ = self.maitai_move.get_widget_and_signals()

        # Add the custom widget to a dock for display
        dock = self.dockarea.addDock(name='MaiTai')
        dock.addWidget(self.maitai_widget)

        # Initialize the hardware connection
        try:
            info, initialized = self.maitai_move.ini_stage()
            if not initialized:
                raise ConnectionError(info)
            print(info)
        except Exception as e:
            error_message = f"Failed to initialize MaiTai hardware: {e}"
            print(error_message)
            # Display error in the UI
            error_dialog = QtWidgets.QMessageBox()
            error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
            error_dialog.setText(error_message)
            error_dialog.setWindowTitle("Connection Error")
            error_dialog.exec_()


    def connect_things(self):
        """Connect signals and slots."""
        # All necessary connections are handled within the plugin's get_widget_and_signals method.
        # This keeps the application logic clean and separated.
        pass

    def setup_actions(self):
        """Setup actions for menus or toolbars (not used in this simple app)."""
        pass

    def setup_menu(self):
        """Setup the main menu (not used in this simple app)."""
        pass

def main():
    from qtpy.QtWidgets import QMainWindow

    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)

    win = QMainWindow()
    area = DockArea()
    win.setCentralWidget(area)
    win.setWindowTitle('MaiTai Laser Control Panel')
    win.resize(450, 600)

    prog = MaiTaiControlApp(area)

    # Ensure the plugin is closed gracefully when the window is closed
    def cleanup():
        prog.maitai_move.close()

    app.aboutToQuit.connect(cleanup)

    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
