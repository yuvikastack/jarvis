from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values
import os

# Load enviroment varibles
env_vars= dotenv_values(".env")

GroqAPIKey= "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"
client = Groq(api_key=GroqAPIKey)

# retrive specific enviroment varibles for username, assistenat name, and API key
Username= os.getenv("Username")
Assistantname= os.getenv("Assistantname", "Jarvis")
GroqAPIKey= env_vars.get("GroqAPIKey")

messages=[]
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

#A list of sysetm insrtuction for the chatbot.
SystemChatBot = [
    {"role": "system", "content": System}
]

#Attempt to load the chat log from a JSON file.
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages= load(f)
except FileNotFoundError:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([],f)
def RealtimeInformation():
    current_date_time=datetime.datetime.now()
    day=current_date_time.strftime("%A")
    date=current_date_time.strftime("%d")
    month=current_date_time.strftime("%B")
    year=current_date_time.strftime("%Y")
    hour=current_date_time.strftime("%H")
    minute=current_date_time.strftime("%M")
    second=current_date_time.strftime("%S")

    # format the information into a string.
    data = f"please use this real-time information if needed,\n"
    data += f"Day:{day}\nDate: {date}\nMonth:{month}\nYear: {year}\n"
    data += f"Time: {hour} hours :{minute} minutes :{second} seconds.\n"
    return data

# Function to modify the chatbot's response for better formatting.
def AnswerModifier(Answer):
    lines= Answer.split('\n')
    non_empty_lines= [line for line in lines if line.strip()]
    modified_answer= '\n'.join(non_empty_lines)
    return modified_answer

#Main chatbot function to handle the queries
def Chatbot(Query):
    """ This function send the user's query to the chatbot and returns the AI's response. """
    try:
        with open(r"Data\ChatLog.json", "r") as f:
            messages=load(f)
        # Append the user's query to the message list.
        messages.append({"role": "user","content": f"{Query}"})

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + [{"role": "system","content": RealtimeInformation()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream= True,
            stop= None
        )

        Answer= " "

        # process the streamed response chunks.
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer= Answer.replace("</s>", "")

        messages.append({"role": "assistant", "content":Answer})

        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        #Return the formatted response.
        return AnswerModifier(Answer=Answer)
    
    except Exception as e:
        print(f"Error: {e}")
        with open(r"Data\ChatLog.json", "w") as f:
            dump([], f, indent=4)
        return Chatbot(Query)
    
if __name__ == "__main__":
    while True:
        user_input = input("Enter the question: ")
        print(Chatbot(user_input))