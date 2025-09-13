# -*- coding: utf-8 -*-
"""
Created the 31/08/2023

@author: Sebastien Weber
"""
from pathlib import Path
import tomllib

from pymodaq_utils.config import BaseConfig, USER


class Config(BaseConfig):
    """Main class to deal with configuration values for this plugin"""
    config_template_path = Path(__file__).parent.joinpath('resources/config_template.toml')
    config_name = f"config_{__package__.split('pymodaq_plugins_')[1]}"

    def get_hardware_config(self, hardware_name: str):
        """Get hardware-specific configuration values from TOML file"""
        hardware_config_path = Path(__file__).parent.joinpath('hardware_config.toml')

        try:
            with open(hardware_config_path, 'rb') as f:
                config_data = tomllib.load(f)
                return config_data.get(hardware_name, {})
        except FileNotFoundError:
            # Fallback defaults if TOML file doesn't exist
            if hardware_name == "maitai":
                return {
                    'port': '/dev/ttyUSB6',
                    'baudrate': 9600,
                    'timeout': 5.0,
                    'wavelength_min': 700.0,
                    'wavelength_max': 1040.0,
                    'wavelength_units': 'nm',
                    'default_wavelength': 800.0
                }
            elif hardware_name == "spirit":
                return {
                    'port': 'COM4',
                    'baudrate': 9600,
                    'timeout': 5.0,
                    'wavelength_min': 520.0,
                    'wavelength_max': 1040.0,
                    'wavelength_units': 'nm',
                    'default_wavelength': 1040.0
                }
            return {}
