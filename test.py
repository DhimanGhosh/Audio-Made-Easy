from Utils.Music import Music
import unittest

class MusicTest(unittest.TestCase):

    def setUp(self):
        print('\nTesting:', end=' ')
    
    def test_valid_music_notation(self):
        print('Valid Music Notation...')
        note = 'Eb'
        music = Music(note)
        is_valid = music.valid_note(note)[1]
        if is_valid:
            self.assertTrue(is_valid)
            print('Result:\tPASS')
        else:
            self.assertFalse(is_valid)
            print('Result:\tFAIL')
    
    def test_invalid_music_notation(self):
        print('Invalid Music Notation...')
        note = 'T#'
        music = Music(note)
        is_valid = music.valid_note(note)[1]
        if is_valid:
            self.assertTrue(is_valid)
            print('Result:\tFAIL')
        else:
            self.assertFalse(is_valid)
            print('Result:\tPASS')
    
    def test_major_scale(self):
        print('Major Scale...')
        note = 'C'
        music = Music(note)
        scale = music.major_scale()
        result = ' '.join(scale)
        expected_result = 'C D E F G A B'
        if result == expected_result:
            self.assertTrue(result == expected_result)
            print('Result:\tPASS')
        else:
            self.assertFalse(result != expected_result)
            print('Result:\tFAIL')
        
    def test_major_chord(self):
        print('Major Chord...')
        note = 'C'
        music = Music(note)
        chord = music.major_chord()
        result = ' '.join(chord)
        expected_result = 'C E G'
        if result == expected_result:
            self.assertTrue(result == expected_result)
            print('Result:\tPASS')
        else:
            self.assertFalse(result != expected_result)
            print('Result:\tFAIL')

    def test_notes_in_major_scale(self):
        print('Notes in Major Scale...')
        note = 'C'
        music = Music(note)
        notes_in_scale = music.notes_in_major_scale()
        result = ' '.join(notes_in_scale)
        expected_result = 'C Dm Em F G Am Bdim'
        if result == expected_result:
            self.assertTrue(result == expected_result)
            print('Result:\tPASS')
        else:
            self.assertFalse(result != expected_result)
            print('Result:\tFAIL')

    def test_note_in_major_scales(self):
        print('Note in Major Scales...')
        note = 'C'
        music = Music(note)
        notes_in_scale = music.note_in_major_scales()
        result = ' '.join(notes_in_scale)
        expected_result = 'A# C C# D# F G G#'
        if result == expected_result:
            self.assertTrue(result == expected_result)
            print('Result:\tPASS')
        else:
            self.assertFalse(result != expected_result)
            print('Result:\tFAIL')

    def test_note_shift_with_capo_position(self):
        print('Note Shift with Capo Position...')
        note = 'D'
        capo_position = 2
        music = Music(note)
        result = music.capo_pos_note_shift(capo_position)
        expected_result = 'C'
        if result == expected_result:
            self.assertTrue(result == expected_result)
            print('Result:\tPASS')
        else:
            self.assertFalse(result != expected_result)
            print('Result:\tFAIL')

    def test_scale_shift_with_capo_position(self):
        print('Scale Shift with Capo Position...')
        note = 'D'
        capo_position = 2
        music = Music(note)
        new_scale = music.capo_pos_scale_shift(capo_position)
        result = ' '.join(new_scale)
        expected_result = 'C Dm Em F G Am Bdim'
        if result == expected_result:
            self.assertTrue(result == expected_result)
            print('Result:\tPASS')
        else:
            self.assertFalse(result != expected_result)
            print('Result:\tFAIL')

    def test_minor_scale(self):
        print('Minor Scale...')
        note = 'C'
        music = Music(note)
        notes_in_scale = music.minor_scale()
        result = ' '.join(notes_in_scale)
        expected_result = 'C D D# F G G# A#'
        if result == expected_result:
            self.assertTrue(result == expected_result)
            print('Result:\tPASS')
        else:
            self.assertFalse(result != expected_result)
            print('Result:\tFAIL')

    def test_notes_in_minor_scale(self):
        print('Notes in Minor Scale...')
        note = 'C'
        music = Music(note)
        notes_in_scale = music.notes_in_minor_scale()
        result = ' '.join(notes_in_scale)
        expected_result = 'Cm Dm D# F/Fm  G/Gm  G# A#'
        if result == expected_result:
            self.assertTrue(result == expected_result)
            print('Result:\tPASS')
        else:
            self.assertFalse(result != expected_result)
            print('Result:\tFAIL')
        
    def tearDown(self):
        print('Test Completed')

if __name__ == "__main__":
    unittest.main()
