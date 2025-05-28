import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_groq import ChatGroq
from langchain.agents import create_tool_calling_agent, AgentExecutor

from tools import get_tools

import warnings
warnings.filterwarnings("ignore", message="Valid config keys have changed in V2")

load_dotenv()

class AssistantResponse(BaseModel):
    answer: str = Field(description="The main answer to the user's query")
    tools_used: List[str] = Field(description="List of tools used to generate the answer")
    confidence: int = Field(description="Confidence score from 1-100")
    sources: Optional[List[str]] = Field(description="Sources of information if applicable", default=None)

    class Config:
        schema_extra = {
            "example": {
                "answer": "The weather in New York is currently sunny with a temperature of 22°C.",
                "tools_used": ["WeatherInfo"],
                "confidence": 95,
                "sources": ["OpenWeatherMap API"]
            }
        }

def extract_json(text):
    """
    Try to extract a JSON object from the LLM output.
    """
    import re, json
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            return None
    return None

def create_agent():
    tools = get_tools()
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.2,
        
    )

    parser = PydanticOutputParser(pydantic_object=AssistantResponse)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are a helpful assistant that can search the web, provide weather information, and perform calculations.

Use the appropriate tools based on the user's query:
- Search tool for general information
- WeatherInfo tool for current weather conditions
- Calculator tool for mathematical calculations

Don't make multiple calls to the same tool in a single query.

After using the necessary tools, format your response as a flat JSON object with the following keys:
answer, tools_used, confidence, sources

Do NOT wrap your output in a "properties" field. Output ONLY the JSON object, nothing else.
Always include which tools you used and provide a confidence score (1-100).
If you used the search tool, include relevant sources.
                """
            ),
            ("placeholder", "{chat_history}"),
            ("human", "{query}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    ).partial(format_instructions=parser.get_format_instructions())

    agent = create_tool_calling_agent(
        llm=llm,
        tools=tools,
        prompt=prompt,
    )

    return AgentExecutor(agent=agent, tools=tools, verbose=True), parser

def main():
    agent_executor, parser = create_agent()
    print("Welcome to the AI Assistant! Type 'exit' to quit.")

    while True:
        query = input("\nYou: ")
        if query.lower() == 'exit':
            print("Goodbye!")
            break

        raw_response = agent_executor.invoke({"query": query, "chat_history": []})

        
        parsed = extract_json(raw_response.get("output", ""))
        if parsed:
            try:
                output = raw_response["output"]
                if isinstance(output, dict):
                    
                    structured_response = AssistantResponse.parse_obj(output)
                elif isinstance(output, str):
                    
                    structured_response = parser.parse(output)
                else:
                    raise ValueError("Unsupported output type: {}".format(type(output)))

                print("\nAssistant:")
                print(f"{structured_response.answer}")
                print(f"\nTools used: {', '.join(structured_response.tools_used)}")
                print(f"Confidence: {structured_response.confidence}%")
                if structured_response.sources:
                    print(f"Sources: {', '.join(structured_response.sources)}")
            except Exception as e:
                print(f"\nAssistant: {raw_response['output']}")
                print(f"\n(Note: Could not parse structured output: {str(e)})")
        

if __name__ == "__main__":
    main()
