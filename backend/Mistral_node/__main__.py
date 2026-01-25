from a2a.server.apps import A2AStarletteApplication
from a2a.types import (
    AgentCard,
    AgentSkill,
    AgentCapabilities
)
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from agent_executor import MistralNodeAgentExecutor
import uvicorn


if __name__ == "__main__":

    agent_skill = AgentSkill(
        id="mistral_generation_and_critique",
        name="Mistral Node Agent",
        description=(
            "Worker agent powered by Mistral that generates answers and "
            "produces structured critiques of other agents' outputs "
            "as part of a multi-round debate system."
        ),
        tags=[
            "worker",
            "llm",
            "mistral",
            "generation",
            "critique",
            "debate"
        ],
        examples=[
            "Answer a factual question",
            "Critique another agent's response"
        ]
    )

    agent_card = AgentCard(
        name="Mistral_Node_Agent",
        description=(
            "Mistral-based worker agent responsible for answer generation "
            "and critique tasks. Does not orchestrate or manage state."
        ),
        url="http://localhost:8006",
        version="1.0.0",
        capabilities=AgentCapabilities(streaming=True),
        default_input_modes=["text"],
        default_output_modes=["text"],
        skills=[agent_skill]
    )


    request_handler = DefaultRequestHandler(
        agent_executor=MistralNodeAgentExecutor(),
        task_store=InMemoryTaskStore()
    )

    app = A2AStarletteApplication(
        http_handler=request_handler,
        agent_card=agent_card
    )

    uvicorn.run(
        app.build(),
        host="0.0.0.0",
        port=8006
    )
