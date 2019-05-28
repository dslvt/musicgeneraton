#%%
import pygame 
from midiutil import MIDIFile
import random as rd
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
get_random_midi(10)
playMusicWithStandartSettings('random.mid')
# degrees  = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number
# track    = 0
# channel  = 0
# time     = 0    # In beats
# duration = 1    # In beats
# tempo    = 60   # In BPM
# volume   = 100  # 0-127, as per the MIDI standard

# MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
#                       # automatically)
# MyMIDI.addTempo(track, time, tempo)

# for i, pitch in enumerate(degrees):
#     MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)

# with open("major-scale.mid", "wb") as output_file:
#     MyMIDI.writeFile(output_file)

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
    tempo = 60 
    volume = 100
    Midi = MIDIFile(1)
    Midi.addTempo(track, time, tempo)
    for i, pitch in enumerate(degrees):
        Midi.addNote(track, channel, pitch, time+i, duration, volume)

    with open("random.mid", "wb") as output_file:
        Midi.writeFile(output_file)

#%%
