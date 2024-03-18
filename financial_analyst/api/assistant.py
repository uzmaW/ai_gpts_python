
from openai import OpenAI

from settings import OPENAI_API_KEY,FMP_API_KEY
import finance_statements as fs
import json
import time

class Assistant:
    client: OpenAI = None
    thread = None
    assistant = None
    def creat_client(self):
        # Create a client for the API
        self.client = OpenAI()
        return self
  
    # Define the main function
    def run(self,user_message):
        # Creating an assistant with specific instructions and tools
        self.assistant = self.client.beta.assistants.create(
            instructions="Act as a financial analyst by accessing detailed financial data through the Financial Modeling Prep API. Your capabilities include analyzing key metrics, comprehensive financial statements, vital financial ratios, and tracking financial growth trends. ",
            model="gpt-4-1106-preview",
            tools=[
                    {"type": "code_interpreter"},
                    {"type": "function", "function": {"name": "get_income_statement", "parameters": {"type": "object", "properties": {"ticker": {"type": "string"}, "period": {"type": "string"}, "limit": {"type": "integer"}}}}},
                    # same for the rest of the financial functions
                ])
        self.create_thread(self.assistant.id, user_message)
        
        while True:
            run = self.client.beta.threads.runs.retrieve(thread_id=self.thread.id, run_id=run.id)

            # Add run steps retrieval here
            run_steps = self.client.beta.threads.runs.steps.list(thread_id=self.thread.id, run_id=run.id)
            print("Run Steps:", run_steps)

            if run.status == "requires_action":
                tool_calls = run.required_action.submit_tool_outputs.tool_calls
                tool_outputs = []

                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    if function_name in fs.available_functions:
                        function_to_call = fs.available_functions[function_name]
                        output = function_to_call(**function_args)
                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": output,
                        })

                # Submit tool outputs and update the run
                self.client.beta.threads.runs.submit_tool_outputs(
                    thread_id=self.thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )

            elif run.status == "completed":
                # List the messages to get the response
                messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
                for message in messages.data:
                    role_label = "User" if message.role == "user" else "Assistant"
                    message_content = message.content[0].text.value
                    print(f"{role_label}: {message_content}\n")
                break  # Exit the loop after processing the completed run

            elif run.status == "failed":
                print("Run failed.")
                break

            elif run.status in ["in_progress", "queued"]:
                print(f"Run is {run.status}. Waiting...")
                time.sleep(5)  # Wait for 5 seconds before checking again

            else:
                print(f"Unexpected status: {run.status}")
                break

    def create_thread(self,assistant_id, user_message):
        # Create a thread for the user's message
        self.thread = self.client.beta.threads.create(
            assistant_id=assistant_id,
            user_input=user_message
        )
        
    def create_message(self, user_message):
         # Adding a user message to the thread
        self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=user_message
        )
            

  