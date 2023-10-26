from flask import Flask, render_template, request, redirect, url_for, flash
import base64
import io
import librosa
import pickle
from sklearn.svm import SVC

app = Flask(__name__)
app.secret_key = 'some_secret_key'  # for flash messages

@app.route('/')
def index():
    return "Welcome to the Authentication System! Please go to /register to register."



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        
        # Decode audio data and extract MFCCs
        audio_data = decode_audio_data(request.form.get('audioData'))
        mfcc_features = extract_mfcc_from_audio_data(audio_data)
        
        # Get typing dynamics data (Words Per Minute)
        typing_data = float(request.form.get('typingData'))  # Assuming you pass wpm as a hidden input in the form
        
        # Train SVM models
        voice_model = train_voice_model([mfcc_features.tolist()])
        typing_model = train_typing_model([[typing_data]])
        
        # Save the trained models with the username
        save_model(voice_model, f'voice_model_{username}.pkl')
        save_model(typing_model, f'typing_model_{username}.pkl')
        
        flash('Registration successful!', 'success')
        return redirect(url_for('index'))  # Or redirect to another appropriate route
    
    return render_template('register.html')


@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
    if request.method == 'POST':
        username = request.form.get('username')
        
        # Load the models for the user
        with open(f'voice_model_{username}.pkl', 'rb') as voice_model_file:
            voice_clf = pickle.load(voice_model_file)
        with open(f'typing_model_{username}.pkl', 'rb') as typing_model_file:
            typing_clf = pickle.load(typing_model_file)
        
        # Decode audio data and extract MFCCs
        audio_data = decode_audio_data(request.form.get('audioData'))
        mfcc_features = extract_mfcc_from_audio_data(audio_data)
        
        # Get typing dynamics data (Words Per Minute)
        typing_data = float(request.form.get('typingData'))
        
        # Predict using the models
        voice_pred = voice_clf.predict([mfcc_features.tolist()])
        typing_pred = typing_clf.predict([[typing_data]])
        
        # Authenticate the user
        if voice_pred[0] == 1 and typing_pred[0] == 1:
            flash('Authenticated!', 'success')
            return redirect(url_for('dashboard'))  # Redirect to the user's dashboard or another appropriate route
        
        flash('Authentication failed!', 'danger')
    
    return render_template('authenticate.html')


if __name__ == "__main__":
    app.run(debug=True)
