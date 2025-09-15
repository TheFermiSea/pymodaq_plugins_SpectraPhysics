A Technical Guide to the PyMoDAQ Ecosystem for Automated Plugin and Application Development
Architectural Analysis of the PyMoDAQ Framework
The PyMoDAQ ecosystem is a sophisticated, multi-repository framework designed for modular data acquisition and scientific application development. Its architecture is deliberately decoupled into distinct layers, each encapsulated within a specific Python package. This separation of concerns provides a high degree of flexibility, allowing developers to use the ecosystem not only as a comprehensive data acquisition application but also as a software development kit (SDK) for creating bespoke scientific tools. Understanding the role and interplay of these layers—control, data, presentation, and utilities—is a prerequisite for effective development within the framework.
The Core Orchestration Engine: PyMoDAQ
The PyMoDAQ repository contains the central application logic that orchestrates experimental control and data acquisition. It serves as the integration point for all other components in the ecosystem, providing the primary user-facing application and the backend for automated measurements.
The Dashboard Module
At the heart of the PyMoDAQ application is the Dashboard, a primary graphical component that acts as the container and manager for an entire experimental setup.1 Within the  
Dashboard, users instantiate and configure control modules corresponding to the physical hardware used in their experiment. This modular assembly allows for the creation of complex setups involving multiple instruments. The configuration of a Dashboard, including the number and type of all control modules and their specific settings, can be saved into a preset file, enabling rapid and reproducible initialization of the same experimental configuration at a later time.2
Control Modules
The fundamental units of hardware interaction are the standardized control modules. These modules provide a generic user interface and control logic, abstracting the specifics of the underlying hardware, which are handled by instrument plugins.
DAQ_Move_module: This module represents and controls an "actuator"—any piece of hardware that sets or changes a physical parameter, such as a motorized translation stage, a variable power supply, or a function generator.1 Multiple  
  DAQ_Move_module instances can be active within the Dashboard, corresponding to each controllable degree of freedom in an experiment.  
DAQ_Viewer_module: This module represents and controls a "detector"—any piece of hardware that measures a physical quantity, such as a camera, a spectrometer, a photodiode, or a multimeter.1 As with actuators, any number of  
  DAQ_Viewer_module instances can be instantiated to monitor various experimental outputs.
