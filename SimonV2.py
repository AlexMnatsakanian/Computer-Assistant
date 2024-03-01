import speech_recognition as sr
#import pyttsx3
import pywhatkit
import datetime
from datetime import date
import wikipedia
import pyjokes
import os
import time
import keyboard
import re
from urllib.parse import quote
import webbrowser as web
import pyautogui as pg
import random
from win10toast import ToastNotifier
import ctypes
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from os import system
import psutil
import requests
import json
import geocoder
import dadjokes
from elevenlabs import generate, play, set_api_key
from elevenlabs.api import History
from playsound import playsound

# Define global variables
__version__ = 2
NAME = 'simon'  # Name of the assistant
MASTER = 'Alex'  # Name of the user

# API key for ElevenLabs text to speech AI
set_api_key("API key for ELEVENLABS")
# history = History.from_api()
# for item in history:
#     print(item)

# *****Uncomment only if you do not run the program as a task on startup*****
#ctypes.windll.kernel32.SetConsoleTitleW(f'SIMON.exe')

# Show a notification when the assistant is online
ToastNotifier().show_toast("SIMON.EXE", "S.I.M.O.N Is [Online]", duration=10, icon_path="SIMON.ico" ,threaded=True)

CONVERSATION_LOG = "Conversation Log.txt"
g = geocoder.ip('me')

# engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id)

print(g)


# Common sentences for text to speech (to save data)
greetings = ['greeting1.mp3','greeting2.mp3']
goodbye_message = 'GoodbyeAlex.mp3'
invalid_volume = 'InvalidVolume.mp3'
hello = 'HelloIAmSimon.mp3'
good_morning = ['GoodMorningAlex1.mp3','GoodMorningAlex2.mp3','GoodMorningAlex3.mp3']
good_afternoon = ['GoodAfternoonAlex1.mp3']
good_evening = ['GoodEveningAlex1.mp3','GoodEveningAlex2.mp3','GoodEveningAlex3.mp3']
say_command_again = ['SayCommandAgain1.mp3','SayCommandAgain2.mp3']

# Text to speech function using ElevenLabs API
def talk(text):
    audio = generate(
      text=text,
      voice="James",
      model="eleven_multilingual_v1"
    )

    play(audio)
    #engine.say(text)
    #engine.runAndWait()

# Function to greet the user
def greet_me():
    hour = int(datetime.datetime.now().hour)

    if hour>=0 and hour <12:
        #talk("Good morning " + MASTER)
        playsound(random.choice(good_morning))
    elif hour>=12 and hour<18:
        #talk("Good afternoon " + MASTER)
        playsound(random.choice(good_afternoon))
    else:
        #talk("Good evening " + MASTER)
        playsound(random.choice(good_evening))

    #talk("How may I help you?")
    playsound(random.choice(greetings))


def start_conversation_log(self):
    today = str(date.today())
    today = today
    with open(CONVERSATION_LOG, "a") as f:
        f.write("Conversation started on: " + today + "\n")

def remember(self, command):
    with open(CONVERSATION_LOG, "a") as f:
        f.write("User: " + command + "\n")

# Function to proccess news using news api
def news():
    url = 'http://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=ENTERKEYHERE'
    news = requests.get(url).text
    news_dict = json.loads(news)
    arts = news_dict['articles']
    talk('Todays Headlines are..')
    for index, articles in enumerate(arts):
        talk(articles['title'])
        index = index + 1
        if not index % 3:
            talk('would you like me to continue?')
            command = get_audio()
            if 'yes' in command:
                pass
            if 'no' in command:
                break
        if index == len(arts)-1:
            break
        talk('Moving on the next news headline..')
    talk('These were the top headlines, Have a nice day Sir!!..')

# Function to proccess weather using weather api 
def weather():
    api_url = "https://fcc-weather-api.glitch.me/api/current?lat=" + \
        str(g.latlng[0]) + "&lon=" + str(g.latlng[1])
    data = requests.get(api_url)
    data_json = data.json()
    if data_json['cod'] == 200:
        main = data_json['main']
        wind = data_json['wind']
        weather_desc = data_json['weather'][0]
        talk('The weather consists of ' + weather_desc['main'] + ', the wind speed is ' + str(wind['speed']) + ' meters per second, the temperature is ' + str(main['temp']) + ' degrees celcius, and the humidity is ' + str(main['humidity']))

