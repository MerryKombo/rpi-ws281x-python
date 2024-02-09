# Roundernetes aRGB

Taken from  http://github.com/richardghirst/rpi_ws281x.

## Pre-requisites

Code found here: https://www.waveshare.com/wiki/PI4-FAN-PWM
```bash
python3 -m venv .
./bin/pip install rpi_ws281x
./bin/pip install gpiozero
./bin/pip install pigpio
./bin/pip3 install lgpio RPi.GPIO
./bin/pip3 install --upgrade lgpio
./bin/pip3 install requests
./bin/pip3 install matplotlib
```

## LED

| LED Number | Location | Description                             |
|------------|----------|-----------------------------------------|
| 0          | interior | between dami-3bplus 2 and dami-3bplus-3 |
| 1          | interior | between dami-3bplus-3 and dami-3bplus-1 |
| 2          | interior | between dami-3bplus-1 and goun-3bplus-1 |
| 3          | interior | between goun-3bplus-1 and goun-3bplus-2 |
| 4          | interior | goun-3bplus-2                           |
| 5          | interior | dami-3b-1                               |
| 6          | interior | between dami-3b-2 and goun-3bplus-3     |
| 7          | interior | between goun-3bplus-3 and dami-3bplus-2 |
| 8          | exterior | between dami-3bplus-1 and goun-3bplus-1 |
| 9          | exterior | goun-3bplus-1                           |
| 10         | exterior | between goun-3bplus-2 and goun-3bplus-2 |
| 11         | exterior | goun-3bplus-2                           |
| 12         | exterior | between goun-3bplus-2 and dami-3b-1     |
| 13         | exterior | dami-3b-1                               |
| 14         | exterior | between dami-3b-1 and dami-3b-2         |
| 15         | exterior | dami-3b-2                               |
| 16         | exterior | between dami-3b-2 and goun-3bplus-3     |
| 17         | exterior | between goun-3bplus-3 and dami-3bplus-2 |
| 18         | exterior | dami-3bplus-2                           |
| 19         | exterior | between dami-3bplus-2 and dami-3bplus-3 |
| 20         | exterior | dami-3bplus-3                           |
| 21         | exterior | between dami-3bplus-3 and dami-3bplus-1 |
| 22         | exterior | dami-3bplus-1                           |
| 23         | exterior | between dami-3bplus-1 and goun-3bplus-1 |


| Board Name | LED Numbers (interior) | LED Numbers (exterior) |
|------------|------------------------|------------------------|
| dami-3bplus-2 | 0                    | 8, 18, 19             |
| dami-3bplus-3 | 0, 1                 | 8, 19, 20, 21         |
| dami-3bplus-1 | 1, 2                 | 8, 21, 22             |
| goun-3bplus-1 | 2, 3, 9              | 8, 9, 10, 22, 23      |
| goun-3bplus-2 | 3, 4, 10, 11         | 10, 11, 12            |
| dami-3b-1     | 5, 13                | 13, 14                |
| dami-3b-2     | 5, 6, 15             | 14, 15, 16            |
| goun-3bplus-3 | 6, 7                 | 16, 17                |
| dami-3bplus-2 | 7                    | 17, 18, 19            |

## Systemd

### Light server

Create a new service file in `/etc/systemd/system/` with a `.service` extension.
For example, you could name it `light_server.service`. As for the content, have a look at the `light_server.service` file in this repository.
Now, you need to reload the systemd manager configuration with the following command:
```bash
sudo systemctl daemon-reload
```
Enable the service to start at boot time:
```bash
sudo systemctl enable light_server.service
```
Start the service:
```bash
sudo systemctl start light_server.service
```
Check the status of the service:
```bash
sudo systemctl status light_server.service
```
This should show that your service is active and running.

Stop the service:
```bash
sudo systemctl stop light_server.service
```

### Load client

Create a new service file in `/etc/systemd/system/` with a `.service` extension.
For example, you could name it `load_client.service`. As for the content, have a look at the `load_client.service` file in this repository.

```bash
sudoedit /etc/systemd/system/load_client.service
```

Now, you need to reload the systemd manager configuration with the following command:
```bash
sudo systemctl daemon-reload
```
Enable the service to start at boot time:
```bash
sudo systemctl enable load_client.service
```
Start the service:
```bash
sudo systemctl start load_client.service
```
Check the status of the service:
```bash
sudo systemctl status load_client.service
```
This should show that your service is active and running.

If in trouble, launch this command to get detailed logs:
```bash
sudo journalctl -u load_client -f &
```

Stop the service:
```bash
sudo systemctl stop load_client.service
```
