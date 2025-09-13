

{73}------------------------------------------------

# The Main Menu

![](_page_73_Figure_2.jpeg)

Figure 6-1: The Main Menu

The Main menu (Figure 6-1) is the first screen that appears when you start the software (after the Com Port Confirm menu). Large and easily seen from a distance, it serves as both monitor and input screen.

The five control features include:

- Sub-menu selection
- On/off control
- Wavelength select/monitor
- Output power monitor
- Shutter open/close

The menu functions are described below as they appear on the screen from left to right, top to bottom.

**Submenu Selection**—allows you to select Quit, the Setup menu, the Info menu and the Scan menu.

**QUIT**— exits the program. Press this button prior to powering down the computer.

SETUP—takes you to the Setup menu.

**INFO**—takes you to the Info menu.

**SCAN**—takes you to the Scan menu.

**EMISSION indicator**—when on, shows that pulsed laser output is available, even though there may actually be no emission if the shutter is closed; when off, indicates that the laser is turned off.

{74}------------------------------------------------

**PULSING indicator**—when on, indicates the output beam is pulsing; when off, there is no output (laser is off) or the output beam is not pulsing (i.e., it is running CW).

**SET WAVELENGTH controls and indicators**—allows you to select an operation wavelength between 750 and 850 nm or 780 and 920 nm.

There are several ways to set the wavelength: by using the up/down arrows to the left of the "Set Wavelength" window, by typing in a number in the window itself, by dragging the bar in the upper bar graph to the desired location (wavelength numbers corresponding to its position will display in the window), and by using the left and right arrows on the bar graph to move the bar. Each tick on the bar graph is 2 nm.

**ACTUAL WAVELENGTH indicators**—indicate a relative output wavelength value in the lower bar graph and an absolute value in the lower numeric window.

When the system is active, the arrow in the lower bar graph indicates the current output wavelength. When the requested wavelength is changed by the operator in the "Set Wavelength" window, the arrow will move toward that same value as the unit automatically compensates. When the desired value and actual value are equal, the arrow will stop and will be in line with the upper bar and the "Actual Wavelength" value in the window will match the "Set" value.

**OUTPUT POWER indicator**—is displayed in Watts as a relative value via a mark on a bar graph, and as an absolute value in the lower window.

The system is automatically optimized for maximum output power at each wavelength; there is no power setting control.

SHUTTER button—opens and closes the internal shutter.

To open the shutter, click on the SHUTTER button and hold down the mouse button about 3 seconds (for safety reasons) until the shutter light over the button turns on. Actual emission will occur only if and when the laser is turned on using the ON/OFF button (see below). To close the shutter, simply click on the SHUTTER button again. The shutter closes immediately, blocking the laser beam.

**ON/OFF button**—turns the laser on and off.

To turn on the laser, click on the ON/OFF button and hold the mouse button down about 3 seconds until the EMISSION light over the wavelength display turns on. To turn off the laser, simply click on the ON/OFF button again. The laser turns off immediately. Actual emission will occur only when the shutter is open (see above).

**SYSTEM STATUS monitor**—provides status information at the bottom of the screen.

{75}------------------------------------------------

# The Setup Menu

| Setup |
|-------|
|-------|

| OK |
|----|
|----|

| System        |                            |
|---------------|----------------------------|
| Watchdog Time | 3.00 (seconds, 0 disables) |
| Standby Delay | never                      |

| Pump laser |
|------------|
|------------|

| Pct Cur      | 0.00          |
|--------------|---------------|
| Control Mode | Current Power |
| Power        | 3.60          |
| SHG Fine     | 5             |

| RF                |              |
|-------------------|--------------|
| BF Phase Percent  | 50.00        |
| Modelocker Enable | On       Off |

The Setup menu (Figure 6-2) is for Spectra-Physics service personnel only.

![](_page_75_Figure_4.jpeg)

Caution!

The parameters shown in Figure 6-2 are set at the factory for optimum system performance. Do not use this menu to modify any parameters. In particular, do not set the unit to current mode or change the power setting. Increasing power may actually decrease output performance! These controls are for diagnostic purposes only and are to be used only by someone trained on this laser by Spectra-Physics.

