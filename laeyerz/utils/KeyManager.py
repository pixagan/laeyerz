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
KeyManager module for API key management
in the Laeyerz framework.
"""

import os
import inspect
from pathlib import Path
import json
from dotenv import load_dotenv
from dotenv import dotenv_values
#load_dotenv()



class KeyManager:
    
    def __init__(self, filename=None):
        print("Load API Keys")
        self.key_path = filename
        self.keys = {}

        if filename is None:

            keys_path = self.find_local_env()
            if keys_path is None:
                raise ValueError("No .env file provided with API keys")
            else:
                keys = self.load_file(keys_path)
                self.keys = dict(keys)
         
        else:

            keys_path = Path(filename).expanduser().resolve()
            if not keys_path.exists():
                raise FileNotFoundError(f"Key file not found: {keys_path}")
            else:
                keys = self.load_file(keys_path)
            self.keys = dict(keys)


    def load_file(self, path: Path) -> dict:
        
        if path.name == ".env" or path.name.startswith(".env.") or path.suffix == ".env":
            keys = dotenv_values(path)

        elif path.suffix == ".json":
            with open(path) as f:
                keys = json.load(f)
        else:
            raise ValueError(f"Unsupported key file type: {path.suffix}")

        return dict(keys)


    def find_local_env(self) -> Path | None:
        # caller = file that instantiated KeyManager
        frame = inspect.stack()[2]
        caller_file = Path(frame.filename).resolve()
        env_path = caller_file.parent / ".env"

        return env_path if env_path.exists() else None


    def __getitem__(self, key: str) -> str:
        if key not in self.keys:
            raise KeyError(f"Missing key: {key}")
        return self.keys[key]


    def loadKeys(self):
        with open(self.key_path, 'r') as file:
            keys = json.load(file)
            self.keys = keys
        print("Keys")


    def get(self, key: str, default=None):
        return self.keys.get(key, default)


    def checkKeyExists(self, key):
        if key in self.keys:
            return True
        else:
            return False


    def get_keys(self):
        return self.keys


#----------------------------------------------------------------------


def main():

 
    km = KeyManager()


   


#----------------------------------------------------------------------

if __name__ == "__main__":
    main()


#----------------------------------------------------------------------

     