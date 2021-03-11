#############################################################
# ONLINE FUNCTION TO COLLECT DATA FROM HEADSET IN REAL TIME #
#   THEN DISPLAY IMAGE                                      #
#############################################################

import mindwave
import time
from model_pipeline import model_pipeline

Fs = 128 # sampling rate
dt = 1./Fs 
MAX_TIME = 120 # 2 min cap

print('Connecting...')
headset = mindwave.Headset('/dev/tty.MindWaveMobile-SerialPo')
time.sleep(3) # takes a while to establish connection on my device
print('Connected!')

# make sure connection is good
while headset.poor_signal > 5:
    print('Poor connection or signal, try readjusting headset')
    time.sleep(1)

data = np.zeros((3, Fs * MAX_TIME))

print('Beginning data collection in')
for i in range(3,0, -1):
    print('{}...'.format(i))
    time.sleep(1)
print('Data collection beginning...')

# capping out songs at 2 mins
for i in range(Fs * MAX_TIME):

    while headset.poor_signal > 5:
        # shouldn't happen
        print('Poor connection or signal, try readjusting headset')
        time.sleep(1)

    data[0,i] = headset.raw_value
    data[1,i] = headset.attention
    data[2,i] = headset.meditation

    time.sleep(dt)

emotion_preds = model_pipeline(data[0], data[1], data[2])
print(emotion_preds)