# The Info Menu

The Info menu (Figure 6-3) provides information on several parameters, the most important of which are the "SHG Status," the "History Buffer" and the "Software Rev" (required when calling Spectra-Physics for help). The other indicators are to be used for diagnostic purposes only by persons trained on this laser by Spectra-Physics.

**PUMP POWER indicator**—shows the output of the internal pump laser in Watts and is to be used only for diagnostic purposes by persons trained on this laser by Spectra-Physics. Different wavelengths require different power settings, so this value is dependent on the wavelength selected.

**CURRENT (AMPS) indicators**— show the current output in amperes of each diode laser and are to be used only for diagnostic purposes by persons trained on this laser by Spectra-Physics. Current is related to pump output power, and the current required to maintain a given output power will increase as the diodes age. This is normal.

**TEMPERATURE (DEG C) indicators**—show the current temperature of each diode laser and are to be used only for diagnostic purposes by persons trained on this laser by Spectra-Physics.

{76}------------------------------------------------

| Pump Power          | 5.00                                                                                                   |         |       |         |       |
|---------------------|--------------------------------------------------------------------------------------------------------|---------|-------|---------|-------|
| Current (amps)      | <table> <tr> <td>Diode 1</td> <td>21.00</td> </tr> <tr> <td>Diode 2</td> <td>22.00</td> </tr> </table> | Diode 1 | 21.00 | Diode 2 | 22.00 |
| Diode 1             | 21.00                                                                                                  |         |       |         |       |
| Diode 2             | 22.00                                                                                                  |         |       |         |       |
| Temperature (deg C) | <table> <tr> <td></td> <td>26.00</td> </tr> <tr> <td></td> <td>27.00</td> </tr> </table>               |         | 26.00 |         | 27.00 |
|                     | 26.00                                                                                                  |         |       |         |       |
|                     | 27.00                                                                                                  |         |       |         |       |
| SHG Status:         | Settled                                                                                                |         |       |         |       |
| History Buffer:     | 001 003 001 003 001 003 001 003 002 004 005 000 063 005 000 001                                        |         |       |         |       |
| Error Code:         | 0                                                                                                      |         |       |         |       |

Mai Tai Software Rev: A / 5.01 / T40-4420 REV H

Control software revision: 0453-8640A

## Figure 6-3: The Info Menu

**SHG STATUS monitor**—indicates when the SHG crystal is at operating temperature. Stable output is only possible when this crystal is "settled."

**HISTORY BUFFER list**—shows you the last 16 operations performed by the system. Although typically used by persons operating the system remotely, this list can be used for diagnostic purposes or just to see the most recent sequence of events.

**ERROR CODE indicator**—displays the last error code generated by the system. Although typically used by persons operating the system remotely as a feedback source for branching operations, it can be used for local diagnostic purposes as well.

**SOFTWARE REV statement**—shows the revision level of the current firmware. When calling for service, you will be asked for this number. It is used to determine the capability of your system, as well as its expected performance.

## The Scan Menu

The Scan menu (Figure 6-4) provides a means to scan from a beginning wavelength to an end wavelength in presettable steps, and to stop at each step for a preset period of time.

**OK button**—returns you to the Main menu regardless of the WAVELENGTH SCAN switch setting.

**START WAVELENGTH control**—sets the wavelength at which to begin a scan.

**STOP WAVELENGTH control**—sets the wavelength at which to end a scan.

**WAVELENGTH SCAN ON/OFF switch**—enables/disables the scan function. The system will continue to scan even if you press the OK button and return to the Main menu. This switch must be set to off to stop the scan.

{77}------------------------------------------------

| Scan Controls       |      |
|---------------------|------|
| <button>OK</button> |      |
| Start Wavelength    | 750  |
| Stop Wavelength     | 850  |
| nm/step             | 10   |
| Seconds per step    | 1.00 |

Wavelength Scan

On

Off

## Figure 6-4: The Scan Menu

**nm/STEP control**—sets the interval in nanometers between stops during a scan. When set to "0," stepping is defeated and the system will scan continuously between the begin and end wavelengths; the SECONDS PER STEP function is ignored.

