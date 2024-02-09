import os
import re

def generate_host_file(filename):
    arp_output = os.popen('arp -a').read()
    ip_addresses = re.findall(r'\((.*?)\)', arp_output)

    with open(filename, 'w') as file:
        for ip in ip_addresses:
            file.write(ip + '\n')

if __name__ == '__main__':
    generate_host_file('hosts.txt')