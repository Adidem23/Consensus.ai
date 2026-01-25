from a2a.types import AgentSkill, AgentCapabilities, AgentCard
from a2a.server.apps import A2AStarletteApplication
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.request_handlers import DefaultRequestHandler
from agent_executor import GeminiNodeAgentExecutor
import uvicorn


if __name__ == "__main__":

    agent_skill = AgentSkill(
        id="gemini_generation_and_critique",
        name="Gemini Node Agent",
        description=(
            "Worker agent that generates initial responses and provides "
            "structured critiques on other agents' outputs as part of a "
            "multi-round debate system."
        ),
        tags=[
            "worker",
            "llm",
            "generation",
            "critique",
            "debate",
            "execution-plane"
        ]
    )

    agent_card = AgentCard(
        name="Gemini_Node_Agent",
        description=(
            "Gemini-based worker agent responsible for answering queries "
            "and critiquing other agent outputs. Does not orchestrate, "
            "delegate, or manage global state."
        ),
        url="http://localhost:8005",
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=AgentCapabilities(
            streaming=True
        ),
        skills=[agent_skill]
    )

    request_handler = DefaultRequestHandler(
        agent_executor=GeminiNodeAgentExecutor(),
        task_store=InMemoryTaskStore()
    )

    app = A2AStarletteApplication(
        http_handler=request_handler,
        agent_card=agent_card
    )

    uvicorn.run(
        app.build(),
        host="0.0.0.0",
        port=8005
    )
