import sounddevice as sd
import soundfile as sf

DEVICE = 10  # Замени на индекс своего микрофона
SAMPLE_RATE = 16000
DURATION = 5

print("Говори, товарищ!")

audio = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="float32",
    device=DEVICE
)

sd.wait()

sf.write("microphone.wav", audio, SAMPLE_RATE, subtype="PCM_16")

print("Запись готова!")

import numpy as np

print("Пиковая амплитуда:", np.max(np.abs(audio)))