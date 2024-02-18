from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from moviepy.editor import *
from pydub import AudioSegment

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/api/endpoint/upload": {"origins": "http://127.0.0.1:5173"}})

UPLOAD_FOLDER = 'api/endpoint/extract'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/api/endpoint/extract', methods=['POST'])
def extract_data():
    # Extracting slides data, data is JSON, data = {"topic" : String, "slides_data" : Array(Dicts("title" : String, "bullet_points" = [], "speaker_notes" = []))}
    # Edward you could directly use this data
    data = request.json 
    
    return jsonify({'message': 'Data received successfully'})

@app.route('/api/endpoint/upload', methods=['POST'])
def upload_file():
    if 'pptxFile' not in request.files:
        return jsonify({'error': 'No file part'})
    
    presentation = request.files['pptxFile']
    if presentation.filename == '':
        return jsonify({'error': 'No selected file'})
    '''    

    # file.save(os.path.join(UPLOAD_FOLDER, file.filename))

    # Load audio files from the device
    
    audio_files = ["audio1.mp3", "audio2.mp3", "audio1.mp3"]  # Add paths to your audio files

    # Read each audio file and attach to corresponding slide
    for i, audio_file in enumerate(audio_files):
        slide = presentation.slides[i]
        slide.shapes.add_movie(audio_file, left=0, top=0, width=1, height=1)
        presentation.slides[i] = slide

    # Export the PowerPoint presentation with attached audio as a video
    video_output = "presentation_with_audio.mp4"
    presentation.save("temp_presentation.pptx")  # Save temporary presentation with audio attached
    presentation_to_video = VideoFileClip("temp_presentation.pptx").set_audio(None)
    presentation_to_video.write_videofile(video_output, codec='libx264', fps=24)  # Convert to video
    presentation_to_video.close()
    '''
    return jsonify({'message': 'File uploaded successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
