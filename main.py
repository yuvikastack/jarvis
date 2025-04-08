from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Model import FirstLayerDMM
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.TextToSpeech import TextToSpeech
from Backend.Chatbot import Chatbot
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import json
import os



# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username", "User")
Assistantname = env_vars.get("Assistantname", "Jarvis")
DefaultMessage = f"{Username}: Hello {Assistantname}, How are you?\n{Assistantname}: Welcome {Username}. I am doing well. How may I help you?"

Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

def ReadChatLogJson():
    with open(r'Data/ChatLog.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def ChatLogIntegration(new_message):
    json_data = []
    
    # Create a new log entry
    log_entry = {
        "role": "user" if new_message.startswith(Username) else "assistant",
        "content": new_message.replace(f"{Username}: ", "").replace(f"{Assistantname}: ", "")
    }
    
    # Append only the new message to JSON
    json_data.append(log_entry)

    # Write the new message to ChatLog.json (overwrites previous content)
    with open(r'Data/ChatLog.json', 'w', encoding='utf-8') as file:
        json.dump(json_data, file, indent=4)

def MainExecution():
    print("Listening...")
    Query = SpeechRecognition()
    if not Query.strip():
        print("No valid input detected. Please try again")
        return
    print(f"{Username}: {Query}")
    ChatLogIntegration(f"{Username}: {Query}")  # Store user message
    
    print("Thinking...")
    Decision = FirstLayerDMM(Query)
    if not Decision:
        print(f"{Assistantname}: Sorry, I couldn't understand.")
        ChatLogIntegration(f"{Assistantname}: Sorry, I couldn't understand.")  # Store assistant response
        return
    print(f"Decision: {Decision}\n")

    G = any(i.startswith("general") for i in Decision)
    R = any(i.startswith("realtime") for i in Decision)
    Merged_query = " and ".join(
        [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
    )

    for queries in Decision:
        if any(queries.startswith(func) for func in Functions):
            run(Automation(list(Decision)))
            return

    if G and R or R:
        print("Searching...")
        Answer = RealtimeSearchEngine(Merged_query)
    else:
        for Queries in Decision:
            if "general" in Queries:
                QueryFinal = Queries.replace("general", "").strip()
                Answer = Chatbot(QueryFinal)
                break
            elif "realtime" in Queries:
                QueryFinal = Queries.replace("realtime", "").strip()
                Answer = RealtimeSearchEngine(QueryFinal)
                break
            elif "exit" in Queries:
                print(f"{Assistantname}: Okay, Bye!")
                ChatLogIntegration(f"{Assistantname}: Okay, Bye!")
                os._exit(1)

    print(f"{Assistantname}: {Answer}")
    ChatLogIntegration(f"{Assistantname}: {Answer}")  # Store assistant response
    TextToSpeech(Answer)

def RunAssistant():
    while True:
        MainExecution()
        sleep(0.1)


if __name__ == "__main__":
    print(f"{Assistantname} is ready to assist you!\n")
    RunAssistant()

