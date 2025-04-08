from groq import Groq
from googlesearch import search
from json import load, dump
import datetime
from dotenv import dotenv_values
import os

# Load environment variables
env_vars = dotenv_values(".env")
GroqAPIKey = "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"
client = Groq(api_key=GroqAPIKey)
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname", "Jarvis")

messages = []
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatBot = [{"role": "system", "content": System}]

try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)

def get_real_time_info():
    current_date_time = datetime.datetime.now()
    return f"please use this real-time information if needed,\n" \
           f"Day: {current_date_time.strftime('%A')}\n" \
           f"Date: {current_date_time.strftime('%d')}\n" \
           f"Month: {current_date_time.strftime('%B')}\n" \
           f"Year: {current_date_time.strftime('%Y')}\n" \
           f"Time: {current_date_time.strftime('%H')} hours : {current_date_time.strftime('%M')} minutes\n"

def clean_answer(answer):
    return '\n'.join([line for line in answer.split('\n') if line.strip()])

def google_search(query):
    results = list(search(query, advanced=True, num_results=5))
    return "\n".join([f"Title: {i.title}\nDescription: {i.description}\n" for i in results])

def is_real_time_query(query):
    keywords = ["latest", "news", "current", "happening", "real-time", "update", "trending", "recent"]
    return any(keyword in query.lower() for keyword in keywords)

def chatbot(query):
    try:
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)
        messages.append({"role": "user", "content": query})
        
        if is_real_time_query(query):
            search_results = google_search(query)
            SystemChatBot.append({"role": "user", "content": search_results})
        
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + [{"role": "system", "content": get_real_time_info()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )
        
        answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                answer += chunk.choices[0].delta.content
        
        messages.append({"role": "assistant", "content": answer.strip()})
        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)
        
        return clean_answer(answer)
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred. Please try again."

if __name__ == "__main__":
    while True:
        user_input = input("Enter your query: ")
        print(chatbot(user_input))
