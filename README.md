# S.I.M.O.N (Speech Intelligent Management Operation Network)

Welcome to S.I.M.O.N, a virtual assistant program written in Python. S.I.M.O.N stands for Speech Intelligent Management Operation Network. This program utilizes various libraries and APIs to perform tasks such as speech recognition, web searches, retrieving news, controlling system functions, and more.

## Features

- **Speech Recognition:** S.I.M.O.N can understand spoken commands using the `speech_recognition` library.
- **Web Interaction:** It can perform web searches, open websites, and retrieve information from Wikipedia using `pywhatkit` and `wikipedia` libraries.
- **Text to Speech:** Utilizes ElevenLabs API for text-to-speech functionality to interact with the user.
- **System Control:** Can control system functions such as changing volume, shutting down or putting the PC to sleep.
- **Weather Information:** Retrieves current weather information based on the user's location using the `geocoder` library.
- **News Aggregation:** Provides top headlines using the News API.
- **Random Features:** Can flip a coin, tell jokes, and more.

## Usage

1. Ensure you have all the required libraries installed. You can install them using pip:

```bash
pip install -r requirements.txt
```

2. Run the program:

```bash
python simon.py
```

3. Once the program is running, you can interact with S.I.M.O.N using voice commands.

## Requirements

- Python 3.x
- Libraries: `speech_recognition`, `pywhatkit`, `datetime`, `wikipedia`, `pyjokes`, `os`, `time`, `keyboard`, `re`, `webbrowser`, `pyautogui`, `random`, `win10toast`, `ctypes`, `pycaw`, `psutil`, `requests`, `json`, `geocoder`, `dadjokes`, `elevenlabs`, `playsound`

## Tips

- This Python program uses ElevenLabs API. Because the amount of requests is limited, I have created some sound files that are common phrases used by S.I.M.O.N.
- If you want to repeat this process, you may replace the **playsound()** function with **talk()**.
- You could add the common phrases by passing a phrase as a string into the **talk()** function.
- You can then download the files from the Eleven Labs website which saves all of the audio it generates.
- You may also create your phrases on the Eleven Labs website without changing any part of the program.

## Acknowledgements

- **ElevenLabs API:** Used for text-to-speech functionality.
- **News API:** Provides news headlines for the user.
- **Geocoder API:** Retrieves location-based information such as weather.
- **Pywhatkit:** For performing web searches and playing YouTube videos.
- **Wikipedia API:** Retrieves information from Wikipedia.
- **Pyjokes:** Provides a collection of jokes for entertainment.

## Author

This program was developed by Alex Mnatsakanian for personal or educational purposes. Feel free to contribute or modify the code according to your requirements.

Enjoy using S.I.M.O.N! If you have any feedback or suggestions, feel free to contact me.
