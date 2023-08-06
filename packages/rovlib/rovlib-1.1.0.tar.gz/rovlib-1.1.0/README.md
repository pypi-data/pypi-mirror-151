# ROV Library

A custom library developed by [RobEn](https://github.com/RobEn-AAST) that exactly fits our needs, be it programmatically controlling a Remote Operated Vehicle (ROV) or processing image data from the on-board cameras, it's got you covered.

# Table of contents 🗒

- [Installation](#installation)
- [Usage](#general)
  - [Cameras](#cameras)
  - [Control](#control)
- [Dependency](#dependency)
  - [User side](#)
  - [ROV side](#)
- [Future Plans](#)
- [Authors](#authors)

<a id='installation'></a>

### Installing ⬇

The module is available at pypi, download with a simple

```bash
$ pip install rovlib
```

<a id='general'></a>

### General Usage 🔑

Like any other 3rd party module you can easily import the desired **sub-module** by specifying what you want from the main rovlib module

```python
from rovlib.cameras import RovCam
# or
from rovlib.control import RovMavlink, JoyStickControl
```

More about **rovlib.cameras** ? ➡ [Cameras module](#cameras)
</br>
More about **rovlib.control** ? ➡ [Control module](#control)

---

<a id='cameras'></a>

<h1 align="center"> ROV-cameras 🎥 </h1>

The camera module is required to receive OpenCV frames from ROV cameras being sent by the [On board camera system](https://github.com/RobEn-AAST/ROV-camsys) used in conjunction with this user level module.

<h2 align="center"> How to use it 🔧 </h2>

## Starting a camera 🟢

To start capturing frames from a specific camera you have to start an instance of RovCam similarly as starting a cv2.VideoCapture() instance from opencv.

As it might seem the interface is very similar to [OpenCV](https://opencv.org/)'s as the image data is originally captured on the ROV with OpenCV so it is required to run the script.

```python
from rovlib.cameras import RovCam
import cv2

cam = RovCam(RovCam.FRONT)

while True:
  image = cam.read()

  cv2.imshow("ROV", image)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cv2.destroyAllWindows()
```

The RovCam instance requires the user to specify which camera to get image data from, only a [supported camera](#cam-options) would work

<a id='cam-options'></a>

## Camera Options 📸

As for now the camera option are:

##### Front main camera looking ahead

> RovCam.FRONT

##### Arm facing camera looking exactly at the robotic arm

> RovCam.ARM

##### Misc cameras looking wherever we need to position them (still not supported in this version)

> RovCam.MISC1
> RovCam.MISC2

---

<a id='control'></a>

<h1 align="center"> ROV-control 🕹 </h1>

It is a python sub-module that simplifies the use of [pymavlink](https://mavlink.io/en/mavgen_python/) APIs, to ease the control of our beloved Alenda (the ROV).

<h2 align="center"> How to use it 🔧 </h2>

## Establish communication 🤝

```python
# create an instance of RovMavlink
# Those are the default constructor params.
rov = RovMavlink(connection_type = 'udpin', connection_ip = '0.0.0.0', connection_port = '14550', silent_mode = True)
# Binds to the port in the given address
rov.establish_connection()
```

To start controlling the **vehicle you should Arm it first**. To arm it use there following commands.

```python
# Silent mode is used to shut off prints from the used functions for instance - > 'vehicle Armed successfully'
rov = RovMavlink(silent_mode=False).establish_connection()
rov.arm_vehicle() # you only need to arm the vehicle once, there is no need to arm it every time you want to stablize it

# to disarm vehicle
rov.disarm_vehicle()
```

## Set vehicle mode 🎯

```python
rov = RovMavlink().establish_connection()
rov.arm_vehicle()
rov.set_vehicle_mode(rov.Mode.STABILIZE)
```

Those are all the modes you would need to use. If you used **_set_vehicle_mode()_** with any thing other that Mode enum it would raise a violation ❌.

```python
class Mode(IntEnum):
    STABILIZE = 0
    ACRO = 1
    ALT_HOLD = 2
    AUTO = 3
    GUIDED = 4
    CIRCLE = 7
    SURFACE = 9
    POSHOLD = 16
    MANUAL = 19

# use them as follows
# rov.set_vehicle_mode(Mode.STABILIZE)

```

## sending custom control 🎮

### ⚠ Take care the throttle of x, y, z and rotation is a value between **_-1 to 1_**. any value out side this boundry will raise a violation. ❌🔞

```python
rov.send_control(JoyStickControl(x_throttle = 0.5, y_throttle = 0.5, z_throttle = 0, rotation_throttle = 1))
```

also you can it as follows ⬇

```python
rov = RovMavlink(silent_mode=False).establish_connection()
period = 10 # period for moving the joystick control in seconds
rov.arm_vehicle()
# my_lovely_fake_joy_stick = JoyStickControl(x_throttle=1, y_throttle=1) # name the param u want to add and give it a value between -1 to 1
my_lovely_fake_joy_stick = JoyStickControl(y_throttle=0.8)
rov.send_control(my_lovely_fake_joy_stick)
```

## Orientation of the ROV 🧭

![ROV-Orienation](./imgs/rov-orientation.png?raw=true "orientation")

<a id='authors'></a>

## Authors

- [Karim Kohel](https://github.com/karimkohel)
- [Youssef Abbas](https://github.com/AbbasHabib)
- [Mostafa Wahdan](https://github.com/mhwahdan)
