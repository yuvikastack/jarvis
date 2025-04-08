import speech_recognition as sr
import pyttsx3
from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values
import os
import subprocess
import requests
import keyboard
import asyncio
from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from bs4 import BeautifulSoup
from rich import print

# Initialize speech engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)  # Adjust speed


def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Load environment variables
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey", "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")
Username = os.getenv("Username", "yuvika")
Assistantname = os.getenv("Assistantname", "Jarvis")

# Initialize Groq client
client = Groq(api_key=GroqAPIKey) if GroqAPIKey else None
messages = []

# System instructions
System = f"""Hello, I am {Username}, You are a very accurate AI chatbot named {Assistantname}."""
SystemChatBot = [{"role": "system", "content": System}]

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that."
        except sr.RequestError:
            return "Speech recognition service unavailable."

def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    return f"Day: {current_date_time.strftime('%A')}, Date: {current_date_time.strftime('%d %B %Y')}, Time: {current_date_time.strftime('%H:%M:%S')}"

def AnswerModifier(Answer):
    return '\n'.join([line for line in Answer.split('\n') if line.strip()])

def Chatbot(Query):
    try:
        with open("Data/ChatLog.json", "r") as f:
            messages = load(f)
    except FileNotFoundError:
        messages = []
    
    messages.append({"role": "user", "content": Query})
    
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
        max_tokens=1024,
        temperature=0.7,
        top_p=1,
        stream=True,
    )
    
    Answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content
    Answer = Answer.replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})
    
    with open("Data/ChatLog.json", "w") as f:
        dump(messages, f, indent=4)
    
    return AnswerModifier(Answer)

def Automation(Query):
    Query = Query.lower()
    if "open" in Query:
        return OpenApp(Query.replace("open", "").strip())
    elif "close" in Query:
        return CloseApp(Query.replace("close", "").strip())
    elif "play" in Query:
        return PlayYoutube(Query.replace("play", "").strip())
    elif "content" in Query:
        return Content(Query.replace("content", "").strip())
    elif "google search" in Query:
        return GoogleSearch(Query.replace("google search", "").strip())
    else:
        return Chatbot(Query)

def GoogleSearch(Topic):
    search(Topic)
    return "Google search initiated."

def Content(Topic):
    file_path = f"Data/{Topic.lower().replace(' ', '_')}.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(Chatbot(f"Write an article on {Topic}"))
    subprocess.Popen(["notepad.exe", file_path])
    return "Content generated and opened."

def PlayYoutube(query):
    playonyt(query)
    return "Playing on YouTube."

def OpenApp(app):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return f"Opened {app}."
    except:
        webopen(f"https://www.google.com/search?q={app}")
        return f"Couldn't find {app}, searching online."

def CloseApp(app):
    if "chrome" in app:
        return "Cannot close Chrome."
    try:
        close(app, match_closest=True, output=True, throw_error=True)
        return f"Closed {app}."
    except:
        return f"Couldn't close {app}."

if __name__ == "__main__":
    while True:
        print("Speak your command...")
        user_input = listen()
        print(f"You said: {user_input}")
        response = Automation(user_input)
        print(f"{Assistantname}: {response}")
        speak(response)