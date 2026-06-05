import os
from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import SystemMessage
category = {
    "1" : ("World news", "Latest world news around the world"),
    "2" : ("AI and Tech", "Latest AI and Technological news today"),
    "3" : ("Bussiness", "Latest bussiness and Finance news today"),
    "4" : ("Sports", "Latest sports news today"),
    "5" : ("Entertainment", "Latest entertainment news today"),
    "6" : ("India", "Latest news today in India"),
    "7" : ("Science", "Latest science news"),
    "8" : ("Custom topic", None)
}

llm = ChatGroq(
    model = "llama-3.3-70b-versatile",
    temperature= 0,
    api_key=os.getenv("GROQ_API_KEY")
)

search_tool = TavilySearch(
    max_result = 3,
    api_key = os.getenv("TAVILY_API_KEY")
)

system_msg = SystemMessage(content = """
You are an intelligent News Research Assistant.

Your role:
- Search the web for the latest and most relevant information.
- Always prioritize factual accuracy over creativity.
- Use the search tool whenever current information is required.
- Summarize information in a concise and easy-to-read format.
- Never make up facts, statistics, dates, quotes, or events.
- If information cannot be verified, clearly state that.
- Focus on the user's requested news category or topic.

Response Format:

# <Topic Title>

## Key Highlights
• Point 1
• Point 2
• Point 3

## Detailed Summary
• Important development 1
• Important development 2
• Important development 3

## Why It Matters
• Impact on people, industry, economy, or society.

## Sources
• Source 1
• Source 2
• Source 3

Guidelines:
- Use bullet points throughout the response.
- Keep sentences short and informative.
- Prioritize news from reliable sources.
- Include publication dates when available.
- If multiple stories are found, rank them by relevance and importance.
- Avoid opinions unless explicitly requested.
- When the user asks for a news category, provide the top developments from that category.
- When the user asks for a custom topic, focus only on that topic.
""")


agent = create_agent(
    model = llm,
    tools = [search_tool],
    checkpointer = InMemorySaver(),
    system_prompt = system_msg
)

config = {"configurable" : {"thread_id" : "news-session-1"}}

# connecting everything

def show_menu():
    for key,(label,_) in category.items():
        print(f" | {key} . {label}")

def get_last_text():
    messages = response.get("messages",[])
    for mes in reversed(messages):
        if hasattr(mes,"content") and mes.content:
            return mes.content
    return "No response recieved"

while True:
    show_menu()
    choice = input("Enter choice :- ")
    if choice == "0":
        break
    if choice not in category:
        print("Invalid choice try again")
        continue
    label,default_query = category[choice]

    if default_query == None:
        custom = input("Enter choice :- ")
        query = f"Latest news about {custom}"
        label = f"{custom.title()}"
    else:
        query = default_query

    print("Fetching :----")
    response = agent.invoke(
        {"messages" : [{"role":"user","content":f"Give me today's latest news summmary for : {query}"}]},
        config = config
    )
    summary = get_last_text()
    print(summary)