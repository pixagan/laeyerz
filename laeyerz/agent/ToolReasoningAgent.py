# Copyright 2025 Pixagan Technologies
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from laeyerz.flow.Node import Node
from laeyerz.utils.KeyManager import KeyManager
#from laeyerz.nodes.llm.OpenAINode import OpenAINode as LLM

class ToolReasoningAgent(Node):

   # def __init__(self, name, config, api_key_path, model, role, instructions, tools):
    def __init__(self, name, config):
        super().__init__(name)

        api_key_path = config.get("api_key_path")
        reasoner = config.get("reasoner")
        role   =  config.get("role")
        instructions = config.get("instructions")
        tools = config.get("tools")


        if(config.get('max_steps')):
            self.max_steps = config.get("max_steps")
        else:
            self.max_steps = 10
        
        
        #self.model = model
        self.role = role
        self.task_instructions = instructions   
        self.tools = tools
        self.tool_descriptions = []
        self.km = None
        if api_key_path:
            self.km = KeyManager(api_key_path)
        else:
            self.km = KeyManager()

        if(config.get('reasoner')):
            self.reasoning = reasoner #LLM("Reasoning", model=self.model, config={"api_key": self.km.get("OPENAI_API_KEY")})
        #self.max_steps = 10
        else:
            raise Exception("Reasoner not found in config")


    def add_tool(self, tool):
        print("Adding tool: ", tool["name"])

        properties = {}
        for param in tool["parameters"]:
            properties[param["name"]] = {
                "type": param["type"],
                "description": param["description"]
            }

        self.tool_descriptions.append({
            "type": "function", #tool["type"],
            "function": {
            "name": tool["name"],
                "description": tool["description"],
                "parameters": {
                    "type": "object",
                    "properties": properties
                }
            }
        })

        self.tools[tool["name"]] = tool["function"]



    def run_agent(self, task, task_inputs={}):

        messages = [
            {"role": "system", "content": f"You are a {self.role} agent."},
            {"role": "user", "content": f"Your instructions for the task are : {self.task_instructions}"},
            {"role": "user", "content": f"You are given the following task that you need to complete using the instructions provided along with the tools you have been provided: {task}"},
            
        ]

        context      = []
        isCompleted  = False
        agent_output = None
        nSteps       = 0

        print("----------------------------------Tool Descriptions ------------------------------")
        print("Active Tools : ")
        for tool in self.tool_descriptions:
            print(tool["function"]["name"])
        print("----------------------------------Tool Descriptions ------------------------------")
        
        while not isCompleted:

            prompt_messages = messages.copy()

            if(len(context) > 0):
                
                prompt_messages.append(
                    {
                        "role": "user", "content": f"Previous tool calls: {str(context)}"
                    }
                )

            
            #print("Prompt Messages : ", prompt_messages)
            #print("Tool Descriptions : ", self.tool_descriptions)

            response = self.reasoning.call_llm(prompt_messages, self.tool_descriptions)

            print("----------------------------------Reasoning ------------------------------")
            print(response["message"])
            print("Tool Calls : ", response['tool_calls'])
            print("----------------------------------Reasoning ------------------------------")

            finish_reason = response['finish_reason']
            tool_calls    = response['tool_calls']


            if nSteps > self.max_steps:
                print("----------------------------------Max Steps Reached ------------------------------")
                print("Max steps reached, stopping agent.")
                isCompleted = True
                agent_output = response['message'].content
                print("----------------------------------Agent Response ------------------------------")
                print(agent_output)
                print("----------------------------------Agent Response ------------------------------")
                break

            
            if finish_reason == "stop":
                agent_output = response['message'].content
                isCompleted  = True
                print("----------------------------------Agent Response ------------------------------")
                print(agent_output)
                print("----------------------------------Agent Response ------------------------------")
                break

            elif finish_reason == "tool_calls":
                for tool_call in tool_calls:
                    tool_name = tool_call['function']['name']
                    tool_args = tool_call['function']['arguments']

                    tool_output = self.tools[tool_name](**tool_args)

                    context.append(
                        {
                            "tool_name": tool_name, 
                            "tool_output": str(tool_output)
                        }
                    )

                print("----------------------------------Tool Response ------------------------------")
                print(tool_output)
                print("----------------------------------Tool Response ------------------------------")

            nSteps += 1

        return agent_output



def main():
    agent = ToolReasoningAgent(
    name="TravelPlanner", 
    api_key_path=api_key_path,
    model="gpt-5-mini", 
    role="You are a travel planner", 
    instructions = "Given the city and the request, use the tools to provide the best information to the user", 
    tools={}
    )


if __name__ == "__main__":
    main()