#%%
import pygame 
from midiutil import MIDIFile as mf
import random as rd
from roll import MidiFile as MF

import numpy as np
import mido

# import pyFluidSynth


#%%


#%%
# get_random_midi(10)


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
scales = {'Adonai Malakh':                      '111101010110',
          'Aeolian Flat 1':                     '100110101101',
          'Algerian':                           '101101111001', 
          'Bi Yu':                              '100100010010', 
          'Blues':                              '100101110010', 
          'Blues Diminished':                   '110110110110',
          'Blues Modified':                     '101101110010',
          'Blues Pentacluster':                 '111100100000',
          'Blues Phrygian':                     '110101110010',
          'Blues With Leading Tone':            '100101110011',
          'Chad Gadyo':                         '101101010000',
          'Chaio':                              '101001001010',
          'Chromatic Bebop':                    '111011010111',
          'Chromatic Diatonic Dorian':          '111101011110',
          'Chromatic Dorian':                   '111001011100',
          'Chromatic Dorian Inverse':           '100111010011',
          'Chromatic Hypodorian':               '101110011100',
          'Chromatic Hypodorian Inverse':       '100111001110',
          'Chromatic Hypolydian':               '110010111001',
          'Chromatic Hypolydian Inverse':       '110011101001',
          'Chromatic Hypophrygian Inverse':     '111001110100',
          'Chromatic Lydian':                   '110011100101',
          'Chromatic Lydian Inverse':           '110100111001',
          'Chromatic Mixolydian':               '111001110010',
          'Chromatic Mixolydian Inverse ':      '101001110011',
          'Chromatic Permuted Diatonic Dorian': '111011011101',
          'Chromatic Phrygian':                 '100111001011',
          'Chromatic Phrygian Inverse':         '111010011100',
          'Diminished Scale':                   '101101101101',
          'Dominant Bebop':                     '101011010111',
          'Dorian':                             '101101010110',
          'Dorian Aeolian':                     '101101011110',
          'Dorian Flat 5':                      '101101100110',
          'Dorico Flamenco':                    '110011011010',
          'Eskimo Hexatonic 2':                 '101010101001',
          'Eskimo Tetratonic':                  '101010010000',
          'Full Minor':                         '101101011111',
          'Genus Chromaticum':                  '110111011101',
          'Genus Diatonicum Veterum Correctum': '101011110101',
          'Genus Primum':                       '101001010000',
          'Genus Primum Inverse':               '100001010010',
          'Genus Secundum':                     '100011010101',
          'Gnossiennes':                        '101100110110',
          'Half-Diminished Bebop':              '110101111001',
          'Han-kumoi':                          '101001011000',
          'Harmonic Major':                     '101011011001',
          'Harmonic Minor':                     '101101011001',
          'Harmonic Minor Inverse':             '110011010110',
          'Harmonic Neapolitan Minor':          '111101011001',
          'Hawaiian':                           '101100010101',
          'Hira-joshi':                         '101100011000',
          'Honchoshi Plagal Form':              '110101100010',
          'Houseini':                           '101111011110',
          'Houzam':                             '100111010101',
          'Hungarian Major':                    '100110110110',
          'Ionian Sharp 5':                     '101011001101',
          'Iwato':                              '110001100010',
          'Jazz Minor':                         '101101010101',
          'Jazz Minor Inverse':                 '110101010110',
          'Kiourdi':                            '101101111110',
          'Kokin-joshi, Miyakobushi':           '110001010010',
          'Kung':                               '101010100100',
          'Locrian':                            '110101101010',
          'Locrian 2':                          '101101101001',
          'Locrian Double-Flat 7':              '110101101100',
          'Locrian Natural 6':                  '110101100110',
          'Lydian':                             '101010110101',
          'Lydian Augmented':                   '101010101101',
          'Lydian Diminished':                  '101100110101',
          'Lydian Minor':                       '101010111010',
          'Lydian Sharp 2':                     '100110110101',
          'Magen Abot':                         '110110101101',
          'Major':                              '101011010101',
          'Major Bebop':                        '101011011101',
          'Major Gipsy':                        '110011011001',
          'Major Locrian':                      '101011101010',
          'Major Minor':                        '101011011010',
          'Major and Minor Mixed':              '101111011111',
          'Maqam Hijaz':                        '110011011011',
          'Maqam Shaddaraban':                  '110111100110',
          'Messiaen Mode 3':                    '111011101110',
          'Messiaen Mode 3 Inverse':            '101110111011',
          'Messiaen Mode 4':                    '111100111100',
          'Messiaen Mode 4 Inverse':            '100111100111',
          'Messiaen Mode 5':                    '111000111000',
          'Messiaen Mode 5 Inverse':            '100011100011',
          'Messiaen Mode 6':                    '111010111010',
          'Messiaen Mode 6 Inverse':            '101011101011',
          'Messiaen Mode 7':                    '111110111110',
          'Messiaen Mode 7 Inverse:':           '101111101111',
          'Messiaen Truncated Mode 2':          '110100110100',
          'Messiaen Truncated Mode 3':          '110011001100',
          'Messiaen Truncated Mode 3 Inverse':  '100110011001',
          'Messiaen Truncated Mode 5':          '110000110000',
          'Messiaen Truncated Mode 5 Inverse':  '100001100001',
          'Messiaen Truncated Mode 6':          '101000101000',
          'Messiaen Truncated Mode 6 Inverse':  '100010100010',
          'Minor':                              '101101011010',
          'Minor Bebop':                        '101111010110',
          'Minor Gipsy':                        '101100111001',
          'Minor Locrian':                      '101101101010', 
          'Minor Pentatonic With Leading Tones':'101111110111', 
          'Mixolydian':                         '101011010110', 
          'Mixolydian Flat 5':                  '101011100110',
          'Mixolydian Sharp 5':                 '101011001110',
          'Moorish Phrygian':                   '110111011011',
          'Neapolitan Major':                   '110101010101',
          'Neapolitan Minor':                   '110101011001',
          'Neapolitan Minor Mode':              '111010101100',
          'Neveseri':                           '110100111011',
          'Nohkan':                             '101001101101',
          'Oriental':                           '110011100110',
          'Oriental Pentacluster':              '111001100000',
          'Overtone':                           '101010110110',
          'Pelog':                              '110100011000',
          'Phrygian':                           '110101011010',
          'Phrygian Aeolian':                   '111101011010',
          'Phrygian Flat 4':                    '110110011010',
          'Phrygian Locrian':                   '110101111010',
          'Prokofiev Scale':                    '110101101011',
          'Prometheus':                         '101010100110',
          'Prometheus Neapolitan':              '110010100110',
          'Ritsu':                              '110101001010',
          'Rock n Roll':                        '100111010110',
          'Romanian Bacovia':                   '100011001001',
          'Romanian Major':                     '110010110110',
          'Sabach':                             '101110011010',
          'Sakura Pentatonic':                  '110001011000',
          'Sansagari':                          '100001000010',
          'Scriabin':                           '110010010100',
          'Shostakovich Scale':                 '110110110101',
          'Spanish Pentacluster':               '110111000000',
          'Spanish Phrygian':                   '110111011010',
          'Super Locrian':                      '110110101010',
          'Taishikicho, Ryo':                   '101011110111',
          'Takemitsu Tree Line Mode 1':         '101100101001',
          'Takemitsu Tree Line Mode 2':         '101100101010',
          'Twelve-Tone Chromatic':              '111111111111', 
          'Ultra Locrian':                      '110110101100',
          'Unison':                             '100000000000',
          'Ute Tritonic':                       '100100000010',
          'Utility Minor':                      '101101011011',
          'Verdi Enigmatic':                    '110011101011',
          'Verdi Enigmatic Ascending':          '110010101011',
          'Verdi Enigmatic Descending':         '110011001011',
          'Warao Tetratonic':                   '101100000010',
          'Wholetone Scale':                    '101010101010',
          'Wholetone Scale With Leading Tone':  '101010101011',
          'Youlan Scale':                       '111011110110',
          'Zirafkend':                          '101101011010'}

#%%
