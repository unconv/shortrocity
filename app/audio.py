"""
create a narration audio out of a text 
"""
from data_parser import parse_data
from templates import template_images , template_narrator
from utils import create_dict_pairs
from elevenlabs import set_api_key , generate , save 
from load_dotenv import load_dotenv
load_dotenv()
import os 
set_api_key(os.getenv("ELEVENLABS_KEY"))

def concatenate_text() :
    text=""
    parsed_narrations = parse_data(template_narrator)
    parsed_images = parse_data(template_images)
    l = create_dict_pairs(parsed_narrations,parsed_images)
    for d in l :
        text += d["text"]+"\n\n"
    return text

def generate_audio(text):
    audio = generate(
        text=text , 
        voice="T7QGPtToiqH4S8VlIkMJ",
        model="eleven_multilingual_v2"
    )
    save(audio = audio , filename="./data/audio.mp3")


generate_audio(
    text=concatenate_text()
)