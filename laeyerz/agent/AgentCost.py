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

#Cost Model focussed on the reasoner

class AgentCost:

    def __init__(self):
        self.cost = 0
        self.breakdown = []
        self.total_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
        }

    def add_usage(self, step, tool_name, usage):

        self.breakdown.append({
            "step": step,
            "module": tool_name,
            "usage": usage
        })

        self.total_usage["prompt_tokens"] += usage["prompt_tokens"]
        self.total_usage["completion_tokens"] += usage["completion_tokens"]


    def get_usage_breakdown(self):
        return self.cost

    def get_total_usage(self):

        usage = {
            "prompt_tokens": self.total_usage["prompt_tokens"],
            "completion_tokens": self.total_usage["completion_tokens"],
        }
        return usage

    def reset_usage(self):
        self.breakdown = []
        self.total_usage = {}