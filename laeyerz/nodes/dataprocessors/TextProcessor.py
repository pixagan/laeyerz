from laeyerz.flow.Node import Node

class TextProcessorNode(Node):

    def __init__(self, node_name, config={}):
        super().__init__(node_name, config)

        self.add_actions()
        

    def process(self, text):
        return text


    def combine_pages(self, pages):

        text = ""

        for page in pages:
            text = text + page["content"]

        return {"text": text}


    def split_text(self, text, chunk_size = 200, padding = 30):

        sentences = text.split(".")
    
        chunks = []
        current_chunk = ""

        for sentence in sentences:

            current_chunk = current_chunk + sentence
            chunk_length = len(current_chunk.split(" "))
            if(chunk_length>chunk_size):
                chunks.append(current_chunk)
                current_chunk = ""


        return {"chunks": chunks}


    def page_to_chunks(self, text):

        return text



    def add_actions(self):

        combine_pages_inputs = [
            {
                "name":"pages",
                "type":"list",
                "description":"The pages of the PDF file",
                "inputType":"input",
                "source":"",
                "value":None
            }
        ]

        combine_pages_outputs = [
            {
                "name":"text",
                "type":"string",
                "description":"The combined text of the pages",
                "outputType":"output",
                "source":"",
                "value":None
            }
        ]
        self.add_action(action_name="combine_pages", function=self.combine_pages, parameters=[], inputs=combine_pages_inputs, outputs=combine_pages_outputs, isDefault=True, description="Combine the pages of the PDF file")
        

        split_text_inputs = [
            {
                "name":"text",
                "type":"string",
                "description":"The text to split",
                "inputType":"input",
                "source":"",
                "value":None
            }
        ]
        split_text_outputs = [
            {   
                "name":"chunks",
                "type":"list",
                "description":"The chunks of the text",
                "outputType":"output",
                "source":"",
                "value":None
            }   
        ]
        self.add_action(action_name="split_text", function=self.split_text, parameters=[], inputs=split_text_inputs, outputs=split_text_outputs, isDefault=True, description="Split the text into chunks")
        
       
