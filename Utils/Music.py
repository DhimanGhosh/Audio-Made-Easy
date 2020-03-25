from . import Note_Tone as tone
from winsound import Beep
from time import sleep

class Music:
    def __init__(self, note='C'):
        self.__notesS = ['A','A#','B','C','C#','D','D#','E','F','F#','G','G#']
        self.__notesb = ['A','Bb','Cb','C','Db','D','Eb','Fb','F','Gb','G','Ab']
        self.__open_pos_chords = ['0_A','0_Am','0_B','0_Bm','0_C','0_D','0_Dm','0_E','0_Em','0_F','0_Fm','0_G']

        if len(note) == 3 and note[-2:] == '#b' or note[-2:] == 'b#':
            self.__note = note[0]
        else:
            self.__note = note
        self.__tone = 2
        self.__semi_tone = 1
        self.__major = ''
        self.__minor = 'm'
        self.__diminished = 'dim'
        self.__maj_scale_formula = [self.__tone,self.__tone,self.__semi_tone,self.__tone,self.__tone,self.__tone,self.__semi_tone]
        self.__chord_prog_in_maj_scale_formula = [self.__major,self.__minor,self.__minor,self.__major,self.__major,self.__minor,self.__diminished]
        self.__min_scale_formula = [self.__tone,self.__semi_tone,self.__tone,self.__tone,self.__semi_tone,self.__tone,self.__tone]
        self.__chord_prog_in_min_scale_formula = [self.__minor,self.__minor,self.__major,self.__major+'/'+self.__minor,self.__major+'/'+self.__minor,self.__major,self.__major]
        
        self.__octave4 = tone.notes(4)
        self.__octave5 = tone.notes(5)

        self.__octaves = self.__octave4 + self.__octave5

        # Notes Frequency, Octave 0
        self.__C4  = self.__octave4[0]
        self.__Cs4 = self.__octave4[1]
        self.__D4  = self.__octave4[2]
        self.__Ds4 = self.__octave4[3]
        self.__E4  = self.__octave4[4]
        self.__F4  = self.__octave4[5]
        self.__Fs4 = self.__octave4[6]
        self.__G4  = self.__octave4[7]
        self.__Gs4 = self.__octave4[8]
        self.__A4  = self.__octave4[9]
        self.__As4 = self.__octave4[10]
        self.__B4  = self.__octave4[11]

    def __note_position_in_list(self, note):
        valid_list = self.__valid_list(note)
        for i in range(len(valid_list)):
            if valid_list[i] == note:
                return i
    
    def valid_note(self, note):
        if len(note) == 3 and note[-2:] == '#b' or note[-2:] == 'b#':
            note = note[0]
        if note in self.__notesS:
            return ('S', True)
        if note in self.__notesb:
            return ('b', True)
        if '0_' + note in self.__open_pos_chords:
            return ('0', False)
        return ('', False)
    
    def __valid_list(self, note):
        is_valid_note = self.valid_note(note)
        music_list_to_look = is_valid_note[0]
        if music_list_to_look == 'S':
            return self.__notesS
        elif music_list_to_look == 'b':
            return self.__notesb
        elif music_list_to_look == '0':
            return self.__open_pos_chords

    def major_scale(self):
        valid_list = self.__valid_list(self.__note)
        position = self.__note_position_in_list(self.__note)
        
        notes_in_scale = [valid_list[position]]

        for i in range(6):
            position = position + self.__maj_scale_formula[i]
            if position >= len(valid_list):
                position = position % len(valid_list)
            notes_in_scale.append(valid_list[position])

        return notes_in_scale

    def __major_scale(self, note):
        valid_list = self.__valid_list(note)
        position = self.__note_position_in_list(note)

        notes_in_scale = [valid_list[position]]
        
        for i in range(6):
            position = position + self.__maj_scale_formula[i]
            if position >= len(valid_list):
                position = position % len(valid_list)
            notes_in_scale.append(valid_list[position])

        return notes_in_scale

    def major_chord(self):
        scale = self.major_scale()
        return [scale[0], scale[2], scale[4]]

    def minor_chord(self):
        scale = self.minor_scale()
        return [scale[0], scale[2], scale[4]]

    def notes_in_major_scale(self):
        notes = self.major_scale()
        for i in range(len(notes)):
            notes[i] = notes[i] + self.__chord_prog_in_maj_scale_formula[i]
        return notes

    def __notes_in_major_scale(self, scale):
        notes = self.__major_scale(scale)
        for i in range(len(notes)):
            notes[i] = notes[i] + self.__chord_prog_in_maj_scale_formula[i]
        return notes

    def note_in_major_scales(self):
        valid_list = self.__valid_list(self.__note)
        notes_scales = []
        scales = []
        for i in range(len(valid_list)):
            notes_scales.append(self.__major_scale(valid_list[i]))
        
        for i in range(len(notes_scales)):
            for j in range(len(notes_scales[0])):
                if self.__note == notes_scales[i][j]:
                    scales.append(notes_scales[i][0])
        return scales

    def capo_pos_note_shift(self, capo_pos = 0):
        valid_list = self.__valid_list(self.__note)
        position = 0
        for i in range(len(valid_list)):
            if valid_list[i] == self.__note:
                position = i

        new_note = valid_list[position - capo_pos]
        return new_note

    def capo_pos_scale_shift(self, capo_pos = 0):
        new_note = self.capo_pos_note_shift(capo_pos)
        new_scale = self.__notes_in_major_scale(new_note)
        return new_scale

    def minor_scale(self):
        valid_list = self.__valid_list(self.__note)
        position = self.__note_position_in_list(self.__note)

        notes_in_scale = [valid_list[position]]
        
        for i in range(6):
            position = position + self.__min_scale_formula[i]
            if position >= len(valid_list):
                position = position % len(valid_list)
            notes_in_scale.append(valid_list[position])

        return notes_in_scale

    def __minor_scale(self, note):
        valid_list = self.__valid_list(note)
        position = self.__note_position_in_list(note)

        notes_in_scale = [valid_list[position]]
        
        for i in range(6):
            position = position + self.__min_scale_formula[i]
            if position >= len(valid_list):
                position = position % len(valid_list)
            notes_in_scale.append(valid_list[position])

        return notes_in_scale

    def notes_in_minor_scale(self):
        notes = self.minor_scale()
        for i in range(len(notes)):
            if '/' in self.__chord_prog_in_min_scale_formula[i]:
                join_formula = '/' + notes[i]
                notes[i] = notes[i] + self.__chord_prog_in_min_scale_formula[i]
                parts = notes[i].split('/')
                notes[i] = join_formula.join(parts)+' '
            else:
                notes[i] = notes[i] + self.__chord_prog_in_min_scale_formula[i]
        return notes

    def __notes_in_minor_scale(self, scale):
        notes = self.__minor_scale(scale)
        for i in range(len(notes)):
            if '/' in self.__chord_prog_in_min_scale_formula[i]:
                join_formula = '/' + notes[i]
                notes[i] = notes[i] + self.__chord_prog_in_min_scale_formula[i]
                parts = notes[i].split('/')
                notes[i] = join_formula.join(parts)+' '
            else:
                notes[i] = notes[i] + self.__chord_prog_in_min_scale_formula[i]
        return notes

    def relative_minor(self, major_scale):
        return self.__valid_list(major_scale)[self.__note_position_in_list(major_scale) - 3] + 'm'

    def relative_major(self, minor_scale):
        return self.__valid_list(minor_scale)[self.__note_position_in_list(minor_scale) + 3]

    def best_capo_position(self, chords):
        for chord in chords:
            pass
    
    def __note_freq_detection(self, note):
        if note == 'C':
            return self.__C4
        elif note == 'C#':
            return self.__Cs4
        elif note == 'D':
            return self.__D4
        elif note == 'D#':
            return self.__Ds4
        elif note == 'E':
            return self.__E4
        elif note == 'F':
            return self.__F4
        elif note == 'F#':
            return self.__Fs4
        elif note == 'G':
            return self.__G4
        elif note == 'G#':
            return self.__Gs4
        elif note == 'A':
            return self.__A4
        elif note == 'A#':
            return self.__As4
        elif note == 'B':
            return self.__B4
    
    def note_beep(self, note):
        Beep(self.__note_freq_detection(note), 300)
    
    def note_beep_seq(self, notes):
        # Play notes from same octave
        for note in notes:
            Beep(self.__note_freq_detection(note), 300)
            sleep(0.5)

    def note_beep_scale(self, scale_mode, scale):
        # Play notes using 2 octaves
        if scale_mode == 'm':
            notes = self.__minor_scale(scale)
            note_octave_pos = self.__octaves.index(self.__note_freq_detection(notes[0]))
            scale_freq_range = self.__octaves[note_octave_pos : note_octave_pos + 13]

            position = 0
            scale_freq = [scale_freq_range[position]]
        
            for i in range(6):
                position = position + self.__min_scale_formula[i]
                scale_freq.append(scale_freq_range[position])

        else:
            notes = self.__major_scale(scale)
            note_octave_pos = self.__octaves.index(self.__note_freq_detection(notes[0]))
            scale_freq_range = self.__octaves[note_octave_pos : note_octave_pos + 13]

            position = 0
            scale_freq = [scale_freq_range[position]]
        
            for i in range(6):
                position = position + self.__maj_scale_formula[i]
                scale_freq.append(scale_freq_range[position])
        
        scale_freq.append(scale_freq_range[position + 1]) # Adding 8th Note from Next Octave for that Scale
        
        for freq in scale_freq:
            Beep(freq, 300)
            sleep(0.5)
    
    def __chord_in_scales(self, chord):
        # Major and Minor Scales containing Chords
        if 'm' in chord and 'dim' not in chord:
            note = chord[:-1]
        else:
            note = chord
        
        valid_list = self.__valid_list(note)
        
        # Major Scales with this chord
        notes_scales = dict()
        major_scales_with_chord = []
        for i in range(len(valid_list)):
            notes_scales[valid_list[i]] = self.__notes_in_major_scale(valid_list[i])

        for k,v in notes_scales.items():
            if chord in v:
                major_scales_with_chord.append(k)
        
        # Minor Scales with this chord
        notes_scales = dict()
        minor_scales_with_chord = []
        for i in range(len(valid_list)):
            min_scale1 = min_scale = self.__notes_in_minor_scale(valid_list[i])
            for scale in min_scale:
                if '/' in scale:
                    min_scale1.remove(scale)
                    min_scale1.extend(scale.split('/'))
            notes_scales[valid_list[i] + 'm'] = min_scale1
        
        for k,v in notes_scales.items():
            if chord in v:
                minor_scales_with_chord.append(k)
        
        scales = major_scales_with_chord + minor_scales_with_chord
        return scales
    
    def common_scale(self, chords):
        scales_from_chords = []
        for chord in chords:
            scales_from_chords.append(self.__chord_in_scales(chord))
        list_of_sets = []
        for scale in scales_from_chords:
            list_of_sets.append(set(scale))
        result = list_of_sets[0]
        if len(list_of_sets) > 2:
            for i in range(1, len(list_of_sets)):
                result = result.intersection(list_of_sets[i])
        result = list(result)
        if len(result) == 2:
            minor_note_in_result = [item for item in result if 'm' in item][0]
            minor_note_index = result.index(minor_note_in_result)
            major_note_index = minor_note_index - 1
            if self.relative_minor(result[major_note_index]) == result[minor_note_index] and self.relative_major(result[minor_note_index][:-1]) == result[major_note_index]:
                return (result, 'R')
            else:
                return (result, 'NR')
        else:
            return (result, '')
