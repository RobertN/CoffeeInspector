#!/usr/bin/python

import time
import httplib
import socket

class KaffeState:
	ON = 1
	OFF = 2

def make_request(state):
	connection = httplib.HTTPConnection('localhost')

	if state == KaffeState.ON:
		print "Changing state to: ON"
		connection.request("GET", "http://jeppe.linkoping.osa/kaffe/?state=ON")
	elif state == KaffeState.OFF:
		print "Changing state to: OFF"
		connection.request("GET", "http://jeppe.linkoping.osa/kaffe/?state=OFF")


def check_state():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.settimeout(1)
	try:
		s.connect(("wiki", 80))
	except socket.gaierror:
		return KaffeState.OFF

	return KaffeState.ON

if __name__ == "__main__":

	last_state = KaffeState.OFF
	while 1:
		new_state = check_state()

		# if state has changed, let the server know
		if new_state != last_state:
			last_state = new_state
			make_request(new_state)

		time.sleep(5)

