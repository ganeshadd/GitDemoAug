import requests

def call_llm(prompt):
    url ="http://localhost:11434/api/generate"

    payload = {
        "model":"deepseek-r1:1.5b",
        "prompt":prompt,
        "stream":False
    }

    response= requests.post(url,json=payload)
    return response.json()["response"]

user_input =input("Enter your instruction :")
print("**********User Input***********")
print(user_input)

result =call_llm(user_input)
print ("\n AI Response \n")
print(result)