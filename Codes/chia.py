# -*- coding: utf-8 -*-
#####################################################
#    Project:     Chia Mining System                #
#    Programmer:  Sina Shiri                        #
#    Date:        2021 Jul 27                       #
#    For:         IchiCoin Group, Mining Department #
#####################################################

### import needed Packages ###
# Public Modules
import RPi.GPIO as GPIO
import time
import subprocess, os
import threading

# Config IOs
pi_led = 16
hd_led = 12
p_button = 26
r_button = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(pi_led, GPIO.OUT)
GPIO.setup(hd_led, GPIO.OUT)
GPIO.setup(p_button,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(r_button,GPIO.IN,pull_up_down=GPIO.PUD_UP)
# Turned Off LEDs
GPIO.output(pi_led,False)
GPIO.output(hd_led,False)

# Global varables
wb_addr = "1.1.1.1"
hdd_path = "/mnt/chia_plots_"

# Main Thread: check Internet Ping, Get User Shutdown Command
def main_thread():
	while (True):
		# Wait for Push Shutdown Button
		a = GPIO.input(p_button)
		b = GPIO.input(r_button)
		if a == False:
			time.sleep(2)
			output = subprocess.Popen(["sudo", "shutdown", "-h", "now"],stdout = subprocess.PIPE).communicate()[0]
		if b == False:
			time.sleep(2)
			output = subprocess.Popen(["sudo", "reboot"],stdout = subprocess.PIPE).communicate()[0]
		# Check a web address ping
		output = subprocess.Popen(["ping","-w","1","-c","1",wb_addr],stdout = subprocess.PIPE).communicate()[0]
		output = output.decode("utf-8")
		if ('0% packet loss' in output):
			GPIO.output(pi_led,True)
		else:
			GPIO.output(pi_led,False)

def sub_thread():
	while (True):
		# Check Connected HDD Devices
		cnt = 0
		for i in range(1,41):
			len_path = ""
			try:
				len_path = len(os.listdir(hdd_path+str(i)))
			except:
				continue
			if len_path != 0:
				cnt = cnt + 1
		# Show how many HDD was connected
		for j in range(0,cnt):
			GPIO.output(hd_led, True)
			time.sleep(0.5)
			GPIO.output(hd_led, False)
			time.sleep(0.5)
		time.sleep(10)

# Wait for Init.
time.sleep(60)

# Start Main Thread
mth = threading.Thread(target=main_thread)
mth.start()
print("#######################")
print("\tMain Thread Started...")

# Start Sub Thread
sth = threading.Thread(target=sub_thread)
sth.start()
print("#######################")
print("\tSub Thread Started...")

# Start Maining
print("#######################")
print("\tMining Will Started in 10 seconds...")
os.system("cd /home/pi/Desktop/linux-arm; sleep 10; ./hpool-chia-miner-linux-arm")