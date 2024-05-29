import os, pyaudio, wave, time

from threading import Thread

# https://stackoverflow.com/questions/40704026/voice-recording-using-pyaudio

class Microphone:
  def __init__(self, main):
    self.main = main
    self.format = pyaudio.paInt16
    self.channels = 1
    self.rate = 44100
    self.chunk = 4096
    self.record_duration = 60 # seconds
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

  def get_audio_files(self, filename):
    base_name = filename.split('.h264')[0].split('/captured-media/')[1]
    base_path = os.getcwd()
    capture_path = base_path + "/captured-media/"
    files = os.listdir(capture_path)
    audio_files = []
    marker = 0
    markers = ''

    for file in files:
      if (base_name in file and 'wav' in file):
        audio_files.append(file)
        markers += "[" + str(marker) + ":0]"
        marker += 1

    audio_files.sort()

    return dict(
      files = audio_files,
      markers = markers
    )

  # https://superuser.com/a/587553/572931
  def join_audio_files(self, filename):
    '''
      ffmpeg -i input1.wav -i input2.wav -i input3.wav -i input4.wav \
      -filter_complex '[0:0][1:0][2:0][3:0]concat=n=4:v=0:a=1[out]' \
      -map '[out]' output.wav
    '''

    base_path = os.getcwd() + '/captured-media/'
    audio_files = self.get_audio_files(filename)
    cmd = 'ffmpeg'

    for audio_file in audio_files['files']:
      cmd += ' -i ' + base_path + audio_file

    cmd += " -filter_complex '" + audio_files['markers'] + "concat=n=" + str(len(audio_files['files'])) + ":v=0:a=1[out]'"
    cmd += " -map '[out]' " + filename + '.wav'
    os.system(cmd)

  def start_recording(self):
    self.recording = True
    self.record_frames = []

    self.stream = self.audio.open(format=self.format, channels=self.channels,
                rate=self.rate, input=True, input_device_index = self.device_id,
                frames_per_buffer=self.chunk)
    
    for i in range(0, int(self.rate / self.chunk * self.record_duration)):
      # https://stackoverflow.com/questions/10733903/pyaudio-input-overflowed
      data = self.stream.read(self.chunk, exception_on_overflow=False)
      self.record_frames.append(data)

      if (not self.main.mic.recording):
        break

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
      # combine audio chunks into 1 file
      self.join_audio_files(self.filename)

      # h264 to mp4
      cmd = 'ffmpeg -framerate 30 -i ' + self.filename
      cmd += ' -c copy ' + self.filename + '.mp4'
      os.system(cmd)

      # join wav and mp4 file
      # https://superuser.com/a/277667/572931
      cmd = 'ffmpeg -i ' + self.filename + '.mp4' + ' -i ' + self.filename + '.wav' + ' -c:v copy -c:a aac ' + self.filename  + '-wsound' + '.mp4'
      os.system(cmd)

      self.filename = ""
      self.chunk_id = 0
      self.main.display.draw_text("Recording saved")
      self.main.menu.recording_video = False
      self.main.camera.video_processing = False
      time.sleep(2)
      self.main.active_menu = "Home"
      self.main.display.start_menu()
