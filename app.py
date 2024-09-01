from flask import Flask, render_template, request
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
import wave
import numpy as np
import speech_recognition as sr
import json
import requests

app = Flask(__name__)

upload_folder = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER= upload_folder+ '\static'  # Setting the location for the video to save.
path= UPLOAD_FOLDER
print(path)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html', display=False)

@app.route("/php_scripts/script.php", methods=["POST", "GET"])
def video():
    # Use a fixed filename for the uploaded video
    filename = "uploaded_video.mp4"

    # Save the file to the specified upload folder
    video_path= os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file = request.files['video']
    file.save(video_path)

    # Getting the tranlsation language from user.
    to_language= request.form.get('languages')

    #_____________________________________________________processing____________________________________________________

    extract_audio("C:\\Prith IT\\Lab\\Software Engineering\\Transcripter\\static\\uploaded_video.mp4", "extracted.wav")  # Extracting audio from video.
    process_audio("extracted.wav", "processed.wav")  # Processing the extracted audio.
    transcript = extract_transcript("processed.wav")  # Extracting the transcript from the processed audio.

    if to_language!= 'en' and to_language!= None:
        # *************************************************translation*************************************************
        url = "https://nlp-translation.p.rapidapi.com/v1/translate"

        querystring = {"text":transcript,"to":to_language,"from":"en"}

        headers = {
            "X-RapidAPI-Key": "43cc727829msh5644c8389123bf7p18e60cjsnc980a33f130a",
            "X-RapidAPI-Host": "nlp-translation.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        translated_transcript = response.json()["translated_text"][to_language]
        # *************************************************************************************************************

    else:
        translated_transcript = transcript
    # Adding the translated transcript to the json file.
    with open('transcript_translate.json', 'w')as file:
        json.dump(translated_transcript, file)


    return render_template("index.html", display=True, transcript= translated_transcript)

# ******************************************Extracting audio from video******************************************
def extract_audio(video_path, audio_path):
    # Load the video clip
    video_clip = VideoFileClip(video_path)

    # Extract audio from the video clip
    audio_clip = video_clip.audio

    # Write the audio to a new file
    audio_clip.write_audiofile(audio_path, codec='pcm_s16le')  # You can change the codec if needed

    # Close the video clip
    video_clip.close()

# ******************************************Processing the audio******************************************
def process_audio(input_path, output_path):
    # Open the input audio file
    with wave.open(input_path, 'rb') as input_wave:
        # Get audio parameters
        channels = input_wave.getnchannels()
        sample_width = input_wave.getsampwidth()
        frame_rate = input_wave.getframerate()
        frames = input_wave.getnframes()

        # Read audio data
        audio_data = np.frombuffer(input_wave.readframes(frames), dtype=np.int16)

        # Perform audio processing (example: increase volume by 2)
        processed_audio = audio_data * 2

    # Open the output audio file
    with wave.open(output_path, 'wb') as output_wave:
        # Set output audio parameters
        output_wave.setnchannels(channels)
        output_wave.setsampwidth(sample_width)
        output_wave.setframerate(frame_rate)
        output_wave.setnframes(frames)

        # Write processed audio data
        output_wave.writeframes(processed_audio.tobytes())

# ******************************************Extracting the transcript from the processed audio******************************************
def extract_transcript(audio_path):
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Load the audio file
    with sr.AudioFile(audio_path) as audio_file:
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(audio_file)

        # Record the audio
        audio = recognizer.record(audio_file)

        try:
            # Use Google Web Speech API to recognize the audio
            transcript = recognizer.recognize_google(audio)
            return transcript
        except sr.UnknownValueError:
            print("Google Web Speech API could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")    

if __name__ == "__main__":
    app.run(debug=True)