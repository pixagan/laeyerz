# Laeyerz is a Graph based llm workflow and agent builder app

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


## Let us now create our first simple workflow graph using Laeyerz.


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

### Add edges to order how Laeyerz's Orchestrator organizes compute
```python
simple_flow.add_edge("START", "Model0|model0")
simple_flow.add_edge("Model0|model0", "Model1|model1")
simple_flow.add_edge("Model1|model1", "END")
```

### Setup the inputs and then run the flow

```python

input_data = {
     "input0": "Hello, world!"
}
output = simple_flow.run(input_data)
```


# Code of Conduct

We are committed to providing a safe, inclusive, and welcoming environment.

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported to [contact@pixagan.com].