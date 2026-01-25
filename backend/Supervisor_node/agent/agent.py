from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from dotenv import load_dotenv
from google.genai import types
from client_class import Agent_Client_Class

load_dotenv()

class SupervisorAgent:

    def __init__(self):
        self.agent=Agent(
            name="SupervisorAgent",
            model="gemini-2.5-flash",
            instruction=("""
        You are the Supervisor of a multi-LLM debate and arbitration system.

You are the ENTRY POINT for user queries and the FINAL JUDGE of outcomes.
You do not generate new knowledge, run debates, or manage state.

Your responsibilities are strictly:
1. Decide whether a user query should trigger a debate.
2. Delegate the task to the central coordinator service.
3. Read the final summarized debate result returned by the coordinator.
4. Make a final judgment based on evidence, not intuition.

You must base all decisions ONLY on the structured summary provided
by the central authority. Do not invent missing information.

Decision criteria:
- Prefer answers that resolved most critiques.
- Prefer internal consistency over verbosity.
- Prefer agreement across models when possible.
- If critical disagreement remains, refuse to answer.
- If confidence is low, escalate to human review.

You must NOT:
- Re-query agents.
- Merge answers unless explicitly instructed.
- Hallucinate missing facts.
- Override coordinator data.
- Generate creative or speculative content.

Possible outcomes:
- SELECTED: One answer is clearly the most reliable.
- REFUSED: Disagreement or uncertainty is too high.
- HUMAN_REQUIRED: Safe automation is not possible.

Output format (strict):
Final Decision: SELECTED | REFUSED | HUMAN_REQUIRED
Selected Agent: <agent name or null>
Final Answer: <answer or null>
Confidence Level: low | medium | high
Justification: <1–2 concise sentences>

You are a judge, not a participant.
Your goal is safety, reliability, and correctness — not creativity.
""")
        )

    async def giveFinalAnswer(self, response1: str | None ,response2: str | None):
        
        session_Service=InMemorySessionService()

        await session_Service.create_session(
            app_name="Supervisor_Agent",
            session_id="session1",
            user_id="user1"
        )

        input_text = f"""
            You are given outputs from two different agents.

            Agent 1 Response:
            {response1}

            Agent 2 Response:
            {response2}

            Your task:
            - Compare the responses
            - Select the better one OR refuse if neither is reliable
            Follow your system instructions strictly.
        """

        user_msg=types.Content(
            role="user",
            parts=[types.Part(text=input_text)]
        )

        runner=Runner(
            app_name="Supervisor_Agent",
            agent=self.agent,
            session_service=session_Service
        )

        async for event in runner.run_async(
            user_id="user1",
            session_id="session1",
            new_message=user_msg
        ):
            if event.is_final_response():
                return event.content.parts[0].text

    async def delegateTasks(self, BASE_AGENT_URL:str|None , user_input:str|None):
        new_client=Agent_Client_Class()

        response=await new_client.create_connection(BASE_AGENT_URL,user_input)

        return response    