# Function to change Windows volume
def set_volume(volume_level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    # Set volume level (0.0 to 1.0)
    volume.SetMasterVolumeLevelScalar(volume_level, None)
    
# Function to get Windows volume
def get_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    # Get volume level (0.0 to 1.0)
    current_volume = volume.GetMasterVolumeLevelScalar()
    return current_volume

# Function to recieve default microphone input and convert to text using the default Google API
def get_audio():
    command = ''
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print('[-] listening...')
        listener.energy_threshold = 4000
        listener.dynamic_energy_threshold = True
        listener.pause_threshold = 0.7
        voice = listener.listen(source, timeout=5)
        print('[-] Done listening...')
        command = listener.recognize_google(voice)
        print('[-] Done recognizing...')
        print(command)
        # try:
        #     command = listener.recognize_google(voice)
        #     print('[-] Done recognizing...')
        #     print(command)
        # except Exception as e:
        #     print("Exception: " + str(e))
    return command.lower()

def get_audio_upper():
    command = ''
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print('[-] listening...')
        listener.energy_threshold = 4000
        listener.dynamic_energy_threshold = True
        listener.pause_threshold = 0.7
        voice = listener.listen(source, timeout=5)
        print('[-] Done listening...')
        try:
            command = listener.recognize_google(voice)
            print('[-] Done recognizing...')
            print(command)
        except Exception as e:
            print("Exception: " + str(e))

    return command.lower()

def run():
    try:
        command = get_audio()
        print(command)
        if NAME in command:
            command = command.replace('simon', '')

            if 'play' in command:
                song = command.replace('play', '')
                pywhatkit.playonyt(song)
                talk('playing ' + song)
                print('playing' + song)

            elif 'search for' in command:
                arg = command.replace('search', '')
                pywhatkit.search(arg)
                talk('here is what i found')

            elif 'remember this' in command:
                talk("what should i remember sir")
                rememberMessage = get_audio()
                talk("you asked me to remember"+ rememberMessage)
                remember = open('data.txt', 'w')
                remember.write(rememberMessage)
                remember.close()

            elif 'do you remember anything' in command:
                try:
                    remember = open('data.txt', 'r')
                    talk("you asked me to remember that" + remember.read())
                except:
                    talk("You havent asked me to remmember anything " + MASTER + ".")

            elif 'time' in command:
                jam = datetime.datetime.now().strftime('%I:%M %p')
                talk('Current time is ' + jam)

            elif "what is the weather" in command:
                weather()

            elif 'who is' in command:
                if "your master" in command:
                    talk('My master is Alexander Mnatsakanian, the smartest human in the universe!')
                try:
                    person = command.replace('who is', '')
                    info = wikipedia.summary(person, 2)
                    print(info)
                    talk(info)
                except wikipedia.exceptions.PageError as e:
                    print('Error: ' + str(e))
                    talk('I didnt find anything about' + person)

            elif 'how are you' in command:
                talk('Good')

            elif 'close' in command:
                if 'whatsapp' in command:
                    system('taskkill /F /FI "WINDOWTITLE eq WhatsApp" ')
                    talk('ok')
                if 'spotify' in command:
                    system('taskkill /F /FI "WINDOWTITLE eq Spotify Premium" ')
                    talk('ok')

            elif 'open google classroom' in command:
                web.open('https://classroom.google.com')
                talk('ok')

            elif 'open history zoom' in command:
                web.open('https://zoom.us/j/')
                talk('ok')

            elif 'open youtube' in command:
                web.open('https://www.youtube.com')
                talk('ok')
                
            elif 'open spotify' in command:
                try:
                    os.startfile(r'"C:\Program Files\Google\Chrome\Application\chrome_proxy.exe"')
                    talk('ok')
                except:
                    talk("could not find spotify in computer data")
                    pass

            elif 'screenshot' in command:
                scrnid = date.today().strftime("%b-%d-%Y") +"-"+datetime.datetime.now().strftime('%I-%M-%p')
                img = pg.screenshot()
                object = r'C:\Users\alexm\Pictures/'+scrnid+'.png'
                img.save(object)
                talk('ok')

            elif 'joke' in command:
                if 'python' in command:
                    talk(pyjokes.get_joke())
                if 'dad' in command:
                    print(dadjokes.joke("jokes.txt"))
                    talk(dadjokes.joke("jokes.txt"))

            elif 'cpu' in command:
                usage = str(psutil.cpu_percent())
                talk("CPU is at "+usage)
                battery = psutil.sensors_battery()
                talk("battery is at ")
                talk(battery.percent)

            elif "hello" in command:
                talk("Helloooooo! I am Simon.")
                playsound(greetings)

            elif "who are you" in command:
                #talk("I am a simulated intelligence managment operation network, I was developed by my Genius master Alexander Mnatsakanian")
                playsound('whoami.mp3')

            elif "news" in command:
                news()

            elif 'type what i say' in command:
                talk("what should i type?")
                command = get_audio_upper()
                print(command)
                keyboard.write(command)
                keyboard.press_and_release('enter')

            elif 'volume' in command:
                # Define volume levels corresponding to spoken numbers
                volume_levels = {
                    'one': 0.1, 'two': 0.2, 'three': 0.3,
                    'four': 0.4, 'five': 0.5, 'six': 0.6,
                    'seven': 0.7, 'eight': 0.8, 'nine': 0.9,
                    '10': 1.0,'mute': 0.0
                }
                
                # Extract the volume number from the command
                spoken_number = re.findall(r'\b(one|two|three|four|five|six|seven|eight|nine|10|mute)\b', command)
                
                if spoken_number:
                    # Set volume based on spoken number
                    volume_level = volume_levels.get(spoken_number[0])
                    set_volume(volume_level)
                    talk('Volume set to ' + str(volume_level * 100) + '%')
                elif 'what' in command:
                    # Get current volume level
                    current_volume = get_volume()
                    if current_volume is not None:
                        talk('Current volume level is ' + str(current_volume) + '.')
                    else:
                        talk('Failed to retrieve the current volume level.')
                else:
                    playsound(invalid_volume)

            elif 'flip a coin' in command:
                H_or_t = 'heads', 'tails'
                Hort = random.choice(H_or_t)
                talk(Hort)
                print(Hort)

            elif 'goodbye for now' in command:
                    ToastNotifier().show_toast("SIMON.EXE", "S.I.M.O.N Is [Offline]", duration=2, icon_path="SIMON.ico", threaded=True)
                    print("Simon is shutting down")
                    #talk("goodbye" + MASTER)
                    playsound(goodbye_message)
                    time.sleep(3)
                    quit()

            elif 'shut down my pc' in command:
                os.system("shutdown /s /t 1")

            elif ('put my pc to sleep' or 'good night') in command:
                os.system("sleep /s /t 1")

            else:
                #talk('Please say the command again.')
                playsound(random.choice(say_command_again))

        elif NAME not in command:
            pass

        else:
            pass

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        pass

    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        pass

    except sr.WaitTimeoutError:
        pass

greet_me()

while True:
    run()


