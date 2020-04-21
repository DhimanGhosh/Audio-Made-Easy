import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import os
from random import randint
from datetime import datetime

class Voice_Assistant:
    search_terms = ['wikipedia', 'open youtube', 'open google', 'open stackoverflow', 'play music', 'time', 'open code']

    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[0].id)

    def __speak(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    def __wish_me(self):
        hour = int(datetime.now().hour)
        if 0 <= hour < 12:
            self.__speak('Good Morning!')
        elif 12 <= hour < 18:
            self.__speak('Good Afternoon!')
        else:
            self.__speak('Good Evening!')
        
        self.__speak('Hello Sir. I am yout Jarvis. How may I help you?')
    
    def __take_command(self):
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print('Listening...')
            r.pause_threshold = 1
            audio = r.listen(source)
        
        try:
            print('Recognizing...')
            query = r.recognize_google(audio, language='en-in')
            print(f'User Said: {query}\n')
        except Exception:
            print('Say that again please...')
            return 'None'
        return query
    
    def start_AI_engine(self):
        self.__wish_me()
        while True:
            query = self.__take_command().lower()

            # Logic for executing tasks based on query
            if 'wikipedia' in query:
                self.__speak('Searching Wikipedia...')
                query = query.replace('wikipedia', '')
                results = wikipedia.summary(query, sentences=2)
                self.__speak('According to Wikipedia')
                print(results)
                self.__speak(results)
            
            elif 'open youtube' in query:
                self.__speak('What to search for?')
                while True:
                    search_term = self.__take_command()
                    if search_term != 'None':
                        break
                webbrowser.open_new_tab(f"https://www.youtube.com/search?q={search_term}")
            
            elif 'open google' in query:
                self.__speak('What to search for?')
                while True:
                    search_term = self.__take_command()
                    if search_term != 'None':
                        break
                webbrowser.open_new_tab(f"https://www.google.com/search?q={search_term}")
            
            elif 'open stackoverflow' in query:
                webbrowser.open('stackoverflow.com')
            
            elif 'play music' in query:
                music_dir = 'D:\\SONGS\\'
                songs = os.listdir(music_dir)
                os.startfile(os.path.join(music_dir, songs[randint(0, len(songs))]))
            
            elif 'time' in query:
                str_time = datetime.now().strftime("%H:%M:%S")
                self.__speak(f'Sir, The Time is {str_time}')
            
            elif 'open code' in query:
                code_path = 'C:\\Users\\dgkii\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe'
                os.startfile(code_path)
            
            elif 'bye' in query or 'quit' in query or 'stop' in query:
                self.__speak('Quiting Sir, Thanks for your time')
                return False
        return True