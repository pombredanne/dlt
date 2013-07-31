# Copyright 2013 Agustin Henze <tin@sluc.org.ar>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from .base import Field, Paragraph


class Tokenizer(object):
    """A tokenizer of the debian copyright file machine readable compliant.
    The output is a list of Paragraph instances, where each paragraph is
    filled by a list of Field instances.
    """

    def get_paragraphs(self, data):
        """Tokenize the input data, first split the data into paragraph and
        then get the tokens of the paragraph content"""
        tokenized_paragraph = []
        tmp = ""
        current_line_number = 0
        for line_number, line in enumerate(data):
            if len(line.strip()) == 0:
                tokens = self._tokenize_paragraph(tmp, current_line_number)
                if tokens:
                    tokenized_paragraph.append(tokens)
                tmp = ""
            else:
                if not tmp:
                    current_line_number = line_number
                tmp += line
        if tmp:
            data_parsed = self._tokenize_paragraph(tmp, current_line_number)
            if data_parsed:
                tokenized_paragraph.append(data_parsed)
        return tokenized_paragraph

    def _tokenize_paragraph(self, txt, start_line_number):
        """Tokenize a paragraph. Return a list of fields with their respective
        values"""
        paragraph = Paragraph()
        current_field = None
        for line_number, line in enumerate(txt.splitlines(True)):
            if line.startswith(" "):
                if current_field:
                    current_field.add_content(line)
                else:
                    current_field = Field("",
                                          line,
                                          line_number + start_line_number + 1)
                    paragraph.add_field(current_field)
                continue
            line_splited = line.split(":")
            field_name = line_splited[0]
            value = ":".join(line_splited[1:])
            current_field = Field(field_name,
                                  value,
                                  line_number + start_line_number + 1)
            paragraph.add_field(current_field)
        return paragraph
