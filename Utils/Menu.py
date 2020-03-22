# Logic for each choice of menu
from .Music import Music

class Menu:
    def __init__(self):
        print('''
        ###########################################
        ###    Welcome to Music Theory Guide    ###
        ###########################################

            1. Major Scale
            2. Major Chord
            3. Notes in Major Scale
            4. Note in Major Scales
            5. Note shift with capo position (Guitar)
            6. Scale shift with capo position (Guitar)
            7. Minor Scale
            8. Minor Chord
            9. Notes in Minor Scale
            10. Relative Minor/Major
            11. Play Tone Based on Note
            12. Play Tone in Sequence (Scale / Note Sequence)
            13. Scale from Chords
            14. Best Capo position for easy play (Feature coming soon)
            15. Quit
        ''')

    def major_scale(self, wob):
        wob.set_wrong_flag(False)
        while True:
            note = input("Note: ")
            if note is '':
                continue
            else:
                break
        music = Music(note)
        if music.valid_note(note)[1]:
            if music != None:
                result = music.major_scale()
                print("Notes for {} Major Scale: ".format(note) + ' '.join(result))
            else:
                self.Study_Music_Theory()
        else:
            self.Study_Music()

    def major_chord(self, wob):
        wob.set_wrong_flag(False)
        while True:
            note = input("Note: ")
            if note is '':
                continue
            else:
                break
        music = Music(note)
        if music.valid_note(note)[1]:
            if music != None:
                result = music.major_chord()
                print("Major Chord Progression for {} Major Scale: ".format(note) + ' '.join(result))
            else:
                self.Study_Music_Theory()
        else:
            self.Study_Music()

    def notes_in_major_scale(self, wob):
        wob.set_wrong_flag(False)
        while True:
            note = input("Note: ")
            if note is '':
                continue
            else:
                break
        music = Music(note)
        if music.valid_note(note)[1]:
            if music != None:
                result = music.notes_in_major_scale()
                print("Notes in {} Major Scale: ".format(note) + ' '.join(result))
            else:
                self.Study_Music_Theory()
        else:
            self.Study_Music()

    def note_in_major_scales(self, wob):
        wob.set_wrong_flag(False)
        while True:
            note = input("Note: ")
            if note is '':
                continue
            else:
                break
        music = Music(note)
        if music.valid_note(note)[1]:
            if music != None:
                result = music.note_in_major_scales()
                print("{} Major Note is present in Scales: {}".format(note, ' '.join(result)))
            else:
                self.Study_Music_Theory()
        else:
            self.Study_Music()

    def note_shift_with_capo_position(self, wob):
        wob.set_wrong_flag(False)
        while True:
            note = input("Note: ")
            if note is '':
                continue
            else:
                break
        music = Music(note)
        if music.valid_note(note)[1]:
            if music != None:
                capo_position = int(input('Capo on Fret Number: '))
                result = music.capo_pos_note_shift(capo_position)
                print("Result Note for {} with Capo at {}: {}".format(note, capo_position, result))
            else:
                self.Study_Music_Theory()
        else:
            self.Study_Music()

    def scale_shift_with_capo_position(self, wob):
        wob.set_wrong_flag(False)
        while True:
            note = input("Original Scale: ")
            if note is '':
                continue
            else:
                break
        music = Music(note)
        if music.valid_note(note)[1]:
            if music != None:
                capo_position = int(input('Capo on Fret Number: '))
                new_note = music.capo_pos_note_shift(capo_position)
                result = music.capo_pos_scale_shift(capo_position)
                print("Result Scale for {} with Capo at {}: {}".format(note, capo_position, new_note))
                print("Notes: " + ' '.join(result))
            else:
                self.Study_Music_Theory()
        else:
            self.Study_Music()

    def minor_scale(self, wob):
        wob.set_wrong_flag(False)
        while True:
            note = input("Note: ")
            if note is '':
                continue
            else:
                break
        music = Music(note)
        if music.valid_note(note)[1]:
            if music != None:
                result = music.minor_scale()
                print("Notes for {} Minor Scale: ".format(note) + ' '.join(result))
            else:
                self.Study_Music_Theory()
        else:
            self.Study_Music()

    def minor_chord(self, wob):
        wob.set_wrong_flag(False)
        while True:
            note = input("Note: ")
            if note is '':
                continue
            else:
                break
        music = Music(note)
        if music.valid_note(note)[1]:
            if music != None:
                result = music.minor_chord()
                print("Major Chord Progression for {} Major Scale: ".format(note) + ' '.join(result))
            else:
                self.Study_Music_Theory()
        else:
            self.Study_Music()

    def notes_in_minor_scale(self, wob):
        wob.set_wrong_flag(False)
        while True:
            note = input("Note: ")
            if note is '':
                continue
            else:
                break
        music = Music(note)
        if music.valid_note(note)[1]:
            if music != None:
                result = music.notes_in_minor_scale()
                print("Notes in {} Minor Scale: ".format(note) + ' '.join(result))
            else:
                self.Study_Music_Theory()
        else:
            self.Study_Music()
    
    def relative_minor_major(self, wob):
        wob.set_wrong_flag(False)
        scl = input('1. Relative Major\n2. Relative Minor\nChoice: ')
        if int(scl) == 1:
            while True:
                note = input("Minor Note: ")
                if note is '':
                    continue
                else:
                    break
            music = Music(note)
            if music.valid_note(note)[1]:
                if music != None:
                    result = music.relative_major(note)
                    print("Relative Major of {}m is: {}".format(note, result))
                else:
                    self.Study_Music_Theory()
            else:
                self.Study_Music()
        elif int(scl) == 2:
            while True:
                note = input("Major Note: ")
                if note is '':
                    continue
                else:
                    break
            music = Music(note)
            if music.valid_note(note)[1]:
                if music != None:
                    result = music.relative_minor(note)
                    print("Relative Minor of {} is: {}".format(note, result))
                else:
                    self.Study_Music_Theory()
            else:
                self.Study_Music()
    
    def play_tone(self, wob):
        wob.set_wrong_flag(False)
        while True:
            note = input("Note: ")
            if note is '':
                continue
            else:
                break
        music = Music(note)
        if music.valid_note(note)[1]:
            if music != None:
                music.note_beep(note)
            else:
                self.Study_Music_Theory()
        else:
            self.Study_Music()
    
    def play_tone_in_seq(self, wob):
        wob.set_wrong_flag(False)
        ch = input('1. Play Notes in a Scale\n2. Play Note Sequence\nChoice: ')
        if int(ch) == 1:
            min_maj = input("1. Minor Scale\n2. Major Scale\nChoice: ")
            if int(min_maj) == 1:
                while True:
                    scale = input("Scale: ")
                    if scale is '':
                        continue
                    else:
                        break
                music = Music(scale)
                if music.valid_note(scale)[1]:
                    if music != None:
                        music.note_beep_scale('m', scale)
                    else:
                        self.Study_Music_Theory()
                else:
                    self.Study_Music()
            elif int(min_maj) == 2:
                while True:
                    scale = input("Scale: ")
                    if scale is '':
                        continue
                    else:
                        break
                music = Music(scale)
                if music.valid_note(scale)[1]:
                    if music != None:
                        music.note_beep_scale('M', scale)
                    else:
                        self.Study_Music_Theory()
                else:
                    self.Study_Music()
        elif int(ch) == 2:
            while True:
                notes = input("Notes: ")
                if notes is '':
                    continue
                else:
                    break
            music = Music()
            music.note_beep_seq(notes.split())
    
    def scale_from_chords(self, wob):
        wob.set_wrong_flag(False)
        # Find Scale from chords and use in best_capo_position() for up-shifting or down-shifting
        chords = input('Chords: ')
        music = Music()
        common_scale = music.common_scale(chords.split())
        result = common_scale[0]
        if common_scale[1] is '' or common_scale[1] == 'NR':
            if len(result) > 0:
                print("'{}' Chords are present in '{}' Scale".format(chords, result))
            else:
                print("'{}' Chords does not share common scale... Please Check the chords Once...".format(chords))
        else:
            print("'{}' Chords are present in '{}' Scale or '{}' Scale".format(chords, result[0], result[1]))
    
    def best_capo_position(self, wob):
        wob.set_wrong_flag(False)
        print('Sorry Feature Coming soon...')

    def wrong_entry(self, wob):
        wob.set_wrong_flag(True)
        print('Wrong Entry!\nTry Again...\n')

    def Study_Music_Theory(self):
        print('Go and study basic music theory first!!!')
        exit()
    
    def Study_Music(self):
        print('Invalid Music Notation!\nI am not here to teach you MUSIC but Guide!')
        exit()