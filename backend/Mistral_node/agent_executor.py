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
        
        user_query= context.get_user_input()
        
        messages=[HumanMessage(content=f'{user_query}')]

        result= await mistral_agent.ainvoke({"messages":messages,"query":user_query})
        print(result)

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