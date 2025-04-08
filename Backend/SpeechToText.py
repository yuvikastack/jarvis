from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt
import time


# Load environment variables from .env file
env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage", "en")  # Default to English

# JavaScript-based Speech Recognition HTML
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = '{InputLanguage}';
        recognition.continuous = true;  // Keep listening continuously
        recognition.interimResults = true; // Capture real-time speech

        recognition.onresult = function(event) {
            const transcript = event.results[event.results.length - 1][0].transcript;
            output.textContent = transcript;
        };

        recognition.onend = function() {
            setTimeout(() => recognition.start(), 500);  // Restart listening after small delay
        };

        function startRecognition() {
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
        }
    </script>
</body>
</html>'''.replace("{InputLanguage}", InputLanguage)

# Save the HTML file
os.makedirs("Data", exist_ok=True)
html_file_path = os.path.join("Data", "Voice.html")
with open(html_file_path, "w") as f:
    f.write(HtmlCode)

# Generate file path for WebDriver
Link = f"file:///{os.path.abspath(html_file_path)}"

# Set Chrome options
Chrome_options = Options()
Chrome_options.add_argument("--use-fake-ui-for-media-stream")
Chrome_options.add_argument("--disable-gpu")
Chrome_options.add_argument("--no-sandbox")
Chrome_options.add_argument("--disable-dev-shm-usage")
Chrome_options.add_experimental_option("detach", True)  # Prevents WebDriver from closing

# Start Selenium WebDriver only ONCE
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=Chrome_options)

# Open the HTML file in the browser
driver.get(Link)
time.sleep(2)  # Allow time for the page to load

# Click Start button to begin recognition
driver.find_element(By.ID, "start").click()
print("[INFO] Listening continuously... Speak now!")

# Function to format the text properly
def QueryModifier(Query):
    new_query = Query.lower().strip()
    question_words = ["how", "what", "when", "which", "who", "why", "whose", "whom", "can you", "where"]

    if any(new_query.startswith(word) for word in question_words):
        new_query = new_query.rstrip('.!?') + "?"
    else:
        new_query = new_query.rstrip('.!?') + "."

    return new_query.capitalize()

# Function to translate text into English
def UniversalTranslator(Text):
    return mt.translate(Text, "en", "auto").capitalize()

# Function to capture speech continuously
def SpeechRecognition():
    try:
        while True:
            Text = driver.find_element(By.ID, "output").text.strip()
            if Text:
                print("[INFO] Recognized:", Text)

                # Process recognized text
                if InputLanguage.lower().startswith("en"):
                    final_text = QueryModifier(Text)
                else:
                    final_text = QueryModifier(UniversalTranslator(Text))

                print("[FINAL OUTPUT]:", final_text)

                # Prevent repetition by clearing output
                driver.execute_script("document.getElementById('output').textContent = '';")

            time.sleep(1)  # Small delay to reduce CPU usage

    except Exception as e:
        print(f"[ERROR] Speech Recognition failed: {e}")
        pass
      
# Start continuous speech recognition loop
if __name__ == "__main__":
    while True:
        Text = SpeechRecognition()
        print (Text)
