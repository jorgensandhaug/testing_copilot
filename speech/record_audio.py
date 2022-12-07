import speech_recognition as sr

def record():
    # create a recognizer object
    r = sr.Recognizer()

    # start recording audio
    with sr.Microphone() as source:
        print("Recording audio...")

        # adjust the energy threshold to filter out noise
        r.energy_threshold = 1000
        r.dynamic_energy_threshold = True

        # listen for when the speaking starts, then start recording
        # When the speaker stops speaking, stop recording
        audio = r.listen(source, phrase_time_limit=5, timeout=5)

    # save the audio file
    with open("output.wav", "wb") as f:
        f.write(audio.get_wav_data())