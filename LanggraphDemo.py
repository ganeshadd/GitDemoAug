#Langgraph Demo
#Research Agent
#Analyze
#Summarize Agent


from  langgraph.graph import StateGraph
from openai import OpenAI


client =OpenAI(api_key="Your API Keygit")
def call_llm(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"user","content":prompt}
        ]
    )
    return response.choices[0].message.content

#Research Agent :One Job ,Clear Task,Reusable
def research(state):
    query= state["query"]
    prompt=f"Find out the top competitors of :{query}"
    print("Reasearch is completed")
    return{"data":call_llm(prompt)}

#Analyze Agent
def analyze(state):
    prompt= f"Analyse the strenths and weakness of :{state['data']}"
    print("Analysis is completed")
    return{"Analysis":call_llm(prompt)}

#Summarizer Agent
def summarize(state):
    prompt =f"Summarize the market trends for:{state['Analysis']},give me the output in structured JSON format "
    print("Summarization is completed")
    return{"Summary":call_llm(prompt)}

graph=StateGraph(dict)
#add nodes 
graph.add_node("Research",research)
graph.add_node("Analysis",analyze)
graph.add_node("Summary",summarize)


#Add Edges
graph.set_entry_point("Research")
graph.add_edge("Research","Analysis")
graph.add_edge("Analysis","Summary")

app =graph.compile()

result =app.invoke({"query":"Mobile Phones"})
print("Here is the result of your analysis : \n",result)


