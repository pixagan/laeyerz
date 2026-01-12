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
OpenAILLMNode module for OpenAI LLM integration
in the Laeyerz framework.
"""
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import io
from laeyerz.flow.Node import Node


class OpenAILLMNode(Node):

    def __init__(self, node_name, config={}, instructions=None):
        super().__init__(node_name=node_name, description='OpenAI LLM Node')
        self.metadata = {
            "node_type": "OpenAI",
            "node_subtype": "LLM",
        }
        self.view = {
            "view_type": "OpenAI",
            "view_subtype": "LLM",
        }

        self.instructions = instructions

        self.client = None

        if(config.get('api_key')):
            self.client = OpenAI(api_key=config.get('api_key'))
        else:
            print("No API key provided")
            raise ValueError("No API key provided")

        
        #adding llm actions
        node_inputs = [
            {
                "name":"messages",
                "type":"list",
                "description":"The input messages to the model",
                "inputType":"input",
                "source":"",
                "value":None
            },
            {
                "name":"model",
                "type":"str",
                "description":"Input to the model",
                "inputType":"input",
                "source":"",
                "value":None
            },
            {
                "name":"tools",
                "type":"list",
                "description":"Input to the model",
                "inputType":"input",
                "source":"",
                "value":None
            }
        ]
        node_outputs = [
            {
                "name":"content",
                "type":"string",
                "description":"Output from the llm model"
            },
            {
                "name":"tokens",
                "type":"object",
                "description":"Tokens Output"
            },
            {
                "name":"finish_reason",
                "type":"string",
                "description":"Finish reason for the llm model"
            },
            {
                "name":"tool_calls",    
                "type":"list",
                "description":"Tool calls for the llm model"
            }
        ]
        self.add_action(action_name="call_llm", function=self.call_llm, parameters=["model"], inputs=node_inputs, outputs=node_outputs, isDefault=True, description="Call the OpenAI LLM")
        
        
        self.config = config
        self.instructions = instructions
    

    def setup(self):
        print(f"Setting up node {self.name}")

    #def call_llm(self, inputs):
    def call_llm(self, messages, model, tools=[]):

        #messages = inputs.get('messages')
        #model    = inputs.get('model')
        #tools    = inputs.get('tools')
        #output_format = inputs.get('output_format')

        #print("Messages : ", messages)
        #print("Model : ", model)
        #print("Tools : ", tools)

        if(self.instructions):
            messages.insert(0, {"role":"developer", "content":self.instructions})

        response = self.client.chat.completions.create(
                model=model,
                messages = messages,
                tools = tools,
                tool_choice = "auto"
        )

        message       = response.choices[0].message
        finish_reason = response.choices[0].finish_reason
        tool_calls    = response.choices[0].message.tool_calls


        outputs = self.response_parser(response)
        return outputs



    def response_parser(self, response):

        #response = 

        parsed_response = {
            "completion_id": response.id,
            "model": response.model,
            "message": response.choices[0].message,
            "content": response.choices[0].message.content,
            "created": response.created,
            "finish_reason": response.choices[0].finish_reason,
            #"usage": response.usage,
            "tokens":{
                "model": response.model,
                "total_tokens": response.usage.total_tokens,
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "service_tier": response.service_tier,
            },
            "service_tier": response.service_tier,
            "tool_calls": [],
        }


        tool_calls = response.choices[0].message.tool_calls

        tool_call_extracted = []

        if tool_calls:
            #print("Tool calls : ", tool_calls)
            for tc in tool_calls:
                tc_id   = tc.id
                tc_type = tc.type
                tc_function = {
                    'arguments': json.loads(tc.function.arguments),
                    'name': tc.function.name,
                }
                tool_call_extracted.append({
                    "id": tc_id,
                    "type": tc_type,
                    "function": tc_function,
                })

        parsed_response["tool_calls"] = tool_call_extracted
        

        return parsed_response



    def generate_image(self, model, prompt, nImages, size='1024x1024'):
        
        img_response = self.client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            n=nImages
        )

        image_bytes = base64.b64decode(img_response.data[0].b64_json)
        return image_bytes




# Return the configured node
if __name__ == "__main__":
    # For testing the node

    llm_node = OpenAILLMNode("LLM", "gpt-4o-mini")

    llm_node.call_llm({"messages": [{"role": "user", "content": "Hello, how are you?"}], "model": "gpt-4o-mini"})
  
    
    # result, next_node = OpenAINode.run(app_state)
    # print(f"Result: {result}")
    # print(f"Next node: {next_node}")






