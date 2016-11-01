#in progress

from TSL2561 import *
import time
from utils import *

tsl = TSL2561() 

#initialization
blink_count=0
last_blink=0
blink_threshold=5
lux_old=500
time_threshold=12
lux_threshold=500
email_min_timespan=60
last_sent=-email_min_timespan

if tsl.foundSensor(): 
	print("Found sensor...")

	tsl.setGain(tsl.GAIN_16X);  
	tsl.setTiming(tsl.INTEGRATIONTIME_13MS)

	x = tsl.getFullLuminosity()     
	print("Full luminosity value: %d" % x)
	print("Full luminosity value: %#08x" % x)
    
	while True:
		now=time.time()
		if now-last_blink>=time_threshold:
			blink_count=0
		full = tsl.getLuminosity(tsl.FULLSPECTRUM)
		visible = tsl.getLuminosity(tsl.VISIBLE)
		infrared = tsl.getLuminosity(tsl.INFRARED)
		lux_diff=full-lux_old
		lux_old=full
		if lux_diff>lux_threshold or lux_diff<-lux_threshold:
			blink_count+=1
			last_blink=now
		if blink_count>=blink_threshold:
			blink_count=0
			if now-last_sent>=email_min_timespan:
				message=email_constructor("the laundry angel","our dear user","Laundry!!!","I see something blinking.")
				email_sender("ardtest304@gmail.com","password",["cx473@nyu.edu","fl1092@nyu.edu"],message)
				last_sent=now
			else:
				print("Too soon.")
			
	
else:
	print("No sensor?")
