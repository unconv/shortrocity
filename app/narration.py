"""
create a narration text out of a raw text from a given website or an article 
ideas:
1. scrape a website text , filter it and generate an add out of it . 
2. create a youtube shorts app generator 
"""
from load_dotenv import load_dotenv
load_dotenv()
import os 
from utils import load_html_text
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from templates import template 

def call():
    # prompt = PromptTemplate.from_template(template)
    # prompt.format(context=load_html_text())
    context = load_html_text()
    # print(prompt.format(context))
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", template)
    ])
    chain = chat_prompt | ChatOpenAI() 
    response = chain.invoke({"context":context })

    with open("./data/response.txt" , "w") as f : 
        f.write(response.content)
    print(response.content)
    return response.content

# print(call())