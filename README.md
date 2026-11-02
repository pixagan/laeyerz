# Laeyerz is an open source python tool to help students and developers quickly prototype workflows and agents

## License

Laeyerz is licensed under the [Apache License 2.0](LICENSE).

This means you are free to use, modify, and distribute this software in
source or binary form, provided you comply with the terms of the license.
See the [NOTICE](NOTICE) file for attribution requirements.

## Getting started
Installing from git repo

You can find the source code in the [GitHub repository](https://github.com/pixagan/laeyerz).

Download the repository and install the dependencies.

```bash
git clone https://github.com/pixagan/Laeyerz.git
cd laeyerz
pip install -r requirements.txt
```

Now use pip install -e . to install the package locally.

```bash
pip install -e .
```

## You can get started with our quickstart below
## You can checkout more examples with out laeyerz example repository
https://github.com/pixagan/laeyerz-examples


# Creating an Agent with Laeyerz

### initialize an LLM Node as the reasoner for the agent
```python
from laeyerz_nodes.llm.OpenAINode import OpenAINode as LLM
reasoner_llm =  LLM("AgentReasoner",  config={"api_key": api_key, "model":"gpt-5-mini"})
```
### Define the role and instructions for the agent
```python
role = "You are an Expense Classifier"
instructions = """You will be given a message describing the transaction. .... with the transaction details.

Tools provided
add_income : Update the income database
add_expense: Update the expense database
"""
```

### Initialize the Agent
```python
from laeyerz.agent.Agent import Agent
agent = Agent( name="IncomeExpenseClassifier", config = {
        "reasoner":reasoner_llm, 
        "role":role, 
        "instructions":instructions, 
        "tools":{}
})
```

### Adding a Tool to the agent
```python
agent.add_tool({
    "name": "name_of_the_function",
    "description": "description_of_the_function",
    "inputs": [
        {
            "name": "input_variable_name",
            "type": "input_type : string/number",
            "description": "A description of the input variable"
        },
        ...
    ],
    "outputs": [a list of the output variables and types similar to input],
    "function": tool_function()
})
```
### Allowable Input Output Data Types
- string
- number
- integer
- boolean
- object
- array


### Running the Agent
Define the inputs as a dictionary, use the agent.run_agent() function as shown belwo.
```python
agent_inputs = {
 "input1":input1
}
agent_response = agent.run_agent(task=agent_inputs, write_to_file=True)
```

### What the Agent Returns
The agent returns teh output, steps showing the breakdown of steps, the task keypoints, and the reasoner's llm usage
```python
{
    "outputs": user_response, 
    "steps": steps, 
    "usage": total_usage, 
    "task_keypoints": task_keypoints
}
```

# To Create a Graph based Workflow
## Let us now create our first simple Workflow Graph using Laeyerz.


### Import the Node and Flow
```python
from laeyerz.flow.Flow import Flow
from laeyerz.flow.Node import Node
```

### The two functions that handle compute

```python
def model0(input0:str)->(str):

    print("Model 0 :", input0)

    output = input0+"_model0"
    outputs = { 
        "output0":output
    }

    return outputs
```

```python
def model1(input1:str)->(str):

    print("Model 1 :", input1)

    output = input1 + "_model1"

    outputs = {
        "output1":output
    }

    return outputs
```


### Create a Node for the first function
### Define the inputs and outputs

```python
node0 = Node("Model0")
node0_inputs = [
    {
        "name":"input0",
        "type":"str",
        "description":"Input to the model",
        "inputType":"source",
        "source":"INPUTS|input0",
        "value":None
    }
]
node0_outputs = [
    {
        "name":"output0",
        "type":"str",
        "description":"Output from the model"
    }
]
node0.set_function("model0",model0, params, node0_inputs, node0_outputs)
```

### Create the second Node for the first function
### Define the inputs and outputs
```python
node1 = Node("Model1")
node1_inputs = [
    {
        "name":"input1",
        "type":"str",
        "description":"Input to the model",
        "inputType":"source",
        "source":"Model0|model0|output0",
        "value":None
    }
]
node1_outputs = [
    {
        "name":"output1",
        "type":"str",
        "description":"Output from the model"
    }
]
node1.set_function("model1",model1, params, node1_inputs, node1_outputs)
```


### Create a workflow and add Nodes

```python
simple_flow = Flow("Flow 1")
simple_flow.add_node(node0)
simple_flow.add_node(node1)
```

### Define you node inputs either as value or as a connection
```python
simple_flow.add_edge("START", "Model0|model0")
simple_flow.add_edge("Model0|model0", "Model1|model1")
simple_flow.add_edge("Model1|model1", "END")
```

### Add edges to order how Laeyerz's Orchestrator organizes compute
```python
simple_flow.add_edge("START", "Model0|model0")
simple_flow.add_edge("Model0|model0", "Model1|model1")
simple_flow.add_edge("Model1|model1", "END")
```

##define what outputs you want returned at the end of the flow
```python

input_data = {
     "input0": "Hello, world!"
}
output = simple_flow.run(input_data)
```


### Setup the inputs as a dictionary and then run the flow

```python

input_data = {
     "input0": "Hello, world!"
}
output = simple_flow.run(input_data)
```


### The flow returns
```python
{
    "outputs": ,
    "steps": 
}
```



# Code of Conduct

We are committed to providing a safe, inclusive, and welcoming environment.

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported to [pixagan@gmail.com].
