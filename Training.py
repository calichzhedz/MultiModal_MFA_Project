import sounddevice as sd
import librosa
import numpy as np
import random
import pickle
from sklearn.svm import SVC
import soundfile as sf
import time

# User registration
username = input("Please enter your unique username: ")

# Voice feature extraction
def extract_mfcc(filename):
    audio_data, sample_rate = librosa.load(filename)
    mfcc_features = librosa.feature.mfcc(y=audio_data, sr=sample_rate)
    return mfcc_features.mean(axis=1)

# Function to record voice
def record_voice(filename, duration=5, sr=22050, device=None):
    pangram = "The quick brown fox jumps over the lazy dog"
    print(f"Please say the following pangram: '{pangram}'")
    audio_data = sd.rec(int(sr * duration), samplerate=sr, channels=1, dtype='int16', device=device)
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

# Collect training data
voice_training_data = []
typing_training_data = []
labels = []

# Record multiple samples for the authenticated user
for i in range(5):
    # Voice data
    record_filename = f"voice_sample_authorized_{i}.wav"
    record_voice(record_filename, device='MacBook Pro Microphone')
    mfcc_features = extract_mfcc(record_filename).tolist()
    voice_training_data.append(mfcc_features)
    
    # Typing data
    wpm = record_typing()
    typing_training_data.append([wpm])
    
    labels.append(1)  # Label '1' for authorized

# Train SVM Classifier for voice
voice_clf = SVC()
voice_clf.fit(np.array(voice_training_data), np.array(labels))

# Train SVM Classifier for typing dynamics
typing_clf = SVC()
typing_clf.fit(np.array(typing_training_data), np.array(labels))

# Save the trained models with usernames
voice_model_filename = f'voice_model_{username}.pkl'
typing_model_filename = f'typing_model_{username}.pkl'

with open(voice_model_filename, 'wb') as voice_model_file:
    pickle.dump(voice_clf, voice_model_file)

with open(typing_model_filename, 'wb') as typing_model_file:
    pickle.dump(typing_clf, typing_model_file)
