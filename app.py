from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import subprocess
import time
from ecapture import ecapture as ec
import wolframalpha
import json
import requests

app = Flask(__name__)

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        return "Hello, Good Morning"
    elif 12 <= hour < 18:
        return "Hello, Good Afternoon"
    else:
        return "Hello, Good Evening"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    command = data.get('command', '').lower()

    if "good bye" in command or "ok bye" in command or "stop" in command:
        response = 'Your personal assistant G-one is shutting down, Good bye'
        return jsonify({'response': response})

    if 'wikipedia' in command:
        speak('Searching Wikipedia...')
        command = command.replace("wikipedia", "")
        results = wikipedia.summary(command, sentences=3)
        speak("According to Wikipedia")
        return jsonify({'response': results})

    elif 'open youtube' in command:
        webbrowser.open_new_tab("https://www.youtube.com")
        response = "YouTube is open now"
        return jsonify({'response': response})

    elif 'open google' in command:
        webbrowser.open_new_tab("https://www.google.com")
        response = "Google Chrome is open now"
        return jsonify({'response': response})

    elif 'open gmail' in command:
        webbrowser.open_new_tab("https://mail.google.com")
        response = "Google Mail is open now"
        return jsonify({'response': response})

    elif "weather" in command:
        api_key = "c18d205f57f85b06715c98cba4386e5d"  # Replace with your OpenWeather API key
        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        city_name = command.split("in")[-1].strip()
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            weather_response = f"Temperature in Kelvin is {current_temperature}, humidity is {current_humidity}%, and the weather description is {weather_description}."
            return jsonify({'response': weather_response})
        else:
            return jsonify({'response': "City Not Found"})

    elif 'time' in command:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        response = f"The time is {strTime}"
        return jsonify({'response': response})

    elif 'who are you' in command or 'what can you do' in command:
        response = ('I am G-One version 1.0 your personal assistant. I can perform tasks like opening YouTube, Google Chrome, Gmail, '
                    'tell the time, take a photo, search Wikipedia, predict weather in different cities, and answer computational or geographical questions.')
        return jsonify({'response': response})

    elif "who made you" in command or "who created you" in command or "who discovered you" in command:
        response = "I was built by abirami"
        return jsonify({'response': response})

    elif "open stackoverflow" in command:
        webbrowser.open_new_tab("https://stackoverflow.com/login")
        response = "Here is StackOverflow"
        return jsonify({'response': response})

    elif 'news' in command:
        news = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
        response = 'Here are some headlines from the Times of India, Happy reading'
        return jsonify({'response': response})

    elif "camera" in command or "take a photo" in command:
        ec.capture(0, "robo camera", "img.jpg")
        response = "Photo taken"
        return jsonify({'response': response})

    elif 'search' in command:
        command = command.replace("search", "").strip()
        webbrowser.open_new_tab(f"https://www.google.com/search?q={command}")
        response = f"Searching {command} on Google"
        return jsonify({'response': response})

    elif 'ask' in command:
        app_id = "your_wolframalpha_app_id"  # Replace with your WolframAlpha App ID
        client = wolframalpha.Client(app_id)
        question = command.replace("ask", "").strip()
        res = client.query(question)
        answer = next(res.results).text
        return jsonify({'response': answer})

    elif "log off" in command or "sign out" in command:
        speak("Ok, your PC will log off in 10 sec. Make sure you exit from all applications.")
        subprocess.call(["shutdown", "/l"])
        response = "Logging off"
        return jsonify({'response': response})

    return jsonify({'response': "Sorry, I didn't understand that."})

if __name__ == '__main__':
    speak("Loading your AI personal assistant G-One")
    speak(wishMe())
    app.run(debug=True)
