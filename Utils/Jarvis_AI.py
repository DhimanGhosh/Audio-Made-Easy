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
        print(f'song title: {song_title}')
        info = pafy.new(song_title)
        #audio = info.getbestaudio(preftype="m4a")
        #audio.download('song.m4a', quiet=True)
        audio = info.getbestaudio()
        self.flush_media_file_created()
        song_created = 'song.' + audio.extension
        audio.download(song_created, quiet=True)
        sleep(2)
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
    ytb = Youtube_mp3()

    def __init__(self):
        self.search_terms = ['wikipedia', 'open youtube', 'open google', 'open stackoverflow', 'play song', 'time', 'open code', 'quit']
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
        
        self.__speak('Hello Sir or Madam. I am yout Jarvis. How may I help you?')
    
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
    
    def __substr_in_list_of_strs(self, lst, substr):
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
                self.__speak('What song to search for?')
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
            retry_song_search_queries = ['retry', 'search again', 'other', 'new', 'different'] ## not able to handle wrong entry correctly; re-executing searched result
            if search_titles[1]:
                self.__speak('Which Number Song? (SAY for example, Number 1)')
                while True:
                    song_number = self.__take_command()
                    if self.__substr_in_list_of_strs(skip_song_search_queries, song_number)[0]: # skip song search; go to main list
                        main_list = True
                        break
                    elif self.__substr_in_list_of_strs(retry_song_search_queries, song_number)[0]:
                        main_list = False # try again for another song; not main list
                        break
                    elif song_number != 'None' and \
                        not self.__substr_in_list_of_strs(skip_song_search_queries, song_number)[0] and \
                        not self.__substr_in_list_of_strs(retry_song_search_queries, song_number)[0]:
                        if 'number' not in song_number:
                            self.__speak('Was expecting a number! Retry...')
                            try_new_song(new=False)
                        break
                if not main_list and not self.__substr_in_list_of_strs(retry_song_search_queries, song_number)[0]:
                    #print(f'search_title: {search_titles[1][int(song_number.strip().split()[-1])]}')
                    if 'number' in song_number and 'user' in search_titles[1][int(song_number.strip().split()[-1])]: # chk if search result is a valid song or not
                        self.__speak('This is a channel name, not a song! Try again...')
                        ### implement this issue in 'Youtube_mp3.get_search_items()'
                    elif 'number' not in song_number or 'number' in song_number and len(song_number.strip().split()) == 1:
                        self.__speak('Was expecting a number! Retry...')
                        try_new_song(new=False)
                    else:
                        self.ytb.play_media(song_number.strip().split()[-1])
                        main_list = True # So that '__try_new_song()' will not execute after song successfully start playing
            else: # for No Search results
                main_list = False
                self.__speak(f'No song found with {song_name}! Try Again...') # try again for another song; not main list
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

    class Abilities(object):
        def __init__(self):
            Voice_Assistant.__speak('Abilities')

        def what_can_you_do(self):
            pass

    def start_AI_engine(self): # Create 'functions' for each search queries for re-use
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
                except wikipedia.exceptions.DisambiguationError as e: # "Bengali Movie Wikipedia"
                    queries = e.options
                    sub_queries = {}
                    self.__speak('Following are the options found, matching your query')
                    for num, option in enumerate(queries):
                        print('{0}. {1}'.format(num + 1, option))
                        sub_queries[num] = option
                    self.__speak('Which Number Page? (SAY for example, Number 1)')
                    while True:
                        page_num = self.__take_command()
                        if page_num != 'None':
                            break
                    new_query = sub_queries[int(page_num.strip().split()[-1]) - 1]
                    results = wikipedia.summary(new_query, sentences=2)
                    self.__speak('According to Wikipedia')
                    print(results)
                    self.__speak(results)

            
            elif 'play the song' in query or 'play it' in query or 'play this song' in query or 'want to hear' in query:
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
                self.__speak(f'Sir or Madam, The Time is {str_time}')
            
            elif 'open code' in query:
                code_path = 'C:\\Users\\dgkii\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe'
                os.startfile(code_path)
            
            elif 'bye' in query or 'quit' in query or 'stop' in query or 'exit' in query:
                hour = int(datetime.now().hour)
                if 0 <= hour <=18:
                    self.__speak('Good Bye Sir or Madam, Thanks for your time! Have a nice day')
                else:
                    if 'good night' in query:
                        self.__speak('Good Bye Sir or Madam, Thanks for your time! Good Night!')
                    else:
                        self.__speak('Good Bye Sir or Madam, Thanks for your time!')
                self.ytb.flush_media_file_created()
                return False
        return True
