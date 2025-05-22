import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import musicLibrary
import requests
import openai
import os
from dotenv import load_dotenv
load_dotenv()


# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set volume (0.0 to 1.0)
engine.setProperty('volume', 1.0)


# Your NewsAPI key
news_api = "0a0c53846b5b4868aa242fd20b606b48"

# Fetch your OpenAI API key from environment variable
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Function to process general AI queries using OpenAI's ChatGPT
def aiProcess(command):
    
    response = client.responses.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please."},
            {"role": "user", "content": command}
        ],
        temperature=0.6
    )
    return response['choices'][0]['message']['content']  # Return the assistant's response

# Function for Jarvis to speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to greet based on time
def greet():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("Initializing Jarvis...")

# Function to listen for the wake word "jarvis"
def listen_for_wake_word():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening .......")
            r.pause_threshold = 1
            audio = r.listen(source)
            word = r.recognize_google(audio).lower()
            return word
    except Exception as e:
        print(f"Error listening for wake word: {e}")
        return ""

# Function to listen for a full command after Jarvis is triggered
def listen_for_command():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Recoginizing......")
            r.pause_threshold = 1
            audio = r.listen(source)
            command = r.recognize_google(audio).lower()
            return command
    except Exception as e:
        print(f"Error while  listening for command: {e}")
        return ""

# Main assistant loop
def main():
    greet()  # Greet user

    while True:
        word = listen_for_wake_word()  # Listen for wake word

        if "jarvis" in word:
            speak("Yes, I'm listening.")
            query = listen_for_command()  # Listen for actual command

            # Handle time query
            if 'time' in query:
                now = datetime.datetime.now()
                hour = now.strftime("%I").lstrip('0')
                minute = now.strftime("%M")
                second = now.strftime("%S")
                meridiem = now.strftime("%p")

                if meridiem == "AM":
                    period = "in the morning"
                elif meridiem == "PM" and int(hour) < 6:
                    period = "in the afternoon"
                else:
                    period = "in the evening"

                speak(f"The clock now strikes {hour} {minute}, and {second} seconds {period}.")

            # Handle simple web opening commands
            elif 'open google' in query:
                speak("Opening Google")
                webbrowser.open("https://www.google.com")

            elif 'open facebook' in query:
                speak("Opening Facebook")
                webbrowser.open("https://www.facebook.com")

            elif 'open youtube' in query:
                speak("Opening YouTube")
                webbrowser.open("https://www.youtube.com")

            elif 'open anime' in query:
                speak("Opening Anime")
                webbrowser.open("https://www.kisskh.co")

            elif 'open linkedin' in query:
                speak("Opening LinkedIn")
                webbrowser.open("https://www.linkedin.com")

            # Handle song playback from custom music library
            elif query.startswith("play"):
                song = query.split(" ")[1]
                link = musicLibrary.music.get(song, None)
                if link:
                    webbrowser.open(link)
                else:
                    speak("Sorry, I couldn't find that song.")

            # Handle news headlines from NewsAPI
            elif "news" in query:
                try:
                    r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={news_api}")
                    if r.status_code == 200:
                        data = r.json()
                        articles = data.get('articles', [])
                        for article in articles[:5]:  # Speak top 5 headlines
                            speak(article['title'])
                    else:
                        speak("Failed to fetch news at this moment.")
                except Exception as e:
                    speak("There was an error while fetching the news.")

            # Small-talk or fun keywords (manual responses)
            elif "joke" in query:
                speak("Why did the programmer quit his job? Because he didn't get arrays.")

            elif "fact" in query:
                speak("Did you know? A group of flamingos is called a flamboyance.")

            elif "weather" in query:
                speak("I can't fetch real-time weather yet, but I hope it's sunny!")

            elif "who is" in query or "what is" in query:
                output = aiProcess(query)
                speak(output)

            # Exit the assistant
            elif 'exit' in query or 'see you' in query:
                speak("Goodbye! See you next time.")
                break

            # Default fallback: use AI to process any unknown command
            elif query:
                output = aiProcess(query)
                speak(output)

# Run the main function
if __name__ == "__main__":
    main()
