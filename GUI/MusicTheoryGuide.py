#!/usr/bin/env python3

'''
    from a.b import c as d
    Same as:
        "import d a.b.c"
    in .kv file
'''
import kivy, os, sys
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config

root_dir = os.path.realpath('..')
sys.path.insert(0, root_dir)

from Utils.Music import Music

class MainLayout(Widget):
    spinner_vals = tuple()
    with open('Features.txt', 'r') as f:
        spinner_vals = tuple(f.readlines())
    music = Music()
    notesS = music.notesS
    notesb = music.notesb
    notes = notesS
    nS = ObjectProperty(None)
    nb = ObjectProperty(None)
    option_menu = ObjectProperty(None)
    input_menu = ObjectProperty(None)
    output = ObjectProperty(None)

    def show_result(self):
        if self.option_menu.text != "Select" and self.input_menu.text != "Select":
            if self.option_menu.text == self.spinner_vals[0]: # "Major Scale"
                note = self.input_menu.text
                music = Music(note)
                result = music.major_scale()
                self.output.text = '     '.join(result)
            
            elif self.option_menu.text == self.spinner_vals[1]: # "Major Chord"
                note = self.input_menu.text
                music = Music(note)
                result = music.major_chord()
                self.output.text = '     '.join(result)
            
            elif self.option_menu.text == self.spinner_vals[2]: # "Notes in Major Scale"
                note = self.input_menu.text
                music = Music(note)
                result = music.notes_in_major_scale()
                self.output.text = '     '.join(result)
            
            elif self.option_menu.text == self.spinner_vals[3]: # "Scale shift with capo position (Guitar)"
                pass
            
            elif self.option_menu.text == self.spinner_vals[4]: # "Minor Scale"
                note = self.input_menu.text
                music = Music(note)
                result = music.minor_scale()
                self.output.text = '     '.join(result)
            
            elif self.option_menu.text == self.spinner_vals[5]: # "Minor Chord"
                note = self.input_menu.text
                music = Music(note)
                result = music.minor_chord()
                self.output.text = '     '.join(result)
            
            elif self.option_menu.text == self.spinner_vals[6]: # "Notes in Minor Scale"
                note = self.input_menu.text
                music = Music(note)
                result = music.notes_in_minor_scale()
                self.output.text = '     '.join(result)
            
            elif self.option_menu.text == self.spinner_vals[7]: # "Relative Minor/Major"
                pass
            
            elif self.option_menu.text == self.spinner_vals[8]: # "Scale from Chords"
                pass
            
            elif self.option_menu.text == self.spinner_vals[9]: # "Play Tone Based on Note"
                self.output.text = "Playing..."
                note = self.input_menu.text
                music = Music(note)
                music.note_beep(note)
                self.output.text = "Click Me"
            
            elif self.option_menu.text == self.spinner_vals[10]: # "Play Tone in Sequence (Scale / Note Sequence)"
                self.output.text = "Playing..."
                scale = self.input_menu.text
                music = Music(scale)
                music.note_beep_scale('M', scale)
                self.output.text = "Click Me"
                pass # Incomplete
                
    def detect_notation(self):
        note_pos = 999
        if self.input_menu.text != "Select":
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
        
        if self.output.text != "Click Me":
            self.show_result()

class MusicTheoryGuideApp(App):
    def build(self):
        return MainLayout()

if __name__ == "__main__":
    kv = Builder.load_file('design.kv')
    Window.size = (700, 400)
    Config.set('graphics', 'resizable', False)
    
    MusicTheoryGuideApp().run()