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
Edge module for workflow edge management
in the Laeyerz framework.
"""


import uuid

class EdgeCondition:

    def __init__(self, condition, action):
        self.condition = condition
        self.action    = action




class Edge:
    #def __init__(self, source, target, label, condition=None):
    def __init__(self, source_node, source_action, target_node, target_action,  label, isConditional=False, condition=None):
        print("Creating Edge : ", source_node, source_action, target_node, target_action, label, isConditional, condition)
        
        self.id = str(uuid.uuid4())
       # self.source = source
        self.source_node = source_node
        self.source_action = source_action
        
        #self.target = target
        self.target_node = target_node
        self.target_action = target_action

        self.isConditional = isConditional
        self.condition     = None
        self.label = label

        if condition is None:
            self.condition = lambda x: True
        else:
            self.condition = condition

    def __str__(self):
        return f"Edge(id={self.id}, source_node={self.source_node}, source_action={self.source_action}, target_node={self.target_node}, target_action={self.target_action}, label={self.label})"


    def next_node(self):

        #for now not conditional

        return self.target_node, self.target_action

    def to_dict(self):
        return {
            "id": str(self.id),
            "source_node": self.source_node,
            "target_node": self.target_node,
            "source_action": self.source_action,
            "target_action": self.target_action,
            "label": self.label,
            "isConditional": str(self.isConditional),
            #"condition": self.condition,
        }

        