Core Extensions
Once a Dashboard is populated with configured control modules, extensions can be launched to perform complex, automated tasks that coordinate the actions of these modules. These extensions leverage the pre-initialized hardware interfaces to execute sophisticated measurement routines.
DAQ_Scan: This is the most frequently used extension, designed for automated data acquisition.2 It allows a user to define a scan by selecting one or more actuators to vary systematically over a defined range while recording data from one or more detectors at each step. This module is capable of performing a wide variety of scientific measurements, from simple 1D scans to complex multi-dimensional parameter sweeps.  
DAQ_Logger: This extension provides functionality for logging data from multiple detectors over time, which is useful for monitoring the stability of an experiment or recording environmental parameters.1 Data can be saved to either hierarchical HDF5 files or a SQL database.  
PID: This extension implements a Proportional-Integral-Derivative (PID) feedback loop controller.2 It can be configured to monitor a value from a detector (the process variable) and actively adjust an actuator's setting (the control variable) to lock the process variable to a desired setpoint. This is essential for applications requiring active stabilization, such as locking a laser's frequency or maintaining a constant sample temperature. A video tutorial demonstrates its use in emulating a PID controller.4
The Data Management Layer: pymodaq_data
The pymodaq_data repository provides a powerful, standalone package for structured data handling.5 Its primary purpose is to establish a standardized data contract used throughout the ecosystem, abstracting the concept of scientific data beyond simple numerical arrays into rich, self-describing objects. This package can be used independently of the main  
PyMoDAQ application for data analysis and management tasks.6
The DataND Object Hierarchy
The core of the pymodaq_data library is a hierarchy of classes, generically referred to as DataND, that are designed to encapsulate experimental data of varying dimensionality (Data0D for single-point values, Data1D for spectra or time traces, Data2D for images, etc.).6 This object-oriented approach ensures that data is handled consistently, regardless of its source or structure.
Encapsulation of Data, Axes, Units, and Metadata
A key feature of the DataND objects is their ability to store not only the raw numerical data (typically as NumPy arrays) but also the critical context required for its interpretation. This includes 6:
Axes: Each data dimension is associated with an axis object that defines the coordinates for that dimension.  
Units: Physical units for both the data and its axes are managed using the pint Python package, preventing ambiguity and facilitating correct calculations.  
Metadata: A flexible dictionary for storing arbitrary metadata, such as instrument settings, timestamps, sample information, or user comments.  
Uncertainty: Provisions for storing error bars or data uncertainty are included.
This comprehensive encapsulation is vital for ensuring data is Findable, Accessible, Interoperable, and Reusable (FAIR), as it packages the data with the information needed to understand and reproduce it.7
HDF5 Serialization and Data Integrity
The pymodaq_data package is designed for seamless serialization to and from the Hierarchical Data Format 5 (HDF5).1 This binary format is well-suited for storing the complex, nested structure of  
DataND objects, preserving the relationships between data, axes, and metadata. This robust data persistence mechanism ensures data integrity from acquisition to analysis.
The Presentation Layer: pymodaq_gui
The pymodaq_gui repository contains a collection of custom graphical components built upon the Qt framework (supporting PyQt5, PyQt6, and PySide6).5 This package provides the reusable UI elements that give the PyMoDAQ application and its extensions a consistent and functional user interface.
Role of Qt Widgets and Graphical Components
This package provides a library of specialized widgets beyond the standard Qt offerings, tailored for scientific applications. These components are used to construct the interfaces of the Dashboard, control modules, and extensions, ensuring a uniform look and feel across the entire platform.8
Data Viewers
A critical feature of pymodaq_gui is its set of "out of the box" data viewers. These viewers are specifically designed to render the DataND objects from the pymodaq_data package.8 There are specialized viewers for each data dimensionality:
0D Viewer: For plotting single-point data as it evolves over time.  
1D Viewer: For displaying line graphs of spectra or time traces, including tools for zooming, panning, and cursors.  
2D Viewer: For displaying images, with integrated tools for adjusting colormaps, viewing histograms, selecting regions of interest (ROIs), and performing lineouts.
This tight integration between the data layer (pymodaq_data) and the presentation layer (pymodaq_gui) allows developers to easily visualize complex scientific data with minimal boilerplate code.
The Utility Layer: pymodaq_utils
The pymodaq_utils repository serves as the foundational layer of the ecosystem, providing a collection of shared helper functions, classes, and constants.5 This package is a dependency for all other PyMoDAQ repositories and is designed to prevent code duplication and enforce consistent behavior across the platform. While its contents are diverse, they generally include utilities for tasks such as configuration file management, logging, mathematical operations, and thread handling.  
The separation of the PyMoDAQ ecosystem into these four distinct repositories is a deliberate and powerful architectural decision. It creates a layered system where each component has a clearly defined responsibility. pymodaq_utils provides the base utilities. pymodaq_data defines the universal "language" of data exchange. pymodaq_gui offers the tools to visualize that data. Finally, the main PyMoDAQ application integrates all these components to provide a complete instrument control and data acquisition solution. This decoupling enables profound flexibility. For instance, a developer could build a command-line acquisition script using only the backend components of PyMoDAQ and pymodaq_data. Conversely, a data analysis and visualization tool could be created using only pymodaq_data and pymodaq_gui, completely independent of any hardware control. This transforms the ecosystem from a single application into a versatile toolkit for a wide range of scientific software development, a potential best exemplified by custom applications like PyMoDAQ-Femto.10
| Repository | Primary Role | Key Components | Relationship to Others |
| :---- | :---- | :---- | :---- |
| PyMoDAQ | Orchestration Engine | Dashboard, DAQ_Move_module, DAQ_Viewer_module, Extensions (DAQ_Scan, DAQ_Logger) | Integrates all other components to form the main application. |
| pymodaq_data | Data Abstraction Layer | DataND object hierarchy (Data0D, Data1D, Data2D), Metadata/Unit handling | Defines the standard data contract used for communication between all components. |
| pymodaq_gui | Presentation Layer | Custom Qt Widgets, DataND Viewers | Provides the graphical elements to build UIs and visualize data from pymodaq_data. |
| pymodaq_utils | Shared Utilities | Helper functions, constants, base classes | Serves as a foundational dependency, providing common utilities to all other repositories. |
A Procedural Guide to Instrument Plugin Construction
The modular architecture of PyMoDAQ is designed for extensibility, with the most common form of extension being the instrument plugin. These plugins are self-contained packages that add support for new hardware, allowing it to be controlled within the PyMoDAQ Dashboard. The development process is highly standardized to ensure compatibility and ease of integration.
The Plugin Development Lifecycle
Creating a new instrument plugin follows a well-defined lifecycle, starting from a template and ending with a distributable package that can be managed by other users.
Initiation using the pymodaq_plugins_template
The official and mandatory starting point for any new plugin is the pymodaq_plugins_template repository.5 This is a GitHub "template repository," which allows a developer to generate a new repository that inherits its complete file structure, boilerplate code, and CI/CD workflows.12 This approach ensures that all new plugins start with a consistent and functional foundation, including setup files, directory structures, and example code.
Repository Configuration and Naming Conventions
Once the new repository is created from the template, it must be given a name that follows a strict convention: pymodaq_plugins_<my_plugin_name>.12 Typically,  
<my_plugin_name> is the name of the hardware manufacturer (e.g., pymodaq_plugins_andor 5,  
pymodaq_plugins_basler 13) or a descriptive name for a category of instruments. This naming scheme is not merely a convention; it is essential for the plugin to be discoverable by PyMoDAQ's management tools.
Packaging and Distribution via PyPI
The template repository includes all the necessary configuration files (e.g., pyproject.toml) to package the plugin as a standard Python wheel.12 This allows the completed plugin to be uploaded to the Python Package Index (PyPI), making it easily installable for any user via a simple command like  
pip install pymodaq_plugins_<my_plugin_name>.14
Management with pymodaq_plugin_manager
The pymodaq_plugin_manager is a graphical utility that simplifies the management of installed plugins.5 It queries a central list of known plugins and compares it against the user's local environment, presenting a list of available, installed, and updatable plugins. Adhering to the established naming and packaging conventions ensures full compatibility with this manager, allowing users to discover and install new plugins directly from the GUI.
Implementation of Actuator Plugins (DAQ_Move)
An actuator plugin provides the specific logic to control a piece of hardware through the generic DAQ_Move_module interface. The core development task is to create a Python class that translates the standardized commands from the PyMoDAQ framework into the specific API calls required by the hardware's driver or SDK.
Inferred Base Class and Inheritance Structure
While the primary developer documentation is not available in the provided materials 11, analysis of the plugin template and existing mock examples 11 indicates that an actuator plugin is a Python class that must inherit from a specific base class, inferred to be  
pymodaq.control_modules.move_utility_classes.DA_Move_Base. This class must be placed within the src/pymodaq_plugins_<my_plugin_name>/daq_move_plugins/ directory of the plugin package. The base class provides the necessary attributes and methods to interface with the DAQ_Move_module.
Mandatory Method Implementation
The plugin class acts as a hardware abstraction layer by implementing a set of mandatory methods that form an "API contract." The DAQ_Move_module calls these methods to interact with the hardware, without needing any knowledge of the device-specific commands. The developer's primary responsibility is to implement the logic within these methods using the manufacturer's provided library.
| Method Name | Inferred Signature | Purpose | Implementation Notes |
| :---- | :---- | :---- | :---- |
| init_hardware | def init_hardware(self) -> bool: | Establishes the connection to the physical device and performs any necessary initialization. | Must return True on successful initialization. This is where the manufacturer's SDK/API is initialized (e.g., opening a serial port, connecting to a DLL). |
| close | def close(self) -> None: | Disconnects from the hardware and releases any acquired resources. | Should ensure all connections are terminated cleanly to prevent resource leaks. |
| move_abs | def move_abs(self, position: float) -> None: | Moves the actuator to a specified absolute position. | This method should contain the device-specific command for an absolute move. It should typically block until the move is complete or use a status-checking mechanism. |
| move_rel | def move_rel(self, position: float) -> None: | Moves the actuator by a specified relative amount from its current position. | Contains the device-specific command for a relative move. Similar blocking or status-checking logic as move_abs is required. |
| get_actuator_value | def get_actuator_value(self) -> float: | Reads and returns the current position or value of the actuator. | This method is called to update the position display in the GUI. It must query the hardware for its current state. |
| stop_motion | def stop_motion(self) -> None: | Immediately halts any ongoing movement of the actuator. | Implements the hardware's emergency stop or halt command. |
Managing Hardware Parameters
Instrument-specific settings, such as a device's serial number, communication port, axis identifier, or velocity limits, are exposed to the user through the GUI. This is achieved by defining a class attribute named params. This attribute is a list of dictionaries, where each dictionary defines a parameter (e.g., its name, type, default value, limits). PyMoDAQ automatically parses this structure and renders a corresponding settings tree in the DAQ_Move_module interface, allowing users to configure the plugin without modifying its code.
Implementation of Detector Plugins (DAQ_Viewer)
A detector plugin provides the logic to acquire data from a measurement device and display it using the generic DAQ_Viewer_module interface. Similar to actuator plugins, the core task is to create a class that bridges the PyMoDAQ framework and the hardware's specific API.
Inferred Base Class and Inheritance Structure
Based on the plugin template structure 11, detector plugins are Python classes that must be placed within the  
src/pymodaq_plugins_<my_plugin_name>/daq_viewer_plugins/ directory. They are inferred to inherit from a base class, likely pymodaq.control_modules.viewer_utility_classes.DA_Viewer_Base. The specific base class or mixin may vary depending on the dimensionality of the detector (0D, 1D, or 2D), as the template provides separate subdirectories for each.11
Mandatory Method Implementation
The "API contract" for a detector plugin centers on initialization, data acquisition, and data emission. The DAQ_Viewer_module uses these methods to manage the detector and receive data for display and saving.
| Method Name | Inferred Signature | Purpose | Implementation Notes |
| :---- | :---- | :---- | :---- |
| init_hardware | def init_hardware(self) -> bool: | Establishes the connection to the physical detector and performs initialization. | Must return True on success. This is where camera SDKs are initialized, communication ports are opened, etc. |
| close | def close(self) -> None: | Disconnects from the hardware and releases resources. | Ensures a clean shutdown of the device connection. |
| grab_data | def grab_data(self, Naverage: int, **kwargs) -> None: | The primary data acquisition method. It acquires data, packages it, and emits it. | This method is called by the DAQ_Viewer_module to trigger a measurement. It should perform the hardware-specific data acquisition, potentially averaging Naverage times if applicable. |
| stop_grab | def stop_grab(self) -> None: | Halts any ongoing or continuous data acquisition process. | Implements the hardware's command to stop acquisition. |
Data Emission Protocol
The most critical concept in detector plugin development is the data emission protocol. After acquiring raw data within the grab_data method, the plugin must package this data into one or more DataND objects from the pymodaq_data library. This step involves creating the appropriate object (Data0D, Data1D, Data2D), populating it with the numerical data, and adding the relevant axes and metadata.  
Once the DataND object is created, the plugin must emit a predefined Qt signal, data_grabed_signal, with the data object(s) as its payload. A typical implementation looks like this: self.data_grabed_signal.emit([my_data_object]). This signal-based mechanism completely decouples the plugin from the rest of the application. The DAQ_Viewer_module listens for this signal. Upon its reception, it takes the DataND object and passes it to the appropriate data viewer for display and to other modules (like DAQ_Scan or DAQ_Logger) for saving. This protocol ensures that as long as a plugin correctly formats and emits its data, it will automatically be compatible with all of PyMoDAQ's display, saving, and processing features.  
The development of a plugin is fundamentally an act of translation. The developer must first understand the proprietary API of the hardware, often by studying the manufacturer's manual and examples.19 The main task is then to translate those device-specific function calls into the standardized methods and data structures required by the PyMoDAQ plugin contract. The generic  
DAQ_Move and DAQ_Viewer modules define this contract, and the plugin's role is to faithfully implement it, creating an abstraction layer that hides the complexity of the specific hardware from the main application.
Advanced Development: Custom Applications and Extensions
Beyond interfacing with standard hardware via plugins, the PyMoDAQ ecosystem serves as a powerful software development kit (SDK) for creating entirely new, specialized scientific applications and for extending the functionality of the core Dashboard. This is possible due to the framework's decoupled, library-like architecture.
Building Standalone Applications
The constituent packages of PyMoDAQ can be used independently to build custom applications from the ground up, leveraging their specialized functionalities for data handling and visualization without needing to run the main Dashboard application.
Leveraging Decoupled Components
As established by the architectural analysis, the pymodaq_data and pymodaq_gui packages are designed to be used as standalone libraries.6 A developer can create a new Python project, add  
pymodaq_data and pymodaq_gui as dependencies, and then import their components just like any other library. This allows for the creation of custom graphical user interfaces that use the DataND objects for internal data management and the specialized data viewers from pymodaq_gui for rich visualization, all within a completely new application context.
Case Study: Deconstructing PyMoDAQ-Femto
PyMoDAQ-Femto serves as the canonical example of a complex, standalone application built upon the PyMoDAQ foundation.10 This application provides a specialized environment for the temporal characterization of ultrashort laser pulses, featuring its own unique user interfaces named  
Simulator and Retriever.10 The installation and launch procedures for  
PyMoDAQ-Femto demonstrate its independence; it is installed via pip and can be started from the command line using its own entry points (e.g., python -m pymodaq_femto.simulator), entirely separate from the main PyMoDAQ application.20  
Interestingly, PyMoDAQ-Femto also showcases a powerful dual-mode design pattern: it can run as a standalone application for simulation and analysis, or it can be plugged into the main PyMoDAQ Dashboard as an extension to work with live experimental data.10 This illustrates the ultimate flexibility of the ecosystem, where components can be both the foundation for new applications and extensions to the existing one.
Integrating Data Acquisition Logic with Custom User Interfaces
The process for building a custom application involves standard GUI development practices, augmented by PyMoDAQ's scientific components. A developer would typically:
Create a main application window using a Qt framework (e.g., PySide6).  
Design and add custom widgets for user input and control specific to the application's domain.  
Incorporate data viewers from pymodaq_gui into the UI layout to display results.  
Implement the application's core logic, which would perform calculations or control hardware, producing results that are packaged into pymodaq_data objects.  
Pass these DataND objects to the integrated data viewers for real-time display.
This approach treats PyMoDAQ's components not as a monolithic program to be modified, but as a "meta-framework" or library of high-level, domain-specific building blocks. While a generic framework like Qt provides buttons and windows, PyMoDAQ provides data objects that understand physical units and GUI elements that know how to plot scientific data with appropriate axes and labels. This significantly accelerates the development of custom scientific software.
Creating Custom Dashboard Extensions
For functionality that is tightly coupled with live data acquisition and control, creating a custom Dashboard extension is the appropriate development path. An extension operates within the main PyMoDAQ application, leveraging the instruments that have already been configured in the Dashboard.
Defining the Role and Structure of an Extension
An extension adds a new, coordinated capability to the Dashboard. It typically provides a dedicated user interface for performing a task that involves multiple configured actuators and detectors. Unlike a standalone application, it is not a separate process but a module loaded by the Dashboard.
Implementation Walkthrough: The ColorSynthesizer Example
The pymodaq_plugins_arduino repository includes an excellent, simple example of a Dashboard extension called ColorSynthesizer.21 This extension is designed to work with three  
DAQ_Move modules that control the red, green, and blue channels of an LED. It provides a color wheel UI where the user can select a color, and the extension then calculates the corresponding RGB values and programmatically sets the three actuator modules to those values. This provides a higher-level, more intuitive interface than manually adjusting three separate sliders.
Interfacing Extensions with Dashboard Control Modules
The key mechanism for an extension is its ability to access and control the instrument modules that are active in the Dashboard. The Dashboard provides a programmatic interface through which an extension can get references to the initialized DAQ_Move and DAQ_Viewer modules. The extension can then call the public methods of these modules, such as move_abs on an actuator or grab_data on a detector, to orchestrate complex sequences of actions. This allows developers to build custom scan routines, feedback loops, or instrument-coordination logic that is not covered by the standard extensions.
Synthesis and Recommendations for AI Agent Implementation
This section consolidates the preceding analysis into a direct, procedural knowledge base tailored for an AI agent tasked with developing within the PyMoDAQ ecosystem. It provides decision logic, code skeletons, and a concise API reference to guide automated code generation.
Decision Logic for Plugin and Application Development
To select the appropriate development strategy, the following decision logic should be applied:
Query: Is the primary goal to add support for a new piece of hardware (actuator or detector)?  
Action: If YES, proceed with the Instrument Plugin Construction workflow (Section II).  
Use the pymodaq_plugins_template to create a new repository.  
Implement the mandatory methods for either a DAQ_Move or DAQ_Viewer plugin.  
Package the result for distribution.  
Query: Is the primary goal to create a new, specialized application with its own unique user interface for a specific scientific task (e.g., data analysis, simulation, a custom measurement protocol)?  
Action: If YES, proceed with the Standalone Application workflow (Section 3.1).  
Create a new, independent Python project.  
Add pymodaq_data and pymodaq_gui as dependencies.  
Build the custom UI using Qt and incorporate data viewers from pymodaq_gui.  
Use pymodaq_data objects for all internal data management.  
Query: Is the primary goal to add a new function that coordinates multiple instruments already configured within the main PyMoDAQ Dashboard?  
Action: If YES, proceed with the Custom Dashboard Extension workflow (Section 3.2).  
Develop a new module that can be loaded by the Dashboard.  
Design a UI for the new functionality.  
Implement the logic to programmatically access and control the existing DAQ_Move and DAQ_Viewer modules within the Dashboard.
Code Skeletons and Implementation Checklists
The following code skeletons provide the basic structure for common development tasks. They should be used as the starting point for code generation.
DAQ_Move Plugin Skeleton
Python
# In file: src/pymodaq_plugins_<manufacturer>/daq_move_plugins/daq_move_<instrument>.py
from pymodaq.control_modules.move_utility_classes import DAQ_Move_base, comon_parameters_fun  
from pymodaq.utils.daq_utils import ThreadCommand
class DAQ_Move_<InstrumentName>(DAQ_Move_base):  
    """  
    Plugin class for the <InstrumentName> actuator.  
    """  
    _controller_units = '<units>'  # e.g., 'm', 'V', 'deg'  
    is_multiaxes = False  # Set True if the controller manages multiple axes  
    _axis_names =       # For multiaxes, list of axis names, e.g.,  
    _epsilon = 0.01        # Minimum move distance
    params = [  
        # Add device-specific parameters here.  
        # Example:  
        # {'title': 'COM Port:', 'name': 'com_port', 'type': 'str', 'value': 'COM1'},  
        # {'title': 'Velocity:', 'name': 'velocity', 'type': 'float', 'value': 1.0, 'min': 0.0},  
    ] + comon_parameters_fun(is_multiaxes, axis_names=_axis_names)
    def __init__(self, parent=None, params_state=None):  
        super().__init__(parent, params_state)  
        self.controller = None
    def commit_settings(self, param):  
        """  
        Apply changes made in the settings tree.  
        """  
        if param.name() == 'velocity':  
            # self.controller.set_velocity(param.value())  
            pass
    def init_hardware(self):  
        """  
        Initialize the connection to the hardware.  
        """  
        try:  
            # TODO: Instantiate the controller object from the manufacturer's library  
            # self.controller = ManufacturerAPI.Controller(self.settings.child('com_port').value())  
            self.status.info = "Controller Initialized"  
            self.status.controller_is_ready = True  
            return True  
        except Exception as e:  
            self.status.info = f"Initialization failed: {str(e)}"  
            self.status.controller_is_ready = False  
            return False
    def close(self):  
        """  
        Close the connection to the hardware.  
        """  
        # TODO: Call the controller's close/disconnect method  
        # self.controller.close()  
        pass
    def get_actuator_value(self):  
        """  
        Get the current position of the actuator.  
        """  
        # TODO: Query the controller for its current position and return it  
        # position = self.controller.get_position()  
        # self.current_position = position  
        # return position  
        pass
    def move_abs(self, position):  
        """  
        Move the actuator to an absolute position.  
        """  
        # TODO: Send the command to move to the absolute position  
        # self.target_position = position  
        # self.controller.move_to(position)  
        self.poll_moving() # Recommended to check movement status
    def move_rel(self, position):  
        """  
        Move the actuator by a relative amount.  
        """  
        # TODO: Send the command to move by the relative amount  
        # self.target_position = self.current_position + position  
        # self.controller.move_by(position)  
        self.poll_moving()
    def stop_motion(self):  
        """  
        Stop the actuator's motion.  
        """  
        # TODO: Send the stop command to the controller  
        # self.controller.stop()  
        self.move_done()
