from laeyerz.nodes.Node import Node


class LLMOutputParser(Node):

    def __init__(self, node_name, config={}):
        super().__init__(node_name, config)


    def extract_open_ai_json(self, llm_out, format, values,):

        content = llm_out.get("content")



        print("Extracting OpenAI JSON from text")


        
    def add_actions(self):
        self.add_action(action_name="extract_open_ai_json", function=self.extract_open_ai_json, inputs=["text"], outputs=["text"])