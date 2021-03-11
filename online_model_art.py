#############################################################
# ONLINE FUNCTION TO COLLECT DATA FROM HEADSET IN REAL TIME #
#   THEN DISPLAY IMAGE                                      #
#############################################################

import mindwave
import time
from model_pipeline import model_pipeline

Fs = 128 # sampling rate
dt = 1./Fs 

print('Connecting...')
headset = mindwave.Headset('/dev/tty.MindWaveMobile-SerialPo')
time.sleep(3) # takes a while to establish connection on my device
print('Connected!')

# make sure connection is good
while headset.poor_signal > 5:
    print('Poor connection or signal, try readjusting headset')
    time.sleep(1)

raw_eeg = []
attention = []
meditation = []

print('Beginning data collection in')
for i in range(3,0, -1):
    print('{}...'.format(i))
    time.sleep(1)
print('Data collection beginning...')

# record until user presses ctrl C
while True:

    try:
        while headset.poor_signal > 5:
            # shouldn't happen
            print('Poor connection or signal, try readjusting headset')
            time.sleep(1)

        raw_eeg = headset.raw_value
        raw_attention = headset.attention
        raw_meditation = headset.meditation

        time.sleep(dt)

    # break out on ctrl C    
    except KeyboardInterrupt:
        print('Recording stopped, saving data...')

data = np.array([eeg, attention, meditation]).reshape(3,-1)

emotion_preds = model_pipeline(data[0], data[1], data[2])
print(emotion_preds)