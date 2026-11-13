# Define Goal: Analyze competitors pricing
# Tasks:Find Competitors
#   -Collect Data
#   -Analyze data
#   -Generate report

#States : Start->Find->Collect->Analyze->Report->End
#Transitions:
# if data missing->collect again
# If complete ->analyze
# Memory: Store competitors,pricing,gaps
# Reflection:
# What data is missing?
# What can be improved?
# What should be searched again?

from langgraph.graph import StateGraph
from typing import TypedDict,List

# AI Thinking
goal ="Analyze competitors pricing for a product"

tasks=[
    "find_competitors",
    "collect_data",
    "analyze_data",
    "generate_report"
]

# AI Control
class Agentstate(TypedDict):
    task: str
    data:List[str]
    report: str
    memory:List[str]

graph =StateGraph(Agentstate)

def find_competitors(state):
    return{"data":["Competitor A","Competitor B"]}

def collect_data(state):
    data = state["data"]
    enriched=[d +"pricing data" for d in data]
    # + Memory
    memory = state.get("memory",[])
    memory.append("Collected pricing data")

    return{"data":enriched,"memory":memory}

def analyze_data(state):
    return{"report":"Basic price comparison"}

def generate_report(state):
    return{"report":state["report"] +"| Final insights added"}

# Memory and Reflection

def reflect(state):
    memory = state.get("Memory",[])
    if len(memory)<2:
        return{"report":"Data insufficient, retry needed"}

    return{"report":state["report"] + "| improved after reflection"}

graph.add_node("find",find_competitors)
graph.add_node("collect",collect_data)
graph.add_node("analyze",analyze_data)
graph.add_node("report",generate_report)
graph.add_node("reflect",reflect)

graph.set_entry_point("find")
graph.add_edge("find","collect")
graph.add_edge("collect","analyze")
graph.add_edge("analyze","report")
graph.add_edge("report","reflect")


app=graph.compile()

result = app.invoke({
    "task":"Analyze pricing",
    "data":[],
    "report":"",
    "memory":[]
})

print(result)