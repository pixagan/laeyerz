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


import simplejson as json

from laeyerz.flow.Node import Node

class Responder(Node):

    def __init__(self, name, config):
        super().__init__(name, {})

        self.name = name
      

        self.llm = config.get('llm')


    def setup(self):
        self.llm_instructions = """Given the task, the state of the task completion and the steps taken to complete the task,
        you now need to create the response to be returned to the user. The response should have three parts,
        1) The Agent's response using the  Reasoner's Final response and any relevant state parameters. Look for Response section in the task instructions. If not explicitly specified, look through the instructions and the task for any relevant requests on what the agent's output should be.
        Format the response accordingly.
        
        2) the parameters specifically requested by the user, if any, which you need to extract from the state, this is the response to the user
        and 
       
       
        3) a summary of the steps taken to complete the task, show this as keypoints, each point a minimal summary of the step taken.
        Respond in the following json format:
        {
            "response": "The Agent's response using the  Reasoner's Final response and any relevant state parameters. Based on what the user has requested in the task, format the response accordingly.",
            "requested_parameters": {
                "parameter_name": "parameter_value",
                "parameter_name": "parameter_value",
                ...
            } , // the parameters specifically requested by the user, if any, which you need to extract from the state, this is the response to the user
            "keypoints": [
                "Summary of the step taken",
                "Summary of the step taken",
                ...
            ] // a keypoint summary of the task completed
        }
        """


    def respond(self, task, agent_instructions, agent_response, state, completion_status):

        messages = [
            {
                "role": "system",
                "content": self.llm_instructions
            },
            {
                "role": "user",
                "content": f"The instructions given to the agent for extraction of the response format and required parameters if any: {agent_instructions}"
            },
            {
                "role": "user",
                "content": f"Task: {task}"
            },
            {
                "role": "user",
                "content": f"The Reasoners's Final Response to the task: {agent_response}"
            },
            {
                "role": "user",
                "content": f"Completion Status: {completion_status}"
            },
            {
                "role": "user",
                "content": f"State: {state}"
            },
        ]

        response = self.llm.call_llm(messages)

        content = response["message"].content

        content = json.loads(content)

        user_response = content["response"]
        requested_parameters = content["requested_parameters"]
    
        task_keypoints = content["keypoints"]

        usage = response["tokens"]

        return user_response, task_keypoints, requested_parameters, usage