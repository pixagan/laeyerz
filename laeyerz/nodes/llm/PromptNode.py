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

"""
PromptNode module for prompt management
in the Laeyerz framework.
"""

from laeyerz.flow.Node import Node

class PromptNode(Node):

    def __init__(self, node_name, config={}, template=None):
        super().__init__(node_name, config)
        self.template = template
        
        self.add_actions()
     


    def generate_prompt_openai(self, *args, **kwargs):

        print("Args : ", args)
        print("Kwargs : ", kwargs)
        print("------------------------------------------------")

        messages = []

        for key, value in kwargs.items():
            messages.append({
                "role": self.template["roles"][key],
                "content": value
            })


        return {"messages": messages}




    def add_prompt_inputs(self, inputs):

        for cinput in inputs:
            newInput = {
                "name":cinput["name"],
                "type":cinput["type"],
                "description":"",
                "inputType":"source",
                "source":"",
                "value":""
            }

            if  "source" in cinput and cinput["source"]:
                newInput["source"] = cinput["source"]

            if  "value" in cinput and cinput["value"]:
                newInput["value"] = cinput["value"]

            self.actions["generate_prompt_openai"].add_input(newInput)
            


    def add_actions(self):

        prompt_inputs = []

        prompt_outputs = [
            {
                "name":"messages",
                "type":"list",
                "description":"The messages to pass to the OpenAI API",
                "outputType":"output",
                "source":"",
                "value":None
            }
        ]

        self.add_action(action_name="generate_prompt_openai", function=self.generate_prompt_openai, parameters=[], inputs=prompt_inputs, outputs=prompt_outputs, isDefault=True, description="Convert inputs into a prompt for LLMs")

