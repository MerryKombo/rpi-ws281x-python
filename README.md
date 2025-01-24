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

### Shutdown Server

The shutdown server can be run as a systemd service. Here are the steps to create and enable the service:

1. Create a new file in `/etc/systemd/system/` named `shutdown-server.service`. The content of the file should be as what you'll find in the `shutdown-server.service` file in this repository.
2. Reload the systemd manager configuration with `sudo systemctl daemon-reload`.  
3. Enable the service to start on boot with `sudo systemctl enable shutdown-server`.  
4. Start the service with `sudo systemctl start shutdown-server`.  
5. Install net-tools using the package manager of your system. `sudo apt-get install net-tools nmap`

You can check the status of your service with `sudo systemctl status shutdown-server`.  

### Shutdown Client

Open a terminal.  
Navigate to the directory where `shutdown-client.py` is located using the `cd` command.
For example:
`cd /home/poddingue/rpi-ws281x-python/`
Run the script with Python. If you want to send a 'reboot' command, you can run the script without any arguments. If you want to send a 'shutdown' command, you can provide any argument:
`./bin/python3 examples/shutdown-client.py` or
`./bin/python3 examples/shutdown-client.py shutdown`.

## Ansible

`ssh-copy-id -i ~/.ssh/roundernetes.pub poddingue@192.168.1.137`
We use Ansible to automate the setup and configuration of our project. Here are the steps we've taken recently:

1. We've created an inventory file (`inventory.ini`) that specifies the hosts we want to manage with Ansible. Here's what it looks like:

```ini
[pis]
192.168.1.28 ansible_python_interpreter=/usr/bin/python3
```

2. We've encountered an issue where Ansible was unable to find the Python interpreter on the remote host. We resolved this by creating a symbolic link between python and python3 on the remote host:
`sudo ln -s /usr/bin/python3 /usr/bin/python`
3. We've also encountered an issue where the Python setuptools package was not installed on the remote host. We resolved this by installing setuptools using the pip package manager:
`python3 -m pip install setuptools`
4. If the pip package manager is not installed on your system, you can install it using the package manager of your operating system. On a Debian-based system like Ubuntu, you can use the apt package manager to install pip for Python 3:
`sudo apt update
sudo apt install python3-pip`
5. Please note that these commands need to be run on the remote host where you are trying to execute the Ansible playbook.

## Stress CPU Setup

This repository contains the necessary files to set up a periodic CPU stress test using systemd.

### Files
- `systemd/stress-cpu.service`: Systemd service file.
- `systemd/stress-cpu.timer`: Systemd timer file.
- `scripts/random-stress-cpu.sh`: Script to run the stress test.

### Via ansible

```[WARNING]: Ansible is being run in a world writable directory (/mnt/c/support/users/FOSDEM/2025/rpi-ws281x-python), ignoring it as an ansible.cfg source.```

It indicates that Ansible is ignoring our ansible.cfg file because it is located in a world-writable directory.
This is a security feature to prevent unauthorized modifications to Ansible's configuration.

#### Why This Happens
A world-writable directory is one where all users on the system have write permissions (e.g., chmod 777).

Ansible ignores ansible.cfg files in such directories to prevent potential security risks (e.g., malicious users modifying the configuration).

### Workaround 

Move the `ansible.cfg` file to a directory that is not world-writable. For example:

1. Create a new directory for Ansible configuration:

```bash
mkdir ~/.ansible
```

2. Move the ansible.cfg file to this directory:

```bash
mv /mnt/c/support/users/FOSDEM/2025/rpi-ws281x-python/ansible.cfg ~/.ansible/ansible.cfg
```

3. Update the roles_path in the new ansible.cfg file to point to the correct location:

```ini
[defaults]
roles_path = /mnt/c/support/users/FOSDEM/2025/rpi-ws281x-python/ansible/roles
```

### Checks

After applying the above fix, run the playbook again:

```bash
ansible-playbook -i ansible/inventory/hosts ansible/playbooks/deploy-stress-test.yml
```

The warning should no longer appear, and Ansible should correctly recognize the ansible.cfg file.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/MerryKombo/rpi-ws281x-python.git
   cd rpi-ws281x-python
