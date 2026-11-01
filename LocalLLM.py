#Import Library
import ollama

#Invoked Local LLM

def call_llm(prompt):
    response = ollama.generate(
            model ="tinyllama",
            prompt = prompt
                    )
    return response["response"]

user_input =input("Enter your instruction :")
print("**********User Input***********")
print(user_input)

result =call_llm(user_input)
print ("\n AI Response \n")
print(result)