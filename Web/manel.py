#setup environment
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain import OpenAI, SerpAPIWrapper, LLMChain
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish
from langchain.memory import ConversationBufferWindowMemory
import re
import os

#setup tools
from langchain import OpenAI, SerpAPIWrapper, LLMChain
from langchain import OpenAI, GoogleSearchAPIWrapper, LLMChain


#os.environ["SERPAPI_API_KEY"] = os.getenv('SERP_API_KEY')

# Define which tools the agent can use to answer user queries
search = GoogleSearchAPIWrapper()
tools = [
    Tool(
        name = "Search",
        func=search.run,
        description="useful for when you need to answer questions about current events"
    )
]


#prompt_template
# Set up the base template
template_with_history = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question


Previous conversation history:
{history}

New question: {input}
{agent_scratchpad}"""


# Set up a prompt template
class CustomPromptTemplate(StringPromptTemplate):
    # The template to use
    template: str
    # The list of tools available
    tools: List[Tool]
    
    def format(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        return self.template.format(**kwargs)
    


prompt_with_history = CustomPromptTemplate(
    template=template_with_history,
    tools=tools,
    # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
    # This includes the `intermediate_steps` variable because that is needed
    input_variables=["input", "intermediate_steps", "history"]
)


#output parser

class CustomOutputParser(AgentOutputParser):
    
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        # Parse out the action and action input
        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)




def lang_model(company,country,openai_key,google_cse_id,google_api_key):

    os.environ["GOOGLE_CSE_ID"] = google_cse_id
    os.environ["GOOGLE_API_KEY"] = google_api_key
    output_parser = CustomOutputParser()

    #setup llm
    os.environ["OPENAI_API_KEY"] = openai_key

    llm = OpenAI(temperature=0)

    # LLM chain consisting of the LLM and a prompt
    llm_chain = LLMChain(llm=llm, prompt=prompt_with_history)

    tool_names = [tool.name for tool in tools]
    agent = LLMSingleActionAgent(
        llm_chain=llm_chain, 
        output_parser=output_parser,
        stop=["\nObservation:"], 
        allowed_tools=tool_names
    )

    memory=ConversationBufferWindowMemory(k=2)

    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=False, memory=memory)
    overview = agent_executor.run(f"A brief overview of the company {company} in {country}")
    products = agent_executor.run(f"give me the main products or services associated to {company} in the country {country}")
    keywords = agent_executor.run(f"the most important keywords strictly associated to {company} in the country {country}, make it short return 'empty' if can't be found")
    # image = agent_executor.run("The image url, return 'empty' if can't be found")
    # location = agent_executor.run("The location or address, return 'empty' if can't be found")
    data = {
        'overview':overview,
        'products':products,
        'keywords':keywords,
        # 'image':image,
        # 'address':location
    }
    return data

def langchain_serp(company,country,openai_key):
    search = SerpAPIWrapper()
    tools = [
        Tool(
            name = "Search",
            func=search.run,
            description="useful for when you need to answer questions about current events"
        )
    ]
    prompt_with_history = CustomPromptTemplate(
    template=template_with_history,
    tools=tools,
    # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
    # This includes the `intermediate_steps` variable because that is needed
    input_variables=["input", "intermediate_steps", "history"]
    )
    output_parser = CustomOutputParser()

    #setup llm
    os.environ["OPENAI_API_KEY"] = openai_key

    llm = OpenAI(temperature=0)

    # LLM chain consisting of the LLM and a prompt
    llm_chain = LLMChain(llm=llm, prompt=prompt_with_history)

    tool_names = [tool.name for tool in tools]
    agent = LLMSingleActionAgent(
        llm_chain=llm_chain, 
        output_parser=output_parser,
        stop=["\nObservation:"], 
        allowed_tools=tool_names
    )

    memory=ConversationBufferWindowMemory(k=2)

    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=False, memory=memory)
    overview = agent_executor.run(f"A brief overview of the company {company} in {country}")
    products = agent_executor.run(f"give me the main products or services associated to {company} in the country {country}")
    keywords = agent_executor.run(f"the most important keywords strictly associated to {company} in the country {country}, make it short return 'empty' if can't be found")
    # image = agent_executor.run("The image url, return 'empty' if can't be found")
    # location = agent_executor.run("The location or address, return 'empty' if can't be found")
    data = {
        'overview':overview,
        'products':products,
        'keywords':keywords,
        # 'image':image,
        # 'address':location
    }
    return data