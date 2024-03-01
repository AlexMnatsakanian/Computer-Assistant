import speech_recognition as sr
import pyttsx3
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
from os import system
import psutil
import requests
import json
import geocoder
import dadjokes

# Define global variables
__version__ = 1
NAME = 'simon'  # Name of the assistant
MASTER = 'Alex'  # Name of the user

ctypes.windll.kernel32.SetConsoleTitleW(f'SIMON.exe')
toast = ToastNotifier()
toast.show_toast("SIMON.EXE", "S.I.M.O.N Is [Online]", duration=10, icon_path="SIMON.ico" ,threaded=True)
listener = sr.Recognizer()
listener2 = sr.Recognizer()
CONVERSATION_LOG = "Conversation Log.txt"
g = geocoder.ip('me')
scrnid = date.today().strftime("%b-%d-%Y") +"-"+datetime.datetime.now().strftime('%I-%M-%p')
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def sendwhatmsg(phone_no, message):
    valid_phone_no = re.compile(r"[+]\d{12}")
    numbers = re.findall(valid_phone_no, phone_no)
    time.sleep(2)
    parsedMessage = quote(message)
    web.open('https://web.whatsapp.com/send?phone='+phone_no+'&text='+parsedMessage)
    time.sleep(2)
    width,height = pg.size()
    pg.click(width/2,height/2)
    time.sleep(5)
    pg.press('enter')

def talk(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)

    if hour>=0 and hour <12:
        talk("good morning" + MASTER)

    elif hour>=12 and hour<18:
        talk("good afternoon" + MASTER)

    else:
        talk("good Evening" + MASTER)

    talk("How may I help you?")


def start_conversation_log(self):
    today = str(date.today())
    today = today
    with open(CONVERSATION_LOG, "a") as f:
        f.write("Conversation started on: " + today + "\n")

# Writes each command from the user to the conversation log
def remember(self, command):
    with open(CONVERSATION_LOG, "a") as f:
        f.write("User: " + command + "\n")

def speak_news():
    url = 'http://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=ENTERHERE'
    news = requests.get(url).text
    news_dict = json.loads(news)
    arts = news_dict['articles']
    talk('Todays Headlines are..')
    for index, articles in enumerate(arts):
        talk(articles['title'])
        index = index + 1
        if not index % 3:
            talk('would you like me to continue?')
            with sr.Microphone() as source:
                voice = listener.record(source, duration=4)
                command = listener.recognize_google(voice)
                command = command.lower()
                if 'yes' in command:
                    pass
                if 'no' in command:
                    break
        if index == len(arts)-1:
            break
        talk('Moving on the next news headline..')
    talk('These were the top headlines, Have a nice day Sir!!..')

def weather():
    api_url = "https://fcc-weather-api.glitch.me/api/current?lat=" + \
        str(g.latlng[0]) + "&lon=" + str(g.latlng[1])
    data = requests.get(api_url)
    data_json = data.json()
    if data_json['cod'] == 200:
        main = data_json['main']
        wind = data_json['wind']
        weather_desc = data_json['weather'][0]
        talk('weather is ' + weather_desc['main'])
        talk('Wind speed is ' + str(wind['speed']) + ' metre per second')
        talk('Temperature: ' + str(main['temp']) + 'degree celcius')
        talk('Humidity is ' + str(main['humidity']))

