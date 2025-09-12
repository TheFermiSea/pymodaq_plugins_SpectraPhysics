import serial
import time
import logging
from pymodaq.utils.daq_utils import ThreadCommand
from pymodaq_utils.logger import set_logger

set_logger('MaiTaiController')
logger = logging.getLogger('MaiTaiController')

class MaiTaiController:
    """
    Controller for the Spectra-Physics MaiTai Ti:Sapphire laser.
    """
    def __init__(self, port, baudrate=9600, timeout=1, mock_mode=False):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.mock_mode = mock_mode
        self.ser = None
        self.is_connected = False
        
        if self.mock_mode:
            self._mock_wavelength = 800.0
            self._mock_power = 1.5
            self._mock_shutter = 'Closed'
            self._mock_on = True
            self._mock_modelocked = True

    def _send_command(self, command, expect_reply=True, timeout=None):
        if self.mock_mode:
            logger.info(f"Mock command: {command}")
            if command == '?WAV': return str(self._mock_wavelength)
            if command.startswith('WAV='): self._mock_wavelength = float(command.split('=')[1]); return 'OK'
            if command == '?P': return str(self._mock_power)
            if command == '?S': return 'OK'
            if command == '?SHUTTER': return self._mock_shutter
            if command == 'SHUTTER=1': self._mock_shutter = 'Open'; return 'OK'
            if command == 'SHUTTER=0': self._mock_shutter = 'Closed'; return 'OK'
            if command == 'ON': self._mock_on = True; return 'OK'
            if command == 'OFF': self._mock_on = False; return 'OK'
            if command == '?ST': return '420' if self._mock_modelocked else '400'
            if command == '?WH': return '1234.5'
            return 'OK'

        if not self.ser:
            raise ConnectionError("Serial port not open.")
        
        self.ser.write((command + '\r\n').encode())
        time.sleep(0.1) # Give the device time to respond
        
        if expect_reply:
            reply_timeout = timeout if timeout is not None else self.timeout
            start_time = time.time()
            response = ''
            while time.time() - start_time < reply_timeout:
                if self.ser.in_waiting > 0:
                    response += self.ser.read(self.ser.in_waiting).decode()
                    if '\n' in response:
                        break
            
            response = response.strip()
            if "Error" in response:
                logger.error(f"MaiTai Error for command '{command}': {response}")
                raise IOError(f"MaiTai command failed: {response}")
            return response
        return None

    def connect(self):
        if self.mock_mode:
            self.is_connected = True
            return True
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            self.is_connected = True
            logger.info("MaiTai connected successfully.")
            return True
        except serial.SerialException as e:
            logger.error(f"Failed to connect to MaiTai on {self.port}: {e}")
            self.is_connected = False
            return False

    def disconnect(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
        self.is_connected = False
        logger.info("MaiTai disconnected.")

    def get_wavelength(self):
        reply = self._send_command('?WAV')
        return float(reply)

    def set_wavelength(self, wavelength: float):
        reply = self._send_command(f'WAV={wavelength:.1f}')
        return 'OK' in reply

    def get_power(self):
        reply = self._send_command('?P')
        return float(reply)

    def get_shutter_state(self):
        reply = self._send_command('?SHUTTER')
        return 'Open' if '1' in reply else 'Closed'

    def open_shutter(self):
        reply = self._send_command('SHUTTER=1')
        return 'OK' in reply

    def close_shutter(self):
        reply = self._send_command('SHUTTER=0')
        return 'OK' in reply

    def laser_on(self):
        reply = self._send_command('ON')
        return 'OK' in reply

    def laser_off(self):
        reply = self._send_command('OFF')
        return 'OK' in reply

    def get_laser_status(self):
        # Using a general query as there's no direct status command for ON/OFF
        # We infer it's on if we can communicate. A better check might be needed.
        if self.mock_mode:
             return "On" if self._mock_on else "Off"
        try:
            self._send_command('?S', expect_reply=True) # A general status query
            # In a real scenario, you might need a more specific command if available
            # Or parse the detailed status from '?ST'
            return "On"
        except Exception:
            return "Off"


    def is_mode_locked(self):
        status_code = int(self._send_command('?ST'))
        # Based on manual Appendix C
        if status_code in [420, 421, 422, 423]:
            return True, "Mode-locked"
        elif status_code in [400, 401, 402, 403]:
            return False, "Not Mode-locked"
        else:
            return False, "Unknown"
    
    def get_warmup_time(self):
        reply = self._send_command('?WH')
        try:
            hours = float(reply)
            minutes = int((hours * 60) % 60)
            return f"{int(hours)}h {minutes}min"
        except ValueError:
            return reply
