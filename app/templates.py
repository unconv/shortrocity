from langchain.prompts import PromptTemplate

from langchain.prompts.chat import ChatPromptTemplate

template = """
Craft a compelling advertisement script as if you were a seasoned content creator expert.
Your task is to create a persuasive and engaging promotional piece tailored to a specific context provided.
Consider the target audience, key messaging, and the overall tone to captivate and drive interest effectively.
Dive into the realm of creativity, utilizing your expertise to seamlessly blend innovation and consumer appeal into a seamless promotional narrative.
Remember to provide details that showcase the uniqueness of the product or service while delivering a memorable and impactful call-to-action.
###############################
your script will be used as a short reel/video along with images that describes the text . 
your script will be passed to a text to speech model to convert it into an audio 
use the following examples as a refrence 
don't output music indicator like [Upbeat music playing] ,[Upbeat music fades out]'
**********************************************
examples :

Example Pair 1:

Image Description 1:
"A vibrant can of Bolt Boost energy drink surrounded by dynamic lightning bolts, symbolizing energy and power."
Ad Text 1:
"Unleash the Power Within! Introducing Bolt Boost – the energy drink that fuels your ambition. Tackle your day with vitality and focus. Time to elevate your energy game!"


Image Description 2:
"An energetic individual conquering challenges with a glowing aura, holding a can of Bolt Boost, surrounded by a vibrant, active environment."
Ad Text 2:
"Revitalize your day with Bolt Boost! Packed with natural ingredients and a burst of flavor, this energy elixir keeps you at your peak. Elevate your performance, embrace the Bolt Boost experience!"

Image Description 3:
"A creative workspace with Bolt Boost cans scattered around, featuring a laptop with artistic tools, showcasing the synergy between the energy drink and creative endeavors."
Ad Text 3:
"Fuel Your Passion! Bolt Boost, the ultimate energy companion for creators. Whether you're a designer, writer, or artist, power up your creativity and break through boundaries. Unleash your potential!"


Image Description 4:
"A visually stunning scene of a creative mind at work, surrounded by Bolt Boost cans and a burst of vibrant colors, highlighting the fusion of creativity and energy."
Ad Text 4:
"Create, Energize, Repeat! Bolt Boost – the choice of innovators. Sip on inspiration and crush creative blocks. Elevate your craft with the energy that matches your ambition."

************************************************
context:{context}
"""

template_narrator = """
scrape all the narrator text from the following context 
use the examples blow as a refrence 
examples : 
\n\nNarrator: "Passion. Quality. Commitment. At McDonald\'s, we\'re passionate about our food, always striving to provide you with the best dining experience possible.
"\n\n[Images of fresh ingredients being prepared and cooked]
\n\nNarrator: "From our balanced options in the Happy Meal to our Quarter Pounder burgers made with 100% fresh beef cooked to order, we\'re committed to serving you quality food.
"\n\n[Close-up shots of various menu items]
 your output should be like below : 

Passion. Quality. Commitment. At McDonald\'s, we\'re passionate about our food, always striving to provide you with the best dining experience possible.\n
From our balanced options in the Happy Meal to our Quarter Pounder burgers made with 100% fresh beef cooked to order, we\'re committed to serving you quality food.\n
context:{context}.
Your response should be single values seperated by a new line \n
append \n to every value you parse 
don't forget any narration 
the count of narrations extracted should be the same as image descriptions
"""

template_images = """
scrape all the images description from the following context 
images description are always enclosed in square brackets [] 
every Narrator text is followed by an image description . please scrape all the images 
use the examples blow as a refrence 
examples : 
\n\nNarrator: "Passion. Quality. Commitment. At McDonald\'s, we\'re passionate about our food, always striving to provide you with the best dining experience possible.
"\n\n[Images of fresh ingredients being prepared and cooked]
\n\nNarrator: "From our balanced options in the Happy Meal to our Quarter Pounder burgers made with 100% fresh beef cooked to order, we\'re committed to serving you quality food.
"\n\n[Close-up shots of various menu items]

 your output should be like below : 

fresh ingredients being prepared and cooked\n
Close-up shots of various menu items\n

context:{context}.
Your response should be single values seperated by a new line \n
append \n to every value you parse 
don't enclude any image indicator in the output . just extract all the image description.
don't add any text to it 
the count of narrations extracted should be the same as image descriptions
don't forget any image.
"""