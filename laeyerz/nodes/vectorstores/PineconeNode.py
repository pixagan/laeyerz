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
Pinecone module for Pinecone vector store operations
in the Laeyerz framework.
"""
# Pinecone Adapter

#import os
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec

#PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')


class PineconeAdapter(Node):
    
    def __init__(self, node_name, config={}, spec=None):

        self.pc   = Pinecone(api_key=config.get('api_key'))
        self.spec = ServerlessSpec(cloud='aws', region='us-east-1')


    def setup(self, config):
        print("Setting up Pinecone")

       # self.create_index(config['name'], config['dimension'], config['metric'], config['spec'])


    def create_index(self, name, dimension=1024, metric="cosine", spec=None):
        print("Creating collection")

        self.create_index(name, dimension, metric, self.spec)

    

    def generate_embeddings(self, data, model="multilingual-e5-large"):
        #Generate Embeddings using deployed models

        embeddings = self.pc.inference.embed(
            model=model,
            inputs=[d['text'] for d in data],
            parameters={"input_type": "passage", "truncate": "END"}
        )

        return embeddings.data

    
    #Index -----

    def check_index(self, index_name):
        #check if index exists
        return self.pc.has_index(index_name)
    
    def create_index(self, index_name='default', dimension=1024, metric="cosine", spec=None):
        #Creating the index
        
        if self.spec is None:
            self.spec = ServerlessSpec(cloud='aws', region='us-east-1')

        if not self.pc.has_index(index_name):
            self.pc.create_index(
                name=index_name,
                dimension=dimension,
                metric=metric,
                spec=self.spec
            )

        while not self.pc.describe_index(index_name).status['ready']:
            time.sleep(1)



    def delete_index(self, index_name):
        #delete the index

        self.pc.delete_index(index_name)

    
    #-----Vectors
    

    def insert_vectors(self, index_name, data, embeddings, namespace="demo1-namespace"):
        #insert vectors

        index = self.pc.Index(index_name)

        records = [
            {
            "id": d['id'], 
             "values": e, 
             "metadata": {'text': d['text']}
            }
            for d, e in zip(data, embeddings)]

        index.upsert(vectors=records, namespace=namespace)
        

    def search(self, index_name, query_embedding, k_nearest=3, namespace="demo1-namespace"):
        #query
        
        index = self.pc.Index(index_name)
        
        results = index.query(
            namespace=namespace,
            vector=query_embedding,
            top_k=k_nearest,
            include_values=False,
            include_metadata=True
        )

        clean_out = []

        for result in results['matches']:
            clean_out.append({
                "id": result['id'],
                "metadata": result['metadata'],
                "score": result['score']
            })
        
        return clean_out



    def modify_vectors(self, index_name, id, values, metadata, namespace="demo1-namespace"):
        #modify vectors
        

        index = self.pc.Index(index_name)

        index.update(
        	id=id, 
        	values=values, 
        	set_metadata=metadata,
        	namespace=namespace
        )

    
        
    def delete_vector(self, index_name, vector_ids, namespace='demo1-namespace'):
        #delete vectors
        
        index = self.pc.Index(index_name)
        index.delete(ids=vector_ids, namespace=namespace)
        



    def add_actions(self):
        
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
        self.add_action(action_name="store", function=self.call_llm, parameters=["model"], inputs=node_inputs, outputs=node_outputs, isDefault=True, description="Call the OpenAI LLM")
        
        self.add_action(action_name="search", function=self.call_llm, parameters=["model"], inputs=node_inputs, outputs=node_outputs, isDefault=True, description="Call the OpenAI LLM")

#----------------------------------------------------------------------




def main():

    pc = PineconeAdapter()
 

    text = [
       "At Swiggy, our mission is to elevate the quality of life for urban consumers by offering unparalleled convenience. Innovation has been an integral part of our DNA which encourages us to ideate, experiment and iterate constantly with the focus on identifying and addressing convenience needs of our users at the core of our innovation approach.",
       "Being among the first hyperlocal commerce platforms, Swiggy has successfully pioneered the industry in India, launching Food Delivery in 2014. Today, Swiggy offers its Food Delivery service in 653 cities across India serving ~13mn users1 through a wide network of 196k restaurant partners2. Our sharp focus on innovation coupled with strong execution yielded yet another milestone - we became one of the very few global food delivery platforms to achieve EBITDA profitability in less than 9 years since inception.",
       "We also pioneered Quick Commerce in India with the launch of Instamart in 2020, offering on-demand grocery and a growing array of household items delivered to our users in less than 10-15 minutes. We have successfully scaled our Quick Commerce offering to 27 cities delivering a wide array of ~17k SKUs through a dense network of 523 active dark stores."
        
    ]

    pc.create_index()

    pc.insert(insert_vectors)




#----------------------------------------------------------------------

if __name__ == "__main__":
    main()


#----------------------------------------------------------------------



def pinecone_function(inputs):
    """Pinecone function that processes inputs and returns output"""
    # Extract inputs - you can customize this based on your needs
    chunks = inputs.get('text', '')
    embedding_model = inputs.get('model', 'gpt-3.5-turbo')
    
    # Placeholder for OpenAI API call
    # In a real implementation, you would call the OpenAI API here
    response = f"Faiss processed: {text} using {model}"
    
    return {"output": response}


def create_pinecone_node(node_name):
    """Factory function to create and return an PineconeNode"""
    # Create the PineconeNode with proper initialization
    PineconeNode = Node(
        node_type='Pinecone',
        node_subtype='Vector Store',
        node_name=node_name,
        description='Node for Pinecone API interactions'
    )

    # Set the function and configure inputs/outputs
    PineconeNode.action = 'Pinecone Vector Store call'
    PineconeNode.set_function(pinecone_function)
    PineconeNode.inputs = ['text', 'model']  # Expected input parameters
    PineconeNode.outputs = ['output']  # Expected output parameters
    
    return PineconeNode


# Create a default instance
#FaissNode = create_faiss_node()


# Return the configured node
if __name__ == "__main__":
    # For testing the node
    from laeyerzflow.flow.AppState import AppState
    
    app_state = AppState()
    app_state.update('text', 'Hello from OpenAI!')
    app_state.update('model', 'gpt-4')
    
    # result, next_node = OpenAINode.run(app_state)
    # print(f"Result: {result}")
    # print(f"Next node: {next_node}")






