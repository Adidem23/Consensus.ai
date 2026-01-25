import operator
import os
import httpx
import asyncio
from dotenv import load_dotenv
from mistralai import Mistral
from langgraph.graph import START , StateGraph , END
from langchain.messages import AnyMessage ,HumanMessage
from typing_extensions import Annotated , TypedDict
from langgraph.types import Command

load_dotenv()

MISTRAL_API_KEY=os.getenv("MISTRAL_API_KEY","")


class AgentState(TypedDict):
    user_msgs:Annotated[list[AnyMessage],operator.add]
    query: str | None
    llm_count:int

async def Generate_Critique_mistral(data):
        
        client = Mistral(api_key=MISTRAL_API_KEY)

        model="mistral-medium-latest"
        
        critique_prompt = f"""
        You are a critique agent in a multi-LLM debate system.

        Another agent has produced the following answer:

        ANSWER:
        {data["Agent_first_Output"]}

        Your task is to critically evaluate the answer.

        You must identify:
        - Any factual inaccuracies or imprecise statements.
        - Missing assumptions, prerequisites, or context.
        - Logical gaps, ambiguities, or unclear reasoning.
        - Claims that are asserted without adequate justification.
        - Oversimplifications or important edge cases not addressed.

        Rules:
        - Do NOT rewrite the answer.
        - Do NOT provide an alternative or improved answer.
        - Do NOT summarize or agree with the answer.
        - Be precise, concrete, and technical.
        - Use short bullet points where appropriate.

        Evaluation standard:
        - Assume the answer can be improved unless it is fully correct, complete, and well-scoped.
        - If the answer is mostly correct, critique limitations in depth, scope, or rigor.


        Output:
        - Critique text only.

"""
       
        completion=client.chat.complete(
        model = model,
        messages = [
            {
                "role":"system",
                "content":critique_prompt
            },
            {
                "role": "user",
                "content": f"give me the critique with instruction provided for {data['Agent_first_Output']}",
            },
        ]
   )
        

        critique_text = completion.choices[0].message.content

        try:
            async with httpx.AsyncClient(timeout=60) as client:
                        Update_data_Critique={
                           "Agent_Node_name":data['Agent_Node_name'],
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
                        await Generate_Critique_mistral(record)
                    return 

                await asyncio.sleep(POLL_INTERVAL)

async def normal_response_call(state:AgentState):
    client = Mistral(api_key=MISTRAL_API_KEY)

    model="mistral-medium-latest"
    
    chat_response = client.chat.complete(
    model = model,
    messages = [
        {
            "role": "user",
            "content": f"{state['query']}",
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

            return Command(
         update={"user_msgs":state['user_msgs']+[chat_response],"llm_count":state.get('llm_count',0)+1},goto=END
    )

    except Exception as e:
                    return e

    


builder=StateGraph(AgentState)

builder.add_node("normal_response_call",normal_response_call)

builder.add_edge(START,"normal_response_call")

mistral_agent=builder.compile()

async def runagent():
      user_input=input('Enter : ')
      messages = [HumanMessage(content=user_input)]
      messages =await mistral_agent.ainvoke({"messages": messages,"query":user_input})
      print(messages)

if __name__=="__main__":
      asyncio.run(runagent())