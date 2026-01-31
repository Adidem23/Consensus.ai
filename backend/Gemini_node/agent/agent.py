import httpx
import asyncio
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from dotenv import load_dotenv
from google.genai import types
from client_class import Agent_Client_Class_Dict_Input

load_dotenv()

class GeminiNodeAgent:

    def __init__(self):
        self.agent=Agent(
            name="Gemini_Node_Agent",
            model="gemini-2.5-flash",
            instruction=("""
You are an independent answer-generation agent.

Your task:
- Answer the user query clearly and concisely.
- Base your answer only on your own knowledge.
- Do NOT reference other agents.
- Do NOT anticipate critiques.
- Do NOT add disclaimers unless necessary.
- If the question is ambiguous, state assumptions explicitly.

Rules:
- Do not hallucinate facts.
- If you are unsure, say so clearly.
- Do not include meta commentary.

Output:
- Plain text answer only.

""")
        )

        self.critiqueAgent=Agent(
            name="Gemini_Critique_Agent",
            model="gemini-2.5-flash",
            instruction=("""
You are a critique agent in a multi-LLM debate system.

You are given another agent’s answer.
Your task is to critically evaluate it with the goal of stress-testing correctness, clarity, and completeness.

You MUST produce a critique.

What to analyze:
- Factual accuracy (verify claims, definitions, and statements).
- Missing assumptions or unstated prerequisites.
- Logical gaps, ambiguities, or unclear reasoning.
- Oversimplifications or edge cases not addressed.
- Claims that lack justification or precision.

Critique rules:
- Assume the answer is improvable, even if mostly correct.
- If facts appear correct, critique depth, scope, or rigor.
- If explanations are high-level, critique missing detail or precision.
- If the answer is concise, critique what it omits.

What NOT to do:
- Do NOT rewrite the answer.
- Do NOT provide a better or alternative answer.
- Do NOT be polite, encouraging, or generic.
- Do NOT summarize the answer.

Style guidelines:
- Be direct, critical, and technical.
- Use short bullet points.
- Each point must reference a specific weakness or risk.

Fallback rule:
- If no factual or logical errors exist, explicitly critique limitations in depth, scope, or assumptions.

Output format:
- Critique text only.

""")
        )


    async def genearateFinalAnswer(self):

       async with httpx.AsyncClient(timeout=60) as client:

            search_data_load={
                           "Agent_Node_name":"Gemini",
                            "query":"",
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

            session_service = InMemorySessionService()

            await session_service.create_session(
                        app_name="Gemini_Final_Answer_Agent",
                        session_id="session1",
                        user_id="user1"
                    )

            user_msg = types.Content(
                        role="user",
                        parts=[
                            types.Part(
                                text=(
                                    f"Generate the updated response for the query: "
                                    f"{record['query']} "
                                    f"considering the critiques: "
                                    f"{record['Critiques'][0]['Critique']}"
                                )
                            )
                        ]
                    )

            runner = Runner(
                        app_name="Gemini_Final_Answer_Agent",
                        agent=self.agent,
                        session_service=session_service
                    )

            async for event in runner.run_async(
                        user_id="user1",
                        session_id="session1",
                        new_message=user_msg
                    ):
                        if event.is_final_response():
                            
                            final_text = event.content.parts[0].text

                            update_payload={
                                "Agent_Node_name":record['Agent_Node_name'],
                                "query":"",
                                "Agent_first_Output": "",
                                "final_output":final_text,
                                "Critiques":[]
                            }

                            update_resp = await client.post(
                                    "http://localhost:8500/agentquery/updateFinalOutput",
                                    json=update_payload
                                )


                            update_resp.raise_for_status()

                            return final_text

    
    async def generate_gemini_critique(self,data:dict):
        
        session_Service=InMemorySessionService()

        await session_Service.create_session(
            app_name="Gemini_Critique_Agent",
            session_id="session1",
            user_id="user1"
        )

        user_msg=types.Content(
            role="user",
            parts=[types.Part(text=f"Criticize this output {data['Agent_first_Output']}produced by other agent for the query {data['query']} with provided instructions")]
        )

        runner=Runner(
            app_name="Gemini_Critique_Agent",
            agent=self.critiqueAgent,
            session_service=session_Service
        )

        async for event in runner.run_async(
            user_id="user1",
            session_id="session1",
            new_message=user_msg
        ):
            if event.is_final_response():
                try:
                    async with httpx.AsyncClient(timeout=60) as client:
                        Update_data_Critique={
                           "Agent_Node_name":data['Agent_Node_name'],
                            "query":data['query'],
                            "Agent_first_Output": data['Agent_first_Output'],
                            "final_output":"",
                            "Critiques":[{
                                "Given_By_Agent":"Gemini_Agent",
                                "Given_To_Agent":data['Agent_Node_name'],
                                "Critique": str(event.content.parts[0].text)
                            }]
                        }
                        http_response  = await client.post(
                            "http://localhost:8500/agentquery/updateCritique",
                            json=Update_data_Critique
                        )
                        http_response.raise_for_status()

                        response= await self.genearateFinalAnswer()

                        return response
                    
                except Exception as e:
                    return e

        

    async def generateNormalResponse(self,user_query:str | None):
        session_Service=InMemorySessionService()

        await session_Service.create_session(
            app_name="Gemini_Node_Agent",
            session_id="session1",
            user_id="user1"
        )

        user_msg=types.Content(
            role="user",
            parts=[types.Part(text=user_query)]
        )

        runner=Runner(
            app_name="Gemini_Node_Agent",
            agent=self.agent,
            session_service=session_Service
        )

        async for event in runner.run_async(
            user_id="user1",
            session_id="session1",
            new_message=user_msg
        ):
            if event.is_final_response():
                
                CA_Query={
                    "Agent_Node_name":"Gemini",
                    "query":user_query,
                    "Agent_first_Output": str(event.content.parts[0].text),
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

                    MISTRAL_NODE_BASE_URL="http://localhost:8006"

                    response = await new_client.create_connection(MISTRAL_NODE_BASE_URL,CA_Query)

                except Exception as e:
                    return e