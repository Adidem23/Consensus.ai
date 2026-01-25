from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from dotenv import load_dotenv
from google.genai import types
import httpx
import asyncio

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
Your job is to critically evaluate it.

What to do:
- Identify factual errors.
- Identify missing assumptions.
- Identify logical gaps or ambiguities.
- Point out unsupported claims.

What NOT to do:
- Do NOT rewrite the answer.
- Do NOT provide an alternative answer.
- Do NOT be polite or generic.
- Do NOT agree unless the answer is fully correct.

Rules:
- Be precise and concrete.
- Use short bullet points if possible.
- If the answer is correct, explicitly say: "No major issues found."

Output:
- Critique text only.

""")
        )

    
    async def generate_gemini_critique(self,data:dict):
        
        session_Service=InMemorySessionService()

        await session_Service.create_session(
            app_name="Gemini_Critique_Agent",
            session_id="session1",
            user_id="user1"
        )

        user_msg=types.Content(
            role="user",
            parts=[types.Part(text=data['Agent_first_Output'])]
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
                                "Critique": event.content.parts[0].text
                            }]
                        }
                        http_response  = await client.post(
                            "http://localhost:8500/agentquery/updateCritique",
                            json=Update_data_Critique
                        )
                        http_response.raise_for_status()
                        return event.content.parts[0].text
                    
                except Exception as e:
                    return e

        

    async def startDebate(self, CA_Query):
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
                        await self.generate_gemini_critique(record)
                    return 

                await asyncio.sleep(POLL_INTERVAL)

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

                    await self.startDebate(CA_Query)

                except Exception as e:
                    return e