import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder

class MyLayout(Widget):
    spinner_vals = ['Major Scale', 'Major Chord', 'Notes in Major Scale', 'Note in Major Scales', 'Note shift with capo position (Guitar)', 'Scale shift with capo position (Guitar)', 'Minor Scale', 'Minor Chord', 'Notes in Minor Scale', 'Relative Minor/Major', 'Play Tone Based on Note', 'Play Tone in Sequence (Scale / Note Sequence)', 'Scale from Chords']
    notesS = ['A','A#','B','C','C#','D','D#','E','F','F#','G','G#']
    notesb = ['A','Bb','Cb','C','Db','D','Eb','Fb','F','Gb','G','Ab']

    '''option_menu = ObjectProperty(None)
    input_menu = ObjectProperty(None)

    print("Option Menu Displayed Text: " + option_menu.text)
    print("Input Menu Displayed Text: " + input_menu.text)'''

class MyApp(App):
    def build(self):
        return MyLayout()

kv = Builder.load_file('design.kv')

if __name__ == "__main__":
    MyApp().run()