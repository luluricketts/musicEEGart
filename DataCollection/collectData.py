import mindwave
import time
import json

Fs = 128 # sampling rate
dt = 1/Fs 
MAX_TIME = 120 # 2 min cap

print('Connecting...')
headset = mindwave.Headset('/dev/tty.MindWaveMobile-SerialPo')
time.sleep(3) # takes a while to establish connection on my device
print('Connected!')

# make sure connection is good
while headset.poor_signal > 5:
    print('Poor connection or signal, try readjusting headset')
    time.sleep(1)

out_file_path = 'data/'

eeg = dict()
user = input('User ID: ')
song_id = input('Song ID: ')
song_name = input('Song Title: ')
eeg['genre'] = input('Genre: ')
eeg['song'] = song_name
eeg['user'] = user

out_file_path = 'data/'
out_file_name = 'user{}song{}'.format(user, song_id)

attention = []
meditation = []
raw_eeg = []

print('Beginning data collection in')
for i in range(1,4):
    print('{}...'.format(i))
    time.sleep(1)
print('Data collection beginning...')

# capping out songs at 2 mins for training seems ok (128 * 120 = 15360 samples per trial)
for i in range(Fs * MAX_TIME):

    while headset.poor_signal > 5:

        # shouldn't happen
        print('Poor connection or signal, try readjusting headset')
        time.sleep(1)

    attention.append(headset.attention)
    meditation.append(headset.meditation)
    raw_eeg.append(headset.raw_value)

    time.sleep(dt)

print('Data collection completed...saving as json object')

eeg['attention'] = attention
eeg['meditation'] = meditation
eeg['raw_eeg'] = raw_eeg

with open('{}.json'.format(out_file_path + out_file_name), 'w') as outfile:
    json.dump(eeg, outfile)

print('Process completed for user {} for song: {}'.format(user, song_name))