def run():
    try:
        with sr.Microphone() as source:
            print('[-] listening...')
            listener.energy_threshold = 4000
            listener.dynamic_energy_threshold = True
            listener.pause_threshold = 0.7
            voice = listener.listen(source, timeout=5)
            print('[-] Done listening...')
            command = listener.recognize_google(voice)
            command = command.lower()
            print('[-] Done recognizing...')
            if NAME in command:
                command = command.replace('simon', '')
                if 'play' in command:
                    song = command.replace('play', '')
                    pywhatkit.playonyt(song)
                    talk('playing ' + song)
                    print('playing' + song)
                elif 'search' in command:
                    arg = command.replace('search', '')
                    pywhatkit.search(arg)
                    talk('here is what i found')
                elif 'remember this' in command:
                    talk("what should i remember sir")
                    voice = listener.record(source, duration=5)
                    rememberMessage = listener.recognize_google(voice)
                    rememberMessage = rememberMessage.lower()
                    talk("you asked me to remember"+ rememberMessage)
                    remember = open('data.txt', 'w')
                    remember.write(rememberMessage)
                    remember.close()
                elif 'do you remember anything' in command:
                    remember = open('data.txt', 'r')
                    talk("you asked me to remember that" + remember.read())
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
                    web.open('https://classroom.google.com/u/2/h')
                    talk('ok')
                elif 'open history zoom' in command:
                    web.open('https://zoom.us/j/99086251499?pwd=Q0FhYldtU3JHN0pyYzZZQnJPSmczdz09')
                    talk('ok')
                elif 'open youtube' in command:
                    web.open('https://www.youtube.com/?gl=US&tab=r1')
                    talk('ok')
                elif 'open cw' in command:
                    web.open('https://www.cwtv.com/')
                    talk('ok')
                elif 'open method school' in command:
                    web.open('https://methodschools.net/student/courses.php?id=259')
                    talk('ok')
                elif 'open warzone' in command:
                    os.startfile('C:\Program Files\Call of Duty Modern Warfare\Modern Warfare Launcher.exe')
                    talk('ok')
                elif 'open whatsapp' in command:
                    os.startfile(r'C:\Users\alexm\AppData\Local\WhatsApp\WhatsApp.exe')
                    talk('ok')
                elif 'open spotify' in command:
                    try:
                        os.startfile(r'C:\Users\alexm\AppData\Roaming\Spotify\Spotify.exe')
                        talk('ok')
                    except:
                        talk("could not find spotify in computer data")
                        pass
                elif 'screenshot' in command:
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
                elif 'voice' in command:
                     if 'female' in command:
                         engine.setProperty('voice', voices[1].id)
                         talk("Hello Sir, I have switched my voice. How is it?")
                     else:
                         engine.setProperty('voice', voices[0].id)
                         talk("Hello Sir, I have switched my voice. How is it?")
                elif 'cpu' in command:
                    usage = str(psutil.cpu_percent())
                    talk("CPU is at"+usage)
                    battery = psutil.sensors_battery()
                    talk("battery is at")
                    talk(battery.percent)
                elif "hello" in command:
                    talk("Hello! I am simon. How can I help you?")
                elif "who are you" in command:
                    talk("I am a simulated intelligence managment operation network, I was developed by my Genius master Alexander Mnatsakanian")
                elif "news" in command:
                    speak_news()
                elif 'type what i say' in command:
                    talk("what should i type?")
                    print('[-] listening...')
                    voice = listener.listen(source, timeout=3)
                    print('[-] Done listening...')
                    command = listener.recognize_google(voice)
                    command = command.lower()
                    print('[-] Done recognizing...')
=
                    print(command)
                    keyboard.write(command)
                    keyboard.press_and_release('enter')
                elif 'volume' in command:
                    command = command.replace('volume', '')
                    if '1' in command:
                        engine.setProperty('volume',0.1)
                        if '0' in command:
                            engine.setProperty('volume',1.0)
                        talk('ok')
                    elif '2' in command:
                        engine.setProperty('volume',0.2)
                        talk('ok')
                    elif '3' in command:
                        engine.setProperty('volume',0.3)
                        talk('ok')
                    elif '4' in command:
                        engine.setProperty('volume',0.4)
                        talk('ok')
                    elif '5' in command:
                        engine.setProperty('volume',0.5)
                        talk('ok')
                    elif '6' in command:
                        engine.setProperty('volume',0.6)
                        talk('ok')
                    elif '7' in command:
                        engine.setProperty('volume',0.7)
                        talk('ok')
                    elif '8' in command:
                        engine.setProperty('volume',0.8)
                        talk('ok')
                    elif '9' in command:
                        engine.setProperty('volume',0.9)
                        talk('ok')
                    elif 'what' in command:
                        volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
                        talk(volume)
                        print(volume)
                elif 'flip a coin' in command:
                    H_or_t = 'heads', 'tails'
                    Hort = random.choice(H_or_t)
                    talk(Hort)
                    print(Hort)
                elif 'goodbye for now' in command:
                        toast.show_toast("SIMON.EXE", "S.I.M.O.N Is [Offline]", duration=2, icon_path="SIMON.ico", threaded=True)
                        print("Simon is shutting down")
                        talk("goodbye" + MASTER)
                        time.sleep(1)
                elif 'shut down my pc' in command:
                    os.system("shutdown /s /t 1")
                else:
                    talk('Please say the command again.')
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

wishMe()
while True:
    run()
