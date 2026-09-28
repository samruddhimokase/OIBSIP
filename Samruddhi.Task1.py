import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests
import time

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

def get_weather(city="Mumbai"):
    api_key = "bd5e378503939ddaee76f12ad7a97608"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        res = requests.get(url).json()
        if res.get("cod") == 200:
            temp = res["main"]["temp"]
            desc = res["weather"][0]["description"]
            speak(f"The weather in {city} is {desc} with a temperature of {temp} degrees Celsius.")
        else:
            speak("City not found or weather service unavailable.")
    except Exception:
        speak("Unable to fetch weather details at the moment.")

def run_assistant():
    speak("Hello! Voice Assistant active.")
    
    while True:
        query = listen()

        if not query:
            continue

        # 1. Greetings
        if "hello" in query or "hi" in query:
            speak("Hello! How can I help you today?")

        # 2. Time
        elif "time" in query:
            str_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {str_time}")

        # 3. Date
        elif "date" in query or "today" in query:
            today_date = datetime.datetime.now().strftime("%B %d, %Y")
            speak(f"Today is {today_date}")

        # 4. Weather
        elif "weather" in query:
            speak("Which city weather would you like to check?")
            city = listen()
            if city:
                get_weather(city)
            else:
                get_weather("Mumbai")

        # 5. Play Song / Music on YouTube
        elif "play" in query or "song" in query or "youtube" in query:
            song = query.replace("play", "").replace("song", "").replace("youtube", "").strip()
            if not song:
                song = "music"
            speak(f"Playing {song} on YouTube")
            webbrowser.open(f"https://www.youtube.com/results?search_query={song}")

        # 6. Set Reminder
        elif "reminder" in query or "remind" in query:
            speak("Setting a short reminder for 5 seconds...")
            time.sleep(5)
            speak("Reminder alert! Time is up.")

        # 7. Exit
        elif "exit" in query or "stop" in query or "bye" in query:
            speak("Goodbye! Have a nice day.")
            break

if __name__ == "__main__":
    run_assistant()