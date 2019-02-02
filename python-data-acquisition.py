# USB ACCELEROMETER DEMO IN PYTHON

import serial
import math
from time import sleep

# FOR LINUX, RASPBERRY PI, ...
port = '/dev/ttyACM0'
# FOR WINDOWS
# port = 'COM1'

usbacc = serial.Serial(port)

# CHANGE RANGE TO +- 4
RANGE = 4
usbacc.write('RANGE ' + str(4))


# CHANGE FREQUENCY
# YOU DON'T NEED TO WAIT OR SLEEP
# IT IS ONLY FOR VISUAL EFFECT
usbacc.write('FREQ 6.25')
sleep(0.5)
usbacc.write('FREQ 12.5')
sleep(0.5)
usbacc.write('FREQ 25')
sleep(0.5)
usbacc.write('FREQ 50')
sleep(0.5)
usbacc.write('FREQ 100')
sleep(0.5)

# STOP AND START FOR FUN
usbacc.write('STOP')
usbacc.write('START')

# READ N SAMPLES
n_samples = 100

input_csv = []

for _ in range(n_samples):
	 input_csv.append(usbacc.readline())

# FUNCTION FOR CONVERSION
# FROM LIST OF CSV STRINGs TO
# LIST OF LIST OF FLOATS
def csv_to_2D_list(csv_list):
	# YOU CAN USE acc_sample.strip() OR acc_sample[0:-2]
	# TO GET RID OFF TWO LAST CHARACTERS: '\r\n'
	# '40,-100,127\r\n' --[0:-2] OR STRIP--> '40,-100,127' --
	# SPLIT--> ['40','-100','127'] --LIST AND MAP--> [4.0,-100.0,127.0]
	return [list(map(float, acc_sample[0:-2].split(','))) for acc_sample in csv_list]

acc = csv_to_2D_list(input_csv)

# PRINT COLLECTED DATA AND 
# CALCULATE AVERAGE ACCELERETION IN m/s^2
accx_avg = 0.0
accy_avg = 0.0
accz_avg = 0.0

for sample in acc:
	print(sample)
	accx_avg = accx_avg + sample[0]
	accy_avg = accy_avg + sample[1]
	accz_avg = accz_avg + sample[2]

accx_avg = accx_avg / float(n_samples)
accy_avg = accy_avg / float(n_samples)
accz_avg = accz_avg / float(n_samples)

# CALCULATE TOTAL AVERAGE ACCELERATION
g = 9.81 # VELUE OF G IN METERS PER SECOND SQUARE
a = g * math.sqrt(accx_avg**2 + accy_avg**2 + accz_avg**2) * (RANGE / 512.0)
print('\nTotal average acceleration is equal ' + str(a) + ' m/s^2')

# CLOSE USB CONNECTION
usbacc.close()
