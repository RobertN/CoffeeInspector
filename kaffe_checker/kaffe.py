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
	ERROR = 3

def make_request(state):
	print "Sending request"
	connection = httplib.HTTPConnection('www.yawnmedia.se')

	if state == KaffeState.ON:
		print "Changing state to: ON"
		try:
			connection.request("GET", "http://www.yawnmedia.se/kaffe/?state=ON")
		except:
			print "Failed to set new state - no connection"
	elif state == KaffeState.OFF:
		print "Changing state to: OFF"
		try:
			connection.request("GET", "http://www.yawnmedia.se/kaffe/?state=OFF")
		except:
			print "Failed to set new state - no connection"

def check_connection(interface, ip):
	if_output = ""

	# Check if the interface is listed when running ifconfig
	if_output = subprocess.check_output("ifconfig", stderr=subprocess.STDOUT, shell=True)
	if if_output.find(interface) == -1:
		return False

	# Retrieve the output from ifconfig "wlan0"
	try:
		if_output = subprocess.check_output("ifconfig " + interface, stderr=subprocess.STDOUT, shell=True)
	except subprocess.CalledProcessError:
		return False

	if if_output.find("inet addr:" + ip) != -1:
		# print "Found IP adress for " + interface
		return True

	# print "Did not find IP address"
	return False

def get_server_state():
	connection = httplib.HTTPConnection('www.yawnmedia.se');
	try:
		connection.request("GET", "http://www.yawnmedia.se/kaffe/");
		response = connection.getresponse();
	except socket.gaierror:
		print "Failed to connect to server"
		return KaffeState.ERROR

	state = response.read()

	values = state.split(';')

	if values[0] == "OFF":
		return KaffeState.OFF
	elif values[0] == "ON":
		return KaffeState.ON

def check_state():
	if check_connection("eth0", "10.30.3.") == False:
		return KaffeState.OFF

	return KaffeState.ON

if __name__ == "__main__":
	
	last_wifi_reset = 0
	print "Server state: " + str(get_server_state())
	print "True state: " + str(check_state())

	while 1:
		
		server_state = get_server_state()

		while 1:
			if not check_connection("wlan0", "192.168.1.") or (server_state == KaffeState.ERROR and time.time() - last_wifi_reset > 300):
				last_wifi_reset = time.time()
				os.system("./restartWifi.sh &")
				time.sleep(30)
				os.system("killall -9 restartWifi.sh")
			else:
				break

		if check_state() != server_state:
			print "Changing state"
			request = make_request(check_state())

		time.sleep(5)

