#!/usr/bin/env python3
"""
MaiTai Port Scanner and Configuration Utility - Threaded Version

Automatically scans USB serial ports in parallel to locate the SpectraPhysics
MaiTai laser, tests communication using proper SCPI commands, and updates the
hardware configuration file with the correct port settings.

Requirements:
    - pyserial
    - rich (optional for formatting)

Usage:
    python find_maitai_port_threaded.py [--config-path <path>] [--test-only] [--verbose]
"""

import argparse
import glob
import serial
import time
import tomllib
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional, Tuple, Dict, Any, List

try:
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.panel import Panel
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Warning: rich not available, using plain output")


class MaiTaiPortScanner:
    """Threaded scanner to locate MaiTai laser on USB serial ports"""

    # MaiTai communication settings from manual
    SERIAL_SETTINGS = {
        'baudrate': 9600,
        'bytesize': serial.EIGHTBITS,
        'parity': serial.PARITY_NONE,
        'stopbits': serial.STOPBITS_ONE,
        'xonxoff': True,  # XON/XOFF flow control
        'rtscts': False,  # Do NOT use hardware RTS/CTS
        'timeout': 0.8  # Reduced timeout for faster scanning
    }

    # SCPI test commands to verify MaiTai communication
    TEST_COMMANDS = [
        'READ:WAVELENGTH?',
        'READ:WAVE?',
        '*IDN?',
        'READ:PLAS:POW?'
    ]

    def __init__(self, verbose: bool = False, max_workers: int = 6):
        self.verbose = verbose
        self.console = Console() if RICH_AVAILABLE else None
        self.max_workers = max_workers
        self._lock = threading.Lock()

    def get_usb_serial_ports(self) -> List[str]:
        """Get list of available USB serial ports"""
        ports = glob.glob('/dev/ttyUSB*')
        return sorted(ports)

    def test_port_communication(self, port: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Test if MaiTai responds on given port

        Returns:
            Tuple of (success, response, error_message)
        """
        try:
            with serial.Serial(port, **self.SERIAL_SETTINGS) as ser:
                time.sleep(0.3)  # Allow connection to stabilize

                # Clear any existing data
                ser.flushInput()
                ser.flushOutput()

                for cmd in self.TEST_COMMANDS:
                    command = f"{cmd}\r\n"
                    ser.write(command.encode('ascii'))
                    time.sleep(0.4)  # Reduced wait time for faster scanning

                    if ser.in_waiting > 0:
                        try:
                            raw_response = ser.readline()
                            response = raw_response.decode('ascii').strip()
                            if response and len(response) > 0:
                                return True, response, None
                        except UnicodeDecodeError:
                            # Non-ASCII response suggests different device
                            continue

                return False, None, "No valid SCPI response"

        except serial.SerialException as e:
            return False, None, f"Serial error: {str(e)[:50]}"
        except Exception as e:
            return False, None, f"Error: {str(e)[:50]}"

    def scan_ports_parallel(self) -> Optional[Tuple[str, str]]:
        """
        Scan all USB serial ports for MaiTai laser using parallel threading

        Returns:
            Tuple of (port, response) if found, None otherwise
        """
        ports = self.get_usb_serial_ports()

        if not ports:
            self._print_message("No USB serial ports found", "red")
            return None

        self._print_message(f"Scanning {len(ports)} USB serial ports in parallel for MaiTai laser...", "blue")

        if RICH_AVAILABLE and self.console:
            return self._scan_with_rich_progress(ports)
        else:
            return self._scan_with_plain_output(ports)

    def _scan_with_rich_progress(self, ports: List[str]) -> Optional[Tuple[str, str]]:
        """Scan ports with rich progress display"""
        found_result = None
        completed_ports = set()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:

            # Create a single task for overall progress
            main_task = progress.add_task("Scanning ports in parallel...", total=None)

            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Submit all port tests
                future_to_port = {
                    executor.submit(self.test_port_communication, port): port
                    for port in ports
                }

                # Process completed tests as they finish
                for future in as_completed(future_to_port):
                    port = future_to_port[future]

                    try:
                        success, response, error = future.result()
                        completed_ports.add(port)

                        if success and found_result is None:
                            found_result = (port, response)
                            # Cancel remaining tasks
                            for remaining_future in future_to_port:
                                if remaining_future != future:
                                    remaining_future.cancel()
                            break

                        if self.verbose and error:
                            progress.console.print(f"[dim]{port}: {error}[/dim]")

                    except Exception as e:
                        if self.verbose:
                            progress.console.print(f"[dim]{port}: Exception: {e}[/dim]")

            progress.remove_task(main_task)

            if found_result:
                port, response = found_result
                self.console.print(f"[green]MaiTai found on {port}[/green]")
                self.console.print(f"[dim]Response: {response}[/dim]")
                return found_result

        return None

    def _scan_with_plain_output(self, ports: List[str]) -> Optional[Tuple[str, str]]:
        """Scan ports with plain text output"""
        found_result = None
        results = {}

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all port tests
            future_to_port = {
                executor.submit(self.test_port_communication, port): port
                for port in ports
            }

            # Process results as they complete
            for future in as_completed(future_to_port):
                port = future_to_port[future]

                try:
                    success, response, error = future.result()
                    results[port] = (success, response, error)

                    if success and found_result is None:
                        found_result = (port, response)
                        # Cancel remaining futures
                        for remaining_future in future_to_port:
                            if remaining_future != future:
                                remaining_future.cancel()
                        break

                except Exception as e:
                    results[port] = (False, None, f"Exception: {str(e)[:50]}")

        if found_result:
            port, response = found_result
            print(f"{port}: SUCCESS - Response: {response}")
            return found_result

        # Print all results for verbose mode
        if self.verbose:
            for port in sorted(ports):
                if port in results:
                    success, response, error = results[port]
                    if not success:
                        print(f"{port}: {error if error else 'No response'}")

        return None

    def _print_message(self, message: str, style: str = None):
        """Thread-safe message printing"""
        with self._lock:
            if self.console and style:
                self.console.print(f"[{style}]{message}[/{style}]")
            else:
                print(message)

    def update_config_file(self, port: str, config_path: Path) -> bool:
        """
        Update hardware configuration file with discovered port

        Args:
            port: The serial port where MaiTai was found
            config_path: Path to hardware_config.toml

        Returns:
            True if update successful, False otherwise
        """
        try:
            # Read existing config
            if config_path.exists():
                with open(config_path, 'rb') as f:
                    config_data = tomllib.load(f)
            else:
                config_data = {}

            # Update MaiTai port
            if 'maitai' not in config_data:
                config_data['maitai'] = {}

            old_port = config_data['maitai'].get('port', 'not set')
            config_data['maitai']['port'] = port

            # Write updated config in TOML format
            self._write_toml_config(config_data, config_path)

            if self.console:
                self.console.print(f"[green]Configuration updated successfully[/green]")
                self.console.print(f"[dim]Changed port from '{old_port}' to '{port}'[/dim]")
            else:
                print(f"Configuration updated: {old_port} -> {port}")

            return True

        except Exception as e:
            self._print_message(f"Failed to update config: {e}", "red")
            return False

    def _write_toml_config(self, config_data: Dict[str, Any], config_path: Path):
        """Write configuration data to TOML file"""
        # Simple TOML writer since tomllib is read-only
        lines = []

        for section, values in config_data.items():
            lines.append(f"[{section}]")
            if isinstance(values, dict):
                # Add comment for maitai section
                if section == "maitai":
                    lines.append("# MaiTai Ti:Sapphire Laser Configuration")
                elif section == "spirit":
                    lines.append("# Spirit 1040 SHG HE Configuration")

                for key, value in values.items():
                    if isinstance(value, str):
                        lines.append(f'{key} = "{value}"')
                    else:
                        lines.append(f'{key} = {value}')
            lines.append("")  # Empty line between sections

        with open(config_path, 'w') as f:
            f.write('\n'.join(lines))

    def display_summary(self, port: str, response: str, config_updated: bool):
        """Display summary of results"""
        if self.console:
            # Create a summary table
            table = Table(title="MaiTai Detection Summary", show_header=True)
            table.add_column("Property", style="cyan", width=20)
            table.add_column("Value", style="green")

            table.add_row("Port Found", port)
            table.add_row("SCPI Response", response)
            table.add_row("Config Updated", "Yes" if config_updated else "No")
            table.add_row("Communication", "9600 baud, 8N1, XON/XOFF")
            table.add_row("Scan Method", "Parallel Threading")

            panel = Panel(table, title="[bold green]SUCCESS[/bold green]", border_style="green")
            self.console.print(panel)
        else:
            print("\n--- MaiTai Detection Summary ---")
            print(f"Port Found: {port}")
            print(f"SCPI Response: {response}")
            print(f"Config Updated: {'Yes' if config_updated else 'No'}")
            print(f"Communication: 9600 baud, 8N1, XON/XOFF")
            print(f"Scan Method: Parallel Threading")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Scan for MaiTai laser and update configuration (threaded version)"
    )
    parser.add_argument(
        '--config-path',
        type=Path,
        help='Path to hardware_config.toml (default: auto-detect)'
    )
    parser.add_argument(
        '--test-only',
        action='store_true',
        help='Only test communication, do not update config'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed output'
    )
    parser.add_argument(
        '--max-workers',
        type=int,
        default=6,
        help='Maximum number of parallel threads (default: 6)'
    )

    args = parser.parse_args()

    # Auto-detect config path if not provided
    if args.config_path is None:
        script_dir = Path(__file__).parent
        config_path = script_dir.parent / 'src' / 'pymodaq_plugins_spectraphysics' / 'hardware_config.toml'
    else:
        config_path = args.config_path

    # Initialize scanner
    scanner = MaiTaiPortScanner(verbose=args.verbose, max_workers=args.max_workers)

    # Measure scan time
    start_time = time.time()

    # Scan for MaiTai
    result = scanner.scan_ports_parallel()

    scan_time = time.time() - start_time

    if result is None:
        scanner._print_message("MaiTai laser not found on any USB serial port", "red")
        scanner._print_message(f"Scan completed in {scan_time:.2f} seconds", "yellow")
        if scanner.console:
            scanner.console.print("[yellow]Please check:[/yellow]")
            scanner.console.print("  • Physical USB connection")
            scanner.console.print("  • MaiTai power status")
            scanner.console.print("  • USB-to-serial driver installation")
        else:
            print("Check: USB connection, power, drivers")
        return 1

    port, response = result
    config_updated = False

    # Update configuration if requested
    if not args.test_only:
        config_updated = scanner.update_config_file(port, config_path)

    # Display summary
    scanner.display_summary(port, response, config_updated)

    if scanner.console:
        scanner.console.print(f"[dim]Scan completed in {scan_time:.2f} seconds using {args.max_workers} threads[/dim]")
    else:
        print(f"Scan completed in {scan_time:.2f} seconds using {args.max_workers} threads")

    return 0


if __name__ == "__main__":
    exit(main())
