# voice_to_text.py

import threading
import queue
import time
import requests
from gtts import gTTS
from io import BytesIO
from pygame import mixer
import speech_recognition as sr

# Import the function from srm_chatbot.py
from personal import get_srm_response

# Initialize the mixer for audio playback
mixer.init()

def speak_text(text):
    mp3file = BytesIO()
    tts = gTTS(text, lang="en", tld='us')
    tts.write_to_fp(mp3file)

    mp3file.seek(0)

    try:
        mixer.music.load(mp3file, "mp3")
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(0.1)
    except KeyboardInterrupt:
        mixer.music.stop()
    mp3file.close()

def text2speech(text_queue, textdone, llm_finished, audio_queue, stop_event):
    while not stop_event.is_set():
        if not text_queue.empty():
            text = text_queue.get(timeout=0.5)
            mp3file = BytesIO()
            tts = gTTS(text, lang="en", tld='us')
            tts.write_to_fp(mp3file)
            audio_queue.put(mp3file)
            text_queue.task_done()

        if llm_finished.is_set():
            textdone.set()
            break

def play_audio(audio_queue, textdone, stop_event):
    while not stop_event.is_set():
        if audio_queue.empty() and textdone.is_set():
            break
        if not audio_queue.empty():
            mp3audio = audio_queue.get()
            mp3audio.seek(0)
            mixer.music.load(mp3audio, "mp3")
            mixer.music.play()
            while mixer.music.get_busy():
                time.sleep(0.1)
            audio_queue.task_done()

def main():
    rec = sr.Recognizer()
    mic = sr.Microphone()
    rec.dynamic_energy_threshold = False
    rec.energy_threshold = 400

    stop_event = threading.Event()

    while True:
        with mic as source:
            rec.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")

            try:
                audio = rec.listen(source, timeout=20, phrase_time_limit=30)
                text = rec.recognize_google(audio, language="en-EN")

                if "srm" in text.lower():
                    request = text.lower()

                    # Send the request to the LangChain chatbot
                    response = get_srm_response(request)

                    print(f"AI: {response}")
                    speak_text(response)

            except Exception as e:
                continue


if __name__ == "__main__":
    main()
