import pyaudio
import wave
import time
from pynput import keyboard
import os

say = False # <- Set this to "True" and press Ctrl+S if you want to know wether the song is playing or stopped in the command prompt!

directory_path = "C:\Anwesh\Python-Projects\songs" # <- Put your song file path by clicking the folder and doing Ctrl+Shift+c 
paused = False                                     # or right clicking the folder and click "Copy Path"
show_input = False
def on_press(key):
    global paused
    if key == keyboard.Key.space:
        if stream.is_stopped():     
            stream.start_stream()
            paused = False
            if say == True:
                print("Playing")
            return False
        elif stream.is_active():   
            stream.stop_stream()
            paused = True
            if say == True:
                print("Stopped")
            return False
    return False


file_num = 0
choice = input("Do you want to type in the song name (n) or browse the files (b)? ")

print(" ")

if choice.upper()=='N':
    song_name = input("Whats the song name?: ")
    print(f"Playing: {song_name.upper()}.wav")
    wf = wave.open(f"{directory_path}/{song_name.upper()}.wav" , 'rb')
elif choice.upper()=='B':
    song_root_list = []
    song_list = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_num  += 1
            file_path = os.path.join(root, file)
            print(f"{file_num}){file}")
            song_root_list.append(file_path)
            song_list.append(file)
    print(" ")
    song_num = int(input("Choose the song number from the list: "))
    if len(song_list) < song_num:
        print("Song number isnt there in the list!")
        exit()
    song_path = song_root_list[song_num-1]
    print(f"Playing: {song_list[song_num-1]}")
    wf = wave.open(song_path)

p = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)

stream.start_stream()

while stream.is_active() or paused==True:
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    time.sleep(0.1)


stream.stop_stream()
stream.close()
wf.close()
     
p.terminate()
exit()
