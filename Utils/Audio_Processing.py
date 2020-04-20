import numpy as np, wave, struct, platform

if platform.system() == 'Linux':
    from Note_Tone import Note_Tone
else:
    from Utils.Note_Tone import Note_Tone


class Audio_Process():
	def __init__(self, audio_file):
		self.audio_file = audio_file
		############################## Initialize ##################################
		
		# Some Useful Variables
		self.window_size = 2205    # Size of window to be used for detecting silence
		self.beta = 1   # Silence detection parameter
		self.max_notes = 100    # Maximum number of notes in file, for efficiency
		self.sampling_freq = 44100	# Sampling frequency of audio signal
		self.threshold = 600

		self.Identified_Notes = []
		self.sound = self.sound_square = np.zeros(0)

		self.__tone = Note_Tone()
		self.array = [self.__tone.notes(i) for i in range(2, 9)]
		self.notes = ['C2', 'Cs2', 'D2', 'Ds2', 'E2', 'F2', 'Fs2', 'G2', 'Gs2', 'A2', 'As2', 'B2',
					  'C3', 'Cs3', 'D3', 'Ds3', 'E3', 'F3', 'Fs3', 'G3', 'Gs3', 'A3', 'As3', 'B3',
					  'C4', 'Cs4', 'D4', 'Ds4', 'E4', 'F4', 'Fs4', 'G4', 'Gs4', 'A4', 'As4', 'B4',
					  'C5', 'Cs5', 'D5', 'Ds5', 'E5', 'F5', 'Fs5', 'G5', 'Gs5', 'A5', 'As5', 'B5',
					  'C6', 'Cs6', 'D6', 'Ds6', 'E6', 'F6', 'Fs6', 'G6', 'Gs6', 'A6', 'As6', 'B6',
					  'C7', 'Cs7', 'D7', 'Ds7', 'E7', 'F7', 'Fs7', 'G7', 'Gs7', 'A7', 'As7', 'B7',
					  'C8', 'Cs8', 'D8', 'Ds8', 'E8', 'F8', 'Fs8', 'G8', 'Gs8', 'A8', 'As8', 'B8']

	def __find_nearest_frequency(self, lst, freq): # This function is throwing error; but re-written works
		#lst = np.asarray(lst)
		idx = (np.abs(lst-freq)).argmin()
		#print(idx)
		return lst[idx]
	
	def __read_audio_file(self, audio_file):
		print ('\nReading Audio File...')

		sound_file = wave.open(audio_file, 'r')
		file_length = sound_file.getnframes()

		sound = np.zeros(file_length)
		self.sound_square = np.zeros(file_length)
		for i in range(file_length):
			data = sound_file.readframes(1)
			data = struct.unpack("<h", data)
			sound[i] = int(data[0])
			
		self.sound = np.divide(sound, float(2**15))	# Normalize data in range -1 to 1
	
	def detect_notes_from_audio(self):
		self.__read_audio_file(self.audio_file)

		######################### DETECTING SCILENCE ##################################

		sound_square = np.square(self.sound)
		frequency = []
		dft = []
		i = 0
		j = 0
		k = 0    
		# traversing sound_square array with a fixed window_size
		while(i<=len(sound_square)-self.window_size):
			s = 0.0
			j = 0
			while(j<=self.window_size):
				s = s + sound_square[i+j]
				j = j + 1	
			# detecting the silence waves
			if s < self.threshold:
				if(i-k>self.window_size*4):
					dft = np.array(dft) # applying fourier transform function
					dft = np.fft.fft(self.sound[k:i])
					dft=np.argsort(dft)

					if(dft[0]>dft[-1] and dft[1]>dft[-1]):
						i_max = dft[-1]
					elif(dft[1]>dft[0] and dft[-1]>dft[0]):
						i_max = dft[0]
					else :	
						i_max = dft[1]
					# claculating frequency				
					frequency.append((i_max*self.sampling_freq)/(i-k))
					dft = []
					k = i+1
			i = i + self.window_size

		#print('length',len(frequency))
		#print("frequency")

		for i in frequency :
			#print(i)
			#idx = self.__find_nearest_frequency(self.array, i)
			idx = (np.abs(self.array-i)).argmin()
			#print(idx)
			self.Identified_Notes.append(self.notes[idx])
		return self.Identified_Notes
