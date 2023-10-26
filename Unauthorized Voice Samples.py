import pickle
import os
import librosa
import numpy as np

def extract_mfcc(filename):
    """Extract MFCC features from an audio file."""
    audio_data, sample_rate = librosa.load(filename)
    mfcc_features = librosa.feature.mfcc(y=audio_data, sr=sample_rate)
    return mfcc_features.mean(axis=1)

# Directory path where the selected voice clips are stored
directory_path = "/Users/bretz/Desktop/Vocal/Valid"

# List to hold the extracted features
features_list = []

# Iterate over each file in the directory
for file in os.listdir(directory_path):
    # Check if the file is an audio file (assuming .mp3 format for Common Voice dataset)
    if file.endswith(".mp3"):
        file_path = os.path.join(directory_path, file)
        
        # Extract MFCC features and append to the features list
        features = extract_mfcc(file_path)
        features_list.append(features)

# Convert the list of features to a numpy array
features_array = np.array(features_list)

# Now, features_array holds the MFCC features for all the voice clips in the directory.
# You can label these as "unauthorized" (e.g., label 0) and combine with your "authorized" samples for model training.


# Save the features array to a file
with open('unauthorized_features.pkl', 'wb') as file:
    pickle.dump(features_array, file)
