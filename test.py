#%%

import pygame 
from midiutil import MIDIFile as mf
import random as rd
from roll import MidiFile as MF
from mido import Message, MidiTrack
import numpy as np
import mido
from random import randint
from static import scales


#%%
popul_size = 2
result = []
#predeiined rhythm
mid = MF('midis\\garbadje.mid')
print(mid.get_bar(0))
print(mid.last_note)

def fitness_func(ar):
    return 1

def mutate_bar(ar):
    pass

for i in range(1):
# for i in range(len(mid.get_num_bars())):
    num_epoch = 1
    #create st populaiton
    ref_bar = mid.get_bar(i)
    bar_size = len(ref_bar)
    population = [np.zeros(bar_size, dtype=int) for i in range(popul_size)]
    for j in range(len(population)):
        for k in range(len(population[j])):
            if ref_bar[k] != mid.last_note and ref_bar[k] != 0:
                population[j][k] = randint(1, mid.last_note-1)
            else:
                population[j][k] = ref_bar[k]
    for j in range(num_epoch):
        a = [(k, fitness_func(population[k])) for k in range(len(population))]
        sorted(a, key=lambda score: a[1])
        new_popul = []
        for i in range(num_epoch//2):
            new_popul.append(population[a[0]])
        for i in range(num_epoch//2):
            new_popul.append(new_popul[randint(0, num_epoch//2-1)])
        
        #crossover and mutation
    #save best bar
    a = [(k, fitness_func(population[k])) for k in range(len(population))]
    sorted(a, key=lambda score: a[1])
    result.append(population[a[0][0]])

print(result)
#save song
# mid = MF()
# mid.read_from_array(result)
# mid.save("generated.mid")


#functions

#create bar
     #evaluate fitness function
        #roulette selection
        #crossover and mutation


#roulette selection
# def selection(ar):
#     for

#fitness function

#%%

mid = MF()
track = MidiTrack()
mid.tracks.append(track)

track.append(Message('program_change', program=12, time=0))
track.append(Message('note_on', note=64, velocity=64, time=32))
track.append(Message('note_off', note=64, velocity=127, time=0))

mid.refresh(None)
print(mid.get_total_ticks())

# mid = MF('ab.mid')
# print(mid.get_total_ticks())

# mid.play_music()
#%%
ar = [25, 27, 27, 27, 23, 27, 24, 27, 18, 27, 27, 27, 23, 27, 24, 27, 16, 27, 17, 27, 25, 27,
 27, 27, 18, 27, 27, 27, 21, 27, 22, 27]
avail = [59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84]
velo = [100 for i in range(len(ar))]
mid = MF()
track = MidiTrack()
mid.tracks.append(track)
note_len = 0
note = 0
has_pause = False
pr = len(avail)+1
for i in range(len(ar)):
    if pr != ar[i] and ar[i] != 0:
        if has_pause:
            time = note_len
        else:
            track.append(Message('note_off', note=avail))
        track.append(Message)
        track.append(Message('note_on', note=avail[ar[i], time=time]))


#%%
mid = MF("midis\\ramen king.mid")
print(mid.get_in_one_deli()*mid.deli*mid.get_num_bars()*4, mid.get_total_ticks())
print(mid.get_bar(0))
mid.available_notes()

#%%
def read_from_array(ar, available_notes):




#crossover and mutation
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
