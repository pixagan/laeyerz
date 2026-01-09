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
SentenceTransformerAdapter module for sentence transformer embeddings
in the Laeyerz framework.
"""

from laeyerz.flow.Node import Node
from sentence_transformers import SentenceTransformer


class SentenceTransformerNode(Node):

    def __init__(self, node_name, config={}, model_name='paraphrase-MiniLM-L6-v2'):
        print("Initializing Sentence Transformer")
        super().__init__(node_name, config)
        
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name

        self.add_actions()


    def encode(self, sentences):
        print("")

        embeddings = self.model.encode(sentences)

        return embeddings       #list of embeddings



    def add_actions(self):

        encode_inputs = [
            {
                "name":"sentences",
                "type":"list",
                "description":"The sentences to encode",
                "inputType":"input",
                "source":"",
                "value":None
            }
        ]

        encode_outputs = [
            {
                "name":"embeddings",
                "type":"list",
                "description":"The embeddings of the sentences",
                "outputType":"output",
                "source":"",
                "value":None
            }
        ]

        self.add_action(action_name="encode", function=self.encode, parameters=[], inputs=encode_inputs, outputs=encode_outputs, isDefault=True, description="Encode the sentences")



def main():
    print("Starting Sentence Transformer Adapter")
    sentence_transformer_adapter = SentenceTransformerNode()
    sentence_transformer_adapter.encode(["Hello, how are you?"])
    print("Sentence Transformer Adapter started")



if __name__ == "__main__":
    main()