**SECONDS PER STEP control**—sets the stop duration in tens of milliseconds during a scan.

# Turning On and Off the System

#### To turn on the system:

![](_page_77_Picture_7.jpeg)

The chiller must always be on when the *Mai Tai* power supply is on, even if the laser diodes are not switched on!

- 1. Verify that all connectors are plugged into the power supply (they should never be disconnected—if they were, refer to Chapters 4 and 5, for information on reconnecting them).
- 2. Verify the reservoir in the chiller has been filled to the correct level.
- 3. Turn on the chiller and verify it is set to  $21^{\circ}$ C.

It takes the chiller about 15 minutes to stabilize the temperature of the laser head cold plate and, thus, the output of the laser. To eliminate this stabilization period, leave the chiller on between periods of laser use. As a rule, if the laser is used often, leave the chiller on; if it is used infrequently, turn off the *Model J40* power supply, then turn off the chiller. Refer to the chiller user's manual for more detailed instructions.

- 4. Turn on the power supply power switch.
- 5. Turn on the power supply key switch.

#### **Power Supply Start-up**

As the system starts up, the following message sequence is displayed on the power supply LCD screen:

- "Spectra-Physics" followed by the software version number.
- Self tests 1 through 12 will complete, followed by the announcement:

{78}------------------------------------------------

• "Success. Boot test passed."

This is the final display from the *Model J40* power supply, which indicates it is ready for use.

1. Turn on the computer as you would normally, then double-click the "*Mai Tai*" icon on the desktop to start the control program. The Com Port Setup menu shown below will appear.

MaiTai Controller: COM Port Setup

| COM Port | <input type="number" value="1"/> |
|----------|----------------------------------|
|----------|----------------------------------|

 COM1 for most laptops, but probably COM2 for a desktop PC w/a serial mouse


|  | OK   |
|--|------|
|  | Exit |

# Figure 6-5: The Com Port (SERIAL COM) Setup Menu

- 2. Verify the com port setting is correct for your system, then press OK. The system will look for the *Mai Tai* and, when found, will display the Main menu (Figure 6-1).
- 3. Wait until the status warning on the control screen says "Ready to turn on," then turn on the laser.

Click on the ON/OFF button and hold down the mouse button for about 3 seconds until the "EMISSION" light turns on (the emission light on the laser will also turn on). The laser is on when the EMISSION light is on. However, no light is emitted until the shutter is opened in Step 6.

- 4. Set the desired wavelength from the Main menu.
- 5. Observe the PULSING indicator to verify pulses are present.
- 6. Open the shutter.

Click on the SHUTTER button and hold down the mouse button for about 3 seconds until the SHUTTER light turns on. The shutter will open and emission will be present.

- 7. Observe the output power. It should reach specified power within 30 minutes.
- 8. To temporarily turn off laser emission without turning off the laser, press the SHUTTER button. Emission will stop immediately and the SHUTTER light will turn off. However, the EMISSION light will remain on to warn of possible emission. To open the shutter again, simply press the SHUTTER button again.

{79}------------------------------------------------

## To turn off the system:

1. Press the ON/OFF button to shut off the system.

The system will turn off immediately, as will the EMISSION light.

- 2. Press the SHUTTER button to close the shutter.
- 3. If you are done for the day and wish to turn off the computer, press the QUIT button to exit the program, then turn off the computer as you would normally.
- 4. Turn the *key switch* on the power supply to OFF and remove the key to prevent unauthorized use. To minimize start-up stabilizing time, leave the *power switch* on the power supply in the "on" position and leave the chiller on.

This is the preferred "off" mode for day-to-day operation. If you are not going to use the laser for an extended period of time, turn off the power supply completely, then turn off the chiller.

Warning!

The chiller must always be on when the *Mai Tai* power supply is on, even if the laser diodes are not switched on!

This completes the turn on/off sequence.

# The RS-232 Serial Port

# **Pinout/Wiring**

The *Mai Tai* RS-232 serial port on the power supply accepts a standard 9pin D-sub male/female extension cable for hookup. Only three of the pins are actually used:

