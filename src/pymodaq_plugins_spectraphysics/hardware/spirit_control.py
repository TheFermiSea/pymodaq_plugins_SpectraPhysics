import socket
import time
import logging
from pymodaq_utils.logger import set_logger

set_logger('SpiritController')
logger = logging.getLogger('SpiritController')

try:
    import can
    can_available = True
except ImportError:
    can_available = False
    logger.warning("The 'python-can' library is not installed. CAN bus communication will not be available.")


class SpiritController:
    """
    Controller for the Spectra-Physics Spirit laser, supporting TCP/IP and CAN communication.
    """
    def __init__(self, protocol, ip_address=None, port=None, can_interface=None, can_channel=None, mock_mode=False):
        self.protocol = protocol
        self.ip_address = ip_address
        self.port = port
        self.can_interface = can_interface
        self.can_channel = can_channel
        self.mock_mode = mock_mode
        self.is_connected = False
        
        self.connection = None  # Will hold either socket or can.Bus object

        if self.mock_mode:
            self._mock_rep_rate = 1000.0  # in kHz
            self._mock_power = 8.5
            self._mock_shutter = '0' # Closed
            self._mock_on = True
            self._mock_status = 0b11 # System OK, Laser ON

    def _send_command(self, command, expect_reply=True, timeout=1.0):
        if self.mock_mode:
            logger.info(f"Mock command: {command}")
            if command == '*IDN?': return "Spectra-Physics, Spirit, 12345, Mock v1.0"
            if command == 'REP_RATE?': return str(self._mock_rep_rate)
            if command.startswith('REP_RATE='): self._mock_rep_rate = float(command.split('=')[1]); return ""
            if command == 'POWER?': return str(self._mock_power)
            if command == 'SHUTTER?': return self._mock_shutter
            if command == 'SHUTTER=1': self._mock_shutter = '1'; return ""
            if command == 'SHUTTER=0': self._mock_shutter = '0'; return ""
            if command == 'ON': self._mock_on = True; return ""
            if command == 'OFF': self._mock_on = False; return ""
            if command == 'STATUS?': return str(self._mock_status)
            if command == 'WARMUP?': return "0"
            return ""

        full_command = (command + '\r').encode()
        
        if self.protocol == 'tcpip':
            if not isinstance(self.connection, socket.socket):
                raise ConnectionError("TCP/IP socket not open.")
            
            self.connection.sendall(full_command)
            if expect_reply:
                self.connection.settimeout(timeout)
                response = self.connection.recv(1024).decode().strip()
                if 'ERROR' in response:
                    raise IOError(f"Spirit command '{command}' failed: {response}")
                return response

        elif self.protocol == 'can':
            if not can_available or not isinstance(self.connection, can.Bus):
                raise ConnectionError("CAN bus not available or not open.")
            
            # CAN communication requires specific message IDs and data formatting
            # This is a placeholder and needs to be adapted to the Spirit's CAN protocol specifics
            # Assuming command strings are sent with a specific arbitration ID
            msg = can.Message(arbitration_id=0x123, data=full_command, is_extended_id=False)
            self.connection.send(msg)
            
            if expect_reply:
                # Listening for a response requires a more complex setup, often asynchronous
                # This is a simplified synchronous example
                response_msg = self.connection.recv(timeout)
                if response_msg:
                    return response_msg.data.decode().strip()
                else:
                    raise TimeoutError("No response received on CAN bus.")
        return ""

    def connect(self):
        if self.mock_mode:
            self.is_connected = True
            logger.info("Spirit Controller connected in mock mode.")
            return True
            
        try:
            if self.protocol == 'tcpip':
                self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.connection.connect((self.ip_address, self.port))
                self.is_connected = True
                logger.info(f"Spirit connected via TCP/IP at {self.ip_address}:{self.port}")
            
            elif self.protocol == 'can':
                if not can_available:
                    raise ImportError("The 'python-can' library is required for CAN communication.")
                self.connection = can.Bus(interface=self.can_interface, channel=self.can_channel)
                self.is_connected = True
                logger.info(f"Spirit connected via CAN on {self.can_interface}:{self.can_channel}")

            return True

        except Exception as e:
            logger.error(f"Failed to connect to Spirit laser: {e}")
            self.is_connected = False
            return False

    def disconnect(self):
        if self.connection:
            if self.protocol == 'tcpip':
                self.connection.close()
            elif self.protocol == 'can':
                self.connection.shutdown()
        self.is_connected = False
        logger.info("Spirit laser disconnected.")

    # --- Command Methods ---
    def get_rep_rate(self):
        reply = self._send_command('REP_RATE?')
        return float(reply)

    def set_rep_rate(self, rate_khz: float):
        self._send_command(f'REP_RATE={rate_khz}', expect_reply=False)

    def get_power(self):
        reply = self._send_command('POWER?')
        return float(reply)
        
    def get_shutter_state(self):
        reply = self._send_command('SHUTTER?')
        return 'Open' if reply == '1' else 'Closed'

    def open_shutter(self):
        self._send_command('SHUTTER=1', expect_reply=False)

    def close_shutter(self):
        self._send_command('SHUTTER=0', expect_reply=False)

    def laser_on(self):
        self._send_command('ON', expect_reply=False)

    def laser_off(self):
        self._send_command('OFF', expect_reply=False)
        
    def get_status(self):
        reply = self._send_command('STATUS?')
        return int(reply)

    def get_warmup_time(self):
        """Returns warmup time in minutes."""
        reply = self._send_command('WARMUP?')
        return int(reply)
