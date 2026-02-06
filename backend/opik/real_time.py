import opik
import os 
from opik.evaluation.metrics import AnswerRelevance
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

opik.configure()

api_key = os.getenv("MISTRAL_API_KEY", "")
model = "mistral-medium-latest"

client = Mistral(api_key=api_key)

def handle_user_request(user_question: str):

    opik_client = opik.Opik()
    
    messages = [{"role": "user", "content": user_question}]

    trace = opik_client.trace(
        name="mistral_chat_completion",
        input={"question": user_question, "messages": messages},
        tags=["mistral", "chat", "demo"],
        metadata={
            "provider": "mistral",
            "model": model,
            "env": "local"
        }
    )
    
    try:
        chat_response = client.chat.complete(
            model=model,
            messages=messages
        )
        
        output = chat_response.choices[0].message.content
        
    
        answer_relevance = AnswerRelevance(
            require_context=False,
            model="mistral/mistral-medium-latest"
        )
        
        score = answer_relevance.score(
            input=user_question,
            output=output
        )

        print("score is"+str(score))
        
      
        trace.update(
            output={"response": output},
            metadata={
                "usage": {
                    "prompt_tokens": getattr(chat_response.usage, 'prompt_tokens', None),
                    "completion_tokens": getattr(chat_response.usage, 'completion_tokens', None),
                    "total_tokens": getattr(chat_response.usage, 'total_tokens', None)
                } if hasattr(chat_response, 'usage') and chat_response.usage else {}
            }
        )
        
    except Exception as e:
        
        trace.update(
            output={"error": str(e)},
            metadata={"error": True}
        )
        raise
    finally:
    
        trace.end()
    
    return output

if __name__ == "__main__":
    user_response = handle_user_request("What is machine learning?")
    print(user_response)