DAQ_Move Implementation Checklist:
[ ] Set _controller_units to the correct physical unit.  
[ ] Define all necessary hardware settings in the params list.  
[ ] Implement hardware connection logic in init_hardware().  
[ ] Implement hardware disconnection logic in close().  
[ ] Implement position reading logic in get_actuator_value().  
[ ] Implement absolute and relative move logic in move_abs() and move_rel().  
[ ] Implement motion stop logic in stop_motion().
DAQ_Viewer Plugin Skeleton (2D Example)
Python
# In file: src/pymodaq_plugins_<manufacturer>/daq_viewer_plugins/daq_viewer_<instrument>.py
from pymodaq.control_modules.viewer_utility_classes import DAQ_Viewer_base, comon_parameters  
from pymodaq.data_class import DataFromPlugins, Axis  
from pymodaq.utils.daq_utils import ThreadCommand
class DAQ_Viewer_<InstrumentName>(DAQ_Viewer_base):  
    """  
    Plugin class for the <InstrumentName> 2D detector.  
    """  
    params = [  
        # Add device-specific parameters here.  
        # Example:  
        # {'title': 'Exposure (ms):', 'name': 'exposure', 'type': 'float', 'value': 100.0},  
        # {'title': 'Gain:', 'name': 'gain', 'type': 'int', 'value': 1, 'min': 0},  
    ] + comon_parameters
    def __init__(self, parent=None, params_state=None):  
        super().__init__(parent, params_state)  
        self.controller = None  
        self.x_axis = None  
        self.y_axis = None
    def commit_settings(self, param):  
        """  
        Apply changes made in the settings tree.  
        """  
        if param.name() == 'exposure':  
            # self.controller.set_exposure(param.value())  
            pass
    def init_hardware(self):  
        """  
        Initialize the connection to the hardware.  
        """  
        try:  
            # TODO: Instantiate the controller object from the manufacturer's library  
            # self.controller = ManufacturerAPI.Camera()  

            # TODO: Define the detector axes  
            # image_shape = self.controller.get_sensor_size() # (height, width)  
            # self.x_axis = Axis(name='X_axis', unit='px', data=np.arange(image_shape))  
            # self.y_axis = Axis(name='Y_axis', unit='px', data=np.arange(image_shape))
            self.status.info = "Controller Initialized"  
            self.status.controller_is_ready = True  
            return True  
        except Exception as e:  
            self.status.info = f"Initialization failed: {str(e)}"  
            self.status.controller_is_ready = False  
            return False
    def close(self):  
        """  
        Close the connection to the hardware.  
        """  
        # TODO: Call the controller's close/disconnect method  
        # self.controller.close()  
        pass
    def grab_data(self, Naverage=1, **kwargs):  
        """  
        Acquire data from the detector and emit it.  
        """  
        try:  
            # TODO: Acquire the image data from the camera  
            # image_data = self.controller.grab_frame()  

            # TODO: Package the data into a DataFromPlugins object (which is a subclass of Data2D)  
            # data = DataFromPlugins(name='<InstrumentName>',  
            #                        distribution='uniform2D',  
            #                        data=[image_data],  
            #                        axes=[self.y_axis, self.x_axis])
            # TODO: Emit the data_grabed_signal  
            # self.data_grabed_signal.emit([data])
        except Exception as e:  
            # Handle acquisition errors  
            pass
    def stop(self):  
        """  
        Stop the acquisition.  
        """  
        # TODO: Send the stop command to the controller, if applicable  
        # self.controller.stop_acquisition()  
        return ""
