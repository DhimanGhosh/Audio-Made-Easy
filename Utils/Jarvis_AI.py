import numpy as np
import pandas as pd
import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import requests
import json
import os
import sys
import shutil
import platform
import subprocess
import re
import pygame
import time
import urllib.request as request
from urllib.request import urlopen
from urllib.parse import quote
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from random import randint
from datetime import datetime
from glob import glob
from time import sleep
from Levenshtein import ratio
from mutagen.mp3 import MP3
from winsound import Beep

from pdb import set_trace as debug

utils_dir = assets_dir = datasets_dir = cache_dir = tmp_dir = ''
# ----- Access Other Directories on Particular Platform ----- #
if platform.system() == 'Linux':
    utils_dir = os.path.realpath('../Utils') + '/'
    sys.path.insert(0, utils_dir)
    from Music import Music
    assets_dir = os.path.realpath('../assets') + '/'
    sys.path.insert(0, assets_dir)
    datasets_dir = os.path.realpath('../assets/datasets') + '/'
    sys.path.insert(0, datasets_dir)
    cache_dir = os.path.realpath('../assets/cache') + '/'
    sys.path.insert(0, cache_dir)
    tmp_dir = os.path.realpath('../assets/cache/tmp_dir') + '/'
    sys.path.insert(0, tmp_dir)
elif platform.system() == 'Windows':
    root_dir = os.path.realpath('..\\Audio-Made-Easy')
    sys.path.insert(0, root_dir)
    utils_dir = root_dir + '\\Utils\\'
    assets_dir = root_dir + '\\assets\\'
    datasets_dir = assets_dir + 'datasets\\'
    cache_dir = assets_dir + 'cache\\'
    tmp_dir = cache_dir + 'tmp_dir\\'

features = utils_dir + 'Features.txt'
brain = datasets_dir + 'brain.csv'
jokes = datasets_dir + 'shortjokes.csv'

