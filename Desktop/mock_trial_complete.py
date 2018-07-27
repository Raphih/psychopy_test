### note: in display, keep track of time elapsed to ensure ITI is actually 5 seconds! ###
### arduino registers message to start session, but not to end session ###

from psychopy import visual, core
import serial
import random
import time 

### Create trial log ###
log = open('experiment_log2.txt','w')

### trial parameters ###

display_period = 1
delay_period = 3
ITI = 5


### create window and stimulus parameters ###
win = visual.Window([400,400])
frame_rate = int(win.getActualFrameRate())

gabor1 = visual.GratingStim(win, tex = 'sin', mask = 'gauss', sf = 4, size = 1.0, 
	name = 'gabor1', autoLog = False)
	
gabor2 = visual.GratingStim(win, tex = 'sin', mask = 'gauss', sf = 4, size = 1.0, 
	name = 'gabor2', autoLog = False)
gabor2.ori = 90

stimuli = [gabor1, gabor2]
	
### establish connection with arduino ###
arduino = serial.Serial('/dev/tty.usbmodem12341',115200, timeout = 0.1)
time.sleep(1)



def display(stim1_index, stim2_index):
	stimulus1 = stimuli[stim1_index]
	stimulus2 = stimuli[stim2_index]

	for i in range(frame_rate * display_period):
		stimulus1.draw()
		message = visual.TextStim(win, text='stimulus 1')
		message.pos = (0, 0.7)
		message.draw()
		win.flip()
			
	for i in range(frame_rate * delay_period):
		message = visual.TextStim(win, text='delay')
		message.pos = (0, 0.7)
		message.draw()
		win.flip()
	
	for i in range(frame_rate * display_period):
		message = visual.TextStim(win, text='stimulus 2')
		message.pos = (0, 0.7)
		message.draw()
		stimulus2.draw()
		win.flip()
		
	message = visual.TextStim(win, text='ITI')
	message.pos = (0, 0.7)
	win.flip()
		

def loop_read():
	start('s')
	keep_reading = 1
	while(keep_reading):
		data = arduino.readline() # see if this works
		#print(data)
		if(data):
			data = data.decode("utf-8")
			print(data)
			if data[0:3] == "$MV":
				display(int(data[-3]),int(data[-5]))
			keep_reading += 1
			log.write(data)
			if keep_reading > 100:
				keep_reading = 0
				end('e')				
			
			
			

def start(s):
	arduino.write(s.encode())
	
def end(c):
	arduino.write(c.encode())
	log.close()
	
	

loop_read()
	
	
	
	