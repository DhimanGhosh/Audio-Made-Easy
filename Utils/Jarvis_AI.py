import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import os, pafy, pyglet, pygame, time
import urllib.request
from urllib.parse import *
from bs4 import BeautifulSoup
from random import randint
from datetime import datetime
from playsound import playsound
from time import sleep
import pdb

class Media_Player:
    def __init__(self, audio_file):
        self.__audio_file = audio_file
        pygame.init()
        pygame.mixer.init()
        #file loading
        pygame.mixer.music.load(self.__audio_file)
        print("Playing:",self.__audio_file)
        pygame.mixer.music.play()
        #play and pause
        while pygame.mixer.music.get_busy():
            timer = pygame.mixer.music.get_pos()
            time.sleep(1)
            control = input()
            pygame.time.Clock().tick(10)
            if control == "pause":
                pygame.mixer.music.pause()
            elif control == "play" :
                pygame.mixer.music.unpause()
            elif control == "time":
                timer = pygame.mixer.music.get_pos()
                timer = timer/1000
                print (str(timer))
            elif int(timer) > 10:
                print ("True")
                pygame.mixer.music.stop()
                break
            else:
                continue

class Youtube_mp3:
    def __init__(self):
        self.lst = []
        self.dict = {}
        self.dict_names = {}
        self.playlist = []

    def url_search(self, search_string, max_search):
        textToSearch = search_string
        query = urllib.parse.quote(textToSearch)
        url = "https://www.youtube.com/results?search_query=" + query
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'lxml')
        i = 1
        for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
            if len(self.dict) < max_search:
                self.dict[i] = 'https://www.youtube.com' + vid['href']
                i += 1
            else:
                break
        return url

    def get_search_items(self, num):
        if self.dict != {}:
            i = 1
            for url in self.dict.values():
                try:
                    info = pafy.new(url)
                    self.dict_names[i] = info.title
                    if num == 0:
                        print("{0}. {1}".format(i, info.title))
                    i += 1

                except ValueError:
                    pass
            return self.dict_names

    def play_media(self, num):
        url = self.dict[int(num)]
        info = pafy.new(url)
        #audio = info.getbestaudio(preftype="m4a")
        #audio.download('song.m4a', quiet=True)
        audio = info.getbestaudio()
        audio.download('song.' + audio.extension, quiet=True)
        sleep(2)
        #playsound('song.' + audio.extension)
        os.startfile('song.' + audio.extension)
        #os.remove('song.' + audio.extension)

        # pyglet media player error
        '''song = pyglet.media.load('song.m4a')
        player = pyglet.media.Player()
        player.queue(song)
        print("Playing: {0}.".format(self.dict_names[int(num)]))
        player.play()
        stop = ''
        while True:
            stop = input('Type "s" to stop; "p" to pause; "" to play; : ')
            if stop == 's':
                player.pause() # Remove the downloaded 'song.m4a' file
                break
            elif stop == 'p':
                player.pause()
            elif stop == '':
                player.play()
            elif stop == 'r':
                #player.queue(song)
                #player.play()
                print('Replaying: {0}'.format(self.dict_names[int(num)]))'''
                
    def download_media(self, num):
        url = self.dict[int(num)]
        info = pafy.new(url)
        audio = info.getbestaudio(preftype="m4a")
        song_name = self.dict_names[int(num)]
        print("Downloading: {0}.".format(self.dict_names[int(num)]))
        print(song_name)
        song_name = input("Filename (Enter if as it is): ")
        file_name = song_name + '.m4a'
        if song_name == '':
            audio.download(remux_audio=True)
        else:
            audio.download(filepath = file_name, remux_audio=True)

    def bulk_download(self, url, num):
        info = pafy.new(url)
        audio = info.getbestaudio(preftype="m4a")
        song_name = self.dict_names[int(num)]
        print("Downloading: {0}.".format(self.dict_names[int(num)]))
        print(song_name)
        song_name = input("Filename (Enter if as it is): ")
        file_name = song_name + '.m4a'
        if song_name == '':
            audio.download(remux_audio=True)
        else:
            audio.download(filepath = file_name, remux_audio=True)

    def add_playlist(self, search_query):
        url = self.url_search(search_query, max_search=1)
        self.playlist.append(url)

