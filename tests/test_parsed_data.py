from app.data_parser import parse_data
from app.templates import template_images , template_narrator
from app.utils import create_dict_pairs
parsed_narrations = parse_data(template_narrator)
parsed_images = parse_data(template_images)

def test_parsed_data_length_match():
    assert len(parsed_narrations) == len(parsed_images)

def test_list_length_of_images_narrations():
    l= create_dict_pairs(parsed_narrations , parsed_images)
    assert  len(l) == len(parsed_images)

