from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os

# Load the environment variables from the .env file.
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey", "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")

# Define CSS classes for parsing specific elements in HTML content:
classes = ["zCubwf", "hgKElc", "LIKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee",
           "tw-Data-text-small tw-ta", "Iz6rdc", "O5uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table__webanswer-table", 
           "dDoNo ikb4Bb gsrt", "sXLaOe", "LWKfKe", "VQF4g", "qv3Wpe", "Kno-rdesc", "SPZz6b"]

# Define User-Agent for making web requests.
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4986.75 Safari/537.36'

# Initialize the Groq client with the API key.
if GroqAPIKey:
    client = Groq(api_key=GroqAPIKey)
else:
    client = None
    print("[red]Error: Groq API Key is missing![/red]")

# Predefined professional response for user interactions.
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I am at your service for any additional questions or support you may need—don't hesitate to ask.",
]

# List to store chatbot messages.
messages = []

# System message to provide context to the chatbot.
SystemChatBot = [{"role": "system", "content": "Hello, I am a content writer. You have to write content letters."}]

# Function to perform a Google search.
def GoogleSearch(Topic):
    search(Topic)
    return True

#GoogleSearch('ritesh sarathe')
# Function to generate content using AI and save it to a file.
def Content(Topic):
    if not client:
        print("[red]Error: Groq client not initialized.[/red]")
        return False
    
    def OpenNotepad(file):
        default_text_editor = "notepad.exe"
        if os.path.exists(file):
            subprocess.Popen([default_text_editor, file])
        else:
            print(f"[red]Error: File {file} not found.[/red]")
    
    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": prompt})
        completion = client.chat.completions.create(
            model='mixtral-8x7b-32768',
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )
        Answer = ""
        for chunk in completion:
            if chunk.choices and chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer
    
    Topic = Topic.replace("Content", "").strip()
    ContentBYAI = ContentWriterAI(Topic)
    os.makedirs("Data", exist_ok=True)
    file_path = rf"Data\{Topic.lower().replace(' ', '_')}.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(ContentBYAI)
    OpenNotepad(file_path)
    return True
#Content("application to manager in office ")

# Function to play a video on YouTube.
def PlayYoutube(query):
    playonyt(query)
    return True
#PlayYoutube("kyun faya kyu")

# Function to open an application or a relevant webpage.
def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        url = f"https://www.google.com/search?q={app}"
        headers = {"User-Agent": useragent}
        response = sess.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', {'jsname': 'UWckNb'})
            if links:
                webopen(links[0].get('href'))
        return True
#OpenApp('Word')

# Function to close an application.
def CloseApp(app):
    if "chrome" in app:
        return False
    try:
        close(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        return False

# Function to execute system-level commands.
def System(command):
    actions = {
        "mute": lambda: keyboard.press_and_release("volume mute"),
        "unmute": lambda: keyboard.press_and_release("volume mute"),
        "volume up": lambda: keyboard.press_and_release("volume up"),
        "volume down": lambda: keyboard.press_and_release("volume down")
    }
    if command in actions:
        actions[command]()
    return True

# Function to translate and execute automation commands.
async def TranslateAndExecute(commands: list[str]):
    funcs = []
    for command in commands:
        if command.startswith("open"):
            fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
            funcs.append(fun)
        elif command.startswith("close"):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)
        elif command.startswith("play"):
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))
            funcs.append(fun)
        elif command.startswith("content"):
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)
        elif command.startswith("google search"):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
            funcs.append(fun)
        else:
            print(f"[yellow]No function found for: {command}[/yellow]")
    results = await asyncio.gather(*funcs)
    return results

# Function to execute automation tasks asynchronously.
async def Automation(commands: list[str]):
    await TranslateAndExecute(commands)
    return True
  