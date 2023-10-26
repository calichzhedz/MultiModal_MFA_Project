import sounddevice as sd
import librosa
import numpy as np
import random
import pickle
import time

# User identification
username = input("Please enter your username: ")

# Load the models associated with the username
voice_model_filename = f'voice_model_{username}.pkl'
typing_model_filename = f'typing_model_{username}.pkl'

with open(voice_model_filename, 'rb') as voice_model_file:
    voice_clf = pickle.load(voice_model_file)

with open(typing_model_filename, 'rb') as typing_model_file:
    typing_clf = pickle.load(typing_model_file)

# Voice feature extraction
def extract_mfcc(filename):
    audio_data, sample_rate = librosa.load(filename)
    mfcc_features = librosa.feature.mfcc(y=audio_data, sr=sample_rate)
    return mfcc_features.mean(axis=1)

# Non-pangram sentences for authentication
non_pangram_sentences = [
    "Bananas are great",
    "I love coffee",
    "Rainy days are gloomy",
    "Technology is amazing"
]

# Function to record voice
def record_voice(filename, duration=3, sr=22050, device=None):
    random_sentence = random.choice(non_pangram_sentences)
    print(f"Please say the following sentence: {random_sentence}")
    audio_data = sd.rec(int(sr * duration), samplerate=sr, channels=2, dtype='int16', device=device)
    sd.wait()
    sf.write(filename, audio_data, sr)

# Typing dynamics - record typing data
def record_typing():
    sentence = "The quick brown fox jumps over the lazy dog"  # For simplicity, using a static sentence
    print(f"Please type the following sentence: \n\n{sentence}\n")
    
    input("Press Enter when you are ready to start typing...")
    start_time = time.time()
    typed_sentence = input()
    end_time = time.time()

    total_words = len(typed_sentence.split())
    total_time_minutes = (end_time - start_time) / 60
    wpm = total_words / total_time_minutes

    return wpm

# Record voice for authentication
test_filename = "voice_test_sample.wav"
record_voice(test_filename)
test_features = extract_mfcc(test_filename).reshape(1, -1)
voice_pred = voice_clf.predict(test_features)

# Record typing for authentication
typing_wpm = record_typing()
typing_pred = typing_clf.predict(np.array([[typing_wpm]]))

# Majority voting or combined decision logic
if voice_pred[0] == 1 and typing_pred[0] == 1:
    print("Authenticated!")
else:
    print("Authentication failed!")
