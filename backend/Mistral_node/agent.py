import operator
import os
import httpx
import asyncio
import opik
from dotenv import load_dotenv
from mistralai import Mistral
from langgraph.graph import START , StateGraph , END
from langchain.messages import AnyMessage ,HumanMessage
from typing_extensions import Annotated , TypedDict
from langgraph.types import Command
from client_class import Agent_Client_Class_Dict_Input
from opik import Opik 

load_dotenv()

MISTRAL_API_KEY=os.getenv("MISTRAL_API_KEY","")

opik.configure()

Opik_client=Opik()

class AgentState(TypedDict):
    user_msgs:Annotated[list[AnyMessage],operator.add]
    query: str | None
    dataobj:dict | None
    callNode: str | None
    llm_count:int


async def CreateFinalAnswer(query):
       
       async with httpx.AsyncClient(timeout=60) as client:
                    
                search_data_load={
                           "Agent_Node_name":"Mistral",
                            "query":query,
                            "Agent_first_Output": "",
                            "final_output":"",
                            "Critiques":[]
                }

                response = await client.post(
                        "http://localhost:8500/agentquery/searchForOtherRecords",
                        json=search_data_load
                    )
                response.raise_for_status()

                records = response.json()  
        
                record=records[0]

                final_answer_prompt=f"""
        Generate the updated response for the query: {record['query']} considering the critiques: {record['Critiques'][0]['Critique']}


        """
                Mistral_client = Mistral(api_key=MISTRAL_API_KEY)
                
                model="mistral-medium-latest"
                    
                completion= Mistral_client.chat.complete(
                    model = model,
                    messages = [
                        {
                            "role":"system",
                            "content":final_answer_prompt
                        },
                        {
                            "role": "user",
                            "content": f"generate the final output from the query:{record['query']} considering critique :{record['Critiques'][0]['Critique']}",
                        },
                    ]
                    )
                
                update_payload={
                    "Agent_Node_name":record['Agent_Node_name'],
                    "query":query,
                    "Agent_first_Output": "",
                    "final_output":completion.choices[0].message.content,
                    "Critiques":[]
                    }
                

                update_resp = await client.post(
                                    "http://localhost:8500/agentquery/updateFinalOutput",
                                    json=update_payload
                                )
                        
                update_resp.raise_for_status()

                final_answer_trace = Opik_client.trace(
                    name="mistral_final_response",
                    input={"question": record['query']},
                    output={"response":completion.choices[0].message.content},
                    tags=["mistral", "chat", "llm_debate_agent"],
                    metadata={
                        "provider": "mistral",
                        "model": model,
                        "env": "local"
                    }
                )

                final_answer_trace.end()

                return completion.choices[0].message.content
                   
    
async def Generate_Critique_mistral(state:AgentState):
        
        data=state['dataobj']
        
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
       
        completion= client.chat.complete(
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

                        critique_input=f"give me the critique with instruction provided for {data['Agent_first_Output']}"

                        critique_answer_trace=Opik_client.trace(
                        name="mistral_critique_response",
                        input={"question": critique_input},
                        output={"response":critique_text},
                        tags=["mistral", "chat", "llm_debate_agent"],
                        metadata={
                            "provider": "mistral",
                            "model": model,
                            "env": "local"
                        }
                        )

                        critique_answer_trace.end()

                        await CreateFinalAnswer(data['query'])
                         
                        return Command(
                               update={"llm_count":state.get('llm_count',0)+1}
                        )
                        
        except Exception as e:
                    return e


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
  
            new_client=Agent_Client_Class_Dict_Input()

            normal_answer_trace=Opik_client.trace(
                        name="mistral_normal_response",
                        input={"question": state['query']},
                        output={"response":final_reponse},
                        tags=["mistral", "chat", "llm_debate_agent"],
                        metadata={
                            "provider": "mistral",
                            "model": model,
                            "env": "local"
                        }
            )
                        
            normal_answer_trace.end()

            GEMINI_NODE_URL="http://localhost:8005"

            response = await new_client.create_connection(GEMINI_NODE_URL,CA_Query)
            
    except Exception as e:
                    return e
    

    return Command(
         update={"user_msgs":state['user_msgs'],"llm_count":state.get('llm_count',0)+1},goto=END
    )

    


async def startNode(state:AgentState):
        if(state['callNode']=="Normal"):
           return Command(
            update={"user_msgs":state['user_msgs'],"llm_count":state.get('llm_count',0)+1},goto="normal_response_call"
            )

        elif(state['callNode']=="Debate"):
            return Command(
            update={"user_msgs":state['user_msgs'],"llm_count":state.get('llm_count',0)+1},goto="Generate_Critique_mistral"
            )
               
                    

builder=StateGraph(AgentState)

builder.add_node("normal_response_call",normal_response_call)
builder.add_node("Generate_Critique_mistral",Generate_Critique_mistral)
builder.add_node("startNode",startNode)

builder.add_edge(START,"startNode")

mistral_agent=builder.compile()

# async def runagent():
#       user_input=input('Enter : ')
#       messages = [HumanMessage(content=user_input)]
#       messages =await mistral_agent.ainvoke({"messages": messages,"query":user_input,"callNode":"Normal"})
#       print(messages)

# if __name__=="__main__":
#       asyncio.run(runagent())