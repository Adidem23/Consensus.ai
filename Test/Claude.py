import anthropic
import time

from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

start_time=time.time()

if __name__=="__main__":
        message = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": "What should I search for to find the latest developments in renewable energy?"
                }
            ]
        )
        print(message.content)
       
        end_time=time.time()

        Execution_time=end_time-start_time

        print(f'Executed in {round(Execution_time/60,2)} Seconds')
