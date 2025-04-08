import pygame
import random
import asyncio
import edge_tts
import os
from dotenv import dotenv_values

# Default voice
AssistantVoice = "en-CA-LiamNeural"

# Load environment variables
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get('AssistantVoice', "en-CA-LiamNeural")  # Ensures a fallback value

# Function to convert text to audio
async def TextToAudioFile(text) -> None:
    file_path = r"Data\speech.mp3"

    if os.path.exists(file_path):
        os.remove(file_path)

    # Generate speech
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='+13%')
    await communicate.save(file_path)

# Function to manage text-to-speech (TTS) functionality
def TTS(Text, func=lambda r=None: True):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(TextToAudioFile(Text))

        # Initialize pygame mixer
        pygame.mixer.init()
        pygame.mixer.music.load(r"Data\speech.mp3")
        pygame.mixer.music.play()

        clock = pygame.time.Clock()
        while pygame.mixer.music.get_busy():
            if func() == False:
                break
            clock.tick(10)
        return True
    except Exception as e:
        print(f"Error in TTS: {e}")
    finally:
        try:
            func(False)
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except Exception as e:
            print(f"Error in finally block: {e}")

# Function to handle text-to-speech with long text handling
def TextToSpeech(Text, func=lambda r=None: True):
    Data = str(Text).split(".")
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir."
    ]

    if len(Data) > 4 and len(Text) >= 250:
        TTS(" ".join(Text.split(".")[:2]) + "." + random.choice(responses), func)
    else:
        TTS(Text, func)

# Main execution loop
if __name__ == "__main__":
    while True:
        TextToSpeech(input("Enter the text: "))