DAQ_Viewer Implementation Checklist:
[ ] Define all necessary hardware settings in the params list.  
[ ] Implement hardware connection logic in init_hardware().  
[ ] In init_hardware(), define the Axis objects for the detector's data dimensions.  
[ ] Implement hardware disconnection logic in close().  
[ ] In grab_data(), implement the logic to acquire raw data from the instrument.  
[ ] In grab_data(), package the raw data into a DataFromPlugins (or Data0D, Data1D, Data2D) object, including axes.  
[ ] In grab_data(), emit the packaged data using self.data_grabed_signal.emit().  
[ ] Implement acquisition stop logic in stop().
API Reference for Essential Classes and Methods
This section provides a concise, inferred API reference for the key classes involved in plugin development.
pymodaq.control_modules.move_utility_classes.DAQ_Move_base  
Description: The base class for all actuator plugins.  
Key Attributes:  
settings: A Parameter object from pyqtgraph representing the params tree. Access values via self.settings.child('param_name').value().  
current_position: Should be updated by get_actuator_value to store the last known position.  
Mandatory Methods: init_hardware, close, get_actuator_value, move_abs, move_rel, stop_motion.  
pymodaq.control_modules.viewer_utility_classes.DAQ_Viewer_base  
Description: The base class for all detector plugins.  
Key Attributes:  
settings: Similar to DAQ_Move_base, represents the params tree.  
data_grabed_signal: A Qt Signal that must be emitted from grab_data with a list of DataND objects as the payload.  
Mandatory Methods: init_hardware, close, grab_data, stop.  
pymodaq.data_class.DataFromPlugins  
Description: A specialized subclass of DataND used for emitting data from plugins.  
Key __init__ arguments:  
name (str): The name of the detector.  
distribution (str): The data distribution type (e.g., 'uniform1D', 'uniform2D').  
data (list of np.ndarray): A list containing the raw numerical data array(s).  
axes (list of Axis): A list of Axis objects corresponding to the data dimensions.  
pymodaq.data_class.Axis  
Description: An object representing a data axis.  
Key __init__ arguments:  
name (str): The name of the axis (e.g., 'Wavelength', 'Time', 'X').  
unit (str): The physical unit of the axis (e.g., 'nm', 's', 'µm').  
data (np.ndarray): A 1D NumPy array containing the coordinate values for the axis.
Works cited
PyMoDAQ/PyMoDAQ: Modular Data Acquisition with Python - GitHub, accessed September 13, 2025, https://github.com/PyMoDAQ/PyMoDAQ  
PyMoDAQ — PyMoDAQ 4.4.11 documentation, accessed September 13, 2025, http://pymodaq.cnrs.fr/en/4.4.x/  
pymodaq - PyPI, accessed September 13, 2025, https://pypi.org/project/pymodaq/  
4 - PyMoDAQ's PID module - YouTube, accessed September 13, 2025, https://www.youtube.com/watch?v=u8ifY4WqQEA  
PyMoDAQ - GitHub, accessed September 13, 2025, https://github.com/PyMoDAQ  
Allows data management within the PyMoDAQ ecosystem and HDF5 compatibility - GitHub, accessed September 13, 2025, https://github.com/PyMoDAQ/pymodaq\_data  
(PDF) PyMoDAQ: An open-source Python-based software for modular data acquisition, accessed September 13, 2025, https://www.researchgate.net/publication/350746249\_PyMoDAQ\_An\_open-source\_Python-based\_software\_for\_modular\_data\_acquisition  
PyMoDAQ/pymodaq_gui: Set of Qt widgets and graphical ... - GitHub, accessed September 13, 2025, https://github.com/PyMoDAQ/pymodaq\_gui  
PyMoDAQ/pymodaq_utils: Set of utils modules, class and ... - GitHub, accessed September 13, 2025, https://github.com/PyMoDAQ/pymodaq\_utils  
Welcome to PyMoDAQ-Femto documentation! — PyMoDAQ Femto 3.1.0 documentation, accessed September 13, 2025, https://pymodaq-femto.readthedocs.io/  
PyMoDAQ/pymodaq_plugins_template: Template fro ... - GitHub, accessed September 13, 2025, https://github.com/PyMoDAQ/pymodaq\_plugins\_template  
3.3. Write and release a new plugin — PyMoDAQ 4.4.11 documentation - CNRS, accessed September 13, 2025, https://pymodaq.cnrs.fr/en/4.4.x/tutorials/new\_plugin.html  
PyMoDAQ/pymodaq_plugins_basler: PyMoDAQ plugins for cameras of Basler - GitHub, accessed September 13, 2025, https://github.com/PyMoDAQ/pymodaq\_plugins\_basler  
3. Tutorials — PyMoDAQ 4.4.11 documentation, accessed September 13, 2025, https://pymodaq.cnrs.fr/en/4.4.x/tutorials.html  
PyMoDAQ/pymodaq_plugin_manager readme | GitHub | Ecosyste.ms: Repos, accessed September 13, 2025, https://data.code.gouv.fr/hosts/GitHub/repositories/PyMoDAQ%2Fpymodaq\_plugin\_manager/readme?sha=1.3.0  
PyMoDAQ/pymodaq_plugin_manager: PyMoDAQ plugin Manager. Contains the listing of plugins to include hardware to pymodaq. Let you manage the installed plugins using a User Interface - GitHub, accessed September 13, 2025, https://github.com/PyMoDAQ/pymodaq\_plugin\_manager  
accessed December 31, 1969, https://github.com/PyMoDAQ/PyMoDAQ/tree/main/src/pymodaq  
Extension plugin for pymodaq. Examples to show how to deal with detectors sending events - GitHub, accessed September 13, 2025, https://github.com/PyMoDAQ/pymodaq\_plugins\_mockexamples  
3.4. Story of an instrument plugin development — PyMoDAQ 4.4.11 ..., accessed September 13, 2025, https://pymodaq.cnrs.fr/en/4.4.x/tutorials/plugin\_development.html  
2. Installation — PyMoDAQ Femto 3.1.0 documentation - Read the Docs, accessed September 13, 2025, https://pymodaq-femto.readthedocs.io/en/latest/usage/Installation.html  
PyMoDAQ/pymodaq_plugins_arduino - GitHub, accessed September 13, 2025, https://github.com/PyMoDAQ/pymodaq\_plugins\_arduino

