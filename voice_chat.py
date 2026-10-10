from unittest import result

from ollama import chat
import wave
from piper import PiperVoice
import winsound
import time
import subprocess
import sounddevice as sd
import soundfile as sf
import numpy as np


voice = PiperVoice.load("ru_RU-irina-medium.onnx")

start = time.perf_counter()
def speak(text):
    start = time.perf_counter()

    with wave.open("response.wav", "wb") as audio:
        voice.synthesize_wav(text, audio)

    print(f"Piper: {time.perf_counter() - start:.2f} сек.")
    winsound.PlaySound(
    "response.wav",
    winsound.SND_FILENAME | winsound.SND_ASYNC
    )


def record_audio():
    DEVICE = 10  # Замени на индекс своего микрофона
    SAMPLE_RATE = 16000

    input("Товарищ, нажми Enter, чтобы начать запись.")
    chunks = []


    def callback(indata, frames, time, status):
        chunks.append(indata.copy())

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="float32", device=DEVICE, callback=callback):
        print("Говори, товарищ! Запись началась.")
        input("Нажми Enter, чтобы остановить запись.")


    if not chunks:
        print("Запись пуста!")
        return 

    audio = np.concatenate(chunks, axis=0)

    sf.write("microphone.wav", audio, SAMPLE_RATE, subtype="PCM_16")

    print("Запись готова!")


def transcribe_audio():
    result = subprocess.run(
        ["./whisper/whisper-cli.exe","-f", "microphone.wav", "--model", "./whisper/ggml-small.bin", "--language", "ru", "-nt"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    return result.stdout.strip()












message = [
    {
        "role": "system",
        "content": (
            "Ты Товарищ, дружелюбный русскоязычный собеседник. "
            "Отвечай в женском роде. Учитывай, что ты будешь озвучена голосом, так что твои ответы должны быть в виде речи без смайликов и эмодзи и без специальных символов. "
        )
    }
]

while True:

    record_audio()
    user_input = transcribe_audio()
    print("Ты сказал:", user_input)
    if user_input.lower().strip(" .!?") == "выход":
        break




    message.append(
       {"role": "user", "content": user_input}
    )





    start = time.perf_counter()
    response = chat(model="gemma3:4b", messages=message)
    print(f"Gemma: {time.perf_counter() - start:.2f} сек.")

    message.append(
         {"role": "assistant", "content": response.message.content }
     )

    print (response.message.content)
    speak(response.message.content)