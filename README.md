# What is this?
This is a simple python service which subscribes to two different MQTT topics (https://nanomq.io) and then combines the data to create a new virtual state like `human presence detected` in a room. 

One topic provides data fed in by a noise sensor which is attached to a RPI. It uses the service https://github.com/arnonuem/noise-sniffer.

The other topic provides everything which my Philipps Hue-Bridge knows. This was achieved using the excellent library https://github.com/trickeydan/hue2mqtt-python.

Once the virtual state goes into the condition of no human presence a 10 minute timer is started which, when not interrupted, will turn off the lamps in the living room.

## Architecture

![Architecture overview](https://github.com/arnonuem/py-smart-hue/blob/main/smart-hue-arch.png?raw=true)

# Installation
Clone the repo and install Paho MQTT dependency.
```
sudo pip3 install paho-mqtt
```
Script can be manually started using:
```
python3 /path/to/script
```
The script will run forever.

# Post installation
This is optional but recommended :)

## Installing the script as a system service.
In `/etc/systemd/system/` create a file like `smart-hue.service`.

Add the following content:
```
[Unit]

Description=Run smart-hue

After=default.target

[Service]

Type=simple
User=someuser
Group=someuser
ExecStart=python3 /home/someuser/py-smart-hue/smart-hue.py

[Install]

WantedBy=default.target
```

### Controlling the service
```
sudo systemctl start|stop|status smart-hue.service
```


