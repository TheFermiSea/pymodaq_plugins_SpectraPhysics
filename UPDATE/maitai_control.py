import serial
import time
import logging
from pymodaq_utils.logger import set_logger

set_logger('MaiTaiController')
logger = logging.getLogger('MaiTaiController')

class MaiTaiController:
    """
    Controller for the Spectra-Physics MaiTai Ti:Sapphire laser.
    This version uses the official SCPI commands as documented in the user manual.
    """
    def __init__(self, port, baudrate=9600, timeout=2, mock_mode=False):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.mock_mode = mock_mode
        self.ser = None
        self.is_connected = False

        # Mock mode attributes for testing without hardware
        if self.mock_mode:
            self._mock_wavelength = 800.0
            self._mock_power = 1.5
            self._mock_shutter = '0' # '0' for Closed, '1' for Open
            self._mock_on = True
            self._mock_modelocked_bit = 4 # Bit 2, value 4
            self._mock_warmup_percent = 100
            self._mock_pump_power = 5.0
            self._mock_diode1_current = 21.0
            self._mock_diode2_current = 22.0

    def _send_command(self, command, expect_reply=True, timeout_s=None):
        """Sends a command to the laser and returns the response."""
        if self.mock_mode:
            logger.info(f"Mock command: {command}")
            # Wavelength
            if command == 'READ:WAVelength?': return str(self._mock_wavelength)
            if command.startswith('WAVelength '): self._mock_wavelength = float(command.split(' ')[1]); return 'OK'
            if command == 'WAVelength:MAX?': return '1000.0'
            if command == 'WAVelength:MIN?': return '700.0'
            # Power
            if command == 'READ:POWer?': return str(self._mock_power)
            if command == 'READ:PLASer:POWer?': return str(self._mock_pump_power)
            # Shutter
            if command == 'SHUTter?': return self._mock_shutter
            if command == 'SHUTter 1': self._mock_shutter = '1'; return 'OK'
            if command == 'SHUTter 0': self._mock_shutter = '0'; return 'OK'
            # Laser State
            if command == 'ON': self._mock_on = True; return 'OK'
            if command == 'OFF': self._mock_on = False; return 'OK'
            # Status & Diags
            if command == '*STB?': return str(self._mock_modelocked_bit if self._mock_on else 0)
            if command == 'READ:PCTWarmedup?': return f"{self._mock_warmup_percent}%"
            if command == 'READ:PLASer:DIODe1:CURRent?': return str(self._mock_diode1_current)
            if command == 'READ:PLASer:DIODe2:CURRent?': return str(self._mock_diode2_current)
            if command == 'SYSTem:ERR?': return "0, No error"
            if command == 'PLASer:ERRCode?': return '0'
            if command == 'PLASer:HISTory?': return '001 002 003'
            return 'OK'

        if not self.ser or not self.ser.is_open:
            raise ConnectionError("Serial port is not open.")

        self.ser.reset_input_buffer()
        self.ser.write((command + '\r\n').encode())
        logger.debug(f"Sent: {command}")

        if expect_reply:
            reply_timeout = timeout_s if timeout_s is not None else self.timeout
            start_time = time.time()
            response_bytes = b''
            while time.time() - start_time < reply_timeout:
                if self.ser.in_waiting > 0:
                    response_bytes += self.ser.read(self.ser.in_waiting)
                    if b'\n' in response_bytes:
                        break
                time.sleep(0.05)

            response = response_bytes.decode().strip()
            logger.debug(f"Received: {response}")

            if not response or "Error" in response:
                logger.error(f"MaiTai Error for command '{command}': {response}")
                raise IOError(f"MaiTai command failed or returned an error: {response}")
            return response
        return None

    def connect(self):
        """Establishes the serial connection."""
        if self.mock_mode:
            self.is_connected = True
            logger.info("MaiTai controller is in Mock Mode.")
            return True
        try:
            self.ser = serial.Serial(
                port=self.port, baudrate=self.baudrate, timeout=self.timeout, xonxoff=True
            )
            self.is_connected = self.ser.is_open
            if self.is_connected:
                logger.info(f"MaiTai connected successfully on {self.port}.")
                self.get_id()
            return self.is_connected
        except serial.SerialException as e:
            logger.error(f"Failed to connect to MaiTai on {self.port}: {e}")
            self.is_connected = False
            return False

    def disconnect(self):
        """Closes the serial connection."""
        if self.ser and self.ser.is_open:
            self.ser.close()
        self.is_connected = False
        logger.info("MaiTai disconnected.")

    # -----------------------------------------------------
    # PRIMARY USER COMMANDS
    # -----------------------------------------------------
    def get_id(self):
        return self._send_command('*IDN?')

    def get_wavelength(self):
        reply = self._send_command('READ:WAVelength?')
        return float(reply)

    def set_wavelength(self, wavelength: float):
        self._send_command(f'WAVelength {wavelength:.1f}', expect_reply=False)
        return True

    def get_power(self):
        reply = self._send_command('READ:POWer?')
        return float(reply)

    def get_shutter_state(self):
        reply = self._send_command('SHUTter?')
        return 'Open' if '1' in reply else 'Closed'

    def open_shutter(self):
        self._send_command('SHUTter 1', expect_reply=False)
        return True

    def close_shutter(self):
        self._send_command('SHUTter 0', expect_reply=False)
        return True

    def laser_on(self):
        self._send_command('ON', expect_reply=False)
        return True

    def laser_off(self):
        self._send_command('OFF', expect_reply=False)
        return True

    def get_laser_status(self):
        if self.mock_mode: return "On" if self._mock_on else "Off"
        try:
            self._send_command('*STB?', expect_reply=True)
            return "On"
        except (IOError, ConnectionError):
            return "Off"

    def is_mode_locked(self):
        reply = self._send_command('*STB?')
        try:
            status_byte = int(reply)
            is_locked = (status_byte & 4) != 0
            status_str = "Mode-locked" if is_locked else "Not Mode-locked"
            return is_locked, status_str
        except (ValueError, IndexError) as e:
            logger.error(f"Could not parse status byte: {reply}. Error: {e}")
            return False, "Status Error"

    def get_warmup_time(self):
        return self._send_command('READ:PCTWarmedup?')

    # -----------------------------------------------------
    # SYSTEM & DIAGNOSTIC COMMANDS
    # -----------------------------------------------------
    def get_min_wavelength(self):
        return float(self._send_command('WAVelength:MIN?'))

    def get_max_wavelength(self):
        return float(self._send_command('WAVelength:MAX?'))

    def get_pump_power(self):
        return float(self._send_command('READ:PLASer:POWer?'))

    def get_diode_current(self, diode_num: int):
        if diode_num not in [1, 2]: raise ValueError("Diode number must be 1 or 2")
        return float(self._send_command(f'READ:PLASer:DIODe{diode_num}:CURRent?'))

    def get_diode_temperature(self, diode_num: int):
        if diode_num not in [1, 2]: raise ValueError("Diode number must be 1 or 2")
        return float(self._send_command(f'READ:PLASer:DIODe{diode_num}:TEMPerature?'))

    def get_shg_status(self):
        return self._send_command('READ:PLASer:SHGS?')

    def get_history(self):
        return self._send_command('PLASer:HISTory?')

    def get_history_ascii(self):
        return self._send_command('PLASer:AHISTory?')

    def get_pump_error_code(self):
        return self._send_command('PLASer:ERRCode?')

    def get_system_error(self):
        return self._send_command('SYSTem:ERR?')

    def save_settings(self):
        self._send_command('SAVE', expect_reply=False)
        return True

    def set_watchdog(self, seconds: int):
        self._send_command(f'TIMer:WATChdog {seconds}', expect_reply=False)
        return True

    def set_baud_rate(self, baud: int):
        self._send_command(f'SYSTem:COMMunications:SERial:BAUD {baud}', expect_reply=False)
        return True

    # -----------------------------------------------------
    # DIAGNOSTIC-ONLY COMMANDS (Use with caution)
    # -----------------------------------------------------
    def set_pump_mode(self, mode: str):
        """DANGEROUS: For diagnostic use only. Sets pump mode to 'PPOWer' or 'PCURrent'."""
        if mode not in ['PPOWer', 'PCURrent']: raise ValueError("Mode must be 'PPOWer' or 'PCURrent'")
        logger.warning("Setting pump mode directly. This is for diagnostic use only.")
        return 'OK' in self._send_command(f'MODE {mode}')

    def set_pump_power(self, power: float):
        """DANGEROUS: For diagnostic use only. Sets pump laser output power."""
        logger.warning("Setting pump power directly. This is for diagnostic use only.")
        return 'OK' in self._send_command(f'PLASer:POWer {power:.2f}')
