import os 
import time
import math
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

GOOGLE_GEMINI_API_KEY=os.getenv("GOOGLE_GEMINI_API_KEY_NEW","")

start_time=time.time()

llm=ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_GEMINI_API_KEY,
    temperature=0.7
)

if __name__=="__main__":
    response=llm.invoke(input="What is the best French cheese?")
    print(response)
    end_time=time.time()
    Execution_time=end_time-start_time
    print(f'Executed in {round(Execution_time/60,2)} Seconds')