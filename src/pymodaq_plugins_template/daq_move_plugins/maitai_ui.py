from qtpy import QtWidgets, QtCore
from qtpy.QtCore import Signal, QObject
from qtpy.QtGui import QColor, QPalette

class MaiTaiUI(QObject):
    """
    User interface for the MaiTai laser plugin, inspired by the manual's control panel.
    
    Provides dedicated buttons for shutter control, laser operation, and status displays.
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

        self.power_label = self._create_status_label()
        self.wavelength_label = self._create_status_label()
        self.shutter_label = self._create_status_label("Unknown", "gray")
        self.modelock_label = self._create_status_label("Inactive", "gray")
        self.laser_status_label = self._create_status_label("Off", "gray")
        self.warmup_label = self._create_status_label()

        status_layout.addRow("Output Power (W):", self.power_label)
        status_layout.addRow("Wavelength (nm):", self.wavelength_label)
        status_layout.addRow("Shutter:", self.shutter_label)
        status_layout.addRow("Mode Lock:", self.modelock_label)
        status_layout.addRow("Laser Status:", self.laser_status_label)
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
        
    def _create_status_label(self, text="-", color=None):
        label = QtWidgets.QLabel(text)
        label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        label.setFrameShadow(QtWidgets.QFrame.Sunken)
        label.setMinimumWidth(80)
        label.setAlignment(QtCore.Qt.AlignCenter)
        if color:
            self._set_label_color(label, color)
        return label

    def _set_label_color(self, label: QtWidgets.QLabel, color: str):
        palette = label.palette()
        palette.setColor(QPalette.Window, QColor(color))
        palette.setColor(QPalette.WindowText, QColor("white") if color not in ["lightgray", "orange"] else QColor("black"))
        label.setPalette(palette)
        label.setAutoFillBackground(True)

    def update_power(self, power: float):
        self.power_label.setText(f"{power:.3f}")

    def update_wavelength(self, wavelength: float):
        self.wavelength_label.setText(f"{wavelength:.1f}")

    def update_shutter_status(self, status: str):
        self.shutter_label.setText(status)
        color = "green" if status == "Open" else "red"
        self._set_label_color(self.shutter_label, color)

    def update_modelock_status(self, status: str, locked: bool):
        self.modelock_label.setText(status)
        color = "green" if locked else "orange"
        self._set_label_color(self.modelock_label, color)

    def update_laser_status(self, status: str):
        self.laser_status_label.setText(status)
        color_map = {"On": "green", "Off": "red", "Warming up": "orange"}
        self._set_label_color(self.laser_status_label, color_map.get(status, "lightgray"))

    def update_warmup_time(self, time_str: str):
        self.warmup_label.setText(time_str)
