"""
main file to handle all process 
it should call all the main functions that handle the following scenario 
1.generating data 
2.clean the data generated 
3.get structured data 
4.generate audio 
5.generate images
6.create the overall video 
"""
from app.data_parser  import parse_data 
from app.templates import * 