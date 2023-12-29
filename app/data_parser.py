from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate , SystemMessagePromptTemplate , ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI
from narration import call 
from langchain.schema.messages import SystemMessage
from utils import clean 
from templates import template_images , template_narrator

# context = call()
# output_parser = CommaSeparatedListOutputParser()
# format_instructions = output_parser.get_format_instructions()
# print(format_instructions)

# prompt = PromptTemplate(
#     template=template,
#     input_variables=["context"],
# )

# chat_template = ChatPromptTemplate.from_messages(
#     [SystemMessagePromptTemplate.from_template(template=template_images)])

# model = ChatOpenAI(temperature=0 ,model_name="gpt-3.5-turbo-1106" , )

# input = chat_template.format_messages(context=context)

# messages = [
#     SystemMessage(_input)
# ]
# print(input)

# chain =  chat_template | model
# output = chain.invoke({"context":context}).content
# clean(data=output)
# print(f"model output is\n\n {output} , \nfirst element is \n   {output[0]} , \n type is {type(output)}")
# print(output.split("\n")[0])
# text = output_parser.parse(output)
# print(context)
# print("\n\n***********\n\n")
# print(



def parse_data(template:str)->list:
    context = call()
    chat_template = ChatPromptTemplate.from_messages(
        [SystemMessagePromptTemplate.from_template(template=template)])

    model = ChatOpenAI(temperature=0 ,model_name="gpt-3.5-turbo-1106"  )

    input = chat_template.format_messages(context=context)
    chain =  chat_template | model
    output = chain.invoke({"context":context}).content
    cleaned_list = clean(data=output)
    return cleaned_list
    