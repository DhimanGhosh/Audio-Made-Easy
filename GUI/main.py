import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config
from kivy.base import runTouchApp

class MainLayout(Widget):
    spinner_vals = ['Major Scale', 'Major Chord', 'Notes in Major Scale', 'Note in Major Scales', 'Note shift with capo position (Guitar)', 'Scale shift with capo position (Guitar)', 'Minor Scale', 'Minor Chord', 'Notes in Minor Scale', 'Relative Minor/Major', 'Play Tone Based on Note', 'Play Tone in Sequence (Scale / Note Sequence)', 'Scale from Chords']
    notesS = ['A','A#','B','C','C#','D','D#','E','F','F#','G','G#']
    notesb = ['A','Bb','Cb','C','Db','D','Eb','Fb','F','Gb','G','Ab']
    notes = notesS
    nS = ObjectProperty(None)
    nb = ObjectProperty(None)
    current_active_notation = nS # For change in radio-button; change notations for input_menu
    option_menu = ObjectProperty(None)
    input_menu = ObjectProperty(None)

    def get_input_data(self):
        print(self.option_menu.text)

    def detect_notation(self):
        if self.input_menu.text in self.notes:
            note_pos = self.notes.index(self.input_menu.text)

        if self.nS.active:
            self.notes = self.notesS
            self.current_active_notation = self.nS
            print("Sharp Notation Selected")
        elif self.nb.active:
            self.notes = self.notesb
            self.current_active_notation = self.nb
            print("Flat Notation Selected")
        self.input_menu.text = self.notes[note_pos]
        self.ids.input_menu.values = self.notes

class MusicTheoryGuideApp(App):
    def build(self):
        return MainLayout()

if __name__ == "__main__":
    kv = Builder.load_file('design.kv')
    Window.size = (700, 400)
    Config.set('graphics', 'resizable', False)
    
    MusicTheoryGuideApp().run()