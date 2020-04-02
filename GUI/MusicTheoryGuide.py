#!/usr/bin/env python3

'''
    from a.b import c as d
    Same as:
        "import d a.b.c"
    in .kv file
'''
import kivy, os, sys, platform
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.spinner import Spinner
from time import sleep

if platform.system() == 'Linux':
    utils_dir = os.path.realpath('../Utils/')
    sys.path.insert(0, utils_dir)
    from Music import Music
    features = utils_dir + '/Features.txt'
else:
    root_dir = os.path.realpath('..')
    sys.path.insert(0, root_dir)
    from Utils.Music import Music
    features = root_dir + '/Utils/Features.txt'

class MainLayout(Widget):
    options_spinner_vals = tuple()
    with open(features, 'r') as f:
        options_spinner_vals = tuple([x.strip() for x in f.readlines()])
    music = Music()
    notesS = music.notesS
    notesb = music.notesb
    notes = notesS
    input_spinner_vals = tuple()
    nS = ObjectProperty(None)
    nb = ObjectProperty(None)
    option_menu = ObjectProperty(None)
    input_menu = ObjectProperty(None)
    output = ObjectProperty(None)
    rel_maj_min_options = ('Relative Major', 'Relative Minor')
    sub_menu_selected = dict()
    option_change_detect = ''
    input_change_detect = ''

    def update_input_spinner_vals(self, selected_text):
        # Detect change in option
        if selected_text == self.option_menu.text and self.option_change_detect != selected_text:
            self.ids.input_menu.text = 'Select'
            self.ids.output.text = 'Check Result'
            self.option_change_detect = selected_text
        elif selected_text == self.input_menu.text and self.input_change_detect != selected_text:
            self.ids.input_menu.text = selected_text
            self.ids.output.text = 'Check Result'
            self.input_change_detect = selected_text

        if selected_text == self.options_spinner_vals[7]:
            self.ids.input_menu.text = 'Select'
            self.input_spinner_vals = self.rel_maj_min_options
        elif selected_text in self.rel_maj_min_options:
            self.ids.input_menu.text = selected_text + ' >> Select Scale'
            if selected_text == self.rel_maj_min_options[0]:
                self.input_spinner_vals = tuple([ele + 'm' for ele in self.notes])
            else:
                self.input_spinner_vals = tuple(self.notes)
        else:
            self.input_spinner_vals = tuple(self.notes)
        
        # To Keep track of Selections
        if self.ids.option_menu.text in self.sub_menu_selected:
            self.sub_menu_selected[self.ids.option_menu.text].append(selected_text)
        else:
            self.sub_menu_selected[self.ids.option_menu.text] = [selected_text]
        
        self.ids.input_menu.values = self.input_spinner_vals

    def show_result(self):
        if self.option_menu.text != "Select" and self.input_menu.text != "Select":
            if self.option_menu.text == self.options_spinner_vals[0]: # "Major Scale"
                note = self.input_menu.text
                music = Music(note)
                result = music.major_scale()
                self.output.text = '     '.join(result)
            
            elif self.option_menu.text == self.options_spinner_vals[1]: # "Major Chord"
                note = self.input_menu.text
                music = Music(note)
                result = music.major_chord()
                self.output.text = '     '.join(result)
            
            elif self.option_menu.text == self.options_spinner_vals[2]: # "Chords in Major Scale"
                note = self.input_menu.text
                music = Music(note)
                result = music.chords_in_major_scale()
                self.output.text = '     '.join(result)
            
            elif self.option_menu.text == self.options_spinner_vals[3]: # "Scale shift with capo position (Guitar)"
                pass
            
            elif self.option_menu.text == self.options_spinner_vals[4]: # "Minor Scale"
                note = self.input_menu.text
                music = Music(note)
                result = music.minor_scale()
                self.output.text = '     '.join(result)
            
            elif self.option_menu.text == self.options_spinner_vals[5]: # "Minor Chord"
                note = self.input_menu.text
                music = Music(note)
                result = music.minor_chord()
                self.output.text = '     '.join(result)
            
            elif self.option_menu.text == self.options_spinner_vals[6]: # "Chords in Minor Scale"
                note = self.input_menu.text
                music = Music(note)
                result = music.chords_in_minor_scale()
                self.output.text = '     '.join(result)
            
            elif self.option_menu.text == self.options_spinner_vals[7]: # "Relative Major/Minor"
                # Create New Spinner Menu for (Relative Major and Relative Minor Option)
                print(self.sub_menu_selected)
                rem_lst = ('Select', self.options_spinner_vals[7])
                sub_val = self.sub_menu_selected[self.options_spinner_vals[7]]
                new_val = [i for i in sub_val if i not in rem_lst]
                self.sub_menu_selected[self.options_spinner_vals[7]] = new_val
                if self.sub_menu_selected[self.options_spinner_vals[7]][-2] == self.rel_maj_min_options[0] and self.sub_menu_selected[self.options_spinner_vals[7]][-1] is not None:
                    scale = self.sub_menu_selected[self.options_spinner_vals[7]][-1]
                    music = Music()
                    result = music.relative_major(scale[:-1])
                    self.output.text = result
                elif self.sub_menu_selected[self.options_spinner_vals[7]][-2] == self.rel_maj_min_options[1] and self.sub_menu_selected[self.options_spinner_vals[7]][-1] is not None:
                    scale = self.sub_menu_selected[self.options_spinner_vals[7]][-1]
                    music = Music()
                    result = music.relative_minor(scale)
                    self.output.text = result
                self.ids.input_menu.values = self.rel_maj_min_options
                #self.sub_menu_selected[self.options_spinner_vals[7]] = list(set(new_val))
            
            elif self.option_menu.text == self.options_spinner_vals[8]: # "Scale from Chords"
                pass
            
            elif self.option_menu.text == self.options_spinner_vals[9]: # "Play Tone Based on Note"
                self.output.text = "Playing..."
                note = self.input_menu.text
                music = Music(note)
                music.note_beep(note)
                self.output.text = "Check Result"
            
            elif self.option_menu.text == self.options_spinner_vals[10]: # "Play Tone in Sequence (Scale / Note Sequence)"
                self.output.text = "Playing..."
                scale = self.input_menu.text
                music = Music(scale)
                if self.nS.active:
                    music.note_beep_scale('M', scale)
                elif self.nb.active:
                    music.note_beep_scale('m', scale)
                self.output.text = "Check Result"
                pass # Incomplete
                
    def change_val_with_notation(self): # Incomplete
        # Change the function to dynamically change it's value w.r.t option_menu; set its value as 'self.input_spinner_vals'
        note_pos = 999
        if self.option_menu.text != "Select" or self.input_menu.text != "Select":
            if self.option_menu.text == self.options_spinner_vals[7]: # "Relative Major/Minor"
                pass ## <Not Decided>
            else:
                note_pos = self.notes.index(self.input_menu.text)
        
        if self.nS.active:
            self.notes = self.notesS
        elif self.nb.active:
            self.notes = self.notesb
        self.ids.input_menu.values = self.notes
        
        if self.input_menu.text == "Select":
            self.input_menu.text = "Select"
        elif self.input_menu.text in self.notes: # Check if Input Menu has default data or not
            note_pos = self.notes.index(self.input_menu.text)
        
        if note_pos != 999:
            self.input_menu.text = self.notes[note_pos]
        else:
            self.input_menu.text = "Select"
        
        if self.output.text != "Check Result":
            self.show_result()
        elif self.output.text == "Check Result" and self.option_menu.text == self.options_spinner_vals[10]:
            self.show_result()

class MusicTheoryGuideApp(App):
    def build(self):
        return MainLayout()

if __name__ == "__main__":
    kv = Builder.load_file('design.kv')
    Window.size = (700, 400)
    Config.set('graphics', 'resizable', False)
    
    MusicTheoryGuideApp().run()
