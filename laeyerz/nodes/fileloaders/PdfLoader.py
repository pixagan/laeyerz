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
DocLoad module for document loading operations
in the Laeyerz framework.
"""

import fitz
from laeyerz.flow.Node import Node

class PdfLoader(Node):

    def __init__(self, node_name, config={}):
        super().__init__(node_name, description="Pdf Loader Node")
        print("Loading Doc")


        node_inputs = [
            {
                "name":"filename",
                "type":"string",
                "description":"The filename of the PDF file to load",
                "inputType":"input",
                "source":"",
                "value":None
            }
        ]

        node_outputs = [
            {
                "name":"doc_pages",
                "type":"list",
                "description":"The pages of the PDF file",
                "outputType":"output",
                "source":"",
                "value":None
            }
        ]

        extract_inputs = [
            {
                "name":"loaded_file",
                "type":"file",
                "description":"The PDF file to extract text from",
                "inputType":"input",
                "source":"",
                "value":None
            }
        ]

        self.add_action(action_name="load_pdf", function=self.load_pdf, parameters=[], inputs=node_inputs, outputs=node_outputs, isDefault=True, description="Load a PDF file")
        self.add_action(action_name="extract_pdf_text", function=self.extract_pdf_text, parameters=[], inputs=extract_inputs, outputs=node_outputs, isDefault=True, description="Extract text from a PDF file")





    def extract_pdf_text(self,loaded_file):

        print("Loaded File : ", loaded_file)
        #contents = await loaded_file.read()

        contents = loaded_file

        # Open PDF from bytes
        doc = fitz.open(stream=contents, filetype="pdf")

        full_text = ""

        doc_pages = []

        for page_num, page in enumerate(doc, start=1):
            page_text = page.get_text()
            page_text = page_text.replace("\xa0", " ").strip()
            doc_pages.append({
                "page": page_num,
                "content": page_text
            })

        doc.close()

        print("Doc Pages : ", doc_pages)

        return {"doc_pages": doc_pages}



    def extract_pdf_blocks(self,loaded_file):

        print("Loaded File : ", loaded_file)
        #contents = await loaded_file.read()

        contents = loaded_file

        # Open PDF from bytes
        doc = fitz.open(stream=contents, filetype="pdf")

        full_text = ""

        doc_pages = []

        for page_num, page in enumerate(doc, start=1):

            blocks = page.get_text("blocks")

            print(f"\n--- Page {page_num+1} ---")

            for block in blocks:
                x0, y0, x1, y1, text, block_no, block_type = block

                if text.strip():
                    print(f"\nBlock bbox: ({x0:.1f}, {y0:.1f}, {x1:.1f}, {y1:.1f})")
                    print(text.strip())
            
            doc_pages.append({
                "page": page_num,
                "content": page_text
            })

        doc.close()

        print("Doc Pages : ", doc_pages)

        return {"doc_pages": doc_pages}



    def extract_pdf_dict(self, loaded_file):

        print("Loaded File : ", loaded_file)

        contents = loaded_file

        # Open PDF from bytes
        doc = fitz.open(stream=contents, filetype="pdf")

        full_text = ""

        doc_pages = []

        count = 0
        for page_num, page in enumerate(doc):
            text_dict = page.get_text("dict")

            print(f"\n--- Page {page_num+1} ---")

            for block in text_dict["blocks"]:
                if block["type"] == 0:  # text block
                    block_text = ""

                    for line in block["lines"]:
                        for span in line["spans"]:
                            block_text += span["text"] + " "

                    block_text = block_text.strip()

                    if block_text:
                        print("\nBLOCK:")
                        print(block_text)

            count += 1
            if count > 1:
                break
        

    

    def load_pdf(self, filename:str)->(list):
        print("Loading Doc")

        doc = fitz.open(filename)
        doc_pages = []

        for page_num, page in enumerate(doc, start=1):
            blocks = page.get_text("blocks")  # Extract text blocks

            blocks.sort(key=lambda b: (b[1], b[0]))  # Sort blocks by vertical (y), then horizontal (x) positions

            # Estimate median X position to identify columns
            x_coords = [block[0] for block in blocks]
            median_x = (max(x_coords) + min(x_coords)) / 2

            left_column = []
            right_column = []

            for block in blocks:
                x0, y0, x1, y1, text, _, _ = block
                if x0 < median_x:
                    left_column.append((y0, text))
                else:
                    right_column.append((y0, text))

            # Sort each column vertically
            left_column.sort()
            right_column.sort()

            # Combine columns: left first, then right
            page_text = [text for _, text in left_column + right_column]

            doc_pages.append({
                "page": page_num,
                "content": "\n".join(page_text)
            })

        return {"doc_pages": doc_pages}





if __name__ == "__main__":
    pdf_loader = PdfLoader("PdfLoader")
    document   = pdf_loader.load_pdf("test.pdf")