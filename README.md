# METEK uSonic-3 3D Ultrasonic Anemometer Waggle Plugin
Waggle Sensor Plug-In for the [uSonic-3 CLASS-A MP](https://metek.de/product/usonic-3-class-a/)

The Sonic 3D provides observations of 3 wind components x, y, z and acoustic temperature T at sampling rate up to 50 Hz.. 

[Waggle Sensor Information](https://github.com/waggle-sensor)

## Determine the Serial Port
The Sonic utilzies an RS-485 serial connection to transmit data.

Therefore, to determine which port the instrument is plugged into, PySerial offers a handy toollist to list all serial ports currnetly in use.
```bash
python -m serial.tools.list_ports
```

The default serial settings for the RS-485 interface are:
1. Baud Rate = 57600
1. Data Bits = 8
1. Parity = None
1. Stop Bits = 1

## Data Sample
Below is a sample of the ASCII formatted data string transmitted from the instrument. 
The specific variables included within the string and their location are displayed at the end. 
```bash
1B010000322000000300100000000000;-0.015;0.053;0.062;16.486;0.055;164.451;0.055;1
``` 


## Testing 

Similar to the [Vaisala AQT530 plugin](https://github.com/jrobrien91/waggle-aqt) a docker container will be setup via Makefile 

### 1) Build the Container
```bash
make build
```

### 2) Deploy the Container in Background
```bash
make deploy
```

### 3) Test the plugin
```bash
make run

**METEK uSonic-3 3D Ultrasonic Anemometer Waggle Plugin** <br>
Waggle Sensor Plug-In for the [uSonic-3 CLASS-A MP](https://metek.de/product/usonic-3-class-a/) <br>
The Sonic 3D provides observations of 3 wind components x, y, z and acoustic temperature T at sampling rate up to 50 Hz.<br>
<br>
[Waggle sensor information](https://github.com/waggle-sensor)<br>
<br>
Build of the application was similar to the [Vaisala AQT530 plugin](https://github.com/jrobrien91/waggle-aqt)

**Access the data**<br>
A basic [Cookbook](https://github.com/sujanpal/instrument-cookbooks/blob/main/notebooks/METEK_Sonic3D_access.ipynb)
