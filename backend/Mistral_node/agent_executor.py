import json
from a2a.server.agent_execution import AgentExecutor, RequestContext 
from a2a.server.events import EventQueue
from a2a.types import (
    TaskArtifactUpdateEvent,
    TaskStatusUpdateEvent,
    TaskStatus,
    TaskState
)
from langchain.messages import HumanMessage
from a2a.utils import new_text_artifact
from agent import mistral_agent


class MistralNodeAgentExecutor(AgentExecutor):
    
    async def execute(self, context:RequestContext, event_queue:EventQueue):
        
        raw_input = context.get_user_input()

        try:
            parsed_input = json.loads(raw_input)
        except (TypeError, json.JSONDecodeError):
            parsed_input = raw_input

        if isinstance(parsed_input, dict):
            
            user_query = parsed_input["query"]

            messages = [
                HumanMessage(
                    content=f"User Query:\n{user_query}"
                )
            ]

            result = await mistral_agent.ainvoke({
                "messages": messages,
                "dataobj":parsed_input,
                "callNode":"Debate",
                "query": user_query  
            })

        elif isinstance(parsed_input, str):
            user_query = parsed_input

            messages = [
                HumanMessage(content=user_query)
            ]

            result = await mistral_agent.ainvoke({
                "messages": messages,
                "callNode":"Normal",
                "query": user_query
            })

        await event_queue.enqueue_event(
            TaskArtifactUpdateEvent(
                context_id=context.context_id,
                task_id=context.task_id,
                artifact=new_text_artifact(
                    "Math_agent_anwer",
                    str(result)
                )

            )
        )

        await event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                context_id=context.context_id,
                task_id=context.task_id,
                status=TaskStatus(state=TaskState.completed),
                final=True
            )
        )

    async def cancel(self, context, event_queue):
            raise Exception('Error Processing Request')        