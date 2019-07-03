#%%
import pygame 
from midiutil import MIDIFile as mf
import random as rd
from roll import MidiFile as MF
from mido import Message, MidiTrack
import numpy as np
import mido
from random import randint
from static import scales, input_files, name_notes
from sklearn.linear_model import LinearRegression
import datetime 


#%%

#%%
interval_size = {5: 1, 7: 1, 0: 1, 12: 0, 3: 2, 4: 2, 8: 2, 9: 2, 1: 3, 2: 3, 6: 4, 10: 3, 11: 3}

#initial values
num_epoch = 20
popul_size = 5 
result = []
generated_folder = 'generated'
#predeiined rhythm
file_name = 'ramen king.mid'
mid = MF('midis\\' + file_name)

print(mid.get_bar(0))
print(mid.last_note, 'last')

def get_num_noted(ar):
    notes = []
    for i in range(len(ar)):
        if ar[i] != mid.last_note and ar[i] != 0:
            notes.append(ar[i])
    return notes


def fitness_func(bar_inx, bar):
    funcs = [interval_fitness_func, melodic_mov_func]
    argums = [1, 1, 1]
    total_score = 0
    for itr, func in enumerate(funcs):
        total_score += argums[itr]*func(bar_inx, bar)
    return total_score


def melodic_mov_func(bar_inx, bar):
    x, y = [], []
    pos=1
    for i in range(len(bar)):
        if bar[i] != mid.last_note:
            y.append(bar[i])
            x.append(pos)
            pos+=1
    x = np.array(x).reshape((-1, 1))
    y = np.array(y)
    model = LinearRegression().fit(x, y)
    result = abs(1 - model.score(x, y))*10
    if isinstance(result, type(None)):
        return 1
    return result
    
    

def mean_of_bar(ar):
    notes = get_num_noted(ar)
    total = 0
    for i in range(1, len(notes)):
        dif = abs(notes[i] - notes[i-1])
        if dif > 12:
            total += 5
        else:
            total += interval_size[dif]
    return total/len(notes)

def var_of_bar(ar):
    notes = get_num_noted(ar)
    total = 0
    mean = mean_of_bar(ar)
    for i in range(1, len(notes)):
        total += (notes[i] - mean)**2
    return total/len(notes)

def interval_fitness_func(inx, bar):
    a, b = 1, 1
    mean, variance = 0, 0
    bar_mean = mean_of_bar(bar)
    bar_var = var_of_bar(bar) 

    for i in range(inx, mid.get_num_bars()):
        try:
            mean+=(1/(i+1))*(abs(bar_mean-mean_of_bar(mid.get_bar(i))))

            variance += (1/(i+1))*(abs(bar_var-var_of_bar(mid.get_bar(i))))
        except ZeroDivisionError:
            print("check interval fitness")

    return a*mean + b*variance

def mutate_bar(ar):
    if rd.random() > 0.8:
        # print(ar, 'before')
        notes = get_num_noted(ar)
        # print(notes, 'notes')
        avail = mid.available_notes()
        base = avail[0]
        #normalazing avail notes
        for i in range(len(avail)):
            avail[i] -= base - 1
        # print(avail)

        for i in range(len(notes)):
            if rd.random() < 0.1:
                #change for one random note
                notes[i] = randint(1, len(avail)-1)
            if rd.random() < 0.1:
                #swap with next
                if i != len(notes)-1:
                    notes[i], notes[i+1] = notes[i+1], notes[i]
        cur_note = 0
        for i in range(len(ar)):
            if ar[i] != mid.last_note and ar[i] != 0:
                ar[i] = notes[cur_note]
                cur_note+=1
        # print(ar, notes, 'after')
    return ar

def has_no_artefacts(ar):
    for i in range(len(ar)):
        assert(ar[i] <= mid.last_note)