class _Media_Player: # Supports only mp3
    REPLAY = False

    def __init__(self, audio_file=cache_dir + 'KKHBH.mp3'): # If nothing is found; for the time being; just play the initialised value
        '''
        Play, Pause, Stop, Resume, Restart(Stop + Play), Replay <A MODE to restart the song once it finishes>

        forward (+10 seconds), backward (-10 seconds) ---- 'pygame.mixer.music.get_pos' && 'pygame.mixer.music.set_pos'

        volume-up (), volume-down () ---- 'pygame.mixer.music.get_volume()' && 'pygame.mixer.music.set_volume()'

        next, prev -- for playlist playing (for single audio ---- SAY: "That was the last song" <resume_playing>)
        '''
        self.__audio_file = audio_file
        self.__audio = MP3(self.__audio_file)
        self.__audio_sample_rate = self.__audio.info.sample_rate
        self.__audio_channels = self.__audio.info.channels
        self.__audio_length = self.__audio.info.length
        self.__audio_sample_rate = self.__audio.info.sample_rate
        self.__song_name = audio_file.split()[0]
        #pygame.mixer.music.rewind() # restart music
        #pygame.mixer.music.queue # queue a sound file to follow the current
        self.__songtracks = os.listdir()
        self.__playlist = []
        for track in self.__songtracks:
            self.__playlist.append(track)
    
    def play(self):
        if pygame.mixer.get_init():
            pygame.mixer.quit() # quit it, to make sure it is reinitialized
        pygame.mixer.pre_init(frequency=self.__audio_sample_rate, size=-16, channels=self.__audio_channels, buffer=4096)
        pygame.mixer.init()
        pygame.mixer.music.load(self.__audio_file)
        pygame.mixer.music.play()
        print(self.__song_name + " ---- Playing")

    def pause(self):
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        print("Playback Paused")

    def resume(self):
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            pygame.mixer.music.unpause()
        print(self.__song_name + " ---- Resumed")

    def stop(self):
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            #pygame.mixer.music.fadeout(5)
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        print("Stopped")
    
    def replay(self):
        self.REPLAY = not self.REPLAY
        if self.REPLAY:
            print(f'{self.__audio_file} ---- is set to REPLAY')
        else:
            print(f'{self.__audio_file} ---- is set NOT to REPLAY')
        return self.REPLAY

    def restart(self):
        self.stop()
        self.play()
        print(self.__song_name + " ---- Restarting")
    
    def current_time(self):
        timer = 0
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            timer = pygame.mixer.music.get_pos()
            timer = int(timer//1000)
        return timer

    def __un_used_functions(self):
        pygame.mixer.music.rewind() # restart music
        pygame.mixer.music.queue # queue a sound file to follow the current

class _Song_Search_and_Download: # Will be implemented LATER
    '''
    Using bs4: (Web scraping)

    >>>> ---- For example ---- <<<<
    ---SEARCHING---
    1. query: 'mithe alo'
    2. go to https://www.google.com/search?q=mithe+alo
    3. grep for 'Movie / Album' : <Cockpit>
    4. open the link to get its information; lets say 'wikipedia'
    5. grep for 'mithe alo' in the page using 'wikipedia' API -OR- there itself (will help to get the length of this song)
    6. get the length from there
    
    ---DOWNLOADING---
    1. 
    '''
    pass

class _Youtube_mp3: # Download songs from youtube and create a mp3 file of that
    def __init__(self):
        '''
        Overview:
            Throw me a song query... I will play it for you!

        Description:
            That also with the help of YouTube. Now guess my library size. LOL!
        '''
        self.lst = []
        self.dict = {}
        self.dict_names = {}
        self.playlist = []
        try:
            os.mkdir(cache_dir)
            print('Cache folder created')
        except FileExistsError:
            print('Cache folder already present')
        try:
            os.mkdir(tmp_dir)
            print('tmp folder created')
        except FileExistsError:
            print('tmp folder already present')
        for f in glob('*.exe'):
            shutil.copy(cache_dir + f, tmp_dir)

    def url_search(self, search_string, max_search): # search youtube and returns list of 5 links
        self.dict = {} # Flushing the buffer for new song request
        self.dict_names = {}
        textToSearch = search_string
        print(f'textToSearch: {textToSearch}')
        query = quote(textToSearch)
        url = "https://www.youtube.com/results?search_query=" + query
        response = urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'lxml')
        i = 1
        for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
            if len(self.dict) < max_search:
                self.dict[i] = 'https://www.youtube.com' + vid['href']
                i += 1
            else:
                break
        #return url
        return self.dict

    def clean_file_name(self, name):
        name = name.replace(' ', '-')
        name = name.replace('_', '-')
        name = name.split('--')[0]
        ## ---- Unable to handle non elglish characters ---- ## (Search for song 'Sudhu Tui from Bengali movie Villain')
        #getVals = list([val for val in name if val.isalpha() or val.isnumeric() or val=='-'])
        '''pattern = re.compile("[A-Za-z0-9 -]+")
        name = pattern.fullmatch(name)'''
        #name = "".join(getVals) 
        return name

    def test_url(self, url): # (in folder 'assets\cache')
        os.chdir(tmp_dir)
        try:
            #command = 'youtube-dl -f bestaudio ' + url + ' --exec "ffmpeg -i {}  -codec:a libmp3lame -qscale:a 0 {}.mp3 && del {} " '
            command = ['youtube-dl','-cit','--embed-thumbnail','--no-warnings','--extract-audio','--audio-quality', '0','--audio-format', 'mp3', url]
            print(f'Download Command: {command}')
            subprocess.call(command)
            sleep(2)
            if glob('*.mp3') or glob('*.webm') or glob('*.m4a'): # song found
                new_name = song_name = ''
                print(f"media files:\n{glob('*.*')}")
                if glob('*.webm'):
                    song_name = glob('*.webm')[0]
                    print(f"song_name webm: {song_name}\ncleaned_song_name webm: {self.clean_file_name(song_name) + '.' + song_name.split('.')[-1]}")
                    os.rename(song_name, self.clean_file_name(song_name) + '.' + song_name.split('.')[-1])
                    song_name = glob('*.webm')[0]
                    new_name = song_name.split('.')[0] + '.mp3'
                    command = f"ffmpeg -i {song_name} -vn -ar 44100 -ac 2 -b:a 192k {new_name}"
                    subprocess.call(command)
                    print(f'\n\n\nNAME of FILE to PLAY: {song_name}\n{new_name}\n\n')
                elif glob('*.m4a'):
                    song_name = glob('*.m4a')[0]
                    print(f"song_name m4a: {song_name}\ncleaned_song_name m4a: {self.clean_file_name(song_name) + '.' + song_name.split('.')[-1]}")
                    os.rename(song_name, self.clean_file_name(song_name) + '.' + song_name.split('.')[-1])
                    song_name = glob('*.m4a')[0]
                    new_name = song_name.split('.')[0] + '.mp3'
                    command = f'ffmpeg -i {song_name} -codec:v copy -codec:a libmp3lame -q:a 2 {new_name}'
                    subprocess.call(command)
                    print(f'\n\n\nNAME of FILE to PLAY: {song_name}\n{new_name}\n\n')
                elif glob('*.mp3'):
                    song_name = glob('*.mp3')[0]
                    print(f"song_name mp3: {song_name}\ncleaned_song_name mp3: {self.clean_file_name(song_name) + '.' + song_name.split('.')[-1]}")
                    os.rename(song_name, self.clean_file_name(song_name) + '.' + song_name.split('.')[-1])
                    new_name = glob('*.mp3')[0]
                    shutil.copy(new_name, cache_dir)
                    os.chdir(cache_dir)
                    print(f'\n\n\nNAME of FILE to PLAY: {song_name}\n{new_name}\n\n')
                shutil.copy(new_name, cache_dir)
                # os.chdir(cache_dir)
                # shutil.rmtree(os.path.join(cache_dir, tmp_dir))
                return new_name
            else:
                return None
        except Exception:# (HTTPError) # url is not a song
            return None

    def play_media(self, song_name): # Play media based on url; since .mp3 will already be downloaded in 'test_url()'; no need to download it again; ---- Just Returns '_Media_Player' object with loaded song----
        os.chdir(cache_dir)
        print(f'song_name before cleaning: {song_name}')
        song_name = self.clean_file_name(song_name)
        print(f'song_name after cleaning: {song_name}')
        self.player = _Media_Player(audio_file=song_name)
        return self.player

    def play_media_from_cache(self, song_name):
        '''
        For Cache storing:
        1. Check if the name of the song is there in cache folder or not.
        2. If it is there play from cache or download it and play
        (Store only the 'initials of song'; not the full name && 'encrypt' them --------- 'decrypt' while using)
        '''
        pass

    def add_playlist(self, search_query):
        url = self.url_search(search_query, max_search=1)
        self.playlist.append(url)

