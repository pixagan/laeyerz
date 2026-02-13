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
MongoNode module for MongoDB database operations
in the Laeyerz framework.
"""

from laeyerz.flow.Node import Node


#import os
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

# filepath = os.getenv('MONGO_URI')
# mongo_db = os.getenv('MONGO_DB')



class MongoNode(Node):

    def __init__(self, node_name, config={}):
        super().__init__(node_name, config)
        self.client = MongoClient(config.get('MONGO_URI'))
        self.db     = self.client[config.get('MONGO_DB')]
        print("MongoNode initialized", self.client, self.db, config.get('MONGO_URI'), config.get('MONGO_DB'))
        #self.collection = self.db[config.get('MONGO_COLLECTION')]


    def create_collection(self, collection_name):
        """Create a new collection in MongoDB"""
        newCollection = self.db[collection_name]
        return newCollection


    def get_collection(self, collection_name):
        """Get a collection from MongoDB"""
        return self.db[collection_name]


    def create_document(self, collection_name, data):
        """Create a new document in MongoDB"""

        data["created_at"] = datetime.now()
        data["updated_at"] = datetime.now()
       
        newItem = self.db[collection_name].insert_one(data)

        return newItem



    def create_many(self, collection_name, data_list):
        
        print("Creating many",collection_name, data_list)
        
        self.db[collection_name].insert_many(data_list)
        
        

    def load_all_documents(self, collection_name):
        """Read documents matching the query"""
        return self.db[collection_name].find()



    def load_documents(self, collection_name, query):
        """Read documents matching the query"""
        return self.db[collection_name].find(query).to_list(length=None)


    def load_document_id(self, collection_name, id):
        """Read documents matching the query id"""
        if isinstance(id, str):
            document_id = ObjectId(id)
        else:
            document_id = id
        return self.db[collection_name].find_one({"_id": document_id})


    def check_document_exists(self, collection_name, query):
        """Check if a document exists in the collection"""
        return self.db[collection_name].find_one(query) is not None


    def load_document(self, collection_name, query):
        """Read a single document matching the query"""
        return self.db[collection_name].find_one(query)



    def update_document_id(self, collection_name, document_id, new_values):
        """Update documents matching the query"""
        query = {"_id": ObjectId(do2cument_id)}
        update_operation = { '$set' : 
            new_values
        }
        return self.db[collection_name].update_one(query, update_operation)
       


    def update_document(self, collection_name, query, new_values):
        """Update documents matching the query"""
        update_operation = { '$set' : 
            new_values
        }
        return self.db[collection_name].update_one(query, update_operation)
       

    def delete_document_id(self, collection_name, document_id):
        """Delete a document matching the query"""
        return self.db[collection_name].delete_one({"_id": ObjectId(document_id)})



    def delete(self, collection_name, query):
        """Delete documents matching the query"""
        return self.collection.delete_many(query)



    def close(self):
        """Close the MongoDB connection"""
        self.client.close()