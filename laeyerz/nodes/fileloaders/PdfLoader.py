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

        self.add_action(action_name="load_pdf", function=self.load_pdf, parameters=[], inputs=node_inputs, outputs=node_outputs, isDefault=True, description="Load a PDF file")


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