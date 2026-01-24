import os
from mistralai import Mistral
from dotenv import load_dotenv
import time
import math

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY","")
model = "mistral-medium-latest"

start_time=time.time()

client = Mistral(api_key=api_key)


if __name__=="__main__":

    chat_response = client.chat.complete(
    model = model,
    messages = [
        {
            "role": "user",
            "content": "What is the best French cheese?",
        },
    ]
    )

    print(chat_response)
    
    end_time=time.time()

    Execution_time=end_time-start_time

    print(f'Executed in {round(Execution_time/60,2)} Seconds')

    


