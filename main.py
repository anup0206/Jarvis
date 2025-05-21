

import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import musicLibrary

engine = pyttsx3.init()

def speak(text):
    """Convert text to speech — Jarvis talks"""
    engine.say(text)
    engine.runAndWait()

def greet():
    """Greet the user based on the time of day"""
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("Initializing Jarvis...")

def listen_for_wake_word():
    """Listen once for the wake word 'jarvis'"""
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening ...")
            r.pause_threshold = 1
            audio = r.listen(source)
            word = r.recognize_google(audio).lower()
            return word
    except Exception as e:
        print(f"Error listening for wake word: {e}")
        return ""

def listen_for_command():
    """Listen for the user's actual command after wake word"""
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Recognizing......")
            r.pause_threshold = 1
            audio = r.listen(source)
            command = r.recognize_google(audio).lower()
            return command
    except Exception as e:
        print(f"Error listening for command: {e}")
        return ""

def main():
    greet()

    while True:
        # Step 1: Listen for wake word
        word = listen_for_wake_word()

        if "jarvis" in word:
            speak("Yes, I'm listening.")
            # print("\nJarvis Activated..... \nListening for command...\n")

            # Step 2: Listen for the command after wake word detected
            query = listen_for_command()

            if 'time' in query:
                now = datetime.datetime.now()
                hour = now.strftime("%I").lstrip('0')  # 12-hour format
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

            elif query.startswith("play"):
                song = query.split(" ")[1]
                link = musicLibrary.music[song]
                webbrowser.open(link)

            elif 'exit' in query or 'see you' in query:
                speak("Goodbye!")
                break

            elif query:
                speak("I'm not sure how to help with that yet.")

if __name__ == "__main__":
    main()
