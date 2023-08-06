# CreaTeBME
Python Package for interfacing the bluetooth IMU module for CreaTe M8 BME.

## Installation
To install the latest stable version simply run `pip install CreaTeBME`.

## Usage

### Easy Wireless
To connect to the sensors, a simple call of the `connect()` method can be used. This method will return a list of `ImuSensor` objects.
```python
from CreaTeBME import connect

sensors = connect()
```
The `take_mesurement()` method of the ImuSensor objects can in return be used to read out the gyroscope and accelerometer data.
```python
while True:
    for sensor in sensors:
        measurement = sensor.take_measurement()
        # Do something with the data
```
This will return a list of the accelerometer and gyroscope data in the form `[acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z]`. The accelerometer values are given in `g (9.81 m/s^2)` and the gyroscope values in `deg/s`.

### Manual Wired and Wireless

Another way of connecting IMU sensors is to manually create `ImuSensor` objects. This can be done by specifying the mode and the address of the sensor.
```python
from CreaTeBME.ImuSensor import ImuSensor, MODE_WIRED, MODE_WIRELESS

sensor_wired = ImuSensor(MODE_WIRED, 'COM4')
sensor_wireless = ImuSensor(MODE_WIRELESS, '01:23:45:67:89:AB')
```
For a wired sensor, the address is the serial port on the computer, on Windows this will be `COM` followed by a number.
For a wired sensor, the bluetooth address is used, this will look like `01:23:45:67:89:AB`.

## Common errors

### Windows installation
On Windows, during the installation a compile error for pybluez will likely come up.
To solve this, install the pybluez 0.22 wheel before installing this package. A PyBluez 0.22 wheel for Python 3.8 can be found [here](https://github.com/CreaTe-M8-BME/CreaTeBME/raw/main/PyBluez-0.22-cp38-cp38-win_amd64.whl).
Download it to your current directory and install it using `pip install PyBluez-0.22-cp38-cp38-win_amd64.whl`.

### Running in PyCharm
When using this package and running your program in PyCharm, an error complaining about CMD not being found can show. To solve this, run `py xxx.py` in the terminal, where `xxx` is the file name of the python file you want to run.

