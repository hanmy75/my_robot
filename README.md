MY AI robot powered by google assistant
=======================================

### Update packages with AIY project repo
```
$ echo "deb https://dl.google.com/aiyprojects/deb stable main" | sudo tee /etc/apt/sources.list.d/aiyprojects.list
$ wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
$ sudo apt-get update
$ sudo apt-get upgrade -y
$ sudo reboot
```

### Install essential packages
- Install protobuf and google-assistant-library
```
$ sudo apt-get install -y git aiy-python-wheels
```

- Fix wheels installation fail
```
$ pip3 download protobuf
$ sudo nano /var/lib/dpkg/info/aiy-python-wheels.postinst
    ...
    # pip3 install --no-deps --no-cache-dir --disable-pip-version-check \
    #     /opt/aiy/python-wheels/protobuf-3.6.1-cp35-cp35m-linux_armv6l.whl
    ...
$ sudo dpkg --configure --force-overwrite --force-overwrite-dir -a
$ sudo apt-get install -y git aiy-python-wheels
$ sudo reboot
```

### Install mjpg-streamer
```
$ sudo apt-get install -y cmake libjpeg8-dev
$ cd ~
$ git clone https://github.com/jacksonliam/mjpg-streamer.git
$ cd ~/mjpg-streamer/mjpg-streamer-experimental
$ make
$ sudo make install
```

### Install MY Robot
```
$ git clone https://github.com/hanmy75/my_robot.git
$ sudo pip3 install -e my_robot/src
```
- Copy cert (assistant.json) to /home/pi


### Install snowboy
```
$ sudo apt -y install swig python3-pyaudio python3-pip libatlas-base-dev
$ sudo pip3 install pyaudio
$ pip3 install requests
$ git clone https://github.com/Kitt-AI/snowboy.git
$ cd ~/snowboy/swig/Python3
$ make
```

### Install ADS1115
```
$ cd ~
$ git clone https://github.com/adafruit/Adafruit_Python_ADS1x15.git
$ cd Adafruit_Python_ADS1x15
$ sudo python3 setup.py install
```

### Setup I2S amp
```
$ sudo nano /boon/config.txt
 ...
 #dtparam=audio=on
 dtoverlay=hifiberry-dac
 dtoverlay=i2s-mmap

[pi4]
 ...
```

### Pin-out
| Pin | BCM |  Usage  |
| :---: | :---: | :---: |
|     |     |   SW    |
|  16 |  23 |   NECK  |
|     |     |   I2C   |
|  3  |  2  |   SDA   |
|  5  |  3  |   SCL   |
|     |     | I2S AMP |
|  35 |  19 |  LRCLK  |
|  12 |  18 |   BCLK  |
|  40 |  21 |   DIN   |
|     |     |  Motor  |
|  24 |  8  |  M-ULA  |
|  22 |  25 |  M-ULB  |
|  27 |  0  |  M-URA  |
|  29 |  5  |  M-URB  |
|  32 |  12 |  M-DLA  |
|  28 |  1  |  M-DLB  |
|  31 |  6  |  M-DRA  |
|  33 |  13 |  M-DRB  |
|  36 |  16 |  M-WSTA |
|  38 |  20 |  M-WSTB |


### Reference
pi-zero PIN out : https://pinout.xyz

ADS1x15 : https://github.com/adafruit/Adafruit_Python_ADS1x15

HT16K33 : https://github.com/adafruit/Adafruit_CircuitPython_HT16K33

WEB UI  : https://hackaday.io/project/25092-zerobot-raspberry-pi-zero-fpv-robot
