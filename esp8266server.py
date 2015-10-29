#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import logging
import sys, serial
from time import *
import datetime, string

def enum(**enums):
    return type('Enum', (), enums)

Status = enum(ERR=['ERROR', 'Fail'], OK=['OK', 'ready', 'no change', 'SEND OK'], BUSY='busy', LINK='Link')

def send_cmd( sCmd, waitTm=1, retry=5, delay=1):
	lp = 0
	ret = ""

	print( "Sending command: %s" % sCmd )

	for i in range(retry):
		ser.flushInput()
		ser.write( sCmd + "\r\n" )
		ret = ser.readline()	# Eat echo of command.
		sleep( 0.2 )
		while( lp < waitTm or 'busy' in ret):
			while( ser.inWaiting() ):
				ret = ser.readline().strip( "\r\n" )
				print( ret )
				lp = 0
			if( ret in Status.OK ): break
			#if( ret == 'ready' ): break
			if( ret in Status.ERR ): break
			sleep( delay )
			lp += 1

		sleep(delay)
		if( ret in Status.OK ): break

	print( "Command result: %s" % ret )
	return ret

def send_response(response, cid='0'):
	# no need to wait for response between these commands (or retry), so just send them out
	# ser.flushInput()
	ser.write( "AT+CIPSEND=" + cid + "," + str(len(response)) + "\r\n")
	sleep(0.3)
	ser.write( response + "\r\n" )
	sleep(0.3)

	send_res = False
	for i in range(100):
		while( ser.inWaiting() ):
			ret = ser.readline().strip( "\r\n" )
			# print ret
			if( ret == Status.OK[3] ):
				# print "send ok!"
				send_res = True
		if send_res: break
		sleep(0.1)

	sleep(0.3)
	ser.write( "AT+CIPCLOSE=" + cid + "\r\n" )
	sleep(0.3)


def process_request(response):
	has_link = False
	cid = '0'
	while( ser.inWaiting() ):
		ret = ser.readline().strip( "\r\n" )
		# print ret
		if (ret in Status.LINK):
			has_link = True
		ipd_str = '+IPD,'
		if (ipd_str in ret):
			cid = ret[ret.find(ipd_str) + len(ipd_str)]
	
	if has_link:
		# process response
		send_response(response, cid)

if len(sys.argv) != 5:
	print "Usage: esp8266test.py port baud_rate ssid password"
	sys.exit()

port = sys.argv[1]
#Baud rate should be: 9600 or 115200
speed = sys.argv[2]
ssid = sys.argv[3]
pwd = sys.argv[4]
p = 80

ser = serial.Serial(port,speed)
if ser.isOpen():
    ser.close()
ser.open()
ser.isOpen()

send_cmd( "AT" )
send_cmd( "AT+CWMODE=1" ) # set device mode (1=client, 2=AP, 3=both)
send_cmd( "AT+CWLAP", 30) # scan for WiFi hotspots
send_cmd( "AT+CWJAP=\""+ssid+"\",\""+pwd+"\"", 5 ) # connect
send_cmd( "AT+CIFSR", 5) # check IP address

send_cmd( "AT+CIPMUX=1" ) # multiple connection mode
send_cmd("AT+CIPSERVER=1," + str(p))

# process requests
while (1):
	process_request("GOT IT! (" + str(datetime.datetime.now()) + ")")
	sleep(0.3)

ser.close()