| Pin Numbers | Usage                               |
|-------------|-------------------------------------|
| 2           | transmit data ( <i>Mai Tai</i> out) |
| 3           | receive data ( <i>Mai Tai</i> in)   |
| 5           | signal ground                       |

## **Communications Parameters**

Communications must be set to 8 data bits, no parity, one stop bit, using the XON/XOFF protocol (do not use the hardware RTS/CTS setting in your communications software). The baud rate is set to 9600 at power up.

# Command/Query/Response Format

In the interest of standardization, the RS-232 commands and queries used on the *Mai Tai* follow the SCPI protocol (Standardized Commands for Programmable Instruments). This protocol was developed with the user in mind, thus all commands are easily readable by the user. The following rules apply:

{80}------------------------------------------------

- All commands and responses are in ASCII format.
- Commands to the *Mai Tai* system are terminated by an ASCII carriage return, line feed, or both.

In this document, a carriage return is indicated by <CR> and a line feed by <LF>.

- All responses from the *Mai Tai* are terminated by an ASCII line feed character.
- All queries end with a question mark (?). If a query has no command associated with it, it is preceded with READ.
- The *Mai Tai* will not generate any signals on the RS-232 unless a query command is received first.
- Parameters are separated from commands by spaces.
- Commands have both a "short" and "long" form.

The long form is the completely written command. The short form is derived from the long form by dropping every character after the fourth character. If the fourth character is a vowel, a three-letter form is used. The only exceptions to this pattern are "OFF" and "ON".

Example:

Long form: SHUTTER 1 Short form: SHUT 1

In the examples in this document, the long form of the command is used with the short form portion of it written in capital letters and, when contained within text, the entire command is italicized (e.g., SHUT*ter* 1).

• Several commands have variations or subcommands which are separated by semicolons (:). Short and long forms of the various commands and subcommands may be freely mixed. For example, all of the following are equivalent:

READ:PLAS:DIOD1:CURR?

READ:PLASER:DIODE1:CURRENT?

READ:PLAS:DIODE1:CURR?

However, for consistency and readability, it is best to choose one form and stay with it throughout.

## Typical Command Usage

The control flow of a *Mai Tai* program might look like this:

- 1. Turn on the system, then wait approximately 15 seconds for the computers to initialize.
- 2. Begin issuing a series of READ:PCTW*armedup*? queries and wait for it to return a 100 to indicate the system is fully warmed up (i.e., 100% warm).
- 3. Set the output wavelength to 800 nm by issuing the WAV*elength* 800 command.
- 4. Turn on the laser by issuing the ON command.
- 5. Open the shutter by issuing the SHUT*ter* 1 command.

{81}------------------------------------------------

# Commands and Queries Used by the Mai Tai

## Quick Reference

The following is a list of the commands and queries used by the *Mai Tai* and are provided as a reference guide. A list with explanations follows in the next section.

CONTrol:PHAse **CONTrol:PHAse?** CONTrol:MLENable CONTrol:MLENable? ON OFF MODE MODE? PLASer: ERRCode? PLASer:HISTory? PLASer: AHISTory? PLASer:PCURrent PLASer: PCURrent? PLASer:POWer PLASer: POWer? **READ:PCTWarmedup? READ:PLASer:POWer?** READ:PLASer:PCURrent? **READ:PLASer:SHGS?**

READ:PLASer:DIODe(n):CURRent? READ:PLASser:DIODe(n):TEMPerature? READ:POWer? READ:WAVelength?

SAVe

SHUTter (n) SHUTter?

SYSTem:COMMunications:SERial:BAUD (nnnn)

SYSTem:ERR?

TIMer:WATChdog (n)

WAVelength (nnn) WAVelength? WAVelength:MIN? WAVelength:MAX?

\*IDN?

\*STB?

{82}------------------------------------------------

## Full Description

This sections explains the commands and queries in detail. The form of the command is followed by the form of the associated query, which is followed by an explanation of each.

## **CONTrol:PHASe nn.nn**

## **CONTrol:PHASe?**

Sets/reads the RF phase control. You should not have to use this control. Phase is reset to the factory setting every time the wavelength command is used.

