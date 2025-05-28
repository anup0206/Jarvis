import speech_recognition as sr  # For capturing and recognizing speech from mic
import datetime  # To fetch and format current date and time
import webbrowser  # To open URLs in the default web browser
import musicLibrary  # Your custom music library with song URLs
import requests  # To make HTTP requests for news API
import openai  # To interact with OpenAI's GPT models
import os  # To handle environment variables securely
import sys
import platform  # To detect operating system info
import asyncio  # For asynchronous programming (async/await)
import subprocess  # To run external programs (mpv for audio playback)
import edge_tts  # Microsoft neural text-to-speech engine
from dotenv import load_dotenv  # Loads environment variables from a .env file

# Load environment variables from a .env file located in your project directory
load_dotenv()

# Initialize OpenAI client safely - if no API key, fallback to offline mode
try:
    api_key = os.getenv("OPENAI_API_KEY")  # Retrieve the key securely
    if api_key:
        client = openai.OpenAI(api_key=api_key)
        print("OpenAI client initialized successfully")
    else:
        print("No OpenAI API key found - running in offline mode")
        client = None
except Exception as e:
    print(f"OpenAI initialization error: {e}")
    client = None  # Disable AI processing if initialization fails

# News API key for fetching current news headlines
news_api = "0a0c53846b5b4868aa242fd20b606b48"  # Replace with your valid key or keep as is for demo

# Function: Speak text out loud using Microsoft's neural voices via Edge-TTS
async def speak(text, voice="en-US-GuyNeural"):
    try:
        communicate = edge_tts.Communicate(text, voice=voice)
        await communicate.save("output.mp3")  # Save speech audio to file
        # Play the generated audio silently, suppressing output to keep terminal clean
        subprocess.run(
            ["mpv", "output.mp3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print(f"Speech error: {e}")
        print(f"Jarvis: {text}")  # Fallback to console if speech fails

# Basic fallback AI responses when OpenAI is not available
def get_fallback_response(command):
    command = command.lower()
    if "einstein" in command:
        return "Albert Einstein was a theoretical physicist famous for the theory of relativity."
    elif "newton" in command:
        return "Isaac Newton formulated the laws of motion and gravity."
    elif "tesla" in command:
        return "Nikola Tesla contributed to the design of modern AC electricity."
    elif "python" in command:
        return "Python is a high-level programming language known for its simplicity."
    elif "how are you" in command:
        return "I'm functioning well, thank you!"
    elif "what can you do" in command:
        return "I can tell time, play music, open websites, and answer your questions."
    else:
        return "I'm in offline mode. I can still help with basic tasks."

# Process user command with OpenAI GPT if available, else fallback
def aiProcess(command):
    if client:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Jarvis, a helpful AI assistant."},
                    {"role": "user", "content": command},
                ],
                temperature=0.6,
                max_tokens=100,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI error: {e}")
    return get_fallback_response(command)

# Greet the user with appropriate message depending on time of day
async def greet():
    hour = datetime.datetime.now().hour
    if hour < 12:
        await speak("Good morning!")
    elif hour < 18:
        await speak("Good afternoon!")
    else:
        await speak("Good evening!")
    await speak("Jarvis is ready to assist you!")

# Setup microphone for listening with calibration to ambient noise
def setup_microphone():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Calibrating microphone... ")
            r.adjust_for_ambient_noise(source, duration=1)  # Adjust to environment noise
        return r
    except Exception as e:
        print(f"Microphone setup error: {e}")
        return None

# Listen briefly for wake word ("Jarvis") — low latency listening
def listen_for_wake_word(recognizer):
    try:
        with sr.Microphone() as source:
            print("Listening ...")
            recognizer.pause_threshold = 1  # Pause length before considering input ended
            audio = recognizer.listen(source, timeout=1, phrase_time_limit=3)
            return recognizer.recognize_google(audio, language="en-US").lower()
    except (sr.WaitTimeoutError, sr.UnknownValueError):
        return ""  # No sound or unclear speech means no wake word detected
    except Exception:
        return ""

# Listen for the full user command after wake word detected
def listen_for_command(recognizer):
    try:
        with sr.Microphone() as source:
            print("Recognizing...")
            recognizer.pause_threshold = 1
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            command = recognizer.recognize_google(audio, language="en-US").lower()
            print(f"Command heard: {command}")
            return command
    except sr.WaitTimeoutError:
        return ""
    except sr.UnknownValueError:
        return ""
    except Exception as e:
        print(f"Command error: {e}")
        return ""

# Open a website in the default browser
def open_website(url, site_name):
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Failed to open {site_name}: {e}")

# Fetch and speak the latest news headlines using NewsAPI
async def get_news(country="us", limit=3):
    """
    Fetches the top headlines using NewsAPI and speaks them.
    :param country: Country code for news (default: 'us')
    :param limit: Number of top headlines to read out (default: 3)
    """
    try:
        await speak(f"Fetching the latest {limit} news headlines from {country.upper()}...")
        url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={news_api}"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            if not articles:
                await speak("I couldn't find any news articles at the moment.")
            else:
                for i, article in enumerate(articles[:limit], start=1):
                    title = article.get("title", "No title")
                    source = article.get("source", {}).get("name", "Unknown source")
                    await speak(f"Headline {i}: {title} — from {source}")
        else:
            await speak(f"Failed to fetch news. Status code: {response.status_code}")
    except Exception as e:
        print(f"[News Error]: {e}")
        await speak("There was a problem fetching the news.")

# Main loop of Jarvis assistant
async def main():
    print(f"Running Jarvis with Edge-TTS on {platform.system()} {platform.release()}")
    recognizer = setup_microphone()
    if not recognizer:
        print("Mic initialization failed. Exiting.")
        return

    await greet()  # Friendly start

    while True:
        try:
            word = listen_for_wake_word(recognizer)
            if "jarvis" in word:
                await speak("Yes, how can I help?")
                query = listen_for_command(recognizer)

                if not query:
                    continue  # No command detected, listen again

                # Handle commands
                if "time" in query:
                    now = datetime.datetime.now()
                    time_str = now.strftime("%I:%M %p")
                    await speak(f"The time is {time_str}")

                elif "open google" in query:
                    open_website("https://www.google.com", "Google")

                elif "open youtube" in query:
                    open_website("https://www.youtube.com", "YouTube")

                elif query.startswith("play"):
                    try:
                        song = query.replace("play", "").strip()
                        if not song:
                            await speak("Please tell me which song you'd like to play.")
                        else:
                            link = musicLibrary.music.get(song)
                            if link:
                                await speak(f"Playing {song}")
                                webbrowser.open(link)
                            else:
                                await speak(
                                    f"Sorry, I couldn't find '{song}' in your music library."
                                )
                    except Exception as e:
                        print(f"Error playing music: {e}")
                        await speak("Something went wrong while trying to play the song.")

                elif "news" in query:
                    await get_news()

                elif "joke" in query:
                    await speak("Why did the programmer quit? Because he didn't get arrays!")

                elif "fact" in query:
                    await speak("A group of flamingos is called a flamboyance!")

                elif any(phrase in query for phrase in ["exit", "quit", "goodbye", "stop"]):
                    await speak("Goodbye! Have a great day!")
                    break

                else:
                    await speak("Let me think about that...")
                    answer = aiProcess(query)
                    await speak(answer)

        except KeyboardInterrupt:
            await speak("Goodbye!")
            break
        except Exception as e:
            print(f"Main loop error: {e}")

# Entry point for the program
if __name__ == "__main__":
    asyncio.run(main())
