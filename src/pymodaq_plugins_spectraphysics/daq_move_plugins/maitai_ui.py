from qtpy import QtWidgets, QtCore
from qtpy.QtCore import Signal, QObject
from pymodaq_gui.utils import QLED

class MaiTaiUI(QObject):
    """
    User interface for the MaiTai laser plugin, using standard PyMoDAQ widgets.
    """
    
    # Signals to connect to plugin methods
    laser_on_signal = Signal()
    laser_off_signal = Signal()
    open_shutter_signal = Signal()
    close_shutter_signal = Signal()

    def __init__(self, parent_widget: QtWidgets.QWidget):
        super().__init__()
        self.parent_widget = parent_widget
        self.setup_ui()

    def setup_ui(self):
        """Create and arrange the UI elements."""
        main_layout = QtWidgets.QVBoxLayout()
        control_group = QtWidgets.QGroupBox("MaiTai Laser Control")
        grid_layout = QtWidgets.QGridLayout()

        # Status Indicators
        status_group = QtWidgets.QGroupBox("Status")
        status_layout = QtWidgets.QFormLayout()

        self.power_label = QtWidgets.QLabel("-")
        self.wavelength_label = QtWidgets.QLabel("-")
        self.shutter_led = QLED(self.parent_widget, on_color="green", off_color="red")
        self.modelock_led = QLED(self.parent_widget, on_color="green", off_color="orange")
        self.laser_status_led = QLED(self.parent_widget, on_color="green", off_color="red")
        self.warmup_label = QtWidgets.QLabel("-")

        status_layout.addRow("Output Power (W):", self.power_label)
        status_layout.addRow("Wavelength (nm):", self.wavelength_label)
        status_layout.addRow("Shutter:", self.shutter_led)
        status_layout.addRow("Mode Lock:", self.modelock_led)
        status_layout.addRow("Laser Status:", self.laser_status_led)
        status_layout.addRow("Warmup:", self.warmup_label)
        status_group.setLayout(status_layout)

        # Control Buttons
        controls_group = QtWidgets.QGroupBox("Controls")
        controls_layout = QtWidgets.QHBoxLayout()
        self.on_button = QtWidgets.QPushButton("Laser ON")
        self.off_button = QtWidgets.QPushButton("Laser OFF")
        self.open_shutter_button = QtWidgets.QPushButton("Open Shutter")
        self.close_shutter_button = QtWidgets.QPushButton("Close Shutter")
        
        controls_layout.addWidget(self.on_button)
        controls_layout.addWidget(self.off_button)
        controls_layout.addStretch()
        controls_layout.addWidget(self.open_shutter_button)
        controls_layout.addWidget(self.close_shutter_button)
        controls_group.setLayout(controls_layout)

        grid_layout.addWidget(status_group, 0, 0)
        grid_layout.addWidget(controls_group, 1, 0)
        
        control_group.setLayout(grid_layout)
        main_layout.addWidget(control_group)
        main_layout.addStretch()
        self.parent_widget.setLayout(main_layout)
        
        # Connect button signals
        self.on_button.clicked.connect(self.laser_on_signal.emit)
        self.off_button.clicked.connect(self.laser_off_signal.emit)
        self.open_shutter_button.clicked.connect(self.open_shutter_signal.emit)
        self.close_shutter_button.clicked.connect(self.close_shutter_signal.emit)
        
    def update_power(self, power: float):
        self.power_label.setText(f"{power:.3f}")

    def update_wavelength(self, wavelength: float):
        self.wavelength_label.setText(f"{wavelength:.1f}")

    def update_shutter_status(self, status: str):
        self.shutter_led.set_as(status == "Open")

    def update_modelock_status(self, status: str, locked: bool):
        self.modelock_led.set_as(locked)

    def update_laser_status(self, status: str):
        self.laser_status_led.set_as(status == "On")

    def update_warmup_time(self, time_str: str):
        self.warmup_label.setText(time_str)