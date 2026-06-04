#closed source me agar aapko ek single word bhi likhna h so u have to pay for it
# we use hugging face ai for the open source flagship model (mistral)

from langchain.chat_models import init_chat_model  #for the generalize purpose for sab ke liye 
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage , SystemMessage , HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model = "llama-3.3-70b-versatile", temperature = 0.7)   # large language model loaded from groq playground

history = [
    SystemMessage(content = "You are helpful AI and always gives accurate response.")
]

print("Welcome type 'quit' to exit.")
while True:
    que = input("You :- ").strip()
    if que == "quit":
        break
    history.append(HumanMessage(que))
    response = llm.invoke(history)
    history.append(AIMessage(response.content))
    print(f"Bot :- {response.content}")