from flask import Flask, request, jsonify
from flask_cors import CORS
from pptx import Presentation as Pre
import os
from moviepy.editor import *
from spire.presentation.common import *
from spire.presentation import *

# os.environ["FFMPEG_PATH"] = './venv/lib/python3.10/site-packages/ffmpeg'

from pydub import AudioSegment

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/api/endpoint/upload": {"origins": "http://127.0.0.1:5173"}})

# Function to read audio files
def read_audio(audio_file):
    return AudioSegment.from_file(audio_file)

# Function to read PowerPoint file
def read_pptx(pptx_file):
    return Pre(pptx_file)

def convert_pptx_to_images(pptx_file):
    prs = Presentation()
    prs.LoadFromFile(pptx_file)
    for i, slide in enumerate(prs.Slides):
        # Specify the output file name
        fileName = f"slide_{i}.png"
        # Save each slide as a PNG image
        image = slide.SaveAsImage()
        image.Save(fileName)
        image.Dispose()
    prs.Dispose()

# Function to create video with audio narration
def create_video(pptx_file, audio_files, output_video):
    prs = read_pptx(pptx_file)
    
    clips = []
    for i, slide in enumerate(prs.slides):
        audio_file = audio_files[i]
        audio = read_audio(audio_file)
        slide_image = f"slide_{i}.png"  # assuming you want to use images of slides
        # You need to implement a function to convert slides to images
        
        # Create a clip for each slide with its corresponding audio
        slide_clip = ImageClip(slide_image).set_duration(audio.duration_seconds)
        audio_clip = AudioFileClip(audio_file)
        audio_clip = audio_clip.set_duration(audio.duration_seconds)
        slide_clip = slide_clip.set_audio(audio_clip)
        clips.append(slide_clip)
    
    # Concatenate all clips to form the video
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_video, fps=24)

def delete_images():
    directory = os.getcwd()
    for filename in os.listdir(directory):
        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".pptx"): # Specify the file extensions you want to delete
            filepath = os.path.join(directory, filename)
            os.remove(filepath)

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
    name = presentation.filename
     # Save the uploaded presentation to a temporary file
    presentation.save("temp_presentation.pptx")

    if name == '':
        return jsonify({'error': 'No selected file'})    

    pptx_file = "temp_presentation.pptx"
    audio_files = ["audio1.mp3", "audio2.mp3", "audio1.mp3"]  # example audio files
    if(name.endswith(".pptx")):
        name = name[:-5]
    output_video = f"created_videos/{name}.mp4"
    
    convert_pptx_to_images(pptx_file)

    create_video(pptx_file, audio_files, output_video)

    delete_images()
    
    return jsonify({'message': 'File uploaded successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
