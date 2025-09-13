# Guide to Updating the PyMoDAQ SpectraPhysics MaiTai Plugin

## 1. Overview

This document outlines the necessary changes to the `pymodaq_plugins_spectraphysics` codebase to correctly and completely implement control for the SpectraPhysics Mai Tai laser. The initial implementation used an incorrect command set and did not fully leverage the PyMoDAQ framework's capabilities for data handling with units.

The required modifications are in four main areas:

- **Hardware Control Layer (`maitai_control.py`)**: This file has been updated to use the full, official set of SCPI commands documented in the Mai Tai User's Manual, ensuring compliant and complete communication.

- **Plugin Layer (`daq_move_MaiTai.py`)**: The core DAQ_Move plugin has been refactored to align with PyMoDAQ best practices, particularly by using the DataActuator object with explicit units for all position-related data.

- **Custom UI (`maitai_ui.py`)**: The user interface has been significantly enhanced to match the functionality and layout of the control software depicted in the manual and to display new diagnostic information like pump power and diode currents.

- **Standalone Application (`app/maitai_app.py`)**: The custom PyMoDAQ application provides a standalone GUI for direct laser control, leveraging the updated plugin and UI for a complete, user-friendly experience.

## 2. Hardware Control Layer (`maitai_control.py`) Corrections

The `MaiTaiController` class is now fully compliant with the user manual's specifications.

### 2.1. Serial Port Configuration

The Mai Tai manual (Chapter 6, "Communications Parameters") specifies the use of the XON/XOFF protocol for software flow control. This has been correctly implemented by instantiating `serial.Serial` with `xonxoff=True`.

### 2.2. Full SCPI Command Implementation

All incorrect commands have been replaced with methods that issue the correct SCPI commands. The implementation now covers the full user-accessible command set from the manual (Chapter 6, pages 6-10 to 6-16), including diagnostic queries for pump power, diode currents, system errors, and history buffers.

## 3. Plugin Layer (`daq_move_MaiTai.py`) - PyMoDAQ Best Practices

The `DAQ_Move_MaiTai` plugin has been refactored to adhere to PyMoDAQ's data handling patterns.

### 3.1. Unit-Aware Data Handling

Per PyMoDAQ's documentation, all actuator position data should be handled using `DataActuator` objects that include physical units. This ensures data consistency throughout the framework.

- **`_controller_units`**: The class attribute `_controller_units = "nm"` is now correctly defined.

- **`get_actuator_value()`**: This method now returns `DataActuator(data=wavelength, units=self._controller_units)`.

- **`move_abs()`**: This method now sets `self.target_position` using `DataActuator(data=target_wavelength, units=self._controller_units)`.

- **`set_wavelength_from_ui()`**: This method correctly initiates a move by creating a unit-aware `DataActuator` object.

This change ensures that all wavelength data is explicitly tagged with "nm", preventing ambiguity and enabling proper unit conversions if used in more complex PyMoDAQ modules.

## 4. Custom UI (`maitai_ui.py`) and Standalone App (`maitai_app.py`)

The custom UI and standalone application have been enhanced to provide a more complete control experience.

- **New Diagnostic Displays**: The UI now includes readouts for Pump Power and Diode Currents, which are polled periodically by the plugin.

- **Robust Integration**: The plugin's `poll_status` method now queries all the new diagnostic values from the controller and emits dedicated signals to update the UI, providing a real-time view of the laser's health and performance. The standalone app automatically benefits from these UI improvements.

To run the standalone application, execute the following from your terminal:

```bash
python -m pymodaq_plugins_spectraphysics.app.maitai_app
```