changed_bars = [False for i in range(mid.get_num_bars())]
near_bars = [[] for i in range(mid.get_num_bars())]
# for i in range(1):
for i in range(mid.get_num_bars()):
    print("{} {}".format(i, 'bar'))
    if not changed_bars[i]: 
        #create st populaiton
        ref_bar = mid.get_bar(i)
        bar_size = len(ref_bar)
        population = [ref_bar for i in range(popul_size)]
        for j in range(len(population)):
            for k in range(len(population[j])):
                if ref_bar[k] != mid.last_note and ref_bar[k] != 0:
                    population[j][k] = randint(1, mid.last_note-1)
                else:
                    population[j][k] = ref_bar[k]


        for j in range(num_epoch):
            a = [(k, fitness_func(i, population[k])) for k in range(len(population))]
            a = sorted(a, key=lambda score: score[1])
            # print("{}: {}, {}: ".format('epoch', j, 'score', a[0][0]))
            new_popul = []
            for k in range(len(a)//2):
                new_popul.append(population[a[k][0]])
            for k in range(len(a)//2):
                new_popul.append(new_popul[randint(0, len(a)//2-1)])
            
            for k in range(len(new_popul)):
                new_popul[k] = mutate_bar(new_popul[k])
                has_no_artefacts(new_popul[k])

            population = new_popul
            #crossover and mutation
        #save best bar
        a = [(k, fitness_func(i, population[k])) for k in range(len(population))]
        sorted(a, key=lambda score: a[1])
        # result.append(population[a[0][0]])
        assert(len(population[a[0][0]]) == len(ref_bar))
        # print(population[a[0][0]], 'popul')
        for j in range(len(population[a[0][0]])):
            result.append(population[a[0][0]][j])
        # near_bars.append(mid.bar_similarity(i))
        
        changed_bars[i] = True
        near_coof, transpourisy = mid.bar_similarity(i)
        print(near_coof)
        for j in range(i+1, len(near_coof)):
            if near_coof[j] > 0.9:
                print('copy bar', i, j)
                changed_bars[j] = True
                for k in range(len(population[a[0][0]])):
                    if population[a[0][0]][k] != mid.last_note:
                        near_bars[j].append(population[a[0][0]][k]-transpourisy[j])
                    else:
                        near_bars[j].append(population[a[0][0]][k])
    else:
        print('change bar', i)
        for j in range(len(near_bars[i])):
            result.append(near_bars[i][j])
print(result)

#save song

now = datetime.datetime.now()
time = '-'.join([str(now.month), str(now.day), str(now.hour), str(now.minute)])
gmid = MF()
gmid.read_from_array(avail=mid.available_notes(), ar=result)
gmid.save("{}\\{}-{}{}".format(generated_folder, file_name, time, '_gen.mid'))
#%%
mid = MF('in\\o_la_paloma.mid')
print(str.lower(mid.get_scale())==str.lower('G major'))
count = 0
for name, scale in input_files.items():
    mid = MF('in\\'+name[3:])
    if get_scale_from_name_c(scale)==mid.get_scale2():
        count+=1
    else:
        print(get_scale_from_name_c(scale), mid.get_scale2(), name)
print(count, count/(len(input_files.items())))


#%%

mid = MF()
track = MidiTrack()
mid.tracks.append(track)

track.append(Message('program_change', program=12, time=0))
track.append(Message('note_on', note=64, velocity=64, time=32))
track.append(Message('note_off', note=64, velocity=127, time=0))

mid.refresh(None)
print(mid.get_total_ticks())

# mid.play_music()
#%%
def get_scale_from_name_c(name):
    scales = {'minor': '101101011010',
              'major': '101011010101'}
    name = name.split(' ')
    tonic_name, scale_name = str.lower(name[0]), str.lower(name[1])
    tonic = name_notes.index(tonic_name)
    scale = scales[scale_name]
    return scale[12-tonic:]+scale[0:12-tonic]

print(get_scale_from_name_c('C major'))
  
#%%
ar = [6, 7, 7, 7, 7, 7, 7, 7, 4, 7, 7, 7, 7, 7, 7, 7, 1, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
avail = [72, 75, 77, 78, 79, 82]

velo = [100 for i in range(len(ar))]
mid = MF()
# track = MidiTrack()
# mid.tracks.append(track)
# timestamp = 12
# has_pause = False
# last_note = -1
# time = 0
# pause_time=0
# for i in range(len(ar)):
#     if ar[i] != len(avail) + 1 and ar[i] != 0:
#         if last_note != -1:
#             track.append(Message('note_off', note=last_note, velocity=100, time=time))
#         last_note = avail[ar[i]-1]
#         track.append(Message('note_on', note=last_note, velocity=100, time=pause_time))
#         pause_time=0
#         time=timestamp
#     elif ar[i] == 0:
#         pause_time += timestamp
#     elif ar[i] == len(avail) + 1:
#         time += timestamp
# if pause_time==0:
#     track.append(Message('note_off', note=last_note, velocity=100, time=time))
# mid.refresh()
mid.read_from_array(ar, avail)
mid.draw_roll()

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

mid = MF('midis\\Ocarina of Time.mid')
genmid = MF()
genmid.read_from_array(mid.as_array(), mid.available_notes())
genmid.refresh()
# assert(len(genmid.as_array()) == len(mid.as_array()))
print(len(genmid.as_array()), len(mid.as_array()))
print(genmid.get_total_ticks(), mid.get_total_ticks())
# genmid.draw_roll()
# mid.draw_roll()
genmid.save('gen.mid')


#%%

len(mid.as_array())
#%%
mid.events

#%%
mid.events

#%%
genmid.events

#%%
genmid.as_array()

#%%
mid.as_array()[:40]

#%%
genmid.get_total_ticks()/(1000000/genmid.get_tempo())

#%%
mid.length/genmid.length

#%%
genmid.get_tempo()

#%%
genmid.play()

#%%
