class Music:
    def __init__(self, note):
        self.__notesS = ['A','A#','B','C','C#','D','D#','E','F','F#','G','G#']
        self.__notesb = ['A','Bb','Cb','C','Db','D','Eb','Fb','F','Gb','G','Ab']
        self.__open_pos_chords = ['A','Am','C','D','Dm','E','Em','G']

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
        return ('0', False)
    
    def __valid_list(self, note):
        is_valid_note = self.valid_note(note)
        music_list_to_look = is_valid_note[0]
        if music_list_to_look == 'S':
            return self.__notesS
        elif music_list_to_look == 'b':
            return self.__notesb
        elif music_list_to_look == '0':
            return None

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
        valid_list = self.__valid_list(self.__note)
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

    def notes_in_major_scale(self):
        scale = self.major_scale()
        for i in range(len(scale)):
            scale[i] = scale[i] + self.__chord_prog_in_maj_scale_formula[i]
        return scale

    def __notes_in_major_scale(self, note):
        scale = self.__major_scale(note)
        for i in range(len(scale)):
            scale[i] = scale[i] + self.__chord_prog_in_maj_scale_formula[i]
        return scale

    def note_in_major_scales(self):
        valid_list = self.__valid_list(self.__note)
        notes_scales = []
        scales = []
        for i in range(len(valid_list)):
            notes_scales.append(self.__major_scale(valid_list[i]))
        
        for i in range(12):
            for j in range(7):
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

    def notes_in_minor_scale(self):
        scale = self.minor_scale()
        for i in range(len(scale)):
            if '/' in self.__chord_prog_in_min_scale_formula[i]:
                join_formula = '/' + scale[i]
                scale[i] = scale[i] + self.__chord_prog_in_min_scale_formula[i]
                parts = scale[i].split('/')
                scale[i] = join_formula.join(parts)+' '
            else:
                scale[i] = scale[i] + self.__chord_prog_in_min_scale_formula[i]
        return scale

    def open_pos_chords(self):
        pass