class _Vocabulary: # Reads data from datasets; Store personalised data
    ## ---- SYNONYMS ---- ##
    SYNONYMS = {
        'PLAY'      : ['play', 'begin'], # This will act as 'Replay' (when called while playing a song)
        'PAUSE'     : ['pause', 'hold', 'break', 'suspend', 'interrupt'],
        'RESUME'    : ['resume'],
        'REPLAY'    : ['replay', 'repeat', 'reply'], # 'reply' is added since 'speech_recognition' sometimes hear 'reply' when I say 'replay'... LOL!
        'RESTART'   : ['restart', 'from beginning', 'from starting', 'start'],
        'STOP'      : ['stop', 'close', 'finish', 'end', 'terminate', 'wind up', 'windup'],
    }

    ## ---- JOKES ---- ##
    df = pd.read_csv(jokes)
    joke = df['Joke']
    random_joke_id = np.random.permutation(np.arange(0, len(joke) - 1))[:1]
    JOKES = {
        'joke' : str(joke[random_joke_id[0]])
    }

    ## ---- Conversation ---- ##
    BRAIN = pd.read_csv(brain)

    ## ---- Song Search Abort ---- ##
    skip_song_search_queries = ['skip', 'abort']
    retry_song_search_queries = ['retry', 'search again', 'other', 'new', 'different', 'none of these', 'not these', 'not this'] ## NOTE: not able to handle wrong entry correctly; re-executing searched result

    ## ---- ABILITIES ---- ##
    ABILITIES = ['wikipedia', 'open youtube', 'open google', 'open stackoverflow', 'play song', 'time', 'open code', 'quit', 'news']
    my_abilities_with_keywords = {
            'Search for information on wikipedia': ['info', 'information', 'wiki', 'wikipedia'],
            'Open Youtube and search for you': ['youtube', 'searching youtube', 'youtube search', 'open youtube', 'youtube opening', 'viewing youtube', 'youtube viewing', 'watching youtube', 'youtube watching'],
            'Open Google and search for you': ['google'],
            'Open stackoverflow and search for you': ['stackoverflow'],
            'Stream Song from youtube directly for you': ['stream', 'song', 'streaming', 'music'],
            'Tell you the current time': ['time', 'tell'],
            'Open VS Code for you': ['VS', 'Code'],
            'have general conversation with you': ['conversation', 'talk'],
            'Read out live news for you': ['news', 'break', 'hot'],

            'saying Goodbye': ['Goodbye'],
        } # {'Ability to speak out' : 'keyword/s'}

