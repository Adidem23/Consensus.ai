from a2a.server.agent_execution import AgentExecutor , RequestContext
from a2a.server.events import EventQueue
from a2a.types import (
    TaskArtifactUpdateEvent,
    TaskStatusUpdateEvent,
    TaskStatus,
    TaskState
) 
from a2a.utils import new_text_artifact
from agent.agent import GeminiNodeAgent

class GeminiNodeAgentExecutor(AgentExecutor):
    def __init__(self):
        self.agent=GeminiNodeAgent()
    
    async def execute(self,context:RequestContext,event_queue:EventQueue):

        user_query=context.get_user_input()

        final_response=await self.agent.generateNormalResponse(user_query)

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