## CONTrol:MLENable n (1, 0)

## CONTrol:MLENable?

Turns the mode locker RF drive signal on (1) or off (0). The query returns a 1 or 0. You should not have to use this control. The modulator RF is disabled whenever the pump laser is off and enabled when the pump laser is turned on (unless overridden by this command).

#### ON

Turns on the pump laser. Unless overridden by the *MODE* and/or PLA-Ser:POWer commands, the laser will turn on in power mode at the power level set by the factory.

The shutter is not automatically opened when the ON command is issued.

The response to this command depends on whether or not the system is warmed up. Use the READ:PCTW*armedup*? query to determine the progress of the warm-up cycle. When the response to the READ:PCT-W*armedup*? query reaches 100, the laser can be started. Do not issue an *ON* command while the response to READ:PCTW*armedup*? query is 1 to 99.

| If the response to<br>READ:PCTWarmedup?<br>is... | The response to <i>ON</i> is...                                                               |
|--------------------------------------------------|-----------------------------------------------------------------------------------------------|
| 0                                                | to begin diode temperature stabilization.<br>(approximately 2 minutes)                        |
| 1 to 99                                          | an execution error.<br>(The EXE_ERR bit in the status byte is set.)                           |
| 100                                              | the laser diodes turn on, and the system output ramps to the most recently set power/current. |

## OFF

Turns off the pump laser diodes, but the SHG crystal oven temperature is maintained for a quick warm-up time.

The shutter is not automatically closed.

{83}------------------------------------------------

#### **MODE nnnn (PPOWer/PCURrent)**

The system defaults to power mode and output power is set at the factory for optimum system performance. Do not set the unit to current mode or change the power setting. Increasing power may actually decrease output performance! This control is for diagnostic purposes only and is to be used only by someone trained on this laser by Spectra-Physics.

#### MODE?

The legal parameters are PPOWer for "pump laser power" and PCURrent for "pump laser percent current". The system always turns on in PPOWer mode by default.

The query returns PPOWer or PCURrent.

## PLASer:ERRCode?

Returns the pump laser error code. See Table 6-1 and Table 6-2.

## **PLASer:HISTory?**

Returns the contents of the history buffer. It returns a 16-byte (16 code) status code list from the history buffer with the most recent status codes listed first. The history buffer only stores status codes 0 - 126 generated by the power supply. Status codes from the *Mai Tai* laser head are not recorded and, therefore, will not be returned.

## **PLASer:AHISTory?**

Returns an ASCII version of the history buffer.

## PLASer:PCURrent nn.n (0 to 20.0)

## **PLASer:PCURrent?**

Sets the pump laser percentage of available current. This is only useful when the mode is set to MODE:PCUR*rent*.

The query returns the last commanded pump laser current percentage.

Do not change the power setting. Increasing power may actually decrease output performance! This control is for diagnostic purposes only and is to be used only by someone trained on this laser by Spectra-Physics.

#### PLASer:POWer n.nn (0 to 5.0)

## **PLASer:POWer?**

Sets the pump laser output power. This is useful only when the mode is set to MODE:PPOWer. It is overridden whenever the WAV*elength* command is issued.

The query returns the last commanded pump laser power in Watts. Use the query READ:PLASer:POWer? if you want to get the actual output power.

Do not change the power setting. Increasing power may actually decrease output performance! This control is for diagnostic purposes only and is to be used only by someone trained on this laser by Spectra-Physics.

{84}------------------------------------------------

### **READ:PCTWarmedup?**

Reads the status of the system warm-up time as a percent of the predicted total time (see the table below). The system responds with a value similar to "050%<LF>." When the response is "100%<LF>", the laser can be turned on.

## **READ:PLASer:POWer?**

Reads and returns the output power of the pump laser (0 to 5.5 W).

#### **READ:PLASer:PCURrent?**

Reads and returns the percentage of full operating current for the pump laser.

### **READ:PLASer:SHGS?**

Reads and returns the pump laser SHG status. The system responds " $\emptyset$ S<LF>" if the temperature is settled, "1S<LF>" if the oven is heating, and "2S<LF>" if it is cooling. Values less than zero indicate an error (such as a broken wire or loose cable).