class Voice_Assistant:
    search_terms = ['wikipedia', 'open youtube', 'open google', 'open stackoverflow', 'play song', 'time', 'open code', 'quit']

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
    
    def __stream_online(self, song_name, number=0):
        ytb = Youtube_mp3()
        if number == 0:
            max_search = 5
            ytb.url_search(song_name, max_search)
            ytb.get_search_items(number)
            self.__speak('Which Number Song? (SAY for example, Number 1)')
            while True:
                song_number = self.__take_command()
                if song_name != 'None':
                    break
            ytb.play_media(song_number.split()[-1])
        else:
            max_search = 10
            ytb.url_search(song_name + 'lyric', max_search)
            search_titles = ytb.get_search_items(number)
            for num in search_titles:
                if 'lyric' in search_titles[num]:
                    number = num
                    break
            ytb.play_media(number)
    
    def __substr_in_list_of_strs(self, lst, substr):
        '''
        Objective: Check if a substring is present in a list of strings

        Source: https://www.geeksforgeeks.org/python-finding-strings-with-given-substring-in-list/
        '''
        res_lst_of_strs_with_substr = list(filter(lambda x: substr in x, lst))
        return (bool(res_lst_of_strs_with_substr), res_lst_of_strs_with_substr)

    def start_AI_engine(self):
        self.__wish_me()
        queries_made = []
        while True:
            #print(queries_made)
            query = self.__take_command().lower()
            # Logic for executing tasks based on query
            if 'wikipedia' in query:
                queries_made.append(query)
                self.__speak('Searching Wikipedia...')
                query = query.replace('wikipedia', '')
                try:
                    results = wikipedia.summary(query, sentences=2)
                    self.__speak('According to Wikipedia')
                    print(results)
                    self.__speak(results)
                except wikipedia.exceptions.PageError:
                    self.__speak('Sorry! Page Not Found!')
                except wikipedia.exceptions.DisambiguationError as e:
                    queries = e.options
                    print(queries)
            
            elif 'play the song' in query or 'play it' in query or 'play the song' in query or 'want to hear' in query:
                search_sub = self.__substr_in_list_of_strs(queries_made, 'wikipedia')
                if search_sub[0]: # if wikipedia searched
                    if len(search_sub[1]) > 1:
                        for query in search_sub[1][::-1]:
                            #query = search_sub[1][-1] # get Last searched wiki query
                            song_name = query.replace('wikipedia', '').strip()
                            wiki_res = wikipedia.summary(song_name, sentences=10) # check id query is a valid song or not
                            if 'music' in wiki_res or 'song' in wiki_res or 'film' in wiki_res:
                                self.__stream_online(song_name, '1')
                        else:
                            self.__speak('No song searched in wikipedia!')
                    else:
                        query = search_sub[1][-1]
                        song_name = query.replace('wikipedia', '').strip()
                        wiki_res = wikipedia.summary(song_name, sentences=10) # check id query is a valid song or not
                        if 'music' in wiki_res or 'song' in wiki_res or 'film' in wiki_res:
                            self.__stream_online(song_name, 1)
                        else:
                            self.__speak('No song searched in wikipedia!')
                else:
                    self.__speak('No song found in search queries! Instead ask to play song...')
            
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
            
            elif 'play song' in query:
                self.__speak('What to search for?')
                while True:
                    search_term = self.__take_command()
                    if search_term != 'None':
                        break
                self.__stream_online(search_term)
                # music_dir = 'D:\\SONGS\\'
                # songs = os.listdir(music_dir)
                # os.startfile(os.path.join(music_dir, songs[randint(0, len(songs))]))
            
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
