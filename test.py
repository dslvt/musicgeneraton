#%%

import pygame 
from midiutil import MIDIFile as mf
import random as rd
from roll import MidiFile as MF
import numpy as np
import mido

from static import scales




#%%
mid = MF('midis\\ramen king.mid')
# print(mid.get_bar(1))
print(mid.bar_similarity(0))
#%%
# get_random_midi(10)
print(mid.get_bar(1))

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
    mid = MF("midis/mozard.mid")
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

#%%
mid = mf(1)
for i in range(16):
    mid.addNote(0, 0, 80, (1/4)*i, 1/4, 100)
for i in range(4):
    mid.addNote(0, 0, 72, i, 1, 80)
with open("check.mid", "wb") as output_file:
    mid.writeFile(output_file)

#%%
m = MF('midis\\Ocarina of Time.mid')
m.play()

#%%
def stop():
    zaglushka = MF('check.mid')
    zaglushka.play()

#%%
stop()

#%%
for i, track in enumerate(MF('check.mid').tracks):
    print("Track {}: {}".format(i, track.name))
    for msg in track:
        msg = msg.dict()
        if not isinstance(msg, mido.MetaMessage):
            # print(msg.keys())
            # print(type(msg.message.pitch))
            # for key in msg.dict().keys():
            #     print("{}".format(key))
            # print("{} {}".format(msg.dict()['note'], msg.dict()['message']))
            try:
                print("vel: {}, type: {}, time: {}, note: {}".format(msg['velocity'], msg['type'], msg['time'], msg['note']))
            except KeyError:
                pass

#%%
dir(mido.Message)

#%%
mid = mido.MidiFile()
track = mido.MidiTrack()
mid.tracks.append(track)

track.append(mido.Message('program_change', program=12, time=0))
# track.append(mido.Message('note_on', note=64, velocity=64, time=0))
# track.append(mido.Message('note_off', note=64, velocity=127, time=240))
for i in range(16):
    track.append(mido.Message('note_on', note=64, velocity=64, time=0))
    track.append(mido.Message('note_off', note=64, velocity=64, time=120))




mid.save('new_song.mid')

#%%
mid = mido.MidiFile('midis\\major-scale.mid')
print(mid.length)

#%%
m = MF('midis\\major-scale.mid')
m.print_notes()

#%%

#%%


#%%
nodes = {}
for i, track in enumerate(MF('midis\\major-scale.mid').tracks):
    print("Track {}: {}".format(i, track.name))
    for msg in track:
        msg = msg.dict()
        if not isinstance(msg, mido.MetaMessage):
            # print(msg.keys())
            # print(type(msg.message.pitch))
            # for key in msg.dict().keys():
            #     print("{}".format(key))
            # print("{} {}".format(msg.dict()['note'], msg.dict()['message']))
            try:
                # print(msg["note"])
                if nodes.get(msg["note"]) is None:
                    nodes[msg["note"]] = 1
                else:
                    nodes[msg["note"]] += 1
                # print("vel: {}, type: {}, time: {}, note: {}".format(msg['velocity'], msg['type'], msg['time'], msg['note']))
            except KeyError:
                pass
for key in nodes.keys():
    nodes[key] //= 2

keys = list(nodes.keys())
keys.sort()
tonic = keys[0]
pattern = ''
for i in range(12):
    if (tonic+i) in keys:
        pattern+='1'
    else:
        pattern+='0'

# print(pattern,  ' initial [attern ', (pattern[1:len(pattern)] + pattern[0]))
fscale = []
for key, value in scales.items():
    for i in range(12):
        if pattern == value:
            if key not in fscale:
                fscale.append(key)
        else:
            pattern = pattern[1:len(pattern)]+pattern[0]
            # print(pattern)

print(fscale)

#%%
deli = 8
# mid = MF('midis\\major-scale.mid')
mid = MF('a.mid')

in_one_deli = round(mid.get_total_ticks()/(round((1000000/mid.get_tempo())*mid.length)*deli))
print(in_one_deli, 'iod')
length = mid.length
nodes = mid.available_notes()
nodes.sort()
ar = np.empty([1, round((1000000/mid.get_tempo())*mid.length)*deli], dtype=int)


for i in range(ar.shape[1]):
    ar[0][i] = -1

for inx, channel in enumerate(mid.get_events()):
    timer = 0
    last_note = -1
    for msg in channel:
        if msg.type == 'note_on':
            print('new note ', msg.time, timer)
            if msg.time != 0:
                base = round(timer/in_one_deli)
                for i in range(round(msg.time/in_one_deli)):
                    ar[0][i+base] = 0
                timer += msg.time
            last_note = nodes.index(msg.note)
            
        elif msg.type == 'note_off':
            base = round(timer/in_one_deli)
            for i in range(round(msg.time/in_one_deli)):
                ar[0][i+base] = len(nodes)
            ar[0][base] = last_note
            timer += msg.time

print(ar)

#%%
mid = MF('a.mid')
mid.print_notes()
# mid.play()
print(mid.length)
mid.draw_roll()

# for idx, channel in enumerate(mid.get_events()):
#     timer = 0
#     is_note_now = false
#     for msg in channel:
#         if msg.type == "note_on":
            
#         if msg.type == "note_off":

print(mid.get_total_ticks(), round((1000000/mid.get_tempo())*mid.length)*deli)


#%%

mid = MF('midis\\mozart.mid')
print(mid.as_array())

#%%
mid = MF('midis\\ramen king.mid')
print(mid.as_array())

#%%
