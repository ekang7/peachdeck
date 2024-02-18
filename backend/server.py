from flask import Flask, request, jsonify
from flask_cors import CORS
from pptx import Presentation as Pre
import os
from moviepy.editor import *
from spire.presentation.common import *
from spire.presentation import *
import spacy
import os
import urllib.request
import html2text
import predictionguard as pg
from langchain import PromptTemplate, FewShotPromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np
from getpass import getpass
import lancedb
from lancedb.embeddings import with_embeddings
import pandas as pd
from elevenlabs import generate, play, set_api_key

set_api_key("5021690210e628f74d2dede4a39b6e9a") # Eleven Labs API Key

# Given an input (string), index, and slide number, returns the mp3 file to the generated audio for the string with the corresponding avatar.
def generateAudio(input, i, slide_no):
  names = ["Voice1", "Voice2", "Voice3", "Voice4", "Voice5", "Voice6"]
  # Generate the bytes for the output audio
  audio = generate(
    text = input,
    voice = names[i]
  )
  # play(audio, notebook=True)
  # The path where you want to save the mp3 file
  file_path = "slide" + str(slide_no) + ".mp3"
  with open(file_path, "wb") as file:
    file.write(audio)
  return file_path

#NICE 
# Given an array of inputs and an index selecting the avatar, generates an array of mp3 files
def generateAllFiles(inputs, i):
  slide_no = 1
  files = []
  for input in inputs:
    fpath = generateAudio(input, i, slide_no)
    files.append(fpath)
    slide_no += 1
  return files
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
# Load the medium model with word vectors
nlp = spacy.load("en_core_web_md")
# The two reference terms
biology = nlp("Biology")
history = nlp("History")
# Function to determine similarity
def find_closest_topic(text):
    # Convert the input text to a spaCy document
    doc = nlp(text)

    # Calculate similarity with 'Biology' and 'History'
    similarity_to_biology = doc.similarity(biology)
    similarity_to_history = doc.similarity(history)

    # Determine which similarity is greater
    if similarity_to_biology > similarity_to_history:
        return "Biology", similarity_to_biology
    else:
        return "History", similarity_to_history
def embed_batch(batch):
    return [model.encode(sentence[:80]) for sentence in batch]

def embed(sentence):
  return model.encode(sentence)

# LanceDB setup
dir_name = ".lancedb"
if not os.path.exists(dir_name):
    os.mkdir(dir_name)
uri = ".lancedb"
db = lancedb.connect(uri)
# Embeddings setup
name="clip-ViT-B-32"
model = SentenceTransformer(name)

pg_access_token = 'q1VuOjnffJ3NO2oFN8Q9m8vghYc84ld13jaqdF7E'
os.environ['PREDICTIONGUARD_TOKEN'] = pg_access_token

# Now let's augment our Q&A prompt with this external knowledge on-the-fly!!!
template = """### System:
Use the below input Context from the user to create a presentation script that is less than 50 tokens about the Subject from the user. If you cannot answer the question, respond with "Sorry, I can't find an answer, but you might try looking in the following resource."

### User:
Context: {context}

Subject: {subject}

### Assistant:
"""
qa_prompt = PromptTemplate(
    input_variables=["context", "subject"],
    template=template,
)
history_presentation = False
biology_presentation = False

def rag_answer(subject):
  global history_presentation, biology_presentation
  # opening up the data tables

  # Example usage
  if not history_presentation and not biology_presentation: 
    input_text = subject
    closest_topic, similarity_score = find_closest_topic(input_text)

    if (closest_topic == "history"):
      history_presentation = True
      table = db.open_table("history")
    else: 
      biology_presentation = True
      table = db.open_table("bio")
  elif history_presentation: 
    table = db.open_table("history")
  elif biology_presentation: 
    table = db.open_table("bio")

  # Search the for relevant context
  results = table.search(embed(subject)).limit(5).to_pandas()
  results.sort_values(by=['_distance'], inplace=True, ascending=True)
  doc_use = '\n'.join(results['text'].values[0:3])

  # Augment the prompt with the context
  prompt = qa_prompt.format(context=doc_use, subject = subject)

  # Get a response
  result = pg.Completion.create(
      model="Neural-Chat-7B",
      prompt=prompt
  )

  return result['choices'][0]['text']

# NICE
def convert_extracted_data_ino_fftext(data): # returns a list of slide strings
    slide_fftexts = []
    slides = data["slides_data"] # all the slides (array of dictionaries) 
    for slide in slides: 
        bullet_points = slides[1]
        slide_fftext = ""
        for bullet in bullet_points:
            slide_fftext += rag_answer(bullet)
    slide_fftexts.append(slide_fftext)

def convert_fftext_to_audio(slides): # slides is a list of strings, returns a list of slide audio files 



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
