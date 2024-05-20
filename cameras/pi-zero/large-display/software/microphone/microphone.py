import os, pyaudio, wave

from threading import Thread

# https://stackoverflow.com/questions/40704026/voice-recording-using-pyaudio

class Microphone:
  def __init__(self, main):
    self.main = main
    self.format = pyaudio.paInt16
    self.channels = 1
    self.rate = 44100
    self.chunk = 4096
    self.record_duration = 10 # seconds
    self.device_id = 0
    self.audio = pyaudio.PyAudio()
    self.recorded_audio = [] # keep track of audio chunks
    self.recording = False
    self.filename = ""
    self.chunk_id = 0 # increment as you record new chunks
    self.stream = None
    self.record_frames = []
    self.set_device_id()
  
  def set_device_id(self):
    p = pyaudio.PyAudio()

    for i in range(p.get_device_count()):
      # nasty terminal dump
      # 'Lavalier' is my custom USB mic, have to verify your device's name
      if ('Lavalier' in p.get_device_info_by_index(i).get('name')):
        self.device_id = i

  def record(self, filename):
    self.filename = filename
    Thread(target=self.start_recording).start()

  def start_recording(self):
    self.recording = True

    self.stream = self.audio.open(format=self.format, channels=self.channels,
                rate=self.rate, input=True, input_device_index = self.device_id,
                frames_per_buffer=self.chunk)

    self.record_frames = []
    
    for i in range(0, int(self.rate / self.chunk * self.record_duration)):
        # https://stackoverflow.com/questions/10733903/pyaudio-input-overflowed
        data = self.stream.read(self.chunk, exception_on_overflow=False)
        self.record_frames.append(data)

    self.stop_recording()

  def stop_recording(self):
    self.stream.stop_stream()
    self.stream.close()
    
    if (not self.recording):
      self.audio.terminate()
    
    waveFile = wave.open(self.filename + '-' + str(self.chunk_id) + '.wav', 'wb')
    waveFile.setnchannels(self.channels)
    waveFile.setsampwidth(self.audio.get_sample_size(self.format))
    waveFile.setframerate(self.rate)
    waveFile.writeframes(b''.join(self.record_frames))
    waveFile.close()

    if (self.recording):
      self.chunk_id += 1
      self.start_recording()
    else:
      cmd = 'ffmpeg -framerate 30 -i ' + self.filename
      cmd += ' -c copy ' + self.filename + '.mp4'
      os.system(cmd)
      self.filename = ""
