import wave
from piper import PiperVoice

voice = PiperVoice.load("ru_RU-irina-medium.onnx")

with wave.open("test.wav", "wb") as audio:
    voice.synthesize_wav(
        "Привет, товарищ! Я снова работаю.",
        audio
    )