#### **READ:PLASer:DIODe1:CURRent?**

#### **READ:PLASer:DIODe2:CURRent?**

Reads and returns the current, in Amperes, of the specified pump diode (diode 1 or 2). The value is equal to the actual operating percentage of maximum diode current. A typical response might be "75.1%<LF>".

### **READ:PLASer:DIODe1:TEMPerature?**

#### **READ:PLASer:DIODe2:TEMPerature?**

Reads and returns the current temperature, in degrees C, of the specified pump diode (diode 1 or 2). A typical response might be "20.5<LF>".

#### **READ:POWer?**

Reads and returns the output power, from 0 to 2.00 W, of the Mai Tai.

#### **READ:WAVelength?**

Reads and returns the operating wavelength of the *Mai Tai*. The returned value may not match the commanded wavelength until the system has finished moving to the newly commanded wavelength.

## SAVe

Saves the *Mai Tai* status. Use this command before turning off the ac power in order to return to this mode the next time the unit is turned on.

#### SHUTter n (1, 0)

### SHUTter?

SHUT*ter* 1 opens the shutter.

SHUT*ter* 0 closes the shutter.

SHUT*ter*? Reads and returns the shutter status. It is normal for SHUT*ter*? to return a "0" for approximately 1 second after issuing the SHUT*ter* 1 command or a "1" after issuing the SHUT*ter* 0 command.

{85}------------------------------------------------

## SYSTem:COMMunications:SERial:BAUD nnnn

Sets the baud rate to 300, 600, 1200, 4800, 19200, 38400, or 57600 baud. The system always powers up at 9600 baud.

Note: the demonstration program uses 38400 baud.

Note: the XON/XOFF protocol is used regardless of baud rate. Hard-ware handshaking is not used.

## SYSTem:ERR

Returns a numerical error and a text message (Table 6-1 and Table 6-2). These errors/messages are contained in a buffer which is gradually emptied as this command is used. These errors/messages are not the same as the ones you can obtain with READ:HIST*ory*? SYST*em*:ERR primarily indicates whether or not a command was properly received and executed.

## TIMEr:WATChdog n

Sets the number of seconds for the software watchdog timer. A value of zero disables the software watchdog timer.

If the *Mai Tai* does not receive a valid command (or Query) every n seconds, the pump laser is turned off.

## WAVelength nnn (in nm)

## WAVelength?

Sets the *Mai Tai* wavelength between 750 and 850 or 780 and 920 nm. It will also set the modulator RF phase and the pump laser output power to factory calibrated values.

The query reads and returns the most recent value of the WAV*elength* command. Use it to verify the command was properly received.

## WAVelength:MAX?

## WAVelength:MIN?

These queries return the maximum and minimum values for the WAV*e*-*length* command.

## \*IDN?

Returns a system identification string that contains 4 fields separated by commas such as:

"Spectra-Physics, MaiTai, xxx, 0453-8620A/5.10/J40-4420H."

The first field indicates the laser was made by Spectra-Physics; the second is the model name; the third is reserved; the fourth is the software revision, in this case, the model number, head software revision and power supply software revision.

{86}------------------------------------------------

| Binary<br>Digit | Decimal<br>Value | Name          | Interpretation                                                                                                                                                                         |
|-----------------|------------------|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0               | 1                | CMD_ERR (CE)  | Command error.<br>Something was wrong with the command format, the command was not understood                                                                                          |
| 1               | 2                | EXE_ERR (EE)  | Execution Error<br>A command was properly formatted, but could not be executed.<br>For example, a power command of "P:0<CR>" was sent, when<br>the minimum allowed power is 0.2 watts. |
| 2               | 4                | (reserved)    |                                                                                                                                                                                        |
| 3               | 8                | (reserved)    |                                                                                                                                                                                        |
| 4               | 16               | (reserved)    |                                                                                                                                                                                        |
| 5               | 32               | SYS_ERR (SE)  | Any "system" error. (An open interlock, or an internal diagnostic)                                                                                                                     |
| 6               | 64               | LASER_ON (LO) | Indicates that laser emission is possible.                                                                                                                                             |
| 7               | 128              | ANY_ERR (AE)  | Any of the error bits are set.                                                                                                                                                         |

