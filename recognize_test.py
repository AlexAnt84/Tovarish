import wave
import json
from vosk import Model, KaldiRecognizer

model = Model("vosk-model-small-ru-0.22")

with wave.open("microphone.wav", "rb") as audio:
    print("Каналы:", audio.getnchannels())
    print("Частота:", audio.getframerate())
    print("Разрядность:", audio.getsampwidth())
    print("Количество кадров:", audio.getnframes())
    recognizer = KaldiRecognizer(
        model,
        audio.getframerate()
    )

    while True:
        data = audio.readframes(4000)

        if not data:
            break

    if recognizer.AcceptWaveform(data):
        print("Фраза:", recognizer.Result())
    else:
        print("Промежуточно:", recognizer.PartialResult())
        result = json.loads(recognizer.FinalResult())

print("Распознано:", result["text"])