import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

def speak(text):
    print(f"Assistant: {text}")
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 160)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("Speech output error:", e)

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        print(f"User: {query}")
        return query.lower()
    except Exception:
        return ""

def run_assistant():
    speak("Hello! Voice Assistant active.")
    
    while True:
        query = listen()

        if not query:
            continue

        # 1. Hello
        if "hello" in query or "hi" in query:
            speak("Hello! How can I help you?")

        # 2. Time
        elif "time" in query:
            str_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {str_time}")

        # 3. Date
        elif "date" in query:
            today_date = datetime.datetime.now().strftime("%B %d, %Y")
            speak(f"Today is {today_date}")

        # 4. Search
        elif "search" in query:
            term = query.replace("search", "").strip()
            speak(f"Searching Google for {term}")
            webbrowser.open(f"https://www.google.com/search?q={term}")

        # 5. YouTube
        elif "youtube" in query or "play" in query:
            song = query.replace("play", "").replace("youtube", "").strip()
            speak(f"Opening YouTube for {song}")
            webbrowser.open(f"https://www.youtube.com/results?search_query={song}")

        # 6. Exit
        elif "exit" in query or "stop" in query or "bye" in query:
            speak("Goodbye! Have a nice day.")
            break

if __name__ == "__main__":
    run_assistant()