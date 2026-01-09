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
FAISS module for FAISS vector store operations
in the Laeyerz framework.
"""
# FAISS Adapter

import faiss
from sklearn.preprocessing import normalize
import numpy as np
import uuid

from laeyerz.flow.Node import Node

class FaissNode(Node):

    def __init__(self, node_name, config={}, vector_dim=384, alog="flat"):
        super().__init__(node_name, config)
        print("Faiss Indexing")

        
        self.vector_dim  = vector_dim
        self.index       = None

        self.index = faiss.IndexFlatL2(vector_dim)
        self.metadata = []

        self.add_actions()



    def store(self, vectors, metadata):

        if(len(metadata) != len(vectors)):
            raise ValueError("Metadata and vectors must be of the same length") 

        # for md in metadata:
        #     md['id'] = str(uuid.uuid4())
            
        self.index.add(vectors)
        self.metadata.extend(metadata)


    def search(self, query_vector, k=3):

        distances, indices = self.index.search(query_vector, k)

        print("saved metadata : ",indices, distances)

        results = []
        for i in range(len(indices[0])):
            index = indices[0][i]
            results.append({
                #"id":str(self.metadata[int(index)]["id"]),
                "metadata":self.metadata[int(index)],#["metadata"],
                "score":str(distances[0][int(i)])
            })

        

        return {"results":results}


    def clear(self):
        self.index = None
        self.metadata = []


    def export(self, filename):

        faiss.write_index(self.index, "vector_index.faiss")



    def load(self, filename):

        self.index = faiss.read_index("vector_index.faiss")


    def add_actions(self):
        store_inputs = [
            {
                "name":"vectors",
                "type":"list",
                "description":"The vectors to add",
                "inputType":"input",
                "source":"",
                "value":None

            },
            {
                "name":"metadata",
                "type":"list",
                "description":"The metadata to add",
                "inputType":"input",
                "source":"",
                "value":None
            }
        ]
        store_outputs = []
        self.add_action(action_name="store", function=self.store, parameters=[], inputs=store_inputs, outputs=store_outputs, isDefault=True, description="Add vectors to the FAISS index")

        search_inputs = [
            {
                "name":"query_vector",
                "type":"list",
                "description":"The query vector to search for",
                "inputType":"input",
                "source":"",
                "value":None
            },
            {
                "name":"k",
                "type":"int",
                "description":"The number of results to return",
                "inputType":"input",
                "source":"",
                "value":None
            }
        ]
        search_outputs = [
            {
                "name":"results",
                "type":"list",
                "description":"The search results",
                "outputType":"output",
                "source":"",
                "value":None
            }
        ]
        self.add_action(action_name="search", function=self.search, parameters=[], inputs=search_inputs, outputs=search_outputs, isDefault=True, description="Search the FAISS index")






def main():

    
    # Example: Create random vectors
    num_vectors = 100
    vector_dim  = 128

    vectors = np.random.rand(num_vectors, vector_dim).astype('float32')
    vectors = normalize(vectors, axis=1)


    vector_store = FaissNode("FaissNode", config={}, vector_dim=vector_dim)

    vector_store.store(vectors)

    distances, indices = vector_store.search(vectors[1].reshape(1,-1),3)

    print(distances, indices)


#----------------------------------------------------------------------

if __name__ == "__main__":
    main()



