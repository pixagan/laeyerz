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

class DataConnections:

    def __init__(self, node_id):
        self.node = node_id
        self.connections = []
        self.actions = {}


    def add_action(self, node_in, action_in, data):
        self.actions[node_in + "|" + action_in] = {
            "node":data['node'],
            "action":data['action'],
            "socket":data['socket']
        }


    def add_data_source(self, data_socket_name, data_source_type, data):
        self.actions[data_socket_name] = data_source_type


    def set_node_outputs(self, node_id, outputs):
        for output in outputs:
            output_split = output.split("|")
            self.connections.append({
                "node": output_split[0],
                "action": output_split[1],
                "socket": output_split[2]
            })

    def get_connections(self, node_in, action_in):
        return self.connections[node_in + "|" + action_in]
