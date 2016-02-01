#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
import wave
import pyaudio

def playGong():
    CHUNK = 1024

    wf = wave.open('gong.wav', 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    while True:
        print("Say something!")
        audio = r.listen(source)
        result = ""
        print("1")
        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            result += r.recognize_google(audio)
            print("Google Speech Recognition thinks you said " + result)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        # recognize speech using Wit.ai
        WIT_AI_KEY = "PU7RT4A7RXN4GV2AJTDCWS2UI4IILO5L" # Wit.ai keys are 32-character uppercase alphanumeric strings
        try:
            wit = r.recognize_wit(audio, key=WIT_AI_KEY)
            print("Wit.ai thinks you said " + wit)
            result += wit
        except sr.UnknownValueError:
            print("Wit.ai could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Wit.ai service; {0}".format(e))

        if "tommy" in result.lower():
            print("BONG")
            playGong()