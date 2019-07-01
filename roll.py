import mido
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import colorConverter
import pygame
from static import scales, name_notes
from mido import Message, MidiTrack



# inherit the origin mido class
class MidiFile(mido.MidiFile):

    def __init__(self, filename=None):

        mido.MidiFile.__init__(self, filename)
        self.refresh()    
    
    #if you want update something in track, midi messages, you need use refresh
    def refresh(self, filename=None):
        self.sr = 10
        self.meta = {}
        self.events = self.get_events()
        self.music_file = filename
        for i, event in enumerate(self.events):
            if i != 0 and event != []:
                self.events[0] = event.copy()
                break
        self.deli = 8
        self.last_note = len(self.available_notes())+1
        self.meta = {'time_signature': {'type': 'time_signature',
            'numerator': 4,
            'denominator': 4,
            'clocks_per_click': 24,
            'notated_32nd_notes_per_beat': 8,
            'time': 0},
            'end_of_track': {'type': 'end_of_track', 'time': 0},
            'set_tempo': {'type': 'set_tempo', 'tempo': 428571, 'time': 0},
            'track_name': {'type': 'track_name', 'name': 'FL Keys', 'time': 0}}


    
    def get_num_bars(self):
        return round(250000/self.get_tempo()*self.length)

    def get_tonic(self):
        tonic_mid = 0
        for msg in self.events[0]:
            if msg.type == 'note_on':
                tonic_mid = msg.note
                break
        return tonic_mid

    #return how many ticks in one smallest posible note
    def get_in_one_deli(self):
        return round(self.get_total_ticks()/(round((1000000/self.get_tempo())*self.length)*self.deli))
        
    #return bar in array
    def get_bar(self, n):
        song = self.as_array()
        in_one_deli = self.get_in_one_deli()
        return song[int(n*self.get_total_ticks()/(self.get_num_bars()*in_one_deli)):
        int((n+1)*self.get_total_ticks()/(self.get_num_bars()*in_one_deli))]

    #return array with similarity from 0.0 to 1.0 for all bars and interval to change bar
    def bar_similarity(self, n):
        #check transp
        p = []
        transp = []
        bar = self.normalize_bar(self.get_bar(n))
        for i in range(self.get_num_bars()):
            cof1, cof2 = 0, 0
            init_bar = self.get_bar(i)
            bar1 = self.normalize_bar(init_bar.copy())
            transpose_val = bar[0]-init_bar[0]
            bar2 = self.transpose_bar(self.normalize_bar(init_bar.copy()), transpose_val)
            for j in range(len(bar1)):
                if bar[j] == bar1[j]:
                    cof1+=1
                if bar[j] == bar2[j]:
                    cof2+=1
            if cof1>=cof2:
                transp.append(0)
                p.append(cof1/len(bar))
            else:
                transp.append(transpose_val)
                p.append(cof2/len(bar))
        return p, transp


    def get_bar_ticks(self):
        return self.get_total_ticks()/self.get_num_bars()

    #delete all continues of note and fill it with number of note
    def normalize_bar(self, bar):
        last = -1
        prod = self.last_note
        for i in range(len(bar)):
            if bar[i] != prod:
                last = bar[i]
            elif bar[i] != 0:
                bar[i] = last
        return bar
    

    def transpose_bar(self, bar, n):
        for i in range(len(bar)):
            if not (bar[i]==self.last_note or bar[i]==0):
                bar[i]+=n
        return bar


    def set_filename(self, filename):
        self.music_file = filename
    

    def print_notes(self):
        for i, track in enumerate(self.tracks):
            # print("Track {}: {}".format(i, track.name))
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

    #return all posible notes in array
    def available_notes(self):
        tonic_mid = self.get_tonic() 
        
        tonic_mid = tonic_mid%12
        scale = ['0' for i in range(12)]
        for msg in self.events[0]:
            if msg.type == 'note_on':
                scale[msg.note%12] = '1'
        scale = scale[tonic_mid:]+scale[:tonic_mid]
        points = []
        for scl in scales.values():
            point = 0
            for i in range(12):
                if scl[i] == scale[i]:
                    point+=1
            points.append((scl, point))
        points = sorted(points, key = lambda val: val[1], reverse=True)
        scale = points[0][0]
        lowest_note, higtest_note = 1000, 0
        for msg in self.events[0]:
            if msg.type == 'note_on':
                lowest_note = min(lowest_note, msg.note)
                higtest_note = max(higtest_note, msg.note)
        
        ans = []
        for i in range(lowest_note, higtest_note+1):
            if scale[(i-tonic_mid)%12]=='1':
                ans.append(i)
        return ans

    def get_events(self):
        mid = self
        # print(mid)

        # There is > 16 channel in midi.tracks. However there is only 16 channel related to "music" events.
        # We store music events of 16 channel in the list "events" with form [[ch1],[ch2]....[ch16]]
        # Lyrics and meta data used a extra channel which is not include in "events"

        events = [[] for x in range(16)]

        # Iterate all event in the midi and extract to 16 channel form
        for track in mid.tracks:
            for msg in track:
                try:
                    channel = msg.channel
                    events[channel].append(msg)
                except AttributeError:
                    try:
                        if type(msg) != type(mido.UnknownMetaMessage):
                            self.meta[msg.type] = msg.dict()
                        else:
                            pass
                    except:
                        print("error",type(msg))

        return events

    def get_roll(self):
        events = self.get_events()
        # Identify events, then translate to piano roll
        # choose a sample ratio(sr) to down-sample through time axis
        sr = self.sr

        # compute total length in tick unit
        length = self.get_total_ticks()

        # allocate memory to numpy array
        roll = np.zeros((16, 128, length // sr), dtype="int8")

        # use a register array to save the state(no/off) for each key
        note_register = [int(-1) for x in range(128)]

        # use a register array to save the state(program_change) for each channel
        timbre_register = [1 for x in range(16)]


        for idx, channel in enumerate(events):

            time_counter = 0
            volume = 100
            # Volume would change by control change event (cc) cc7 & cc11
            # Volume 0-100 is mapped to 0-127

            print("channel", idx, "start")
            for msg in channel:
                if msg.type == "control_change":
                    if msg.control == 7:
                        volume = msg.value
                        # directly assign volume
                    if msg.control == 11:
                        volume = volume * msg.value // 127
                        # change volume by percentage
                    # print("cc", msg.control, msg.value, "duration", msg.time)

                if msg.type == "program_change":
                    timbre_register[idx] = msg.program
                    print("channel", idx, "pc", msg.program, "time", time_counter, "duration", msg.time)



                if msg.type == "note_on":
                    print("on ", msg.note, "time", time_counter, "duration", msg.time, "velocity", msg.velocity)
                    note_on_start_time = time_counter // sr
                    note_on_end_time = (time_counter + msg.time) // sr
                    intensity = volume * msg.velocity // 127



					# When a note_on event *ends* the note start to be play 
					# Record end time of note_on event if there is no value in register
					# When note_off event happens, we fill in the color
                    if note_register[msg.note] == -1:
                        note_register[msg.note] = (note_on_end_time,intensity)
                    else:
					# When note_on event happens again, we also fill in the color
                        old_end_time = note_register[msg.note][0]
                        old_intensity = note_register[msg.note][1]
                        roll[idx, msg.note, old_end_time: note_on_end_time] = old_intensity
                        note_register[msg.note] = (note_on_end_time,intensity)


                if msg.type == "note_off":
                    print("off", msg.note, "time", time_counter, "duration", msg.time, "velocity", msg.velocity)
                    note_off_start_time = time_counter // sr
                    note_off_end_time = (time_counter + msg.time) // sr
                    note_on_end_time = note_register[msg.note][0]
                    intensity = note_register[msg.note][1]
					# fill in color
                    roll[idx, msg.note, note_on_end_time:note_off_end_time] = intensity

                    note_register[msg.note] = -1  # reinitialize register

                time_counter += msg.time

                # TODO : velocity -> done, but not verified
                # TODO: Pitch wheel
                # TODO: Channel - > Program Changed / Timbre catagory
                # TODO: real time scale of roll

            # if there is a note not closed at the end of a channel, close it
            for key, data in enumerate(note_register):
                if data != -1:
                    note_on_end_time = data[0]
                    intensity = data[1]
                    # print(key, note_on_end_time)
                    note_off_start_time = time_counter // sr
                    roll[idx, key, note_on_end_time:] = intensity
                note_register[idx] = -1

        return roll

    def get_roll_image(self):
        roll = self.get_roll()
        plt.ioff()

        K = 16

        transparent = colorConverter.to_rgba('black')
        colors = [mpl.colors.to_rgba(mpl.colors.hsv_to_rgb((i / K, 1, 1)), alpha=1) for i in range(K)]
        cmaps = [mpl.colors.LinearSegmentedColormap.from_list('my_cmap', [transparent, colors[i]], 128) for i in
                 range(K)]

        for i in range(K):
            cmaps[i]._init()  # create the _lut array, with rgba values
            # create your alpha array and fill the colormap with them.
            # here it is progressive, but you can create whathever you want
            alphas = np.linspace(0, 1, cmaps[i].N + 3)
            cmaps[i]._lut[:, -1] = alphas

        fig = plt.figure(figsize=(4, 3))
        a1 = fig.add_subplot(111)
        a1.axis("equal")
        a1.set_facecolor("black")

        array = []

        for i in range(K):
            try:
                img = a1.imshow(roll[i], interpolation='nearest', cmap=cmaps[i], aspect='auto')
                array.append(img.get_array())
            except IndexError:
                pass
        return array

    def draw_roll(self):


        roll = self.get_roll()

        # build and set fig obj
        plt.ioff()
        fig = plt.figure(figsize=(4, 3))
        a1 = fig.add_subplot(111)
        a1.axis("equal")
        a1.set_facecolor("black")

        # change unit of time axis from tick to second
        tick = self.get_total_ticks()
        second = mido.tick2second(tick, self.ticks_per_beat, self.get_tempo())
        # print(second)
        if second > 10:
            x_label_period_sec = second // 10
        else:
            x_label_period_sec = second / 10  # ms
        # print(x_label_period_sec)
        x_label_interval = mido.second2tick(x_label_period_sec, self.ticks_per_beat, self.get_tempo()) / self.sr
        # print(x_label_interval)
        plt.xticks([int(x * x_label_interval) for x in range(20)], [round(x * x_label_period_sec, 2) for x in range(20)])

        # change scale and label of y axis
        plt.yticks([y*16 for y in range(8)], [y*16 for y in range(8)])

        # build colors
        channel_nb = 16
        transparent = colorConverter.to_rgba('black')
        colors = [mpl.colors.to_rgba(mpl.colors.hsv_to_rgb((i / channel_nb, 1, 1)), alpha=1) for i in range(channel_nb)]
        cmaps = [mpl.colors.LinearSegmentedColormap.from_list('my_cmap', [transparent, colors[i]], 128) for i in
                 range(channel_nb)]

        # build color maps
        for i in range(channel_nb):
            cmaps[i]._init()
            # create your alpha array and fill the colormap with them.
            alphas = np.linspace(0, 1, cmaps[i].N + 3)
            # create the _lut array, with rgba values
            cmaps[i]._lut[:, -1] = alphas


        # draw piano roll and stack image on a1
        for i in range(channel_nb):
            try:
                a1.imshow(roll[i], origin="lower", interpolation='nearest', cmap=cmaps[i], aspect='auto')
            except IndexError:
                pass

        # draw color bar

        colors = [mpl.colors.hsv_to_rgb((i / channel_nb, 1, 1)) for i in range(channel_nb)]
        cmap = mpl.colors.LinearSegmentedColormap.from_list('my_cmap', colors, 16)
        a2 = fig.add_axes([0.05, 0.80, 0.9, 0.15])
        cbar = mpl.colorbar.ColorbarBase(a2, cmap=cmap,
                                        orientation='horizontal',
                                        ticks=list(range(16)))

        # show piano roll
        plt.draw()
        plt.ion()
        plt.show(block=True)

    def get_tempo(self):
        try:
            return self.meta["set_tempo"]["tempo"]
        except:
            return 500000

    def get_total_ticks(self):
        max_ticks = 0
        for channel in range(16):
            ticks = sum(msg.time for msg in self.events[channel])
            if ticks > max_ticks:
                max_ticks = ticks
        return max_ticks
    
    def play_music(self):
        self.clock = pygame.time.Clock()
        pygame.mixer.music.load(self.music_file)
        print("Music file %s loaded!" % self.music_file)
        
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            # check if playback has finished
            self.clock.tick(30)

    def play(self):
        freq = 44100    # audio CD quality
        bitsize = -16   # unsigned 16 bit
        channels = 2    # 1 is mono, 2 is stereo
        buffer = 1024    # number of samples
        pygame.mixer.init(freq, bitsize, channels, buffer)
        # optional volume 0 to 1.0
        pygame.mixer.music.set_volume(0.8)
        try:
            # use the midi file you just saved
            self.play_music()
        except (KeyboardInterrupt, SystemExit):
            # if user hits Ctrl/C then exit
            # (works only in console mode)
            pygame.mixer.music.fadeout(1000)
            pygame.mixer.music.stop()
            raise SystemExit
        except:
            print('what')
        
    # TODO: return simplified version(one voice) of many voiced song
    def simplify(self):
        pass
    
    def get_scale(self):
        tonic_mid = self.get_tonic()
        tonic_mid = tonic_mid%12

        scale = ['0' for i in range(12)]
        for msg in self.events[0]:
            if msg.type == 'note_on':
                scale[msg.note%12] = '1'
        scale = scale[tonic_mid:]+scale[:tonic_mid]
        points = []
        for scl in scales.values():
            point = 0
            for i in range(12):
                if scl[i] == scale[i]:
                    point+=1
            points.append((scl, point))
        points = sorted(points, key = lambda val: val[1], reverse=True)
        scale = points[0][0]
        # print(tonic_mid, scale)
        # print(name_notes[tonic_mid%12])
        scale_name = ''
        for key, value in scales.items():
            if scale == value:
                scale_name = key
                break
        # print(scale_name)
        
        return ''.join([name_notes[tonic_mid%12], ' ', scale_name])

    def get_scale2(self):
        scales = {'minor': '101101011010',
                  'major': '101011010101'}
        
        field = ['0' for i in range(128)]
        points = {name : [0 for i in range(128)] for name in scales.keys()}
        for msg in self.events[0]:
            if msg.type == 'note_on':
                field[msg.note] = '1'
        
        max_score = 0
        max_sc, max_tonic = '', ''
        for sc, mask in scales.items():
            for i in range(len(field)-len(mask)):
                score = 0
                for j in range(len(mask)):
                    if field[i+j] == scales[sc][j]:
                        score += 1
                points[sc][i] = score
                if max_score < score:
                    max_score = score
                    max_sc = sc
                    max_tonic = i%12
        return scales[max_sc][12-max_tonic:]+scales[max_sc][0:12-max_tonic]


   #create array from midi messages
    def as_array(self):
        in_one_deli = self.get_in_one_deli() 
        nodes = self.available_notes()
        nodes.sort()
        ar = np.empty([1, round((1000000/self.get_tempo())*self.length)*in_one_deli], dtype=int)


        for i in range(ar.shape[1]):
            ar[0][i] = -1

        for inx, channel in enumerate(self.get_events()):
            timer = 0
            last_note = -1
            for msg in channel:
                if msg.type == 'note_on':
                    if msg.time != 0:
                        base = round(timer/in_one_deli)
                        for i in range(round(msg.time/in_one_deli)):
                            ar[0][i+base] = 0
                        timer += msg.time
                    last_note = nodes.index(msg.note)
                    
                elif msg.type == 'note_off':
                    base = round(timer/in_one_deli)
                    for i in range(round(msg.time/in_one_deli)):
                        ar[0][i+base] = len(nodes)+1
                    ar[0][base] = last_note+1
                    timer += msg.time
        stop_deli = ar.shape[1]
        for i in range(stop_deli):
            if ar[0][i] == -1:
                stop_deli = i
                break
        print(ar)
        ar = ar[0][:stop_deli]
        return ar

    #create midi messages from array
    def read_from_array(self, ar, avail):
        track = MidiTrack()
        self.tracks.append(track)
        timestamp = 60
        last_note = -1
        time = 0
        pause_time=0

        #just system infrmation
        control = [10, 7, 101, 100, 6, 10, 7, 101, 100, 6, 10, 7]
        value = [64, 100, 0, 0, 12, 64, 100, 0, 0, 12, 64, 100]
        for i in range(len(control)):
            track.append(Message('control_change', channel = 0, control=control[i], value=value[i], time=0))
        for i in range(len(ar)):
            # print(type(ar[i]), 'type ar[i]')
            # assert(isinstance(ar[i], int))
            if ar[i] != len(avail) + 1 and ar[i] != 0:
                if last_note != -1:
                    track.append(Message('note_off', note=last_note, velocity=100, time=time))
                # print(ar[i]-1, i, avail)
                last_note = avail[ar[i]-1]
                track.append(Message('note_on', note=last_note, velocity=100, time=pause_time))
                pause_time=0
                time=timestamp
            elif ar[i] == 0:
                pause_time += timestamp
            elif ar[i] == len(avail) + 1:
                time += timestamp
        if pause_time==0:
            track.append(Message('note_off', note=last_note, velocity=100, time=time))

        #just system information
        control=[101, 100, 6, 10, 7, 101, 100, 6, 10, 7, 101, 100, 6, 10, 7]
        value = [0, 0, 12, 64, 100, 0, 0, 12, 64, 100, 0, 0, 12, 64, 100]
        time = [192, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(len(control)):
            track.append(Message('control_change', channel = 0, control=control[i], value=value[i], time=time[i]))
        
        
        self.refresh()