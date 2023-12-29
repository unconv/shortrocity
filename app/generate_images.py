"""
a text to image module . 
responsible for generating images by using DALLE-3 openai model 
"""
import base64
from data_parser import parse_data
from templates import template_images , template_narrator
from utils import create_dict_pairs
import os 


def get_images_descriptions() :
    images=[]
    parsed_narrations = parse_data(template_narrator)
    parsed_images = parse_data(template_images)
    l = create_dict_pairs(parsed_narrations,parsed_images)
    for d in l :
        images.append(d["image"])

    return images 

def generate_images(images=get_images_descriptions()):
    from openai import OpenAI
    client = OpenAI()
    for i , img in enumerate(images) : 
        response = client.images.generate(
        model="dall-e-3",
        prompt=img,
        size="1024x1024",
        quality="standard",
        n=1,
        response_format="b64_json"
        )
        image_b64 = response.data[0].b64_json

        if not os.path.exists("./data/images/"):
            os.makedirs("./data/images/")


        with open(f"./data/images/image_{i}.webp" , "wb") as f :
            f.write(base64.b64decode(image_b64))



generate_images()