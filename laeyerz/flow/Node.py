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
Node module for defining workflow nodes
in the Laeyerz framework.
"""
import uuid

from laeyerz.flow.AppState import AppState

from laeyerz.utils.Dictify import dictify


class NodeConfig:
    def __init__(self):

        self.api_key = ""
        


class NodeInputMap:

    def __init__(self, inputs):
        self.source = ""
        self.value  = ""
        self.type   = ""

    def get_inputs(self):
        return self.inputs

    def set_inputs(self, inputs):
        self.inputs = inputs


class NodeOutputMap:

    def __init__(self, outputs):
        self.outputs = outputs

    def get_outputs(self):
        return self.outputs

    def set_outputs(self, outputs):
        self.outputs = outputs




def default_function():
    print(f"Running Node ")
    return {"output": "Dummy Node run"}


class Action:

    def __init__(self, action_name, function, parameters={}, inputs=[], outputs=[], description=""):
        self.id = str(uuid.uuid4())
        self.action_name = action_name
        self.function    = function
        self.inputs      = inputs
        self.parameters  = parameters
        self.outputs     = outputs
        self.description = description


    def run(self, inputs):
        return self.function(**inputs)


    def add_input(self, input_in):
        self.inputs.append(input_in)


    def get_tools(self):

        tool_dict = {
            "name": self.action_name,
            "description": self.description,
            "description": self.function.description,
            "inputs": self.inputs,
            "outputs": self.outputs,
        }
        return self.function.get_tools()


    def to_dict(self):

        action_dict = {
            "id": self.id,
            "action_name": self.action_name,
            "function": "",
            "inputs": self.inputs,
            "parameters": self.parameters,
            "outputs": self.outputs,
            "description": self.description,
        }

        return action_dict

    



class NodeInput:
    def __init__(self, name, type, description):
        self.name = name
        self.type = type
        self.description = description
        self.sourceType = ""
        self.options = []
        self.required = True
        self.default  = None
        self.value    = ""



class NodeOutput:
    def __init__(self, name, type, description):
        self.name = name
        self.type = type
        self.description = description


class Node:

    def __init__(self, node_name, description="", config={}):
        self.id       = str(uuid.uuid4())
        self.metadata = {
            "node_type": "",
            "node_subtype": "",
        }
        self.view = {
            "view_type": "",
            "view_subtype": "",
        }
        self.name     = node_name
        self.action   = ""
        self.description = description
        self.input_map = []
        self.output_map = []
        self.inputs  = []
        self.outputs = []
        self.input_parser  = None
        self.output_parser = None
        self.function  = default_function
        self.sources = []
        self.targets = []
        self.current_action = None
        

        self.actions = {}
        self.action_map = {}
        

        self.config = {} #NodeConfig()
        
        self.setup()

        self.inputs = []
        self.out = None


    def __str__(self):
        return f"Node(id={self.id}, type={self.nodetype}, name={self.name}, inputs={self.inputs},description={self.description})"


    def setup(self):
        print(f"Setting up node {self.name}")

    def unpack_inputs(self):
        for key, value in self.inputs.items():
            key_split = key.split(":")
            section = key_split[0]
            iid = key_split[1]
            key_val = app_state.get(section, iid)
            # print("Key Val : ", key_val)
            node_inputs[value] = key_val[key]

        return node_inputs


    def pack_outputs(self, result):
        for index, (key, value) in enumerate(self.outputs.items()):
            value_split = value.split(":")
            section = value_split[0]
            iid = value_split[1]
            app_state.update(section, iid, result[index])


    def add_action(self, action_name, function, parameters={}, inputs=[], outputs=[], isDefault=False, description=""):

        if action_name not in self.actions:

            if (len(outputs) > 0):
               #output_keys = [{"key": output["name"], "type": output["type"]} for output in outputs]
               output_keys = [output["name"] for output in outputs]
            else:
                output_keys = None
            function2 = dictify(function, output_keys)

            #function2 = function

            newAction = Action(action_name=action_name, function=function2, inputs=inputs,parameters=parameters, outputs=outputs, description=description)
            self.actions[action_name] = newAction

            if isDefault:
                self.current_action = newAction
                self.function       = newAction.function
                self.inputs         = newAction.inputs
                self.parameters     = newAction.parameters
                self.outputs        = newAction.outputs

            print("Adding Action : ", action_name)
                

        else:
            print(f"Action {action_name} already exists. Use a different action name.")


    def set_action(self, action_name:str):
        self.current_action = action_name
        print("Action Name : ", action_name)
        print("Action Map : ", self.action_map)
        selected_action = self.action_map.get(action_name)

        #selected_action     
        self.function       = selected_action.function
        self.inputs         = selected_action.inputs
        self.parameters     = selected_action.parameters
        self.outputs        = selected_action.outputs



    def get_actions(self):
        return self.actions

    def set_function(self, function_name, function_in, parameters={}, inputs=[], outputs=[], isDefault=True, description=""):
        self.function = function_in
        self.add_action(function_name, function_in, parameters, inputs, outputs, isDefault, description)


    def set_node(self, node_in):
        self.id = node_in["id"]
        self.metadata    = node_in["metadata"]
        self.view        = node_in["view"]
        self.name        = node_in["name"]
        self.description = node_in["description"]
        self.inputs  = node_in["inputs"]
        self.outputs = node_in["outputs"]
        self.action_map = []
        self.current_action = None


    def map_inputs(self, app_state):
        for input in self.inputs:
            if input in self.input_map:
                app_state.update(input, self.input_map[input])
            else:
                app_state.update(input, None)

 

    def run(self, action_name, node_inputs):

        #unpack inputs
        #node_inputs = {}

        print("Inputs : ", self.inputs)
        print("Current Action : ", self.current_action)


        print(f"Node inputs: {node_inputs}")

        # for key, value in self.inputs.items():
        #     key_split = key.split(":")
        #     section = key_split[0]
        #     iid = key_split[1]
        #     key_val = app_state.get(section, iid)
        #     node_inputs[value] = key_val[key]

        #validate inputs

        #result = self.function(**node_inputs)

        result = self.actions[action_name].function(**node_inputs)

        print("Result : ", result)


        #if isinstance(result, tuple):
        # for index, (key, value) in enumerate(self.outputs.items()):
        #     value_split = value.split(":")
        #     section = value_split[0]
        #     iid = value_split[1]
        #     app_state.update(section, iid, result[index])

        # next_node = self.next_node(result, app_state)

        next_node = {}

        return result



    def map_outputs(self, app_state):
        for output in self.outputs:
            if output in self.output_map:
                app_state.update(output, self.output_map[output])
            else:
                app_state.update(output, None)



    def get_inputs(self):
        return self.inputs
    
    def get_outputs(self):
        return self.outputs


    def to_dict(self):

        return {
            "node_id": str(self.id),
            'id': self.name,
            'name': self.name,
            'metadata': self.metadata,
            'view': self.view,
            # 'node_subtype': self.node_subtype,
            # 'node_type': self.node_type,
            'description': self.description,
            'actions': [],
            'inputs': self.inputs,
            'outputs': self.outputs
            }

            #'action': self.action,


    def next_node(self, inputs, app_state):

        if self.targets == []:
            return 'END_NODE'

        if len(self.targets) == 1:
            return self.targets[0]

        if len(self.targets) > 1:
            for target in self.targets:
                isNext = target.evaluate(inputs, app_state)
                if isNext:
                    return target
                else:
                    return None
        
        return None



    def get_settings(self):

        actions = {
            "actions":self.actions,
            "current_action":self.current_action,
        }
        return actions


    def set_settings(self, settings):
        self.actions = settings["actions"]
        self.current_action = settings["current_action"]
        self.params = settings["params"]

  


def main():


    node = Node(id='1', nodetype='custom', name='Custom Node', description='Run the code')
    print(node)
    

    def custom_function(text):
        """This is a custom function that takes a text parameter"""

        print(f"Input: {text}")
        result = text + " How are you?"
        print(f"Processing: {result}")
        return {"processed_text": result}

    # Set a custom function
    node.set_function(custom_function)
    node.inputs = ['text']  # Define expected input
    node.outputs = ['processed_text']  # Define expected output
    
    # Get the function code as text

    app_state = AppState()
    app_state.update('text', 'Hello, World!')

    print(f"App state: {app_state}")


    function_code = node.run(app_state)
    print("Function code:")
    print(function_code)

    #node.run()

if __name__ == '__main__':
    main()