import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.logger import logging

# importing necessary packages from langchain
# from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain # LLMChain is used to connect several components
from langchain.chains import SequentialChain

# Load environment variables from the .env file
load_dotenv()

# Access the environment variables just like you would do with os.environ
key=os.getenv("OPEN_API_KEY")

llm=ChatOpenAI(openai_api_key=key,model_name="gpt-3.5-turbo",temperature=0.7) # temperature ranges from 0 to 2. If you are mentioning the value near to 2, then the model will be more creative and if it is near to 0 then the model will be less creative.

# Defining input prompt
# Inside the curly braces whatever things are there represents a variables
template="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz of {number} multiple choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}
"""

# Define first Prompt Template
quiz_generation_prompt=PromptTemplate(
    input_variables=["text","number","subject","tone","response_json"], # These are the variables which user is going to pass
    template=template
)

# Creating first LLM Chain
quiz_chain=LLMChain(llm=llm,prompt=quiz_generation_prompt,output_key="quiz",verbose=True)

# Template for correct answer (output prompt)
template2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis.
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

# Defining second prompt template
quiz_evaluation_prompt=PromptTemplate(input_variables=["subject","quiz"],template=template2)

# Creating second LLM chain
review_chain=LLMChain(llm=llm,prompt=quiz_evaluation_prompt,output_key="review",verbose=True) # verbose means whatever execution we are doing we will find on the screen itself

# This is an overall chain where we run the two chains in sequence
# Connecting both the LLM Chain with the help of Sequential Chain
generate_evaluate_chain=SequentialChain(chains=[quiz_chain,review_chain],input_variables=["text","number","subject","tone","response_json"],
                                        output_variables=["quiz","review"],verbose=True)



