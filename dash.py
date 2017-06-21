#!/usr/bin/python
#
# I'm not a python person, so most of this has been borrowed of cobbled from
# other peoples stuff. Original used scapy but it killed CPU in a RPi, pcapy is
# much more forgiving. 
#
# bubba@bubba.org 

from impacket.ImpactDecoder import *
from impacket.ImpactPacket import *
import requests
import pcapy
import time

PKT_TIME_DIFF = 60

# Assuming you have OpenDash installed and want to use SmartThings, set these
# Otherwise, it doesn't matter.
install_id = "00ac0059-935c-48e8-8973-xxxxxxxxxx"
access_token = "9fa8b962-2034-4ecb-b99d-xxxxxxxxxx"

def methodA():
	# yep, this script triggers find my wife's iphone.. sigh. 
	# https://github.com/albeebe/PHP-FindMyiPhone
	print "iPhone"
	os.system("php /home/pi/find-my-iphone/send-message.php")

def methodB():
	# this turns the temp down to 71 when pressed
	print "Temp Down"
	device_id = "88bc9887-aeac-488b-9259-xxxxxxxxx"
	requests.get("https://graph.api.smartthings.com:443/api/smartapps/installations/" + install_id + "/devices/" + device_id + "/setCoolingSetpoint/71?access_token=" + access_token)
	# it also calls IFTTT maker applet to resume schedule in 2 hours. I'd use
	# IFTTT soley for this method, but since it takes 15 minutes to kick in, I
	# need to set the temp using ST, then have IFTTT have it resume schedule
	# because resume schedule isn't implemented in ST... IoT what a time to be
	# alive! 
	requests.post("https://maker.ifttt.com/trigger/temp_button_pressed/with/key/b6jmx28KCIglkcwxxxxxxxxx")

def methodC():
	# Toggle my ropelights to set the mood. Toggle setting in OpenDash is nice.
	# If it was on, it turns off, vice versa. 
	print "Ropelights"
	device_id = "e75a3ef6-7a79-4ef5-993b-xxxxxxx"
	requests.get("https://graph.api.smartthings.com:443/api/smartapps/installations/" + install_id + "/devices/" + device_id + "/toggle?access_token=" + access_token)
 
def methodD():
	# Open or close the garage. 
	print "Garage 3rd"
	device_id = "ff440ab0-535c-4711-a1b1-a40869ec7b5c"
	requests.get("https://graph.api.smartthings.com:443/api/smartapps/installations/" + install_id + "/devices/" + device_id + "/toggle?access_token=" + access_token)

dash_buttons = {"10:ae:60:xx:xx:xx": {"name": "Cottonelle", "func": methodA},
                "f0:27:2d:xx:xx:xx": {"name": "Vitamin Water", "func": methodB},
                "74:75:48:xx:xx:xx": {"name": "Elements", "func": methodC},
				"0c:47:c9:xx:xx:xx": {"name": "Dropps", "func": methodB},
				"44:65:0d:xx:xx:xx": {"name": "IceBreakers", "func": methodD}
		}

dash_times = dict()

def arp_sniffer(hdr, data):
	packet = EthDecoder().decode(data)
	ip_hdr = packet.child()
	op_code = ip_hdr.get_ar_op()
	mac = ip_hdr.as_hrd(ip_hdr.get_ar_sha())
	dest_ip = ip_hdr.as_pro(ip_hdr.get_ar_spa())
	if dest_ip == '0.0.0.0' and op_code == 1:
		print "ARP: " + str(mac)
        	if mac in dash_buttons.keys():
                	if mac in dash_times.keys():
                    		prev_time = dash_times[mac]
                    		if (time.time()-prev_time) >= PKT_TIME_DIFF:
                        		dash_buttons[mac]["func"]()
                        		dash_times[mac] = time.time()
                	else:
                    		dash_buttons[mac]["func"]()
                    		dash_times[mac] = time.time()

max_bytes = 1024
promiscuous = 0 # every data packet transmitted can be received and read by a network adapter to which its connected
read_timeout = 100 # in milliseconds
pc = pcapy.open_live("eth0", max_bytes, promiscuous, read_timeout)
packet_limit = 10
pc.setfilter("arp")

while True:
	try:
		pc.loop(packet_limit, arp_sniffer) # capture packets
	except (KeyboardInterrupt, SystemExit):
    	raise
