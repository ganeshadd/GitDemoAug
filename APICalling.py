

from openai import OpenAI
from google import genai

#Defining API KEY
client =OpenAI(api_key="Your_APIKey")

#Calling LLM
def call_llm(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"user","content":prompt}
        ]
    )
    return response.choices[0].message.content

#Building a fucntion to process text

def process_text(text):
    prompt= f"""
    Give me the output in 3 bullet points {text} .
    """
    response =call_llm(prompt)
    return response


user_input =input("What you want to know about:")
#with open("input.txt","r") as file:
 #   content=file.read()

result =process_text(user_input)
print(result)

