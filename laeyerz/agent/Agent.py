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

from datetime import datetime
import json

from laeyerz.flow.Node import Node
from laeyerz.utils.KeyManager import KeyManager
from laeyerz.flow.Steps import Steps
from laeyerz.agent.ToolPalette import ToolPalette
from laeyerz.agent.Reasoner import Reasoner
from laeyerz.agent.AgentState import AgentState
from laeyerz.agent.Responder import Responder
from laeyerz.agent.Planner import Planner
from laeyerz.agent.AgentCost import AgentCost

class Agent(Node):

    def __init__(self, name, config):
        super().__init__(name, config)

        self.name    = name
        api_key_path = config.get("api_key_path")
        reasoner     = config.get("reasoner")
        role         =  config.get("role")
        instructions = config.get("instructions")
        tools        = config.get("tools")
        self.agent_type = "Smart"


        if(config.get('max_steps')):
            self.max_steps = config.get("max_steps")
        else:
            self.max_steps = 20
        
        
        #self.model = model
        self.role = role
        self.agent_instructions = instructions   

        self.tool_palette = ToolPalette("ToolPalette", config={
            "tools": tools
        })

        self.km = None
        if api_key_path:
            self.km = KeyManager(api_key_path)
        else:
            self.km = None


        self.reasoner = Reasoner("Reasoner", config={
            "llm": reasoner
        })

        self.responder = Responder("Responder", config={
            "llm": reasoner
        })

        self.planner = Planner("Planner", config={
            "llm": reasoner
        })

        if(tools):
            for tool in tools:
                self.add_tool(tool)



          


        self.add_actions()

    


    def add_tool(self, tool):
        print("Adding tool: ", tool["name"])

        self.tool_palette.add_tool(tool)


    def finalize(self):
        print("Finalize Agent")


    def run_agent(self, task, write_to_file=False):
        print(f"Running agent {self.name} with task {task}")


        #todos = []

        state   = AgentState('AgentState', config={})

        tool_descriptions = self.tool_palette.get_tool_descriptions()

        print("----------------------------------Tools Provided ------------------------------")
        tool_list = self.tool_palette.tool_list
        for tool in tool_list:
            print(tool["name"])
        print("-------------------------------------------------------------------")
        


        #plan = self.planner.plan_task(self.agent_instructions, tool_descriptions)
        #print("Plan: ", plan)
        plan = {}

        state.update_plan(plan)

        self.reasoner.initialize(self.role, task, self.agent_instructions, tool_descriptions, plan)
        

        nSteps         = 0
        nReasonerSteps = 0
        nToolSteps     = 0
        isCompleted    = False
        agent_output   = {}
        completion_status = {
            "status": "in_progress",
            "n_steps": 0,
            "n_reasoner_steps": 0,
            "n_tool_steps": 0,
            "stopping_criterion":"na"
        }

        #total_usage = []

        agent_cost = AgentCost() 


        state.set_task(task)

        

        while not isCompleted:

            #----- Reason --------------------
            reasoner_input = state.get_state()
            response = self.reasoner.reason(state.get_state())

            #print("Reasoner Response: ", response)

            finish_reason = response['finish_reason']
            tool_calls    = response['tool_calls']
            usage         = response['usage']

            agent_cost.add_usage(nSteps, "reasoner", usage)

            # total_usage.append({
            #     "step": nSteps,
            #     "module": "reasoner",
            #     "tokens": usage
            # })

            state.add_step({
                "step": nSteps,
                "type":"reasoner",
                "name":"Reasoner_LLM",
                "content": response["content"],
                "finish_reason": response['finish_reason'],
                "tool_calls": response['tool_calls'],
                "inputs":{
                    "state": reasoner_input
                },
                "outputs":{
                    "content": response["content"],
                    "finish_reason": response['finish_reason'],
                    "tool_calls": response['tool_calls']
                }
            })

            print("\n")
            print("----------------------------------Reasoning " + str(nSteps) + " ------------------------------")
            print(response["content"])
            print("Tool Calls : ", response['tool_calls'])
            print("----------------------------------Reasoning ------------------------------")
            print("\n")

            nReasonerSteps += 1
            nSteps += 1

            completion_status["n_reasoner_steps"] = nReasonerSteps
            completion_status["n_steps"] = nSteps

            if nSteps > self.max_steps:
                isCompleted = True
                agent_output = {
                    "output": response["content"]
                }
                completion_status["status"] = "stopped"
                completion_status["stopping_criterion"] = "max_steps"
                print("----------------------------------Max Steps Reached ------------------------------")
                print("Max steps reached, stopping agent.")
                break

            #----- Tool Runs ---------------------

            if finish_reason == "tool_calls":
                for tool_call in tool_calls:
                    tool_name = tool_call['name']
                    tool_args = tool_call['arguments']

                    tool_output = self.tool_palette.run_tool(tool_name, tool_args)

                    state.add_step({
                        "step": nSteps,
                        "type":"tool",
                        "name":tool_name,
                        "content": tool_output,
                        "inputs":{
                            "tool_name": tool_name,
                            "tool_args": tool_args
                        },
                        "outputs":{
                            "tool_output": tool_output
                        }
                    })

                    print("\n")
                    print("----------------------------------Tool Response " + str(nSteps) + " ------------------------------")
                    print(tool_output)
                    print("----------------------------------Tool Response ------------------------------")
                    print("\n")


                    nToolSteps += 1
                    nSteps += 1


            elif finish_reason == "stop":
                isCompleted = True
                agent_output = {
                    "output": response["content"]
                }
                completion_status["status"] = "completed"
                completion_status["stopping_criterion"] = "completed"
                break

            #-------- Update Observations --------------------


        # Formulating final response




        print("\n")
        print("----------------------------------Agent Response ------------------------------")
        print(agent_output)
        print("----------------------------------Agent Response ------------------------------")
        print("\n")

        steps = state.get_steps()

        user_response, task_keypoints, requested_parameters, responder_usage = self.responder.respond(task,  self.agent_instructions, agent_output, steps, completion_status)

        # total_usage.append({
        #     "step": nSteps,
        #     "module": "responder",
        #     "tokens": responder_usage
        # })

        agent_cost.add_usage(nSteps, "responder", responder_usage)


        total_usage = agent_cost.get_total_usage()

        agent_output = {
            "output": user_response,
            "task_keypoints": task_keypoints,
            "requested_parameters": requested_parameters,
            "usage": total_usage
        }

       

        if write_to_file:
            self.export_run(task, steps, {}, agent_output)

        return {"outputs": agent_output, "steps": steps}



    def export_run(self, task, steps, context, agent_output):
        print("Writing Agent Run to File")


        curr_date = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{self.name}_{curr_date}.json"

        with open(file_name, "w") as f:
            json.dump({
                "task": task,
                "steps": steps,
                "context": context,
                "agent_output": agent_output["output"],
                "requested_parameters": agent_output["requested_parameters"],
                "task_keypoints": agent_output["task_keypoints"]
            }, f)



    def export_model(self):

        tools = []

        tool_descriptions = self.tool_palette.get_tool_descriptions()

        for tool in tool_descriptions:
            newTool = {
                "type": "function",
                "name": tool["function"]["name"],
                "description": tool["function"]["description"],
                "inputs":[]
            }

            for name, value in tool["function"]["parameters"]["properties"].items():
                newTool["inputs"].append({
                    "name": name,
                    "type": value["type"],
                    "description": value["description"]
                })
            tools.append(newTool)


        agent_model = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "config":{},
            "tools": tools,
            "reasoner": {
                "model": self.reasoner.model,
            },
            "config":{
                "max_steps": self.max_steps
            }
        }
        return agent_model



    def add_actions(self):

        node_inputs = [
            {
                "name":"task",
                "type":"dict",
                "description":"The input task to the agent",
                "inputType":"input",
                "source":"",
                "value":None
            },
        ]
        node_outputs = [
            {
                "name":"outputs",
                "type":"dict",
                "description":"Output from the agent"
            },
            {
                "name":"steps",
                "type":"list",
                "description":"Steps taken by the agent"
            },
        ]
        self.add_action(action_name="run_agent", function=self.run_agent, parameters=["task"], inputs=node_inputs, outputs=node_outputs, isDefault=True, description="Run the agent")
        