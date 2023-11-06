import sounddevice as sd
import numpy as np
import pickle
from sklearn.svm import SVC
from Utils import extract_mfcc, record_voice, record_typing
import os
from pydub import AudioSegment
import random

# List of sentences
sentences = [
    "The quick brown fox jumps over the lazy dog",
    "A journey of a thousand miles begins with a single step",
    "To be or not to be, that is the question",
    "All that glitters is not gold",
    "The pen is mightier than the sword"
]

# Shuffle the list of sentences
random.shuffle(sentences)

# Function to convert mp3 file to wav
def convert_mp3_to_wav(mp3_file_path, wav_file_path):
    sound = AudioSegment.from_mp3(mp3_file_path)
    sound.export(wav_file_path, format="wav")

# Path to the folder containing unauthorized voice data in mp3 format
unauthorized_voice_dir = '/your/file/path/to/Voice/files'
# User registration
username = input("Please enter your unique username: ")

# Collect training data
voice_training_data = []
typing_training_data = []
voice_labels = []
typing_labels = []

# Record multiple samples for the authenticated user
for i in range(5):
    # Get a random sentence without repeating
    sentence = sentences[i]
    
    # Voice data (authorized)
    record_filename = f"voice_sample_authorized_{i}.wav"
    record_voice(record_filename, is_training=True, sentence=sentence)
    mfcc_features = extract_mfcc(record_filename).tolist()
    voice_training_data.append(mfcc_features)
    
    # Typing data (authorized)    
    wpm = record_typing()
    typing_training_data.append([wpm])
    
    voice_labels.append(1)  # Label '1' for authorized voice data
    typing_labels.append(1)  # Label '1' for authorized typing data


# Calculate the average and standard deviation of WPM for the authorized user
authorized_wpm = [wpm for [wpm] in typing_training_data]
average_wpm = np.mean(authorized_wpm)
std_wpm = np.std(authorized_wpm)

# Assuming you've already set 'authorized_wpm' to the list of WPMs for the authorized user
min_authorized_wpm = min(authorized_wpm)
max_authorized_wpm = max(authorized_wpm)

# Generate random WPM for unauthorized users based on a range that doesn't overlap with the authorized user's WPM
for _ in range(5):
    if random.choice([True, False]):
        random_wpm = random.uniform(min_authorized_wpm - 20, min_authorized_wpm - 1)
    else:
        random_wpm = random.uniform(max_authorized_wpm + 1, max_authorized_wpm + 20)
    
    typing_training_data.append([random_wpm])
    typing_labels.append(0)  # Label '0' for unauthorized typing data


# Process and collect unauthorized voice data from mp3 files
for filename in os.listdir(unauthorized_voice_dir):
    if filename.endswith('.mp3'):
        
    
        mp3_file_path = os.path.join(unauthorized_voice_dir, filename)
        # Convert mp3 to wav
        wav_file_path = mp3_file_path.replace('.mp3', '.wav')
        convert_mp3_to_wav(mp3_file_path, wav_file_path)
        
        # Extract MFCC features from the wav file
        mfcc_features = extract_mfcc(wav_file_path).tolist()
        voice_training_data.append(mfcc_features)
        
        # Assuming you have a way to collect typing data for unauthorized users        
        voice_labels.append(0)  # Label '0' for unauthorized

# Train SVM Classifier for voice
voice_clf = SVC()
voice_clf.fit(np.array(voice_training_data), np.array(voice_labels))

# Train SVM Classifier for typing dynamics (assuming you've collected typing data for authorized users only)
typing_clf = SVC()
typing_clf.fit(np.array(typing_training_data), np.array(typing_labels))  # Use typing_labels here


# Save the trained models with usernames
voice_model_filename = f'voice_model_{username}.pkl'
typing_model_filename = f'typing_model_{username}.pkl'

with open(voice_model_filename, 'wb') as voice_model_file:
    pickle.dump(voice_clf, voice_model_file)

with open(typing_model_filename, 'wb') as typing_model_file:
    pickle.dump(typing_clf, typing_model_file)
