# Transcripter
Transcripter is a web-based application built using Flask that allows users to upload a video, extract its audio, enhance the audio quality, and generate a transcript of the spoken content. The application also supports translation of the transcript into a user-specified language using a third-party translation API. This project aims to streamline the process of transcription and translation, providing users with an easy-to-use interface.

Features:
1. Video Upload: Users can upload a video file directly through the web interface.
2. Audio Extraction: The application extracts the audio from the uploaded video.
3. Audio Processing: The extracted audio is processed to enhance quality, such as increasing volume.
4. Transcript Generation: A transcript of the processed audio is generated using speech recognition.
5. Transcript Translation: The generated transcript can be translated into a language of the user's choice using a third-party translation API.
6. JSON Output: The translated transcript is saved as a JSON file.

Setup:
Prerequisites:
- Python 3.x
- Flask
- MoviePy
- SpeechRecognition
- NumPy
- wave (Python's built-in module)
- Requests

Installation:

1. Clone the repository:
  git clone https://github.com/yourusername/transcripter.git
  cd transcripter

2. Create a virtual environment (optional but recommended):
  python -m venv venv
  source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the required packages:
  pip install -r requirements.txt

4. Set up the Flask application: Ensure the UPLOAD_FOLDER path in the code is correctly set to a directory where video files can be uploaded and processed.

Usage:

1. Run the application:
  python app.py

2. The application will start and can be accessed via http://127.0.0.1:5000/ in your web browser.

3. Upload a Video:
Go to the home page and upload a video file using the provided interface.
Select the desired translation language (default is English).

4. Processing and Translation:
The application will automatically extract the audio, enhance it, generate a transcript, and translate it if a non-English language is selected.

5. View the Transcript: 
The translated transcript will be displayed on the web page and saved as transcript_translate.json.
