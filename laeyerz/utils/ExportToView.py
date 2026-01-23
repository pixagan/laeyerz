import json

def export_to_view(flow, filename):

    view_data = {}
    view_data["title"] = flow.name

    nodelist = []
    datasources = []
    nDatasources = 0


 
    inputlist = []
    for key, value in flow.inputs.items():
        inputlist.append(key)

    #Inputs
    inputNode = {
        "id": 'INPUTS',
        "name": 'INPUTS',
        "data": { 
            "label": 'INPUTS',
            "action": 'INPUTS-FLOW',
            "inputs": [],
            "outputs": inputlist,
        },
        "type": 'cNode',
        "position": { "x": 0, "y": 0 },
        "inputs": [],
        "outputs": inputlist,
        "code": 'print("Hello, World!")',
        "state": 'idle',
        "action": 'chatInput',
                
    }

    nodelist.append(inputNode)

    for action in flow.active_actions:

        node_str = action.split("|")
        node_id = action

        source_node   = node_str[0]
        source_action = node_str[1]

        curr_node     = flow.nodes[source_node]

        curr_action    = curr_node.actions[source_action]
        action_inputs  = curr_action.inputs
        action_outputs = curr_action.outputs

        node_inputs = []
        for cinput in action_inputs:
            node_inputs.append(cinput['name'])
            if(cinput['final_source']['node'] == "INPUTS"):
                source = "INPUTS"
            else:
                source = cinput['final_source']['node'] + "|" + cinput['final_source']['action']
            datasources.append(
                {
                    "id": str(nDatasources),
                    "name": node_id + "|" + cinput['name'],
                    "source": source,
                    "sourceHandle": source + "|" + cinput['final_source']['socket'],
                    "target": node_id,
                    "targetHandle": node_id + "|" + cinput['name'],
                }
            )
            nDatasources += 1

        node_outputs = []
        for iout, coutput in enumerate(action_outputs):
            node_outputs.append(coutput['name'])

        newNode = {
            "id": node_id,
            "name": node_id,
            "data": {
                "label": node_id,
                "action": node_id+"-FLOW",
                "inputs": node_inputs,
                "outputs": node_outputs,
            },
            "type": "cNode",
            "position": { "x": 0, "y": 0 },
            "inputs": node_inputs,
            "outputs": node_outputs,
            "code": "",
        }

        nodelist.append(newNode)




    node_outputs = []
    for iout, coutput in enumerate(flow.flow_outputs):
        node_outputs.append("output" + str(iout+1))

        
        output_node   = coutput["node"]
        output_action = coutput["action"]
        output_socket = coutput["socket"]

        datasources.append({
            "id": str(nDatasources),
            "name": "OUTPUTS" + "|" + "output" + str(iout+1),
            "source": output_node + "|" + output_action,
            "sourceHandle": output_node + "|" + output_action + "|" + output_socket,
            "target": "OUTPUTS",
            "targetHandle": "OUTPUTS|" + "output" + str(iout+1),
        })
        nDatasources += 1

 


    #Output Node
    outputNode = {
            "id": 'OUTPUTS',
            "name": 'OUTPUTS',
            "inputs": ['output1'],
            "outputs": [],
            "type": "cNode",
            "position": { "x": 50, "y": 50 },
            "data": { 
              "label": 'Outputs',
              "action": 'END-FLOW',
              "inputs": node_outputs,
              "outputs": [],
            }
        }

    nodelist.append(outputNode)


    view_data["nodes"] = nodelist


    


    #---------Edges ----------------------


    edgelist = []
    for key, edge in flow.edges.items():
        print(edge)
        source = ""
        target = ""
        if(edge.source_node == "START"):
            source = "INPUTS"
        else:
            source = edge.source_node + "|" + edge.source_action


        if(edge.target_node == "END"):
            target = "OUTPUTS"
        else:
            target = edge.target_node + "|" + edge.target_action
        
        

        edge_data = {
            "id": str(edge.id),
            "source": source,
            "target": target,
            "type": "edge",
        }
        edgelist.append(edge_data)



    view_data["edges"] = edgelist

    view_data["datasources"] = datasources


    with open(filename, 'w') as file:
        json.dump(view_data, file)



    #data sources

    #  {
    #         id: '1',
    #         name: 'DataSource 1',
    #         source: 'Inputs',
    #         sourceHandle: 'Inputs|input1',
    #         target: 'Node_1',
    #         targetHandle: 'Node_1|input1',
    #     },

