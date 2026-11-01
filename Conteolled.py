
from openai import OpenAI
import json

#Defining API KEY
client =OpenAI(api_key="Your API Key")

#Calling LLM
def call_llm(prompt):
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role":"user","content":prompt}
        ]
    )
    return response.choices[0].message.content


#Building a fucntion to process text

def process_text(text):
    prompt= f"""
    Return only valid JSON.
    
    {{
    "summary": "",
    "risks": ""
    "Recommendations":""
    
    }} 
     
     Text: {text} .
    """
    response =call_llm(prompt)
    return response

def safe_parse(json_text):
    try:
        return json.loads(json_text)
    except json.JSONDecodeError:
        return None

user_input =input("What you want to know about:")


result =process_text(user_input)
print ("Raw Output:\n")
print(result)

data =safe_parse(result)
if data is None :
    print("Invalida Json -cannot proceed safely")
else:
    print("Valid Data")
    print(data)