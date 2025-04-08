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

# Load environment variables
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey", "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")
Username = os.getenv("Username", "Yuvika")
Assistantname = os.getenv("Assistantname", "Jarvis")

# Initialize Groq client
client = Groq(api_key=GroqAPIKey) if GroqAPIKey else None
messages = []

# System instructions
System = f"""Hello, I am {Username}, You are a very accurate AI chatbot named {Assistantname}."""
SystemChatBot = [{"role": "system", "content": System}]

# Function to get real-time information
def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    return f"Day: {current_date_time.strftime('%A')}, Date: {current_date_time.strftime('%d %B %Y')}, Time: {current_date_time.strftime('%H:%M:%S')}"

# Function to modify chatbot response
def AnswerModifier(Answer):
    return '\n'.join([line for line in Answer.split('\n') if line.strip()])

# Chatbot function
def Chatbot(Query):
    try:
        with open("Data/ChatLog.json", "r") as f:
            messages = load(f)
    except FileNotFoundError:
        messages = []
    
    messages.append({"role": "user", "content": Query})
    
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
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

# Function to determine whether to execute an action or respond as chatbot
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

# Function to perform a Google search
def GoogleSearch(Topic):
    search(Topic)
    return "Google search initiated."

# Function to generate and save content
def Content(Topic):
    file_path = f"Data/{Topic.lower().replace(' ', '_')}.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(Chatbot(f"Write an article on {Topic}"))
    subprocess.Popen(["notepad.exe", file_path])
    return "Content generated and opened."

# Function to play YouTube videos
def PlayYoutube(query):
    playonyt(query)
    return "Playing on YouTube."

# Function to open applications or websites
def OpenApp(app):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return f"Opened {app}."
    except:
        webopen(f"https://www.google.com/search?q={app}")
        return f"Couldn't find {app}, searching online."

# Function to close applications
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
        user_input = input("Enter the question or command: ")
        print(Automation(user_input))