# Table 6-1: Query Errors

## Table 6-2: Error Return List

| Binary<br>DigitS | Decimal<br>Value | Errors Returned        |
|------------------|------------------|------------------------|
| 0100 0000        | 64               | LO                     |
| 1000 0001        | 129              | CE + AE                |
| 1000 0010        | 130              | EE + AE                |
| 1000 0011        | 131              | CE + EE + AE           |
| 1010 0000        | 160              | SE + AE                |
| 1010 0001        | 161              | CE + SE + AE           |
| 1010 0010        | 162              | EE + SE + AE           |
| 1010 0011        | 163              | CE + SE + EE + AE      |
| 1100 0001        | 193              | CE + LO + AE           |
| 1100 0010        | 194              | EE + LO + AE           |
| 1100 0011        | 195              | CE + EE + LO + AE      |
| 1110 0000        | 224              | SE + LO + AE           |
| 1110 0001        | 225              | CE + SE + LO + AE      |
| 1110 0010        | 226              | EE + SE + LO + AE      |
| 1110 0011        | 227              | CE + EE + SE + LO + AE |

{87}------------------------------------------------

#### \*STB?

Returns the product status byte. This is a number between 0 and 255 and consists of the sum of the following weighted values:

- 1 Emission is possible (this bit follow the emission indicator light on the product). Note that the shutter may still be closed, even if this bit is set.
- 2 The *Mai Tai* is modelocked.
- 4 Reserved
- 8 Reserved
- 16 Reserved
- 32 Reserved
- 64 Reserved
- 128 Reserved

This completes the RS-232 command descriptions.

## Using the Chiller

Please refer to the manual that came with the chiller for information on how to operate it. In general, the reservoir should always be full before turning the unit on and the chiller should be set to 21°C whenever the laser is running.

Please note: it takes the chiller about 15 minutes to stabilize the temperature of the laser head cold plate and, thus, the output of the laser. Leaving the chiller on between periods of laser use will eliminate this stabilization period. In general, if the laser is used often, leave the chiller on between laser usage; if it is used infrequently, turn off the power supply, then turn off the chiller.

This completes the operation section.

{88}------------------------------------------------

At Spectra-Physics, we take pride in the durability of our products. We place considerable emphasis on controlled manufacturing methods and quality control throughout the manufacturing process. Nevertheless, even the finest precision instruments will need occasional service. We feel our instruments have favorable service records compared to competitive products, and we hope to demonstrate, in the long run, that we provide excellent service to our customers in two ways. First, by providing the best equipment for the money, and second, by offering service facilities that restore your instrument to working condition as soon as possible.

Spectra-Physics maintains major service centers in the United States, Europe, and Japan. Additionally, there are field service offices in major United States cities. When calling for service inside the United States, dial our toll-free number: **1 (800) 456-2552**. To phone for service in other countries, refer to the Service Centers listing located at the end of this section.

Order replacement parts directly from Spectra-Physics. For ordering or shipping instructions, or for assistance of any kind, contact your nearest sales office or service center. You will need your instrument model and serial numbers available when you call. Service data or shipping instructions will be promptly supplied.

To order optional items or other system components, or for general sales assistance, dial **1 (800) SPL-LASER** in the United States, or **1 (650) 961-2550** from anywhere else.

# Warranty

This warranty supplements the warranty contained in the specific sales order. In the event of a conflict between documents, the terms and conditions of the sales order shall prevail.

The *Mai Tai*<sup> $\mathbb{M}</sup>$  laser system is protected by a 12-month warranty. All mechanical, electronic, optical parts and assemblies are unconditionally warranted to be free of defects in workmanship and material for one the warranty period.</sup>

Liability under this warranty is limited to repairing, replacing, or giving credit for the purchase price of any equipment that proves defective during the warranty period, provided prior authorization for such return has been given by an authorized representative of Spectra-Physics. Warranty repairs or replacement equipment is warranted only for the remaining unexpired
