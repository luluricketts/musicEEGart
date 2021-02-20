import time
import pygame
import csv
import numpy as np

files = ['furelise.mp3', 'showandtell.mp3', 'bootscootinboogie.mp3', 'mobamba.mp3']
pygame.init()
pygame.mixer.init()

user = input('User ID: ')
fields = ['user', 'song']
for i in np.arange(0, 120, 10):
    fields.append('{}-{}'.format(i, i+10))

rows = []

for i,file in enumerate(files):

    if i == 3: # mo bamba
        cont = input('Continue with last song?')
        if cont.lower() == 'no':
            break

    pygame.mixer.music.load(file)
    start = s = time.time()
    song_row = [user, i+1]

    time.sleep(3)
    print('\n\nsong: {}'.format(file[:-4]))
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        t = time.time()

        if round(t - s, 1) % 10. == 0:
            if round(t-s, 1) == 0.:
                continue

            pygame.mixer.music.pause()
            print('\nChoose an emotion for the last 10 seconds:\n')
            #print('0-Happy\t1-Sad\t2-Relaxed\t3-Energized\n4-Anxious\t5-Disgust\t6-Anger')
            print('2-Relaxed\t3-Energized')

            try: 
                emotion = int(input('Your Emotion: '))
            except:
                print('Invalid, please try again')
                emotion = int(input('Your Emotion (0-6)'))
            
            song_row.append(emotion)
            s = time.time()
            pygame.mixer.music.unpause()
        
        if len(song_row) == 14:
            break

    rows.append(song_row)
            
file_path = 'data/emotion_data/'
file_name = 'user{}emotions.csv'.format(user)
with open(file_path + file_name, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(rows)
