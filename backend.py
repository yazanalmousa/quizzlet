import json
import os

from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

# Creating ChatGpt client
load_dotenv()
clientChatOpenAI = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Example response for ChatGpt
example = """
{
    "questions": [
        {
            "question": "What is the capital city of France?",
            "choices": [
                "London",
                "Paris",
                "Berlin",
                "Madrid"
            ],
            "answer": "Paris"
        },
        {
            "question": "Who painted the Mona Lisa?",
            "choices": [
                "Pablo Picasso",
                "Vincent van Gogh",
                "Leonardo da Vinci",
                "Michelangelo"
            ],
            "answer": "Leonardo da Vinci"
        },
        {
            "question": "Which planet is known as the Red Planet?",
            "choices": [
                "Jupiter",
                "Mars",
                "Saturn",
                "Neptune"
            ],
            "answer": "Mars"
        }
    ]
}
"""
# Template of context and constraints for ChatGpt
template = """
            You are an expert quizz maker.
            Generate {number_of_questions} multiple-choice questions of at least {number_of_choices} choices about the following concept {context}.
            Make sure no two options of a question are identical.
            Make sure no two questions are identical.
            The format of the questions should be in json format and answer is not always the first option
            example:<{example}>
            """
prompt = PromptTemplate.from_template(template)
chain = LLMChain(llm=clientChatOpenAI, prompt=prompt)


# Use chain lang to generate questions based on topic,number_of_questions & number_of_choices
def generate_questions_langchain(topic, number_of_questions=10, number_of_choices=4):
    response = chain.run(context=topic, number_of_questions=number_of_questions, number_of_choices=number_of_choices,
                         example=example)
    return json.loads(response)
