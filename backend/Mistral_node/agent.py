import operator
import os
import httpx
import asyncio
from dotenv import load_dotenv
from mistralai import Mistral
from mistralai.async_client import MistralAsyncClient
from mistralai.models.chat_completion import ChatMessage
from langgraph.graph import START , StateGraph , END
from langchain.messages import HumanMessage , SystemMessage , ToolMessage ,AnyMessage
from typing_extensions import Annotated , TypedDict
from langgraph.types import Command
from pydantic import BaseModel

MISTRAL_API_KEY=os.getenv("b24wuVREw1GT4wJyeZSKAAdHNXrbgibU","")

client = Mistral(api_key=MISTRAL_API_KEY)
mistral_client = MistralAsyncClient(api_key=MISTRAL_API_KEY)

class AgentState(TypedDict):
    user_msgs:Annotated[list[AnyMessage],operator.add]
    query: str | None
    llm_count:int


model="mistral-medium-latest"


async def Generate_Critique_mistal(state:AgentState,data:dict):
        critique_prompt = f"""
You are a critique agent in a multi-LLM debate system.

Another agent has produced the following answer:

ANSWER:
{data["Agent_first_Output"]}

Your task:
- Identify factual errors
- Identify missing assumptions
- Identify logical gaps or ambiguities
- Identify unsupported claims

Rules:
- Do NOT rewrite the answer
- Do NOT provide a better answer
- Be precise and concrete
- If no major issues exist, say: "No major issues found."

Output:
- Critique text only.
"""

        completion = await mistral_client.chat(
        model="mistral-medium-latest",
        messages=[
            ChatMessage(role="user", content=critique_prompt)
        ],
        temperature=0.2
        )

        critique_text = completion.choices[0].message.content

        try:
            async with httpx.AsyncClient(timeout=60) as client:
                        Update_data_Critique={
                           "Agent_Node_name":data['Agent_first_Output'],
                            "query":data['query'],
                            "Agent_first_Output": data['Agent_first_Output'],
                            "final_output":"",
                            "Critiques":[{
                                "Given_By_Agent":"Mistral_Agent",
                                "Given_To_Agent":data['Agent_Node_name'],
                                "Critique": critique_text
                            }]
                        }
                        http_response  = await client.post(
                            "http://localhost:8500/agentquery/updateCritique",
                            json=Update_data_Critique
                        )
                        
                        http_response.raise_for_status()

                        return 
            Command(
         update={"user_msgs":state['user_msgs']+[completion],"llm_count":state.get('llm_count')+1},goto=END
        )
            
        except Exception as e:
                    return e
        
async def startDebate(CA_Query):
        MAX_RETRIES = 10  
        POLL_INTERVAL = 2

        async with httpx.AsyncClient(timeout=60) as client:

            for attempt in range(MAX_RETRIES):

                http_response = await client.post(
                    "http://localhost:8500/agentquery/searchForOtherRecords",
                    json=CA_Query
                )

                if http_response.status_code != 200:
                    return

                records = http_response.json()

                if records:
                    for record in records:
                        await Generate_Critique_mistal(record)
                    return 

                await asyncio.sleep(POLL_INTERVAL)

async def normal_response_call(state:AgentState):
    
    chat_response = client.chat.complete(
    model = model,
    messages = [
        {
            "role": "user",
            "content": f'{state['query']}',
        },
    ]
   )
   
    final_reponse= chat_response.choices[0].message.content

    CA_Query={
    "Agent_Node_name":"Mistral",
    "query":state['query'],
    "Agent_first_Output": final_reponse,
    "final_output":"",
    "Critiques":[]
    }

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                            "http://localhost:8500/agentquery/uploadRecord",
                            json=CA_Query
                        )
            response.raise_for_status()

            await startDebate(CA_Query)

    except Exception as e:
                    return e

    Command(
         update={"user_msgs":state['user_msgs']+[chat_response],"llm_count":state.get('llm_count')+1}
    )


builder=StateGraph(AgentState)

builder.add_node("normal_response_call",normal_response_call)

builder.add_edge(START,"normal_response_call")

mistral_agent=builder.compile()