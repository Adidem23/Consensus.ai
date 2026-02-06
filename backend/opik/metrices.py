import os
from opik import Opik
from opik.evaluation import evaluate
from opik.evaluation.metrics import AnswerRelevance
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

opik_client = Opik()

dataset = opik_client.get_or_create_dataset(name="LLM_DEBATE_DATASET")

api_key = os.getenv("MISTRAL_API_KEY", "")
model = "mistral-medium-latest"

client = Mistral(api_key=api_key)


def evaluation_task(dataset_item):

    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": dataset_item['user_question'],
            }
        ]
    )

    output = chat_response.choices[0].message.content
    
    return {
        "output": output,
        "input": dataset_item['user_question']
    }


answer_relevance_metric = AnswerRelevance(require_context=False,model="mistral/mistral-medium-latest")

evaluation = evaluate(
    dataset=dataset,
    task=evaluation_task,
    scoring_metrics=[answer_relevance_metric],
    experiment_name="LLM_DEBATE_EXPERIMENT"
)

print(evaluation)