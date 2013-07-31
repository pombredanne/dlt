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
import unittest
from dlt.tokenizer import Tokenizer
from dlt.parser import Parser
from copyright import two_fp_with_invalid_field


class ParserTest(unittest.TestCase):
    def test_default_init(self):
        tokenizer = Tokenizer()
        paragraphs = tokenizer.get_paragraphs(two_fp_with_invalid_field)
        parser = Parser()
        self.assertFalse(parser.process(paragraphs))

    def _test_data_is_none(self):
        dlt_parser = Parser()
        self.assertRaises(TypeError, dlt_parser.parse, None)

    def _test_data_is_empty(self):
        data = ""
        dlt_parser = Parser()
        data_parsed = dlt_parser.parse(data)
        self.assertEqual(data_parsed, [])

    def _test_format_with_initial_null_lines(self):
        data = "\n\n\nFormat: %s" % self.url
        dlt_parser = Parser()
        data_parsed = dlt_parser.parse(data.splitlines(True))
        for paragraph in data_parsed:
            paragraph_content = paragraph["content"]
            self.assertEqual("header", paragraph["type"])
            for field in paragraph_content:
                field_content = field["content"]
                self.assertTrue("Format" in field_content)
                self.assertEqual(field_content["Format"][0].strip(), self.url)
                self.assertEqual("single_line_values", field["type"])
