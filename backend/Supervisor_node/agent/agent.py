import os 
import opik
from opik.evaluation.metrics import AnswerRelevance
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
            

            
    def get_best_trace_by_relevance(self,project_name: str, user_question: str):
            
            """
            Search traces with filters, evaluate with AnswerRelevance, 
            and return the output of the trace with highest relevance score.
            """
    
            # Initialize Opik client
            opik_client = opik.Opik()

            filter_query = 'name contains "final_response"'
            
            # Search traces with two filters
            traces = opik_client.search_traces(
                project_name=project_name,
                filter_string=filter_query,
                max_results=50  
            )
            
            if not traces:
                print("No traces found matching the filters")
                return None
            
            print(f"Found {len(traces)} traces matching filters")
            

            answer_relevance = AnswerRelevance(
                require_context=False,
                model="mistral/mistral-medium-latest"
            )
            
            best_trace = None
            best_score = -1
            trace_scores = []
            
            for trace in traces:
                try:

                    if hasattr(trace, 'output') and trace.output:

                        if isinstance(trace.output, dict):
                            output_text = trace.output.get('response', str(trace.output))
                        else:
                            output_text = str(trace.output)
                        
                        # Score the trace output against the user question
                        score_result = answer_relevance.score(
                            input=user_question,
                            output=output_text
                        )
                        
                        relevance_score = score_result.value
                        
                        print(f"Trace ID: {trace.id}")
                        print(f"Relevance Score: {relevance_score}")
                        print(f"Reason: {score_result.reason}")
                        print(f"Output: {output_text[:100]}...")
                        print("---")
                        
                        # Track the best scoring trace
                        trace_scores.append({
                            'trace': trace,
                            'score': relevance_score,
                            'output': output_text,
                            'reason': score_result.reason
                        })
                        
                        if relevance_score > best_score:
                            best_score = relevance_score
                            best_trace = trace
                            
                except Exception as e:
                    print(f"Error evaluating trace {trace.id}: {e}")
                    continue
            
            if best_trace:
                print(f"\n🏆 Best trace found!")
                print(f"Trace ID: {best_trace.id}")
                print(f"Best Relevance Score: {best_score}")
                
                if isinstance(best_trace.output, dict):
                    return best_trace.output.get('response', str(best_trace.output))
                else:
                    return str(best_trace.output)
            else:
                print("No valid traces found for evaluation")
                return None
            
    async def giveDummyFinalResponse(self,user_query):

        project_name= os.getenv("OPIK_PROJECT_NAME","")

        best_output = self.get_best_trace_by_relevance(project_name,user_query)
    
        if best_output:
            print(f"\n📝 Best Answer:")
            return best_output
        else:
            print("No suitable answer found")

    async def delegateTasks(self, BASE_AGENT_URL:str|None , user_input:str|None):
        new_client=Agent_Client_Class()

        response= await new_client.create_connection(BASE_AGENT_URL,user_input)

        return response    