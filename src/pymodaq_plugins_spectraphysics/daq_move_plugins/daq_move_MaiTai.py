import numpy as np
import logging
from pymodaq.control_modules.move_utility_classes import DAQ_Move_base, comon_parameters_fun, main
from pymodaq.utils.daq_utils import ThreadCommand
from pymodaq_utils.logger import set_logger
from pymodaq_data.data import DataRaw as DataActuator
from qtpy.QtCore import Signal, QTimer

from pymodaq_plugins_spectraphysics.hardware.maitai_control import MaiTaiController
from pymodaq_plugins_spectraphysics.daq_move_plugins.maitai_ui import MaiTaiUI
from pymodaq_plugins_spectraphysics import config

set_logger('daq_move_MaiTai')
logger = logging.getLogger('daq_move_MaiTai')
maitai_config = config.get_hardware_config("maitai")


class DAQ_Move_MaiTai(DAQ_Move_base):
    """
    PyMoDAQ plugin for controlling SpectraPhysics MaiTai Ti:Sapphire laser.
    Features a custom UI for comprehensive laser status and control.
    """

    
    _controller_units = "nm"
    is_multiaxes = False
    _axis_names = ["Wavelength"]
    _epsilon = 0.1

    # Signals for UI updates
    power_signal = Signal(float)
    wavelength_signal = Signal(float)
    shutter_status_signal = Signal(str)
    modelock_status_signal = Signal(str, bool)
    laser_status_signal = Signal(str)
    warmup_time_signal = Signal(str)

    params = comon_parameters_fun(
        is_multiaxes=False, axis_names=_axis_names, epsilon=_epsilon
    ) + [
        {"title": "Wavelength Bounds:", "name": "bounds_group", "type": "group", "children": [
            {"title": "Min Wavelength (nm):", "name": "min_position", "type": "float", "value": maitai_config.get('wavelength_range_min', 700.0)},
            {"title": "Max Wavelength (nm):", "name": "max_position", "type": "float", "value": maitai_config.get('wavelength_range_max', 1000.0)},
        ]},
        {"title": "Connection:", "name": "connection_group", "type": "group", "children": [
            {"title": "Serial Port:", "name": "serial_port", "type": "str", "value": maitai_config.get("serial_port", "COM1")},
            {"title": "Baudrate:", "name": "baudrate", "type": "list", "limits": [9600, 19200], "value": maitai_config.get("baudrate", 9600)},
            {"title": "Timeout (s):", "name": "timeout", "type": "float", "value": 2.0},
            {"title": "Mock Mode:", "name": "mock_mode", "type": "bool", "value": False},
        ]},
        {"title": "Polling Interval (ms):", "name": "polling_interval", "type": "int", "value": 1000, "min": 100},
    ]

    def ini_attributes(self):
        self.controller: MaiTaiController = None
        self.ui: MaiTaiUI = None
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.poll_status)

    def ini_stage(self, controller=None):
        self.initialized = False
        try:
            port = self.settings.child("connection_group", "serial_port").value()
            baudrate = self.settings.child("connection_group", "baudrate").value()
            timeout = self.settings.child("connection_group", "timeout").value()
            mock_mode = self.settings.child("connection_group", "mock_mode").value()

            self.controller = MaiTaiController(port=port, baudrate=baudrate, timeout=timeout, mock_mode=mock_mode)
            
            if not self.controller.connect():
                raise ConnectionError("Failed to connect to MaiTai hardware")

            info = f"MaiTai Laser connected on {port}"
            self.emit_status(ThreadCommand("Update_Status", [info, "log"]))
            
            if self.ui:
                self.ui.laser_on_signal.connect(self.laser_on)
                self.ui.laser_off_signal.connect(self.laser_off)
                self.ui.open_shutter_signal.connect(self.open_shutter)
                self.ui.close_shutter_signal.connect(self.close_shutter)
                
                self.power_signal.connect(self.ui.update_power)
                self.wavelength_signal.connect(self.ui.update_wavelength)
                self.shutter_status_signal.connect(self.ui.update_shutter_status)
                self.modelock_status_signal.connect(self.ui.update_modelock_status)
                self.laser_status_signal.connect(self.ui.update_laser_status)
                self.warmup_time_signal.connect(self.ui.update_warmup_time)

            polling_interval = self.settings.child("polling_interval").value()
            self.status_timer.start(polling_interval)
            self.poll_status()

            self.initialized = True
            return info, True
        except Exception as e:
            self.emit_status(ThreadCommand("Update_Status", [f"Initialization failed: {e}", "error"]))
            return f"Failed to initialize MaiTai: {e}", False

    def close(self):
        self.status_timer.stop()
        if self.controller:
            self.controller.disconnect()
        self.emit_status(ThreadCommand("Update_Status", ["MaiTai connection closed", "log"]))

    def check_bound(self, wavelength):
        min_wl = self.settings.child("bounds_group", "min_position").value()
        max_wl = self.settings.child("bounds_group", "max_position").value()
        return np.clip(wavelength, min_wl, max_wl)

    def get_actuator_value(self):
        try:
            wavelength = self.controller.get_wavelength()
            return DataActuator(wavelength)
        except Exception as e:
            self.emit_status(ThreadCommand("Update_Status", [f"Error reading wavelength: {e}", "error"]))
            return DataActuator(0)

    def move_abs(self, position: DataActuator):
        try:
            target_wavelength = self.check_bound(position.value())
            if not self.controller.set_wavelength(target_wavelength):
                raise IOError("Failed to set wavelength.")
            self.emit_status(ThreadCommand("Update_Status", [f"Moving to {target_wavelength} nm", "log"]))
            position.set_value(self.controller.get_wavelength())
            self.poll_status()
        except Exception as e:
            self.emit_status(ThreadCommand("Update_Status", [f"Error moving: {e}", "error"]))
        finally:
            self.move_done(position)

    def move_rel(self, position: DataActuator):
        current_pos = self.get_actuator_value()
        self.move_abs(current_pos + position)

    def move_home(self):
        self.move_abs(DataActuator(800.0))

    def stop_motion(self):
        self.move_done(self.get_actuator_value())

    def poll_status(self):
        try:
            if not self.controller or not self.controller.is_connected: return
            
            self.power_signal.emit(self.controller.get_power())
            self.wavelength_signal.emit(self.controller.get_wavelength())
            self.shutter_status_signal.emit(self.controller.get_shutter_state())
            locked, status_str = self.controller.is_mode_locked()
            self.modelock_status_signal.emit(status_str, locked)
            self.laser_status_signal.emit(self.controller.get_laser_status())
            self.warmup_time_signal.emit(self.controller.get_warmup_time())
        except Exception as e:
            logger.warning(f"Status polling failed: {e}")

    def laser_on(self):
        if self.controller.laser_on(): logger.info("Laser turned ON")
        else: logger.error("Failed to turn laser ON")
        self.poll_status()

    def laser_off(self):
        if self.controller.laser_off(): logger.info("Laser turned OFF")
        else: logger.error("Failed to turn laser OFF")
        self.poll_status()
        
    def open_shutter(self):
        if self.controller.open_shutter(): logger.info("Shutter opened")
        else: logger.error("Failed to open shutter")
        self.poll_status()

    def close_shutter(self):
        if self.controller.close_shutter(): logger.info("Shutter closed")
        else: logger.error("Failed to close shutter")
        self.poll_status()

if __name__ == "__main__":
    main(__file__)
