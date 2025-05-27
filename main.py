# Agentic V0.5

from dotenv import load_dotenv
import subprocess
import time
import pexpect  
from langchain.agents import AgentType, initialize_agent
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from composio_langchain import ComposioToolSet, App
import warnings  

load_dotenv()


warnings.filterwarnings("ignore", category=UserWarning, module='langchain')
warnings.filterwarnings("ignore", category=DeprecationWarning, module='langchain')

print("Choose Groq or 1 for Groq Provider or Choose OpenAI or 2 for OpenAI Provider:")
llm_ch = input()
if llm_ch == "Groq" or llm_ch == "1":
    llm = ChatGroq(model="llama-3.3-70b-versatile")
elif llm_ch == "OpenAI" or llm_ch == "2":
    llm = ChatOpenAI(model="gpt-3.5-turbo")
else:
    print("Invalid Type")
    exit()

composio_toolset = ComposioToolSet()

def is_tool_connected(tool_name):
    result = subprocess.run(['composio', 'list'], capture_output=True, text=True)
    return tool_name in result.stdout

def add_tool_if_not_connected(tool_name):
    if not is_tool_connected(tool_name):
        subprocess.run(['composio', "add", tool_name.lower()], check=True)
        time.sleep(2)
        

print("Select a tool: \n 1. Twitter\n 2. Gmail\n 3. Github\n 4. GoogleCalendar\n 5. Mathematical")
toolz = input()


if toolz == "1":
    add_tool_if_not_connected('Twitter')
    tools = composio_toolset.get_tools(apps=[App.TWITTER])
elif toolz == "2":  
    add_tool_if_not_connected('Gmail')
    tools = composio_toolset.get_tools(apps=[App.GMAIL])
elif toolz == "3":
    add_tool_if_not_connected('Github')
    tools = composio_toolset.get_tools(apps=[App.GITHUB])
elif toolz == "4":
    add_tool_if_not_connected('GoogleCalendar')
    tools = composio_toolset.get_tools(apps=[App.GOOGLECALENDAR])
elif toolz == "5":
    add_tool_if_not_connected('Mathematical')
    tools = composio_toolset.get_tools(apps=[App.MATHEMATICAL])
else:
    print("Invalid selection.")
    exit()

print("Give a Task...")

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

subprocess.run(['clear'], check=True)
task = input("What is the Task...\n")


if toolz == "5":
    try:
        answer = eval(task)
        print(f"The answer is: {answer}")
    except Exception as e:
        print(f"Error evaluating the task: {e}")
else:
    agent.invoke(task)
