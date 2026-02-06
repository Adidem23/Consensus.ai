from a2a.server.agent_execution import AgentExecutor , RequestContext
from a2a.server.events import EventQueue
from a2a.types import (
    TaskArtifactUpdateEvent,
    TaskStatusUpdateEvent,
    TaskStatus,
    TaskState
) 
from a2a.utils import new_text_artifact
from agent.agent import SupervisorAgent

class SupervisorAgentExecutor(AgentExecutor):
    def __init__(self):
        self.agent=SupervisorAgent()
    
    async def execute(self,context:RequestContext,event_queue:EventQueue):

        user_query=context.get_user_input()

        GEMINI_NODE_AGENT_URL="http://localhost:8005"
        MISTRAL_NODE_AGENT_URL="http://localhost:8006"

        response1=await self.agent.delegateTasks(GEMINI_NODE_AGENT_URL,user_query)
        response2=await self.agent.delegateTasks(MISTRAL_NODE_AGENT_URL,user_query)
 
        if(response1 and  response2):
            final_response=await self.agent.giveDummyFinalResponse()

        await event_queue.enqueue_event(
            TaskArtifactUpdateEvent(
                context_id=context.context_id,
                task_id=context.task_id,
                artifact=new_text_artifact(
                    "final_answer",
                    str(final_response)
                ),
            )
        )

        await event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                context_id=context.context_id,
                task_id=context.task_id,
                status=TaskStatus(state=TaskState.completed),
                final=True,
            )
        )

    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise Exception('cancel not supported')

