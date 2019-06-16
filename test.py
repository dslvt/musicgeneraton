#%%
import pygame 
from midiutil import MIDIFile as mf
import random as rd
from roll import MidiFile
import numpy as np

# import pyFluidSynth
#%%
def play_music(music_file):
    """
    stream music with mixer.music module in blocking manner
    this will stream the sound from disk while playing
    """
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(music_file)
        print("Music file %s loaded!" % music_file)
    except pygame.error:
        print ("File %s not found! (%s)" % (music_file, pygame.get_error()))
        return
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(30)


#%%
def playMusicWithStandartSettings(music_file):
    music_file = music_file

    freq = 44100    # audio CD quality
    bitsize = -16   # unsigned 16 bit
    channels = 2    # 1 is mono, 2 is stereo
    buffer = 1024    # number of samples
    pygame.mixer.init(freq, bitsize, channels, buffer)
    # optional volume 0 to 1.0
    pygame.mixer.music.set_volume(0.8)
    try:
        # use the midi file you just saved
        play_music(music_file)
    except KeyboardInterrupt:
        # if user hits Ctrl/C then exit
        # (works only in console mode)
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()
        raise SystemExit

#%%
# get_random_midi(10)
playMusicWithStandartSettings('midis/AmazingGrace.mid')


#%%
def get_random_midi(n):
    degrees = [] 
    for i in range(n):
       degrees.append(rd.randint(60, 80)) 
    
    print(degrees)
    track = 0
    channel = 0
    time = 0
    duration = 1
    tempo = 100 
    volume = 100
    Midi = mf(1)
    Midi.addTempo(track, time, tempo)
    for i, pitch in enumerate(degrees):
        Midi.addNote(track, channel, pitch, time+i, duration, volume)

    with open("random.mid", "wb") as output_file:
        Midi.writeFile(output_file)

#%%
def drawMidi(music_file):
    mid = MidiFile("midis/mozard.mid")
    # get the list of all events
    # events = mid.get_events()
    # get the np array of piano roll image
    roll = mid.get_roll()
    # draw piano roll by pyplot
    mid.draw_roll()


#%%
#global variables
tempo = 100
gvolume = 1
music_file = 'midis\\Ocarina of Time.mid'
voices = 10
min_note = 1/16

#popul init
n_popul = 10
popul = np.array()



#%%
playMusicWithStandartSettings(music_file)

#%%
mid = mf(1)
for i in range(16):
    mid.addNote(0, 0, 80, (1/4)*i, 1/4, 100)
for i in range(4):
    mid.addNote(0, 0, 72, i, 1, 80)
with open("check.mid", "wb") as output_file:
    mid.writeFile(output_file)

#%%
m = MidiFile('midis\\Ocarina of Time.mid')
m.play()

#%%
def stop():
    zaglushka = MidiFile('check.mid')
    zaglushka.play()

#%%
stop()

#%%
