import httpx
import json
from typing import Dict
from a2a.client import (
    A2ACardResolver,
    ClientConfig,
    ClientFactory,
    create_text_message_object
)
from a2a.types import TransportProtocol
from a2a.utils.message import get_message_text
from langchain_core.messages import ToolMessage


class Agent_Client_Class_Dict_Input:
    """
    A2A Client that accepts ONLY dict input and
    safely delivers it to the agent executor.

    """

    async def create_connection(self, url: str, user_input: Dict):

        if not isinstance(user_input, dict):
            raise TypeError(
                "Agent_Client_Class_Dict_Input only accepts dict input"
            )


        serialized_payload = json.dumps(user_input, ensure_ascii=False)

        async with httpx.AsyncClient(timeout=60.0) as httpx_client:


            resolver = A2ACardResolver(
                httpx_client=httpx_client,
                base_url=url
            )
            agent_card = await resolver.get_agent_card()


            config = ClientConfig(
                httpx_client=httpx_client,
                supported_transports=[
                    TransportProtocol.jsonrpc,
                    TransportProtocol.http_json
                ],
                streaming=agent_card.capabilities.streaming,
            )

            client = ClientFactory(config).create(agent_card)


            request = create_text_message_object(
                content=serialized_payload
            )

            result = None


            async for response in client.send_message(request):
                task, _ = response


                if task.artifacts:
                    result = get_message_text(task.artifacts[-1])


                for artifact in task.artifacts or []:
                    for part in artifact.parts:
                        root = part.root
                        if isinstance(root, ToolMessage):
                            try:
                                payload = json.loads(root.content)
                                for item in payload:
                                    if item.get("type") == "text":
                                        result = item["text"]
                            except json.JSONDecodeError:
                                pass

            return result
