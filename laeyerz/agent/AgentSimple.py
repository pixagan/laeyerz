from laeyerz.flow.Node import Node
from laeyerz.utils.KeyManager import KeyManager
from laeyerz.nodes.llm.OpenAILLMNode import OpenAILLMNode as LLM

class AgentSimple(Node):

    def __init__(self, name, api_key_path, model, role, instructions, tools):
        super().__init__(name)
        
        self.model = model
        self.role = role
        self.task_instructions = instructions   
        self.tools = tools
        self.tool_descriptions = []
        self.km = None
        if api_key_path:
            self.km = KeyManager(api_key_path)
        else:
            self.km = KeyManager()
        self.orch = LLM("Orchestrator", config={"api_key": self.km.get("OPENAI_API_KEY")})



    def add_tool(self, tool):
        print("Adding tool: ", tool)

        self.tool_descriptions.append({
            "type": tool["type"],
            "function": {
            "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["parameters"]
            }
        })

        self.tools[tool["name"]] = tool["function"]



    def run_agent(self, task):

        messages = [
            {"role": "system", "content": f"You are a {self.role}. {self.task_instructions}"},
            {"role": "user", "content": f"You are given the following task that you need to complete using the instructions provided along with the tools you have been provided: {task}"},
        ]

        context      = []
        isCompleted  = False
        agent_output = None

        print("----------------------------------Tool Descriptions ------------------------------")
        print(self.tool_descriptions)
        print("----------------------------------Tool Descriptions ------------------------------")
        
        while not isCompleted:

            prompt_messages = messages.copy()

            if(len(context) > 0):
                
                prompt_messages.append(
                    {
                        "role": "user", "content": f"Previous tool calls: {str(context)}"
                    }
                )

            response = self.orch.call_llm(prompt_messages, self.model, self.tool_descriptions)

            print("----------------------------------Orchestrator ------------------------------")
            print(response)
            print("----------------------------------Orchestrator ------------------------------")

            finish_reason = response['finish_reason']
            tool_calls    = response['tool_calls']

            
            if finish_reason == "stop":
                agent_output = response['message'].content
                isCompleted  = True
                print("----------------------------------Agent Output ------------------------------")
                print(agent_output)
                print("----------------------------------Agent Output ------------------------------")
                break

            elif finish_reason == "tool_calls":
                for tool_call in tool_calls:
                    tool_name = tool_call['function']['name']
                    tool_args = tool_call['function']['arguments']

                    tool_output = self.tools[tool_name](**tool_args)

                    context.append(
                        {
                            "tool_name": tool_name, 
                            "tool_output": tool_output
                        }
                    )

                print("----------------------------------Tool Calls ------------------------------")
                print(tool_output)
                print("----------------------------------Tool Calls ------------------------------")



        return agent_output



def main():
    agent = AgentSimple(
    name="AgentSimple", 
    api_key_path=api_key_path,
    model="gpt-5-mini", 
    role="You are a travel planner", 
    instructions = "Given the city and the request, use the tools to provide the best information to the user", 
    tools={}
    )


if __name__ == "__main__":
    main()