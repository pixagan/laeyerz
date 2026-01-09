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
Flow module for managing workflow execution
in the Laeyerz framework.
"""
import uuid
import json

from laeyerz.flow.Node import Node  
from laeyerz.flow.AppState import AppState, GraphState
from laeyerz.flow.Edge import Edge
from laeyerz.flow.Evals import Evals
from laeyerz.flow.Observe import Observe

class Flow:

    def __init__(self,name=""):

        self.id             = str(uuid.uuid4())
        self.name           = name
        self.description    = ""
        
        self.nodes          = {}
        self.node_map       = {}
        self.node_id_map    = {}
        self.nodelist       = []
        self.node_path      = {}

        self.edges          = {}
        self.edge_map       = {}
        self.edgelist       = []
        
        self.graph_state    = GraphState()
        self.state          = AppState()

        self.components     = {}
        self.components_map = {}
        self.flowtype       = "workflow"

        self.start = None
        self.end   = None

        self.max_steps = 50

        self.output = ""

        self.steps = []

        self.inputs = {}

        self.flow_outputs = []


    def get_node(self, node_id):

        for node in self.nodes:
            if(node.id == node_id):
                return node

        return None



    def set_flow(self, flow_in):

        self.id = flow_in["id"]
        self.name = flow_in["name"]
        self.description = flow_in["description"]

        for node in flow_in["nodes"]:
            newNode = Node(node)
            self.nodes.append(newNode)




    def load_file(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data


    def create_node(self, title, function_in):
        newNode = Node(title)
        newNode.set_function(function_in)
        self.nodes.append(newNode)
        return newNode


    def add_node(self, node):

        for key, cAction in node.actions.items():
            for iI,cinput in enumerate(cAction.inputs):
                if(cinput['source'] and cinput['source'] != "" and cinput['source'] != None):
                    source_split = cinput['source'].split("|")
                    node_name = source_split[0]
                    if(node_name == "INPUTS"):
                        source = {
                            "node":"INPUTS",
                            "action":"INPUTS",
                            "socket":source_split[1]
                        }
                    elif(node_name == "GLOBAL"):
                        source = {
                            "node":"GLOBAL",
                            "action":"GLOBAL",
                            "socket":source_split[1]
                        }
                    else:
                        source = {
                            "node":source_split[0],
                            "action":source_split[1],
                            "socket":source_split[2]
                        }
                    node.actions[key].inputs[iI]['final_source'] = source
                    node.actions[key].inputs[iI]['inputType'] = "source"
        
        self.nodes[node.name] = node
        self.nodelist.append(node.name)

        for key, value in node.actions.items():
            self.graph_state.add_section(node.name+"|"+key)




    def add_data_source(self, data_socket_name, data_source_type):

        #get selected node
        data_socket_split = data_socket_name.split("|")
        socket_node        = data_socket_split[0]
        socket_action_name = data_socket_split[1]
        socket_input_name  = data_socket_split[2]
        
        #get the sources
        source_split = data_source_type.split("|")
        node_name = source_split[0]
        source = {}
        if(node_name == "INPUTS"):
                source = {
                    "node":"INPUTS",
                    "action":"INPUTS",
                    "socket":source_split[1]
                }
        elif(node_name == "GLOBAL"):
            source = {
                "node":"GLOBAL",
                "action":"GLOBAL",
                "socket":source_split[1]
            }
        else:
            source = {
                "node":source_split[0],
                "action":source_split[1],
                "socket":source_split[2]
            }

        for cinput in self.nodes[socket_node].actions[socket_action_name].inputs:
            if(cinput['name'] == socket_input_name):
                cinput['final_source'] = source
                cinput['inputType'] = "source"
                break
        #self.nodes[socket_node].actions[socket_action_name].inputs[socket_input_name]['source'] = source

        return True

       


    def set_node_input(self,data_socket_name, value ):
        data_socket_split = data_socket_name.split("|")
        socket_node        = data_socket_split[0]
        socket_action_name = data_socket_split[1]
        socket_input_name  = data_socket_split[2]

        for cinput in self.nodes[socket_node].actions[socket_action_name].inputs:
            if(cinput['name'] == socket_input_name):
                cinput['value'] = value
                cinput['inputType'] = "value"
                break

        return True



    def set_node_outputs(self, outputs):

        flow_outputs = []
        for output in outputs:
            output_split = output.split("|")
            flow_outputs.append({
                "node": output_split[0],
                "action": output_split[1],
                "socket": output_split[2]
            })
        self.flow_outputs = flow_outputs


    def run_node(self, node_name, inputs):
        
        outputs, next_node = self.nodes[node_name].run(inputs)

        return outputs


    def delete_node(self, node_name):

        if(node_name == "START"):
            self.start = None
            return True

        if(node_name == "END"):
            self.end = None
            return True


        if(node_name != 'START' and node_name != 'END' and node_name in self.nodelist):
            del self.nodes[node_name]
            self.graphstate.remove_section(node_name)
            self.nodelist.remove(node_name)
            return True

        return False




    def get_node_state(self, node_name):
        return self.graphstate.get_section(node_name)



    def add_edge(self, source, destination, isConditional=False, condition=None):

        #check if source == "START, destination = "END"
        if(source == "START" and destination == "END"):
            self.start = None
            self.end   = None

            return True


        if(source == "START" and destination != "END"):
            destination_split  = destination.split("|")
            destination_node   = destination_split[0]
            destination_action = destination_split[1]
            


            newEdge = Edge("START", "START", destination_node, destination_action, "START"+"-"+destination_action, False, None)
            self.edges[newEdge.id] = newEdge
            self.edgelist.append(newEdge.id)
            self.nodes[destination_node].sources.append(newEdge.id)
             
            #self.node_path[destination_node+"|"+destination_action] = newEdge.id

            self.start      = destination_node
            self.start_edge = newEdge.id
            #self.nodes[destination_node].sources.append("START")
            
            
            return True
            
            
            

        if(source != "START" and destination == "END"):
            source_split = source.split("|")
            source_node = source_split[0]
            source_action = source_split[1]

            newEdge = Edge(source_node, source_action, "END", "END", source_action + "-" + "END", False, None)
            self.edges[newEdge.id] = newEdge
            self.edgelist.append(newEdge.id)

            self.nodes[source_node].targets.append(newEdge.id)
            self.node_path[source_node+"|"+source_action] = newEdge.id
            self.end = source_node
            self.end_edge = newEdge.id
            #self.nodes[source_node].targets.append("END")

            return True


        if(source != "START" and destination != "END"):
            source_split = source.split("|")
            source_node = source_split[0]
            source_action = source_split[1]

            destination_split = destination.split("|")
            destination_node = destination_split[0]
            destination_action = destination_split[1]

            newEdge = Edge(source_node, source_action, destination_node, destination_action, source_action + "-" + destination_action, False, None)
            self.edges[newEdge.id] = newEdge
            self.edgelist.append(newEdge.id)

            self.nodes[source_node].targets.append(newEdge.id)
            self.node_path[source_node+"|"+source_action] = newEdge.id
            self.nodes[destination_node].sources.append(newEdge.id)
            
            
            return True

        

    def delete_edge(self, edge_id):

        for edge in self.edges:
            print("Match edge : ", edge.id, edge_id)
            if(str(edge.id) == str(edge_id)):
                print("Removing edge : ", edge.id, edge.label)

                print(edge.to_dict())

                #remove connection from nodes
                if(edge.source != "START" and edge.target != "END"):
                    self.nodes[self.node_map[edge.source]].targets.remove(edge.target)
                    self.nodes[self.node_map[edge.target]].sources.remove(edge.source)
                    self.edges.remove(edge)
                    return True

                if(edge.source == "START"):
                    self.start = None
                    self.nodes[self.node_map[edge.target]].sources.remove(edge.source)
                    self.edges.remove(edge)

                    #update app state

                    return True
                
                if(edge.target == "END"):
                    self.end = None
                    self.nodes[self.node_map[edge.source]].targets.remove(edge.target)
                    self.edges.remove(edge)
                    return True


        return False
        


    def finalize(self):
        print("Finalizing Flow : ")



    def run(self, input_data):

        print("Input Data : ", input_data)

        self.inputs = input_data
        for key, value in input_data.items():
            self.graph_state.update_state('INPUTS', key, value)
        print("Graph State : ", self.graph_state.state)
         

        #get first edge from START
        curr_edge = self.edges[self.start_edge]
        
        nSteps = 0

        print("------------------------------------------------")
        print("-------------- Starting Flow : ", self.name)
        print("------------------------------------------------")

        while curr_edge is not None:

            next_node, next_action = curr_edge.next_node()

            if(next_action == "END"):
                break

            print("------------------------------------------------")
            print("Running Node : ", next_node, next_action)
            print("------------------------------------------------")
            
            curr_node = self.nodes[next_node]

            inputd = {}

            for it, cinput in enumerate(curr_node.actions[next_action].inputs):

                print("Cinput : ", cinput)

                if(cinput['inputType'] == "source"):

                    if(cinput['final_source']['node'] == "INPUTS"):
                        inputd[cinput['name']] = self.graph_state.get_values('INPUTS', cinput['final_source']['socket'])
                    
                    elif(cinput['final_source']['node'] == "GLOBAL"):
                        inputd[cinput['name']] = self.graph_state.get_values("GLOBAL", cinput['final_source']['socket'])
                    else:
                        inputd[cinput['name']] = self.graph_state.get_values(cinput['final_source']['node']+"|"+cinput['final_source']['action'], cinput['final_source']['socket'])


                elif(cinput['inputType'] == "value"):
                    inputd[cinput['name']] = cinput['value']
                
            #run the action
            outputs = curr_node.actions[next_action].function(**inputd)


            print("Outputs : ", len(outputs))
            #pack the graph state with the outputs
            #print("Outputs : ", outputs)
            for key, value in outputs.items():
                self.graph_state.update_state(next_node+"|"+next_action, key, value)



            #get next edge
            next_edge = self.node_path[next_node+"|"+next_action]
            
            #next_edge = curr_node.targets[0]
            print("Next Edge : ", next_edge)
            curr_edge = self.edges[next_edge]



        run_outputs = {}

        try:
            for output_label in self.flow_outputs:
                run_outputs[output_label['node']+"|"+output_label['action']+"|"+output_label['socket']] = self.graph_state.get_values(output_label['node']+"|"+output_label['action'], output_label['socket'])
        except Exception as e:
            print("Error getting outputs : ", e)
            run_outputs = {}

        return run_outputs


    def to_dict(self):

        nodes_str = []
        for key, node in self.nodes.items():
            nodes_str.append(node.to_dict())
        
        edges_str = []
        for key, edge in self.edges.items():
            edges_str.append(edge.to_dict())
        
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "nodes": nodes_str, 
            "edges": edges_str,
            "state": {}
            }


    def to_view(self):

        nodes_str = []

        startNode = {
          "id": 'START',
          "name": 'START',
          "node_id": 'START',
          "component": 'TextInput',
          "data": { 
            "label": 'START',
            "action": 'START-FLOW'
          },
          "type": 'cNode',
          "position": { "x": 0, "y": 0 },
          "inputs": ['text'],
          "outputs": ['text'],
          "code": 'print("Hello, World!")',
          "state": 'idle',
          "action": 'chatInput',
          "style": {
            "backgroundColor": "#e3d274",
          }
        }

        nodes_str.append(startNode)

        x_str = 0. + 10.0
        y_str = 0. + 70.0

        for node in self.nodes:

            newNode = {
                "id": node.name,
                "node_id": node.id,
                "name": node.name,
                "component": 'General',
                "data": { 
                    "label": node.name,
                    "action": 'UPDATE'
                },
                "type": 'cNode',
                "position": { "x": x_str, "y": y_str },
                "inputs": node.inputs,
                "outputs": node.outputs,
                "state": 'idle',
                "action": 'chatInput',
                "style": {
                    "backgroundColor": "#e3d274",
                }
                }
            nodes_str.append(newNode)

            x_str = x_str + 10.0
            y_str = y_str + 70.0
        
        

        endNode = {
          "id": 'END',
          "name": 'END',
          "node_id": 'END',
          "component": 'TextInput',
          "type": 'cNode',
          "position": { "x": x_str, "y": y_str },
          "data": { 
            "label": 'END',
            "action": 'END-FLOW'
          },
          "style": {
            "backgroundColor": "#e3d274",
          }
        }

        nodes_str.append(endNode)

        for node in nodes_str:
            print("--------------------------------")
            print("Node : ", node)
            print("--------------------------------")



        edges_str = []

        for edge in self.edges:
            edges_str.append(edge.to_dict())
        
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "nodes": nodes_str, 
            "edges": edges_str,
            "state": {}
            }






    def set_node_action(self, node_id, action_name):
        self.nodes[self.node_id_map[node_id]].set_action(action_name)
        return action_name


   

    def set_action(self, component, action):

        action_function = self.components[component].get_action(action)

        self.appflow.set_action()



    def update_node_title(self, node_id, title):
        self.nodes[self.node_id_map[node_id]].name = title

        return self.nodes[self.node_id_map[node_id]].to_dict()



    def finalize_flow(self):
        for node in self.nodes:
            node.finalize()


    def validate_flow(self):
        for node in self.nodes:
            node.validate()



    def export_flow(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.to_dict(), file)
        return True


def main():

    flow = Flow()


if __name__ == "__main__":
    main()