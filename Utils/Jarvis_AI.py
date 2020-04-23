import numpy as np
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
from glob import glob
from time import sleep
from pdb import set_trace as debug

# Currently Mainly 'voice enabled music streamer'

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
    song_created = ''

    def __init__(self):
        self.lst = []
        self.dict = {}
        self.dict_names = {}
        self.playlist = []
        self.flush_media_file_created()
    
    def flush_media_file_created(self):
        if glob('song.*'):
            file_name_in_dir = glob('song.*')
            if file_name_in_dir:
                try:
                    os.remove(file_name_in_dir[0])
                    self.song_created = ''
                except PermissionError: # say 'STOP' will be implemented after creating 'class Media_Player'
                    print('Silently quiting app!')
                    #print("Please Wait! The song is being played! Let it finish... say 'STOP' or quit external media player (temp) ")

    def url_search(self, search_string, max_search):
        self.dict = {} # Flushing the buffer for new song request
        self.dict_names = {}
        textToSearch = search_string
        query = urllib.parse.quote(textToSearch)
        url = "https://www.youtube.com/results?search_query=" + query
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html)#, 'lxml')
        i = 1
        for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
            if len(self.dict) < max_search:
                self.dict[i] = 'https://www.youtube.com' + vid['href']
                i += 1
            else:
                break
        return url

    def get_search_items(self, num):
        ### 'user' found in url; grab onther search result from self.url_search(string_search, num_of_user_found) and replace those in self.dict
        if self.dict != {}:
            i = 1
            try:
                for url in self.dict.values():
                    info = pafy.new(url)
                    #self.dict_names[i] = info.title
                    self.dict_names[i] = (info.title, url)
                    if num == 0:
                        print("{0}. {1}".format(i, info.title))
                    i += 1

            except ValueError:
                pass

            except OSError:
                print('This video is unavailable') # Bheege Hont Tere; Dostana Hindi movie; desi boyz
                # Truncate last key from 'self.dict'
                del self.dict[list(self.dict.keys())[-1]]
                self.get_search_items(num)
            
            return (self.dict_names, self.dict)

    def play_media(self, num):
        global song_created
        song_title = self.dict[int(num)]
        info = pafy.new(song_title)
        #audio = info.getbestaudio(preftype="m4a")
        #audio.download('song.m4a', quiet=True)
        audio = info.getbestaudio()
        self.flush_media_file_created()
        song_created = 'song.' + audio.extension
        audio.download(song_created, quiet=True)
        print('Loading... Please Wait!')
        sleep(.1)
        #playsound(song_created)
        os.startfile(song_created)

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
        self.ytb = Youtube_mp3()

    def _speak(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    def __wish_me(self):
        hour = int(datetime.now().hour)
        if 0 <= hour < 12:
            self._speak('Good Morning!')
        elif 12 <= hour < 18:
            self._speak('Good Afternoon!')
        else:
            self._speak('Good Evening!')
        
        self._speak('Hello Sir or Madam. I am yout Jarvis. How may I help you?')
    
    def __take_command(self):
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print('Listening...') # execute in seperate threads; if one gets hanged (overloaded) kill that; start new
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
    
    def _substr_in_list_of_strs(self, lst, substr):
        '''
        Objective: Check if a substring is present in a list of strings

        Source: https://www.geeksforgeeks.org/python-finding-strings-with-given-substring-in-list/
        '''
        res_lst_of_strs_with_substr = list(filter(lambda x: substr in x, lst))
        return (bool(res_lst_of_strs_with_substr), res_lst_of_strs_with_substr)
    
    def __stream_online(self, song_name, number=0):
        max_search = 5
        main_list = False

        def try_new_song(new=True):
            if new:
                self._speak('What song to search for?')
                while True:
                    search_term = self.__take_command()
                    if search_term != 'None':
                        break
            else:
                search_term = song_name
            self.__stream_online(search_term)
            
        if number == 0: # direct playing song
            ### Add support for 'search more'; (increase max_search value by let's say=5; show result from 6-10) [say 'refresh', 'more']
            self.ytb.url_search(song_name, max_search)
            search_titles = self.ytb.get_search_items(number)
            skip_song_search_queries = ['skip', 'abort']
            retry_song_search_queries = ['retry', 'search again', 'other', 'new', 'different', 'none of these', 'not these', 'not this'] ## not able to handle wrong entry correctly; re-executing searched result
            if search_titles[1]:
                self._speak('Which Number Song? (SAY for example, Number 1)')
                while True:
                    song_number = self.__take_command()
                    if self._substr_in_list_of_strs(skip_song_search_queries, song_number)[0]: # skip song search; go to main list
                        main_list = True
                        break
                    elif self._substr_in_list_of_strs(retry_song_search_queries, song_number)[0]:
                        main_list = False # try again for another song; not main list
                        break
                    elif song_number != 'None' and \
                        not self._substr_in_list_of_strs(skip_song_search_queries, song_number)[0] and \
                        not self._substr_in_list_of_strs(retry_song_search_queries, song_number)[0]:
                        if 'number' not in song_number:
                            self._speak('Was expecting a number! Retry...')
                            try_new_song(new=False)
                        break
                if not main_list and not self._substr_in_list_of_strs(retry_song_search_queries, song_number)[0]:
                    if 'number' in song_number and 'user' in search_titles[0][int(song_number.strip().split()[-1])][0]: # chk if search result is a valid song or not
                        self._speak('This is a channel name, not a song! Try again...')
                        ### implement this issue in 'Youtube_mp3.get_search_items()'
                    elif 'number' not in song_number or 'number' in song_number and len(song_number.strip().split()) == 1:
                        self._speak('Was expecting a number! Retry...')
                        try_new_song(new=False)
                    elif 'number' in song_number and song_number.strip().split()[-1].isdigit():
                        print(f'Song Title: {search_titles[0][int(song_number.strip().split()[-1])][0]}')
                        self.ytb.play_media(song_number.strip().split()[-1])
                        main_list = True # So that 'try_new_song()' will not execute after song successfully start playing
                    else: ## 'number <non-digit>' is not handled properly
                        print('Say that again please...')
                        try_new_song(new=False)
            else: # for No Search results
                main_list = False
                self._speak(f'No song found with {song_name}! Try Again...') # try again for another song; not main list
            if not main_list:
                try_new_song()
        else: # play song from last wikipedia valid song search
            self.ytb.url_search(song_name + 'lyric', max_search)
            search_titles = self.ytb.get_search_items(number)
            for num in search_titles[0]:
                if 'lyric' in search_titles[0][num][0]:
                    number = num
                    break
            self.ytb.play_media(number)

    class Abilities:
        __my_abilities_with_keywords = {
            'Search for information on wikipedia': ['info', 'information', 'wiki', 'wikipedia'],
            'Open Youtube for you': ['youtube'],
            'Open Google for you': ['google'],
            'Open stackoverflow for you': ['stackoverflow'],
            'Stream Song from youtube directly': ['Stream', 'Song'],
            'Tell you the current time': ['time', 'tell'],
            'Open VS Code for you': ['VS', 'Code'],
            'saying Goodbye': ['Goodbye']
        } # {'Ability to speak out' : 'keyword/s'}
        __my_abilities_with_index = list(zip(list(range(0, len(__my_abilities_with_keywords))), __my_abilities_with_keywords.keys())) # zip ('index numbers', my_abilities)
        
        def __init__(self):
            self.__va = Voice_Assistant()
            self.__unknown_abilities = []
            self.random_2_numbers = list(np.random.permutation(np.arange(0, len(self.__my_abilities_with_keywords) - 1))[:2])

        def what_can_you_do(self): # Return 2 random abilities from 'self.my_abilities'[0:-1] and last one 'Or bid Goodbye'
            first = self.__my_abilities_with_index[self.random_2_numbers[0]][1]
            second = self.__my_abilities_with_index[self.random_2_numbers[1]][1]
            last = self.__my_abilities_with_index[-1][1]
            i_can_do = 'Out of many; I can ' + first + '; or even ' + second + '. Then you can quit this application by ' + last
            self.__va._speak(i_can_do)
            ### Handle any type of 'can you <>'
        
        def how_can_you(self, query): # Handles any type of 'How can you <>'
            what_to_ask = ''
            new_query = query.split()[3:]
            c = 0
            for v in self.__my_abilities_with_keywords.values():
                common_keyword = list(set(new_query) & set(v))
                if common_keyword:
                    if self.__va._substr_in_list_of_strs(v, common_keyword[0])[0]:
                        what_to_ask = self.__va.search_terms[c] #list(self.my_abilities_with_keywords.keys())[list(self.my_abilities_with_keywords.values()).index(common_keyword[0])]
                    break
                else:
                    c += 1

            if what_to_ask:
                self.__va._speak('Just say; ' + what_to_ask)
            else:
                self.__va._speak("I have never told that I can do this!")
                self.__unknown_abilities.append(' '.join(query.split()[3:]))
                self.__va._speak("Anyway I will learn this in future")

        def wikipedia(self, query):
            pass

    def start_AI_engine(self): # Create 'functions' for each search queries for re-use
        self.__abilities = self.Abilities()
        self.__wish_me()
        self.queries_made = []
        while True:
            query = self.__take_command().lower()
            # Logic for executing tasks based on query
            #if self._substr_in_list_of_strs('can do perform'.split(), query)[0]:
            if 'what can you do' in query or 'how can you help' in query:
                self.__abilities.what_can_you_do()
            
            elif 'how can you' in query:
                self.__abilities.how_can_you(query)
            
            elif 'wikipedia' in query:
                self.queries_made.append(query)
                self._speak('Searching Wikipedia...')
                query = query.replace('wikipedia', '')
                try:
                    results = wikipedia.summary(query, sentences=2)
                    self._speak('According to Wikipedia')
                    print(results)
                    self._speak(results)
                except wikipedia.exceptions.PageError:
                    self._speak('Sorry! Page Not Found!')
                except wikipedia.exceptions.DisambiguationError as e: # "Bengali Movie Wikipedia"
                    queries = e.options
                    sub_queries = {}
                    self._speak('Following are the options found, matching your query')
                    for num, option in enumerate(queries):
                        print('{0}. {1}'.format(num + 1, option))
                        sub_queries[num] = option
                    self._speak('Which Number Page? (SAY for example, Number 1)')
                    while True:
                        page_num = self.__take_command()
                        if page_num != 'None':
                            break
                    new_query = sub_queries[int(page_num.strip().split()[-1]) - 1]
                    results = wikipedia.summary(new_query, sentences=2)
                    self._speak('According to Wikipedia')
                    print(results)
                    self._speak(results)
            
            elif 'play the song' in query or 'play it' in query or 'play this song' in query or 'want to hear' in query:
                search_sub = self._substr_in_list_of_strs(self.queries_made, 'wikipedia')
                if search_sub[0]: # if wikipedia searched
                    if len(search_sub[1]) > 1:
                        for query in search_sub[1][::-1]:
                            #query = search_sub[1][-1] # get Last searched wiki query
                            song_name = query.replace('wikipedia', '').strip()
                            wiki_res = wikipedia.summary(song_name, sentences=10) # check id query is a valid song or not
                            if 'music' in wiki_res or 'song' in wiki_res or 'film' in wiki_res:
                                self.__stream_online(song_name, '1')
                        else:
                            self._speak('No song searched in wikipedia!')
                    else:
                        query = search_sub[1][-1]
                        song_name = query.replace('wikipedia', '').strip()
                        wiki_res = wikipedia.summary(song_name, sentences=10) # check id query is a valid song or not
                        if 'music' in wiki_res or 'song' in wiki_res or 'film' in wiki_res:
                            self.__stream_online(song_name, 1)
                        else:
                            self._speak('No song searched in wikipedia!')
                else:
                    self._speak('No song found in search queries! Instead ask to play song...')

            elif 'open youtube' in query:
                self._speak('What to search for?')
                while True:
                    search_term = self.__take_command()
                    if search_term != 'None':
                        break
                webbrowser.open_new_tab(f"https://www.youtube.com/search?q={search_term}")

            elif 'open google' in query:
                self._speak('What to search for?')
                while True:
                    search_term = self.__take_command()
                    if search_term != 'None':
                        break
                webbrowser.open_new_tab(f"https://www.google.com/search?q={search_term}")

            elif 'open stackoverflow' in query:
                webbrowser.open('stackoverflow.com')

            elif 'play song' in query or 'play music' in query or 'play a song' in query:
                self._speak('What to search for?')
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
                self._speak(f'Sir or Madam, The Time is {str_time}')

            elif 'open vs code' in query:
                code_path = 'C:\\Users\\dgkii\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe'
                os.startfile(code_path)
            
            elif 'bye' in query or 'quit' in query or 'stop' in query or 'exit' in query:
                hour = int(datetime.now().hour)
                if 0 <= hour <=18:
                    self._speak('Good Bye Sir or Madam, Thanks for your time! Have a nice day')
                else:
                    if 'good night' in query:
                        self._speak('Good Bye Sir or Madam, Thanks for your time! Good Night!')
                    else:
                        self._speak('Good Bye Sir or Madam, Thanks for your time!')
                self.ytb.flush_media_file_created()
                return False
        return True