class Voice_Assistant: ## NOTE: Play a beep when sub-queries are searched
    '''
    Overview:
        Perform any task just with your voice.
    
    Description:
        This Voice Assistant has a lots of Abilities (mentioned inside sub-class 'Abilities'). Basically when we ask 'AI' engine for any task. Then it asks its own 'Abilities' to perform some task based on input query. Then it takes the output and return it to us.
    '''

    '''
    How to improve its speech recognision:

    Create a list[...] to keep track of words asked as query to VA.
    So as to improve day-by-day its speech recognition; using ''cosine-similarity'' (or any sort of text matching algorithm) between 'new query asked and old queries made'.
    If better result is observed; replace the old one with the new one.
    '''

    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[0].id)
        self.VA_NAME = 'Google'
        self._Vocabulary = _Vocabulary()
        self.ytb = _Youtube_mp3()
        self.search_terms = self._Vocabulary.ABILITIES
        self._song_name = ''
        self.player = _Media_Player()
        self.__retry_list = 1 # if the first 5 searches doesn't contain any media file; then go for next 5 searches

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
        
        self._speak(f'Hello Sir. I am {self.VA_NAME} - Your personal voice assistant!')
        self._speak('How may I help You?')
    
    def _take_command(self, waiting_for_query=''): ## NOTE: Execution Stopped (hanged)
        '''
        NOTE: <To Solve HANG issue>
        Create 2 threads: for handling the mic voice commands
        1. if retries exceed a THRESHOLD_VALUE=5 ======= kill it
        2. it waits for thread 1 to be killed ======= then it will start
        <Cycle interchangely REPEATS>
        '''
        ## NOTE: Create 2 threads (one for handling the mic voice commands) && (amother will wait for its expire)
        r = sr.Recognizer()

        with sr.Microphone() as source:
            # r.adjust_for_ambient_noise(source) # Ambient Noise Cancellation; use only when in a noisy background
            '''
            Intended to calibrate the energy threshold with the ambient energy level. Should be used on periods of audio without speech - will stop early if any speech is detected.
            '''
            ## NOTE: Add what the mic is waiting to hear from you
            print(f'Waiting for: {waiting_for_query}\nListening...') # execute in seperate threads; if one gets hanged (overloaded) kill that; start new ['DEBUGGING' purpose only] <--> comment it when 'using'
            #r.pause_threshold = 1 # let it be as '1'
            r.energy_threshold = 100 # Default: 300 (now less energy reqd. while speaking)
            audio = r.listen(source)
        
        try:
            print('Recognizing...')
            query = r.recognize_google(audio, language='en-in')
            print(f'User Said: {query}\n')
        except Exception:
            print('Say that again please...')
            return 'none'
        return query.lower()
    
    def _substr_in_list_of_strs(self, lst, substr):
        '''
        Objective: Check if a substring is present in a list of strings

        Source: https://www.geeksforgeeks.org/python-finding-strings-with-given-substring-in-list/
        '''
        res_lst_of_strs_with_substr = list(filter(lambda x: substr in x, lst))
        return (bool(res_lst_of_strs_with_substr), res_lst_of_strs_with_substr)
    
    def _stream_online(self, song_name, number=0): # number = song_number to play in the list of search results
        max_search = 5

        if number == 0: # direct play; doesn't involve user
            self._speak('Searching Song...')
            songs_list = self.ytb.url_search(song_name, max_search) ##NOTE: add 'search_more' parameter in 'url_search()' that will hold an integer of 'self.__retry_list'
            print(f'songs_list: {songs_list}')
            if songs_list:
                for sl_no, url in songs_list.items():
                    print(sl_no, url)
                    song_name = self.ytb.test_url(url)
                    if song_name: # valid song found
                        self.player = self.ytb.play_media(song_name)
                        break
                    else:
                        continue
                # if not valid_song:
                #     pass # self.__retry_list += 1 (----if the first 5 searches doesn't contain any media file; then go for next 5 searches----)
            else:
                self.player = None
                pass # Say Again

        '''else: # Not implemented yet
            song_search_query = [song_name + ' ' + key for key in ('lyric', 'full', 'audio', 'official', '|')]
            print(f'song_search_query: {song_search_query}')
            results_found = False
            for query in song_search_query: # search for 'song_name' + ==> ('lyric', 'full', 'audio', 'official', '|')
                self.ytb.url_search(query, max_search)
                #search_titles = self.ytb.get_search_items(number) # Return the result list for each 'query';; don't print the list (since, number != 0)
                if search_titles: # if atleast 1 song found
                    for num in search_titles[0].keys(): # traverse the list for the search query
                        if query.split()[-1] in search_titles[0][num][0]: # if any('lyric', 'full', 'audio', 'official', '|') in search_titles[0][num][0] <-- song_title
                            results_found = True
                            number = num
                            break
                if results_found:
                    break
            if results_found:
                print(f'\n\nsong in wiki search ---- results_found:\n{results_found}\n\n')
                self.player = self.ytb.play_media(number)
            else: # If direct song play did not work for 'play_song_from_last_search()' then call 'self._stream_online(song_name, number=0); since here 'number=1'
                self._stream_online(song_name, number=0)'''
        
        return self.player

    class Abilities: ## NOTE: Handle any type of 'can you <>';; direct perform action rather than telling what to ask
        '''
        Overview:
            The 'Abilities' that I have to perform various tasks.

        Myself:
            My 'Abilities' are very limited.

        NOTE: A task for you... "Please train me with new 'Abilities' so that I can stand in the real world"
        '''

        '''
        NOTE: Add support for wikipedia extract for information like ('Bollywood movies releasing next month')
        '''

        '''
        NOTE: If 'another / again' joke is asked; SAY it;; or else pass this 'query' to main 'Thread' so that ita can execute any of its tasks
            {Don't use this approach;; or else it has to be implemented on every sub-tasks}

        Instead:
            1. Go back to main thread
            2. If 'another / again' is asked
            3. It will check what was the last thing asked <stored in a list[]>
            4. Based on that; it will call the respective function

        NOTE: It can conflict with the feature 'Abilities.play_song_from_last_search(<webpage>)'. Make the commands unique [SMARTer recognision]
        '''

        def __init__(self):
            self.__va = Voice_Assistant()
            self.__my_abilities_with_keywords = self.__va._Vocabulary.my_abilities_with_keywords
            self.__my_abilities_with_index = list(zip(list(range(0, len(self.__my_abilities_with_keywords))), self.__my_abilities_with_keywords.keys())) # zip ('index numbers', my_abilities)
            self.__random_2_numbers = list(np.random.permutation(np.arange(0, len(self.__my_abilities_with_keywords) - 1))[:2])
            self.__call_VA_timout = 1
            self.__queries_made = []
            self.__unknown_abilities = []

        def what_can_you_do(self, query): # Return 2 random abilities from 'self.my_abilities'[0:-1] and 'Bid Goodbye'
            if 'how can you help in ' in query or 'how can you help me ' in query:
                self.how_can_you(query)
            else:
                first = self.__my_abilities_with_index[self.__random_2_numbers[0]][1]
                second = self.__my_abilities_with_index[self.__random_2_numbers[1]][1]
                last = self.__my_abilities_with_index[-1][1]
                i_can_do = 'Out of many; I can ' + first + '; or even ' + second + ' . Or you can quit this application by ' + last
                self.__va._speak(i_can_do)
        
        def how_can_you(self, query): # Handles any type of 'How can you <task>'
            what_to_ask = ''
            print(f'query: {query}')
            if 'how can you help in' in query or 'how can you help me' in query:
                new_query = query.split()[5:]
            else:
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
            
            print(f'what to ask: {what_to_ask}')
            if what_to_ask:
                self.__va._speak('Just say; ' + what_to_ask)
            else:
                self.__va._speak("I have never told that I can do this!")
                self.__unknown_abilities.append(' '.join(query.split()[3:]))
                self.__va._speak("Anyway I will learn this in future")

        def wikipedia(self, query): ## NOTE: Incomplete
            self.__queries_made.append(query)
            self.__va._speak('Searching Wikipedia...')
            query = query.replace('wikipedia', '') ## NOTE: If 'query' is only 'wikipedia' then this line will throw 'wikipedia.exceptions.WikipediaException'; deal with it
            try:
                results = wikipedia.summary(query, sentences=2)
                self.__va._speak('According to Wikipedia')
                print(results)
                self.__va._speak(results)
            except wikipedia.exceptions.PageError:
                self.__va._speak('Sorry! Page Not Found!')
            except wikipedia.exceptions.DisambiguationError as e: # "Bengali Movie Wikipedia"; "SK Wikipedia"
                queries = e.options
                sub_queries = {}
                self.__va._speak('Following are the options found, matching your query')
                for num, option in enumerate(queries):
                    print('{0}. {1}'.format(num + 1, option))
                    sub_queries[num] = option
                self.__va._speak('Which Number Page? (SAY for example, Number 1)') ## NOTE: Incomplete...
                while True:
                    page_num = self.__va._take_command('Which Number Wikipedia Page? (SAY for example, Number 1)')
                    if page_num != 'none':
                        break
                new_query = sub_queries[int(page_num.strip().split()[-1]) - 1]
            except wikipedia.exceptions.WikipediaException: ## NOTE: Incomplete...
                print('Say that again please...')
                self.__va._speak('search wikipedia')
                while True:
                    new_query = self.__va._take_command('what to search in wikipedia')
                    if new_query != 'none':
                        break
                results = wikipedia.summary(new_query, sentences=2)
                self.__va._speak('According to Wikipedia')
                print(results)
                self.__va._speak(results)

        def youtube(self, query):
            self.__queries_made.append(query)
            self.__va._speak('What to search for?')
            while True:
                search_term = self.__va._take_command('What to search in youtube?')
                if search_term != 'none':
                    break
            query = quote(search_term)
            url = "https://www.youtube.com/results?search_query=" + query
            webbrowser.open_new_tab(url)

        def google(self, query):
            self.__queries_made.append(query)
            self.__va._speak('What to search for?')
            while True:
                search_term = self.__va._take_command('What to search in google?')
                if search_term != 'none':
                    break
            query = quote(search_term)
            url = "https://www.google.com/search?q=" + query
            webbrowser.open_new_tab(url)

        def play_song_from_last_search(self, website): ## NOTE: Incomplete
            if website == 'wikipedia':
                search_sub = self.__va._substr_in_list_of_strs(self.__queries_made, 'wikipedia')
                if search_sub[0]: # if wikipedia searched
                    if len(search_sub[1]) >= 1:
                        last_searched_query = search_sub[1][-1]
                        song_name = last_searched_query.replace('wikipedia', '').strip()
                        wiki_res = wikipedia.summary(song_name, sentences=10) # check id query is a valid song or not
                        if 'music' in wiki_res or 'song' in wiki_res or 'film' in wiki_res:
                            self.__va._stream_online(song_name, 1)
                        else:
                            self.__va._speak('No song searched in wikipedia!')
                    else:
                        query = search_sub[1][-1]
                        song_name = query.replace('wikipedia', '').strip()
                        wiki_res = wikipedia.summary(song_name, sentences=10) # check id query is a valid song or not
                        if 'music' in wiki_res or 'song' in wiki_res or 'film' in wiki_res:
                            self.__va._stream_online(song_name, 1) ## Will not work now;; See LINE: 306
                        else:
                            self.__va._speak('No song searched in wikipedia!')
                    return True
            
            elif website == 'youtube':
                pass # self.__va._stream_online();; first result
                return True

            elif website == 'google':
                pass # self.__va._stream_online();; first result with a song name
                return True
            
            else:
                self.__va._speak('No song found in search queries! Instead ask to play song...')
                return False

        def play_song(self, query): # Use multi-threading for 'song playing' and 'media-player controls' (2 threads)
            def any_keyword_match_with_Vocabulary(keyword, list_to_search_in):
                for key in list_to_search_in:
                    if keyword.lower() in key.lower() or key.lower() in keyword.lower(): # Simplest 'text matching algorithm'
                        return True
                return False
            
            paused = False
            replay_song = False
            search_term = ' '.join(query.split()[1:])
            music_player = self.__va._stream_online(search_term)
            if music_player:
                music_player.play()
            else:
                self.__va._speak('Sorry Sir! Did not get you!')
                retry = self.__va._take_command('Waiting for Search Song Again')
                self.play_song(retry)

            control = '' # To detect 'STOP'
            while True:
                call_VA = self.__va._take_command('Waiting for (OK GOOGLE)')
                if self.__va.VA_NAME.lower() in call_VA: # If VA is called
                    music_player.pause()
                    wait = 1
                    control = ''
                    while not control or wait <= self.__call_VA_timout:
                        control = self.__va._take_command('Waiting for Music Control Actions')
                        if control:
                            if any_keyword_match_with_Vocabulary(control, self.__va._Vocabulary.SYNONYMS['PLAY']):  # start from beginning
                                music_player.resume() # Eliminated everything from (_Vocabulary.SYNONYMS['PLAY'])
                            elif any_keyword_match_with_Vocabulary(control, self.__va._Vocabulary.SYNONYMS['PAUSE']): # pause
                                music_player.pause()
                                paused = not paused # To stop replaying when in paused; when VA is called and no query passed
                            elif any_keyword_match_with_Vocabulary(control, self.__va._Vocabulary.SYNONYMS['REPLAY']): # A MODE to restart the song once it finishes
                                replay_song = music_player.replay()
                                music_player.resume()
                            elif any_keyword_match_with_Vocabulary(control, self.__va._Vocabulary.SYNONYMS['RESTART']): # pause
                                music_player.restart()
                            elif any_keyword_match_with_Vocabulary(control, self.__va._Vocabulary.SYNONYMS['RESUME']): # start after pause
                                music_player.resume()
                            elif any_keyword_match_with_Vocabulary(control, self.__va._Vocabulary.SYNONYMS['STOP']): # stop the song && closes the '_Media_Player' instance
                                music_player.stop()
                                print(f'Current Position: {music_player.current_time()}\n')
                                break
                        wait += 1
                        print(f'waiting for control command... timeout[{wait}]')
                    if any_keyword_match_with_Vocabulary(control, self.__va._Vocabulary.SYNONYMS['STOP']): # exit from 'play_song()'
                        break
                    elif wait >= self.__call_VA_timout:
                        if not paused:
                            music_player.resume() # If nothing is said after calling VA
                            print('TIMEOUT Happened.... and Playback RESUMED....')
                elif 'none' in call_VA or '' in call_VA: # If some text from unwanted voice is detected; it will skip and 'restart()' will be called
                    continue
                elif replay_song and not 'when_song_ends()': # To avoid this just using 'not when_song_ends()' (Means, song will never end) [A . False = False]
                    music_player.restart()

        def stackoverflow(self, query):
            self.__va._speak('What to search for?')
            while True:
                search_term = self.__va._take_command('What to search in stackoverflow?')
                if search_term != 'none':
                    break
            query = quote(search_term)
            url = "https://stackoverflow.com/search?q=" + query
            webbrowser.open_new_tab(url)

        def current_time(self, query):
            str_time = datetime.now().strftime("%H:%M:%S")
            self.__va._speak(f'Sir, The Time is {str_time}')

        def open_app(self, query):
            code_path = 'C:\\Users\\dgkii\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe'
            os.startfile(code_path)

        def quit_VA(self, query):
            hour = int(datetime.now().hour)
            if 0 <= hour <=18:
                self.__va._speak('Good Bye Sir, Thanks for your time! Have a nice day')
            else:
                if 'good night' in query:
                    self.__va._speak('Good Bye Sir, Thanks for your time! Good Night!')
                else:
                    self.__va._speak('Good Bye Sir, Thanks for your time!')

        def conversation(self): # This the brain of my VA. Read 'datasets/brain.csv'; create and train model to have conversation with user
            brain = self.__va._Vocabulary.BRAIN
            self.stop = False

            ## Approximating QA system
            # Approximate string matching
            def getApproximateAnswer(q):
                max_score = 0
                answer = ""
                prediction = ""
                for _, row in brain.iterrows():
                    score = ratio(row["Question"], q)
                    if score >= 0.9: # I'm sure, stop here
                        return row["Answer"], score, row["Question"]
                    elif score > max_score: # I'm unsure, continue
                        max_score = score
                        answer = row["Answer"]
                        prediction = row["Question"]

                if max_score > 0.8:
                    return answer, max_score, prediction
                return "Sorry, I didn't get you.", max_score, prediction

            while not self.stop:
                def ask():
                    print('Waiting for you!')
                    while True:
                        question = self.__va._take_command('Waiting for you to have coversation...')
                        if question != 'none':
                            break
                    reply(question)

                def reply(question):
                    answer, _, _ = getApproximateAnswer(question)
                    self.__va._speak(answer)

                    if 'bye' in answer:
                        if 'as you wish' in answer:
                            self.stop = True
                        else:
                            self.quit_VA(question)
                            self.stop = True
                
                ask()
            
            if self.stop:
                return False
            return True

        def read_out_news(self, query): # query: NEWS Category (region / topic / etc...)
            url = 'https://opensourcepyapi.herokuapp.com:443/news' # World News
            r = requests.get(url)
            data = r.json()
            y = json.loads(data)
            sleep(1)
            c = 1

            NEWS_Headlines = list(y['Title'].values())
            random_10_numbers = list(np.random.permutation(np.arange(0, len(NEWS_Headlines) - 1))[:10])
            random_10_news_headlines = [NEWS_Headlines[i] for i in random_10_numbers]

            self.__va._speak('TOP 10 Headlines Today...')
            for news in random_10_news_headlines:
                print(f'Number {c}: {news}')
                self.__va._speak(f'Number {c}')
                self.__va._speak(news)
                c += 1
                Beep(1047, 300)
                sleep(1)
            self.__va._speak('Thank You!')

        '''def read_out_news(self, query): # query: NEWS Category (region / topic / etc...) NOTE: [NEW Function ;; Not working]
            url = 'http://newsapi.org/v2/top-headlines?country=in&apiKey=e1cbf7941ba44b37bcf9e51cf289b804' # INDIA NEWS

            data = dict()
            with urlopen(url) as response:
                source = response.read()
                data = json.loads(source)
            
            sleep(1)
            print(data['articles'][0].keys())

            NEWS = data['articles']
            NEWS_Source = NEWS[0]['source']['name']
            NEWS_Headlines = NEWS[0]['title']
            NEWS_Description = NEWS[0]['description']
            NEWS_Link = NEWS[0]['url']

            print(f'{NEWS_Source}\n{NEWS_Headlines}\n{NEWS_Description}\n{NEWS_Link}\n')

            random_10_numbers = list(np.random.permutation(np.arange(0, len(NEWS_Headlines) - 1))[:10])
            random_10_news = [NEWS[i] for i in random_10_numbers]

            self.__va._speak('TOP 10 Headlines Today...')
            for i in range(len(random_10_news)): ## ERROR (check data-structure)
                news_headlines = random_10_news[i]['title']
                print(f"Number {i+1}: {news_headlines}")
                self.__va._speak(f'Number {i+1}')
                self.__va._speak(news_headlines)
                Beep(1047, 300)
                sleep(1)
            self.__va._speak('Thank You!')'''

        def tell_joke(self):
            jokes = self.__va._Vocabulary.JOKES
            self.__va._speak(jokes['joke'])

            ## ---- another / again ---- ## {check before 'Abilities.__init__()'}

    def start_AI_engine(self): ### TODO: If valid query => calls respective functions in 'Abilities'; Else => calls 'Abilities.what_can_you_do()'
        self.__wish_me()
        self.__if_any_query_made = False
        self.__time_out_between_failed_queries = 1 # seconds
        self.__last_webpage_visited = '' # store the """webpage name from each""" queries_made
        self.__available_webpages = {
            'w' : 'wikipedia',
            'y' : 'youtube',
            'g' : 'google'}

        while True:
            self.__abilities = self.Abilities()
            query = self._take_command('Waiting for commands in main thread').lower()
            print(f'query: {query}')
            # Logic for executing tasks based on query
            ### if self._substr_in_list_of_strs('can do perform'.split(), query)[0]:
            '''
            NOTE: Make all the following 'if conditions' to come from '_Vocabulary'. So that they can be re-usable (if 'another' / 'again' asked)
            '''
            if 'what can you do' in query or 'how can you help' in query:
                self.__if_any_query_made = False
                self.__abilities.what_can_you_do(query)
            
            elif 'how can you' in query:
                self.__if_any_query_made = True
                self.__abilities.how_can_you(query)
            
            elif 'wikipedia' in query:
                self.__if_any_query_made = True
                self.__last_webpage_visited = self.__available_webpages['w']
                self.__abilities.wikipedia(query)

            elif 'open youtube' in query:
                self.__if_any_query_made = True
                self.__last_webpage_visited = self.__available_webpages['w']
                self.__abilities.youtube(query)

            elif 'open google' in query:
                self.__if_any_query_made = True
                self.__last_webpage_visited = self.__available_webpages['w']
                self.__abilities.google(query)
            
            elif 'play the song' in query or 'play it' in query or 'play this song' in query or 'hear' in query or 'listen' in query:
                self.__if_any_query_made = True
                if 'wiki' in self.__last_webpage_visited:
                    if not self.__abilities.play_song_from_last_search(website=self.__available_webpages['w']):
                        self.__if_any_query_made = False
                elif 'youtube' in self.__last_webpage_visited:
                    if not self.__abilities.play_song_from_last_search(website=self.__available_webpages['y']):
                        self.__if_any_query_made = False
                elif 'google' in self.__last_webpage_visited:
                    if not self.__abilities.play_song_from_last_search(website=self.__available_webpages['g']):
                        self.__if_any_query_made = False

            elif 'play ' in query:
                self.__if_any_query_made = True
                self.__abilities.play_song(query)

            elif 'open stackoverflow' in query:
                self.__if_any_query_made = True
                self.__abilities.stackoverflow(query)

            elif 'time' in query:
                self.__if_any_query_made = True
                self.__abilities.current_time(query)

            elif 'open vs code' in query: ## NOTE: don't use absolute path; instead search for its executable (.exe) file and then execute
                self.__if_any_query_made = True
                self.__abilities.open_app(query)

            elif 'bye' in query or 'quit' in query or 'stop' in query or 'exit' in query:
                self.__if_any_query_made = True
                self.__abilities.quit_VA(query)
                return False

            elif 'conversation' in query or 'talk' in query:
                self.__if_any_query_made = True
                self._speak('Sure Sir!')
                return(self.__abilities.conversation())

            elif query == 'none' and not self.__if_any_query_made: # Stop executing when not asked anything
                self.__abilities.what_can_you_do(query)
                sleep(self.__time_out_between_failed_queries)

            elif 'news' in query:
                self.__if_any_query_made = True
                self.__abilities.read_out_news(query)

            elif 'joke' in query:
                self.__if_any_query_made = True
                self.__abilities.tell_joke()

            elif 'another' in query or 'again' in query:
                pass
                #last_thing_asked = self.__get_last_thing_asked()
        return True
