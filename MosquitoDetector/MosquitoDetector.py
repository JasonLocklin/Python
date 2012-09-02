#!/usr/bin/env python
"""
Mosquito Ringtone Detector

Detects the Mosquito ringtone via a microphone.

Author: Jason Locklin
	http://artsweb.uwaterloo.ca/~jalockli

You are free to Copy, Modify and Redistribute the following program
under the General Public License Version 3: 
           http://www.gnu.org/licenses/gpl.html
"""

# Required Python libraries
import pyaudio
from numpy import zeros,linspace,short,fromstring,hstack,transpose
from scipy import fft
from time import sleep
try: from pygame import mixer
except: print("You do not have pygame installed")

#Sensitivity, 0.05: Extremely Sensitive, may give false alarms
#                                       in some environments
#             0.1: Probably Ideal
#             1: Poorly sensitive, will only go off for relatively
#                                                       loud rings
SENSITIVITY= 0.07

#Ringtones to detect (Mosquito ringtone is 18000 hz)
RINGTONE = (16000,17000,17400,18000,19000,20000,21000,22000)
#Bandwidth for detection (i.e., detect sounds within this margin
#                                of error of the ringtone)
BANDWIDTH = 30

#Set up audio sampler
NUM_SAMPLES = 2048
SAMPLING_RATE = 44100
SPECTROGRAM_LENGTH = 100
pa = pyaudio.PyAudio()
_stream = pa.open(format=pyaudio.paInt16,
                  channels=1, rate=SAMPLING_RATE,
                  input=True,
                  frames_per_buffer=NUM_SAMPLES)

#Play a beep when sound detected.
try:
   mixer.init() #you must initialize the mixer
   alert=mixer.Sound('bell.ogg')
except: pass

print("Mosquito detector working. Press CTRL-C to quit.")
#Listen for ringtone
while True:
   while _stream.get_read_available()< NUM_SAMPLES: sleep(0.01)
   audio_data  = fromstring(_stream.read(
         _stream.get_read_available()), dtype=short)[-NUM_SAMPLES:]
   normalized_data = audio_data / 32768.0
   intensity = abs(fft(normalized_data))[:NUM_SAMPLES/2]
   frequencies = linspace(0.0, float(SAMPLING_RATE)/2, num=NUM_SAMPLES/2)
   for tone in RINGTONE:
      if max(
         intensity[(frequencies < tone+BANDWIDTH) &
                   (frequencies > tone-BANDWIDTH )]) > max(
         intensity[(frequencies < tone-1000) &
                   (frequencies > tone-2000)]) + SENSITIVITY:
         try: alert.play()
         except: print('\a') #try the system beep instead
         print("Mosquito Detected!")
   sleep(0.01)





