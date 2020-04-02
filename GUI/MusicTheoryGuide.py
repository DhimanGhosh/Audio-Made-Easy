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
    major_minor_options = ('Major', 'Minor')
    guitar_frets_options = tuple([str(i) for i in range(1, 23)]) # For Capo position entry
    sub_menu_selected = dict() # To Keep track of options selected
    output_text = 'See Automated Result\n\n\nPress to Reset App'
    option_change_detect = ''
    input_change_detect = ''

    def change_val_with_notation(self): # Notation Handle ### Incomplete
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
        
        if self.output.text != self.output_text:
            self.show_result()
        elif self.output.text == self.output_text and self.option_menu.text == self.options_spinner_vals[10]:
            self.show_result()

    def update_input_spinner_vals(self, selected_text): # Spinner Handle
        # ----- Detect change in option ----- #
        if selected_text == self.option_menu.text and self.option_change_detect != selected_text:
            self.ids.input_menu.text = 'Select'
            self.ids.output.text = self.output_text
            self.option_change_detect = selected_text
        elif selected_text == self.input_menu.text and self.input_change_detect != selected_text:
            self.ids.input_menu.text = selected_text
            self.ids.output.text = self.output_text
            self.input_change_detect = selected_text

        # ----- Change Input Spinner Values ----- #
        ## ---- Relative Major/Minor ---- ##
        #BUG #2 Sub-Menu for Relative Major/Minor not showing
        if selected_text == self.options_spinner_vals[7]:
            self.ids.input_menu.text = 'Select'
            self.input_spinner_vals = self.rel_maj_min_options
        elif selected_text in self.rel_maj_min_options: ##  ************ NOT - WORKING ************
            self.ids.input_menu.text = selected_text + ' >> Select Scale'
            if selected_text == self.rel_maj_min_options[0]:
                self.input_spinner_vals = tuple([ele + 'm' for ele in self.notes])
            else:
                self.input_spinner_vals = tuple(self.notes)
        ## ---- Relative Major/Minor ---- ##
        
        ## ---- Scale shift with capo position (Guitar) ---- ##
        if selected_text == self.options_spinner_vals[3]: # Select M/m
            self.ids.input_menu.text = 'Select Major/Minor'
            self.input_spinner_vals = self.major_minor_options
        elif selected_text in self.major_minor_options: # Select Capo Position
            self.ids.input_menu.text = selected_text + ' >> Select Capo Position'
            self.input_spinner_vals = self.guitar_frets_options
        elif selected_text in self.guitar_frets_options: # Select Scale
            self.ids.input_menu.text = selected_text + ' >> Select Scale'
            if self.major_minor_options[1] in self.sub_menu_selected[self.ids.option_menu.text]:
                self.input_spinner_vals = tuple([ele + 'm' for ele in self.notes])
            else:
                self.input_spinner_vals = tuple(self.notes)
        ## ---- Scale shift with capo position (Guitar) ---- ##
        
        ## ---- Chords in Minor Scale ---- ##
        if selected_text == self.options_spinner_vals[6]:
            self.input_spinner_vals = tuple([ele + 'm' for ele in self.notes])
        ## ---- Chords in Minor Scale ---- ##

        else: # For no inner lists
            self.input_spinner_vals = tuple(self.notes)

        # ----- To Keep track of Selections ----- #
        if self.ids.option_menu.text in self.sub_menu_selected:
            self.sub_menu_selected[self.ids.option_menu.text].append(selected_text)
        else:
            self.sub_menu_selected[self.ids.option_menu.text] = [selected_text]
        
        self.ids.input_menu.values = self.input_spinner_vals

        ## Auto-Show Output in Output-Area on selecting Both Option_Menu and Input_Menu
        if self.ids.option_menu.text != 'Select':
            if self.ids.input_menu.text in self.notes or self.ids.input_menu.text in [i+'m' for i in self.notes]:
            	self.show_result()

    def show_result(self): # Result Handle
        if self.option_menu.text != "Select" and self.input_menu.text != "Select":
            if self.option_menu.text == self.options_spinner_vals[0]: # "Major Scale"
                note = self.input_menu.text
                music = Music(note)
                result = music.major_scale()
                output_text = '     '.join(result) + '\n\n\n' + self.output_text.split('\n')[-1]
            
            elif self.option_menu.text == self.options_spinner_vals[1]: # "Major Chord"
                note = self.input_menu.text
                music = Music(note)
                result = music.major_chord()
                output_text = '     '.join(result) + '\n\n\n' + self.output_text.split('\n')[-1]
            
            elif self.option_menu.text == self.options_spinner_vals[2]: # "Chords in Major Scale"
                note = self.input_menu.text
                music = Music(note)
                result = music.chords_in_major_scale()
                output_text = '     '.join(result) + '\n\n\n' + self.output_text.split('\n')[-1]
            
            elif self.option_menu.text == self.options_spinner_vals[3]: # "Scale shift with capo position (Guitar)"
                ## Implement Code from 'update_input_spinner_vals()'
                pass
            
            elif self.option_menu.text == self.options_spinner_vals[4]: # "Minor Scale"
                note = self.input_menu.text
                music = Music(note)
                result = music.minor_scale()
                output_text = '     '.join(result) + '\n\n\n' + self.output_text.split('\n')[-1]
            
            elif self.option_menu.text == self.options_spinner_vals[5]: # "Minor Chord"
                note = self.input_menu.text
                music = Music(note)
                result = music.minor_chord()
                output_text = '     '.join(result) + '\n\n\n' + self.output_text.split('\n')[-1]
            
            elif self.option_menu.text == self.options_spinner_vals[6]: # "Chords in Minor Scale"
                note = self.input_menu.text
                music = Music(note[:-1])
                result = music.chords_in_minor_scale()
                output_text = '     '.join(result) + '\n\n\n' + self.output_text.split('\n')[-1]
            
            elif self.option_menu.text == self.options_spinner_vals[7]: # "Relative Major/Minor"
                #BUG #1 Clicking on Output Button make the inner-input menu (self.notes) disable; have to re-select inner-input
                print(self.sub_menu_selected)
                rem_lst = ('Select', self.options_spinner_vals[7])
                sub_val = self.sub_menu_selected[self.options_spinner_vals[7]]
                new_val = [i for i in sub_val if i not in rem_lst]
                self.sub_menu_selected[self.options_spinner_vals[7]] = new_val
                if self.sub_menu_selected[self.options_spinner_vals[7]][-2] == self.rel_maj_min_options[0] and self.sub_menu_selected[self.options_spinner_vals[7]][-1] is not None:
                    scale = self.sub_menu_selected[self.options_spinner_vals[7]][-1]
                    music = Music()
                    result = music.relative_major(scale[:-1])
                    output_text = result + '\n\n\n' + self.output_text.split('\n')[-1]
                elif self.sub_menu_selected[self.options_spinner_vals[7]][-2] == self.rel_maj_min_options[1] and self.sub_menu_selected[self.options_spinner_vals[7]][-1] is not None:
                    scale = self.sub_menu_selected[self.options_spinner_vals[7]][-1]
                    music = Music()
                    result = music.relative_minor(scale)
                    output_text = result + '\n\n\n' + self.output_text.split('\n')[-1]
                self.ids.input_menu.values = self.rel_maj_min_options
                #self.sub_menu_selected[self.options_spinner_vals[7]] = list(set(new_val))
            
            elif self.option_menu.text == self.options_spinner_vals[8]: # "Scale from Chords"
                pass
            
            elif self.option_menu.text == self.options_spinner_vals[9]: # "Play Tone Based on Note"
                self.output.text = "Playing..."
                note = self.input_menu.text
                music = Music(note)
                music.note_beep(note)
                self.output.text = self.output_text
                output_text = self.output_text + '\n\n\n' + self.output_text.split('\n')[-1]
            
            elif self.option_menu.text == self.options_spinner_vals[10]: # "Play Tone in Sequence (Scale / Note Sequence)"
                self.output.text = "Playing..."
                scale = self.input_menu.text
                music = Music(scale)
                if self.nS.active:
                    music.note_beep_scale('M', scale)
                elif self.nb.active:
                    music.note_beep_scale('m', scale)
                output_text = self.output_text + '\n\n\n' + self.output_text.split('\n')[-1]
                pass # Incomplete

            self.output.text = output_text

    def reset(self, btn_status): # Reset Application
        self.ids.nS.active = True
        self.ids.option_menu.text = self.ids.input_menu.text = 'Select'
        self.ids.input_menu.values = tuple()
        self.ids.output.text = self.output_text

class MusicTheoryGuideApp(App):
    def build(self):
        return MainLayout()

if __name__ == "__main__":
    kv = Builder.load_file('design.kv')
    Window.size = (700, 400)
    Config.set('graphics', 'resizable', False)
    
    MusicTheoryGuideApp().run()
