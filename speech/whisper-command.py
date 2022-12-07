from api import chat, start_browser 
from tts import text_to_audio
from record_audio import record
from play_audio import play
import whisper



# Set options
options = dict(language="english", beam_size=5, best_of=5, fp16=False)
translate_options = dict(task="translate", **options)


    
def transcribe():
    # Transcribe the audio file
    # Print now transcribing message
    print("Now transcribing: output.wav")
    model = whisper.load_model("tiny")
    result = model.transcribe("output.wav", **translate_options)
    print("Transcribed result", result["text"])
    # Print stopped transcribing message
    print("Stopped transcribing: output.wav")
    return result["text"]

    
    


if __name__ == "__main__":
    start_browser()
    while True:
        record()
        message = transcribe()
        response = chat(message)
        print(response)
        text_to_audio(response)
        play("tts.wav")





