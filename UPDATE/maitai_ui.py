from qtpy import QtWidgets, QtCore
from qtpy.QtCore import Signal
from pymodaq.utils.gui_utils.widgets import QLED

class MaiTaiUI(QtWidgets.QWidget):
    """
    Custom User Interface for the MaiTai Laser.
    Resembles the control panel from the MaiTai manual, including wavelength control.
    """
    laser_on_signal = Signal()
    laser_off_signal = Signal()
    open_shutter_signal = Signal()
    close_shutter_signal = Signal()
    set_wavelength_signal = Signal(float)

    def __init__(self, parent=None, min_wl=700.0, max_wl=1000.0):
        super().__init__(parent)
        self.min_wl = min_wl
        self.max_wl = max_wl
        self.setWindowTitle("MaiTai Laser Control")
        self.setup_ui()

    def setup_ui(self):
        """Create and arrange widgets."""
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        # Wavelength Control Group
        wl_group = QtWidgets.QGroupBox("Wavelength Control")
        wl_layout = QtWidgets.QGridLayout()
        wl_group.setLayout(wl_layout)
        main_layout.addWidget(wl_group)

        self.wl_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.wl_slider.setMinimum(int(self.min_wl * 10))
        self.wl_slider.setMaximum(int(self.max_wl * 10))

        self.wl_spinbox = QtWidgets.QDoubleSpinBox()
        self.wl_spinbox.setMinimum(self.min_wl)
        self.wl_spinbox.setMaximum(self.max_wl)
        self.wl_spinbox.setDecimals(1)
        self.wl_spinbox.setSuffix(" nm")

        wl_layout.addWidget(QtWidgets.QLabel("Set Wavelength:"), 0, 0)
        wl_layout.addWidget(self.wl_spinbox, 0, 1)
        wl_layout.addWidget(self.wl_slider, 1, 0, 1, 2)

        self.current_wl_label = QtWidgets.QLabel("Actual: N/A")
        wl_layout.addWidget(self.current_wl_label, 2, 0, 1, 2)

        # Main Control Group
        control_group = QtWidgets.QGroupBox("Laser Control")
        control_layout = QtWidgets.QGridLayout()
        control_group.setLayout(control_layout)
        main_layout.addWidget(control_group)

        self.laser_on_button = QtWidgets.QPushButton("Laser ON")
        self.laser_off_button = QtWidgets.QPushButton("Laser OFF")
        control_layout.addWidget(self.laser_on_button, 0, 0)
        control_layout.addWidget(self.laser_off_button, 0, 1)

        self.shutter_open_button = QtWidgets.QPushButton("Open Shutter")
        self.shutter_close_button = QtWidgets.QPushButton("Close Shutter")
        control_layout.addWidget(self.shutter_open_button, 1, 0)
        control_layout.addWidget(self.shutter_close_button, 1, 1)

        # Status Display Group
        status_group = QtWidgets.QGroupBox("Laser Status")
        status_layout = QtWidgets.QFormLayout()
        status_group.setLayout(status_layout)
        main_layout.addWidget(status_group)

        self.power_label = QtWidgets.QLabel("N/A")
        status_layout.addRow("Output Power (W):", self.power_label)
        self.laser_status_label = QtWidgets.QLabel("Unknown")
        status_layout.addRow("Laser Status:", self.laser_status_label)

        self.shutter_led = QLED()
        self.shutter_status_label = QtWidgets.QLabel("Unknown")
        shutter_layout = QtWidgets.QHBoxLayout()
        shutter_layout.addWidget(self.shutter_led); shutter_layout.addWidget(self.shutter_status_label)
        status_layout.addRow("Shutter:", shutter_layout)

        self.modelock_led = QLED()
        self.modelock_status_label = QtWidgets.QLabel("Unknown")
        modelock_layout = QtWidgets.QHBoxLayout()
        modelock_layout.addWidget(self.modelock_led); modelock_layout.addWidget(self.modelock_status_label)
        status_layout.addRow("Mode-Lock:", modelock_layout)

        self.warmup_label = QtWidgets.QLabel("N/A")
        status_layout.addRow("Warmup:", self.warmup_label)

        # Diagnostic Info
        diag_group = QtWidgets.QGroupBox("Diagnostics")
        diag_layout = QtWidgets.QFormLayout()
        diag_group.setLayout(diag_layout)
        main_layout.addWidget(diag_group)

        self.pump_power_label = QtWidgets.QLabel("N/A")
        diag_layout.addRow("Pump Power (W):", self.pump_power_label)
        self.diode1_current_label = QtWidgets.QLabel("N/A")
        diag_layout.addRow("Diode 1 Current (A):", self.diode1_current_label)
        self.diode2_current_label = QtWidgets.QLabel("N/A")
        diag_layout.addRow("Diode 2 Current (A):", self.diode2_current_label)


        main_layout.addStretch()

        # --- Connect signals ---
        self.laser_on_button.clicked.connect(self.laser_on_signal)
        self.laser_off_button.clicked.connect(self.laser_off_signal)
        self.shutter_open_button.clicked.connect(self.open_shutter_signal)
        self.shutter_close_button.clicked.connect(self.close_shutter_signal)

        # Wavelength control connections
        self.wl_slider.valueChanged.connect(lambda val: self.wl_spinbox.setValue(val / 10.0))
        self.wl_spinbox.valueChanged.connect(lambda val: self.wl_slider.setValue(int(val * 10)))
        self.wl_spinbox.editingFinished.connect(self.emit_set_wavelength)
        self.wl_slider.sliderReleased.connect(self.emit_set_wavelength)

    def emit_set_wavelength(self):
        """Emit the signal to set a new wavelength."""
        self.set_wavelength_signal.emit(self.wl_spinbox.value())

    # --- Public slots for updating the UI ---
    def update_wavelength(self, value: float):
        self.current_wl_label.setText(f"Actual: {value:.2f} nm")
        self.wl_slider.blockSignals(True)
        self.wl_spinbox.blockSignals(True)
        self.wl_slider.setValue(int(value * 10))
        self.wl_spinbox.setValue(value)
        self.wl_slider.blockSignals(False)
        self.wl_spinbox.blockSignals(False)

    def update_power(self, value: float):
        self.power_label.setText(f"{value:.3f}")

    def update_laser_status(self, status: str):
        is_on = status.lower() == 'on'
        self.laser_status_label.setText(status)
        self.shutter_open_button.setEnabled(is_on)
        self.shutter_close_button.setEnabled(is_on)
        self.wl_spinbox.setEnabled(is_on)
        self.wl_slider.setEnabled(is_on)


    def update_shutter_status(self, status: str):
        self.shutter_status_label.setText(status)
        self.shutter_led.set_as(status.lower() == 'open')

    def update_modelock_status(self, status: str, is_locked: bool):
        self.modelock_status_label.setText(status)
        self.modelock_led.set_as(is_locked)

    def update_warmup_time(self, status: str):
        self.warmup_label.setText(status)

    def update_pump_power(self, value: float):
        self.pump_power_label.setText(f"{value:.3f}")

    def update_diode1_current(self, value: float):
        self.diode1_current_label.setText(f"{value:.2f}")

    def update_diode2_current(self, value: float):
        self.diode2_current_label.setText(f"{value:.2f}")


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = MaiTaiUI()
    widget.show()
    app.exec_()
