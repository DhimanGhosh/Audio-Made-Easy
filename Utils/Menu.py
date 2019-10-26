from .Music import Music
# Logic for each choice of menu

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
            8. Notes in Minor Scale
            9. Best Capo position for easy play (Feature coming soon)
            10. Quit
        ''')

    def major_scale(self, wob):
        wob.set_wrong_flag(False)
        note = input("Note: ")
        music = Music(note)
        if music.valid_note(note):
            if music != None:
                result = music.major_scale()
                print("Notes for {} Major Scale: ".format(note) + ' '.join(result))
            else:
                self.Study_Music_Theory()
        else:
            self.Study_Music()

    def major_chord(self, wob):
        wob.set_wrong_flag(False)
        note = input("Note: ")
        music = Music(note)
        if music.valid_note(note):
            if music != None:
                result = music.major_chord()
                print("Major Chord Progression for {} Major Scale: ".format(note) + ' '.join(result))
            else:
                self.Study_Music_Theory()
        else:
            self.Study_Music()

    def notes_in_major_scale(self, wob):
        wob.set_wrong_flag(False)
        note = input("Note: ")
        music = Music(note)
        if music.valid_note(note):
            if music != None:
                result = music.notes_in_major_scale()
                print("Notes in {} Major Scale: ".format(note) + ' '.join(result))
            else:
                self.Study_Music_Theory()
        else:
            self.Study_Music()

    def note_in_major_scales(self, wob):
        wob.set_wrong_flag(False)
        note = input("Note: ")
        music = Music(note)
        if music.valid_note(note):
            if music != None:
                result = music.note_in_major_scales()
                print("{} Major Note is present in Scales: ".format(note) + ' '.join(result))
            else:
                self.Study_Music_Theory()
        else:
            self.Study_Music()

    def note_shift_with_capo_position(self, wob):
        wob.set_wrong_flag(False)
        note = input("Note: ")
        music = Music(note)
        if music.valid_note(note):
            if music != None:
                capo_position = int(input('Capo on Fret Number: '))
                result = music.capo_pos_note_shift(capo_position)
                print("Result Note for {} with Capo at {}: ".format(note, capo_position) + result)
            else:
                self.Study_Music_Theory()
        else:
            self.Study_Music()

    def scale_shift_with_capo_position(self, wob):
        wob.set_wrong_flag(False)
        note = input("Original Scale: ")
        music = Music(note)
        if music.valid_note(note):
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
        note = input("Note: ")
        music = Music(note)
        if music.valid_note(note):
            if music != None:
                result = music.minor_scale()
                print("Notes for {} Minor Scale: ".format(note) + ' '.join(result))
            else:
                self.Study_Music_Theory()
        else:
            self.Study_Music()

    def notes_in_minor_scale(self, wob):
        wob.set_wrong_flag(False)
        note = input("Note: ")
        music = Music(note)
        if music.valid_note(note):
            if music != None:
                result = music.notes_in_minor_scale()
                print("Notes in {} Minor Scale: ".format(note) + ' '.join(result))
            else:
                self.Study_Music_Theory()
        else:
            self.Study_Music()
    
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
        print('I am not here to teach you MUSIC but Guide!')
        exit()