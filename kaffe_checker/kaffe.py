#!/usr/bin/python

import time
import httplib
import socket
import sys
import subprocess
import os

class KaffeState:
	ON = 1
	OFF = 2

def make_request(state):
	print "Sending request"
	connection = httplib.HTTPConnection('www.yawnmedia.se')

	if state == KaffeState.ON:
		print "Changing state to: ON"
		connection.request("GET", "http://www.yawnmedia.se/kaffe/?state=ON")
	elif state == KaffeState.OFF:
		print "Changing state to: OFF"
		connection.request("GET", "http://www.yawnmedia.se/kaffe/?state=OFF")

def check_connection():
	interface = "wlan0"
	if_output = ""

	# Check if the interface is listed when running ifconfig
	if_output = subprocess.check_output("ifconfig", stderr=subprocess.STDOUT, shell=True)
	if if_output.find("wlan0") == -1:
		return False

	# Retrieve the output from ifconfig "wlan0"
	try:
		if_output = subprocess.check_output("ifconfig " + interface, stderr=subprocess.STDOUT, shell=True)
	except subprocess.CalledProcessError:
		return False

	if if_output.find("inet addr:192.168.1.") != -1:
		print "Found IP adress for " + interface
		return True

	print "Did not find IP address"
	return False

def get_server_state():
	connection = httplib.HTTPConnection('www.yawnmedia.se');
	connection.request("GET", "http://www.yawnmedia.se/kaffe/");
	response = connection.getresponse();

	state = response.read()

	values = state.split(';')

	if values[0] == "OFF":
		return KaffeState.OFF
	elif values[0] == "ON":
		return KaffeState.ON

def check_state():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.settimeout(3)
	try:
		s.connect(("10.30.0.237", 80))
	except socket.gaierror:
		return KaffeState.OFF

	return KaffeState.ON

if __name__ == "__main__":

	last_state = check_state()

	while 1:
		while 1:
			if not check_connection():
				os.system("./restartWifi.sh &")
				time.sleep(30)
				os.system("killall -9 restartWifi.sh")
			else:
				break

		new_state = check_state()

		# if state has changed, let the server know
		if new_state != last_state:
			last_state = new_state
			request = make_request(new_state)


		if get_server_state() != last_state:
			request = make_request(last_state)

		time.sleep(5)

