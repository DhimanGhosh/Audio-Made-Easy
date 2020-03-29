import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config

class MainLayout(Widget):
    spinner_vals = ['Major Scale', 'Major Chord', 'Notes in Major Scale', 'Note in Major Scales', 'Note shift with capo position (Guitar)', 'Scale shift with capo position (Guitar)', 'Minor Scale', 'Minor Chord', 'Notes in Minor Scale', 'Relative Minor/Major', 'Play Tone Based on Note', 'Play Tone in Sequence (Scale / Note Sequence)', 'Scale from Chords']
    notesS = ['A','A#','B','C','C#','D','D#','E','F','F#','G','G#']
    notesb = ['A','Bb','Cb','C','Db','D','Eb','Fb','F','Gb','G','Ab']

class MusicTheoryGuideApp(App):
    def build(self):
        return MainLayout()

kv = Builder.load_file('design.kv')
Window.size = (700, 400)
Config.set('graphics', 'resizable', False)

if __name__ == "__main__":
    MusicTheoryGuideApp().run()