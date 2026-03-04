import speech_recognition as sr
import webbrowser
import musiclibrary
import requests
import time
from gtts import gTTS
from playsound import playsound
import os

# News API (environment variable + backup)
newsapi = os.getenv("NEWS_API_KEY") or "91eb684c17314ebea3c2ef11b6bafad8"

recognizer = sr.Recognizer()


def speak(text):
    print("Jarvis:", text)

    tts = gTTS(text=text, lang='en')

    filename = "voice.mp3"

    tts.save(filename)

    playsound(filename)

    os.remove(filename)


def get_news():

    speak("Here are the top headlines")

    try:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")

        print("Status Code:", r.status_code)

        if r.status_code == 200:

            data = r.json()

            articles = data.get("articles", [])

            if not articles:
                speak("Sorry I could not find any news")
                return

            for article in articles[:5]:

                title = article["title"]

                print(title)

                speak(title)

                time.sleep(1)

        else:
            speak("Unable to fetch news")

    except Exception as e:

        print("News error:", e)

        speak("There was an error getting the news")


def process_command(text):

    text = text.lower()

    if "stop" in text:

        speak("Goodbye")

        return False

    elif "google" in text:

        speak("Opening Google")

        webbrowser.open("https://google.com")

    elif "youtube" in text:

        speak("Opening YouTube")

        webbrowser.open("https://youtube.com")

    elif "facebook" in text:

        speak("Opening Facebook")

        webbrowser.open("https://facebook.com")

    elif "linkedin" in text:

        speak("Opening LinkedIn")

        webbrowser.open("https://linkedin.com")

    elif "news" in text:

        get_news()

    elif "play" in text:

        song_request = text.replace("play", "").strip()

        found = False

        for song in musiclibrary.music:

            if song in song_request:

                speak(f"Playing {song}")

                webbrowser.open(musiclibrary.music[song])

                found = True

                break

        if not found:

            speak("Song not found")

    return True


if __name__ == "__main__":

    speak("Jarvis ready")

    while True:

        try:

            with sr.Microphone() as source:

                print("Listening...")

                audio = recognizer.listen(source)

            text = recognizer.recognize_google(audio)

            print("You said:", text)

            if not process_command(text):

                break

        except sr.UnknownValueError:

            print("Could not understand audio")

        except sr.RequestError:

            print("Internet connection issue")

        except Exception as e:

            print("Unexpected error:", e)