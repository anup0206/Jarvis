import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os

# Initialize the speech engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def greet():
    """Greet the user based on the current time"""
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("Initializing Jarvis...")
def take_command():
    """Listens for voice input and returns recognized text"""
    r = sr.Recognizer()

    try:
        # First, listen for the wake word
        with sr.Microphone() as source:
            print("Listening for wake word...")
            r.pause_threshold = 1
            audio = r.listen(source,timeout=2,phase_time_out=1)
            word = r.recognize_google(audio)

        # Checking the wake word 'jarvis'
        if word.lower() == "jarvis":
            speak("Yo")  # Speak AFTER releasing mic
            print("\nJarvis Activated... Listening for command...\n")

            # Listen again for the actual command
            with sr.Microphone() as source:
                r.pause_threshold = 1
                audio = r.listen(source)
                query = r.recognize_google(audio)
                return query.lower()
        else:
            return ""  # Wake word not matched, return empty string

    except Exception as e:
        print("Sorry, I didn't catch that.")
        return ""  # In case of error, return empty string

def main():
    """Main function to run the assistant"""
    greet()

    while True:
        query = take_command()

        if 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M")
            speak(f"The time is {strTime}")

        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        elif 'open facebook' in query:
            speak("Opening Facebook")
            webbrowser.open("https://www.facebook.com")

        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif 'anime' in query:
            speak("Opening Anime")
            webbrowser.open("https://www.kisskh.co")

        elif 'exit' in query or 'quit' in query:
            speak("Goodbye!")
            break

        elif query:
            # If the query is not recognized
            speak("I'm not sure how to help with that yet.")

if __name__ == "__main__":
    main()
