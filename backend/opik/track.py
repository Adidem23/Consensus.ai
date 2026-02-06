import os
import time
from mistralai import Mistral
from dotenv import load_dotenv
from opik import Opik , track

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY", "")
model = "mistral-medium-latest"

client = Mistral(api_key=api_key)

Opik_client=Opik()

@track(
    name="mistral_chat_completion",
    tags=["mistral", "chat", "demo"],
    metadata={
        "provider": "mistral",
        "model": model,
        "env": "local"
    }
)


def call_llm(prompt: str) -> str:
    
    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )

    output = chat_response.choices[0].message.content

    dataset = Opik_client.get_or_create_dataset(name="LLM_DEBATE_DATASET")

    dataset.insert([
        {"user_question":prompt,"model_answer":output}
    ])

    return output


if __name__ == "__main__":
    prompt = "What is the best French cheese?"

    output = call_llm(prompt)

    print(output)