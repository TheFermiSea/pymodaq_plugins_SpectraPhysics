from pymodaq.control_modules.move_utility_classes import DAQ_Move_base, comon_parameters_fun, main
from pymodaq.utils.daq_utils import ThreadCommand, get_logger
from pymodaq_data.datamodel import DataActuator
from qtpy.QtCore import Signal, QTimer

from pymodaq_plugins_spectraphysics.hardware.spirit_control import SpiritController
from pymodaq_plugins_spectraphysics import config

logger = get_logger('daq_move_Spirit')
spirit_config = config.get_hardware_config("spirit")

class DAQ_Move_Spirit(DAQ_Move_base):
    """
    PyMoDAQ plugin for controlling SpectraPhysics Spirit laser.
    The main actuator is the repetition rate.
    """

    _ui_file = "spirit_ui.py"
    _ui_class_name = "SpiritUI"
    
    _controller_units = "kHz"
    is_multiaxes = False
    _axis_names = ["RepRate"]
    _epsilon = 1

    # Signals for UI updates
    power_signal = Signal(float)
    rep_rate_signal = Signal(float)
    shutter_status_signal = Signal(str)
    status_signal = Signal(int)
    warmup_time_signal = Signal(int)

    params = comon_parameters_fun(
        is_multiaxes=False, axis_names=_axis_names, epsilon=_epsilon
    ) + [
        {"title": "Repetition Rate Bounds:", "name": "bounds_group", "type": "group", "children": [
            {"title": "Min Rep Rate (kHz):", "name": "min_position", "type": "float", "value": 1.0},
            {"title": "Max Rep Rate (kHz):", "name": "max_position", "type": "float", "value": 1000.0},
        ]},
        {"title": "Connection:", "name": "connection_group", "type": "group", "children": [
            {"title": "Protocol:", "name": "protocol", "type": "list", "limits": ["tcpip", "can"], "value": "tcpip"},
            {"title": "TCP/IP Address:", "name": "ip_address", "type": "str", "value": spirit_config.get("ip_address", "192.168.1.222")},
            {"title": "TCP/IP Port:", "name": "port", "type": "int", "value": spirit_config.get("port", 10001)},
            {"title": "CAN Interface:", "name": "can_interface", "type": "str", "value": spirit_config.get("can_interface", "pcan")},
            {"title": "CAN Channel:", "name": "can_channel", "type": "str", "value": spirit_config.get("can_channel", "PCAN_USBBUS1")},
            {"title": "Mock Mode:", "name": "mock_mode", "type": "bool", "value": False},
        ]},
        {"title": "Polling Interval (ms):", "name": "polling_interval", "type": "int", "value": 1000, "min": 100},
    ]

    def ini_attributes(self):
        self.controller: SpiritController = None
        self.ui: SpiritUI = None
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.poll_status)

    def commit_settings(self, param):
        if param.name() == 'protocol':
            is_tcp = param.value() == 'tcpip'
            self.settings.child('connection_group', 'ip_address').show(is_tcp)
            self.settings.child('connection_group', 'port').show(is_tcp)
            self.settings.child('connection_group', 'can_interface').show(not is_tcp)
            self.settings.child('connection_group', 'can_channel').show(not is_tcp)

    def ini_stage(self, controller=None):
        self.initialized = False
        try:
            p = self.settings.child('connection_group')
            self.controller = SpiritController(
                protocol=p.child('protocol').value(),
                ip_address=p.child('ip_address').value(),
                port=p.child('port').value(),
                can_interface=p.child('can_interface').value(),
                can_channel=p.child('can_channel').value(),
                mock_mode=p.child('mock_mode').value()
            )
            
            if not self.controller.connect():
                raise ConnectionError("Failed to connect to Spirit hardware")

            info = "Spirit Laser connected successfully."
            self.emit_status(ThreadCommand("Update_Status", [info, "log"]))
            
            if self.ui:
                self.ui.laser_on_signal.connect(self.laser_on)
                self.ui.laser_off_signal.connect(self.laser_off)
                self.ui.open_shutter_signal.connect(self.open_shutter)
                self.ui.close_shutter_signal.connect(self.close_shutter)
                
                self.power_signal.connect(self.ui.update_power)
                self.rep_rate_signal.connect(self.ui.update_rep_rate)
                self.shutter_status_signal.connect(self.ui.update_shutter_status)
                self.status_signal.connect(self.ui.update_status)
                self.warmup_time_signal.connect(self.ui.update_warmup_time)

            self.status_timer.start(self.settings.child('polling_interval').value())
            self.poll_status()
            self.commit_settings(p.child('protocol')) # set initial visibility

            self.initialized = True
            return info, True
        except Exception as e:
            self.emit_status(ThreadCommand("Update_Status", [f"Initialization failed: {e}", "error"]))
            return f"Failed to initialize Spirit: {e}", False

    def close(self):
        self.status_timer.stop()
        if self.controller: self.controller.disconnect()

    def check_bound(self, value):
        min_val = self.settings.child('bounds_group', 'min_position').value()
        max_val = self.settings.child('bounds_group', 'max_position').value()
        return np.clip(value, min_val, max_val)

    def get_actuator_value(self):
        return DataActuator(self.controller.get_rep_rate())

    def move_abs(self, position: DataActuator):
        try:
            target = self.check_bound(position.value())
            self.controller.set_rep_rate(target)
            self.poll_status()
            position.set_value(self.controller.get_rep_rate())
        except Exception as e:
            self.emit_status(ThreadCommand("Update_Status", [f"Error setting rep rate: {e}", "error"]))
        finally:
            self.move_done(position)

    def move_rel(self, position: DataActuator):
        current_pos = self.get_actuator_value()
        self.move_abs(current_pos + position)

    def move_home(self):
        self.move_abs(DataActuator(1000.0)) # Default home to 1MHz

    def stop_motion(self):
        self.move_done(self.get_actuator_value())

    def poll_status(self):
        try:
            if not self.controller or not self.controller.is_connected: return
            self.power_signal.emit(self.controller.get_power())
            self.rep_rate_signal.emit(self.controller.get_rep_rate())
            self.shutter_status_signal.emit(self.controller.get_shutter_state())
            self.status_signal.emit(self.controller.get_status())
            self.warmup_time_signal.emit(self.controller.get_warmup_time())
        except Exception as e:
            logger.warning(f"Status polling failed: {e}")

    def laser_on(self):
        self.controller.laser_on()
        self.poll_status()

    def laser_off(self):
        self.controller.laser_off()
        self.poll_status()
        
    def open_shutter(self):
        self.controller.open_shutter()
        self.poll_status()

    def close_shutter(self):
        self.controller.close_shutter()
        self.poll_status()

if __name__ == "__main__":
    main(__file__)
