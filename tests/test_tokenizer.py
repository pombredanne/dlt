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


class TokenizerTest(unittest.TestCase):
    def test_data_is_none(self):
        tokenizer = Tokenizer()
        self.assertRaises(TypeError, tokenizer.get_paragraphs, None)

    def test_one_paragraph_one_token(self):
        tokenizer = Tokenizer()
        data = "Files: foobar.foo"
        tokenized_data = tokenizer.get_paragraphs(data.splitlines(True))
        self.assertEqual(len(tokenized_data), 1)
        first_paragraph = tokenized_data[0]
        self.assertEqual(len(first_paragraph), 1)
        first_field = list(first_paragraph)[0]
        self.assertEqual(first_field.line_number, 1)
        self.assertEqual(first_field.name, "Files")
        self.assertEqual(list(first_field)[0], " foobar.foo")

    def test_one_paragraph_three_tokens(self):
        tokenizer = Tokenizer()
        data = """
Files: foobar.foo
Copyright: Foo Bar <foo@bar.com>
License: Beerware

"""
        tokenized_data = tokenizer.get_paragraphs(data.splitlines(True))
        self.assertEqual(len(tokenized_data), 1)
        first_paragraph = tokenized_data[0]
        self.assertEqual(len(first_paragraph), 3)
        first_field = list(first_paragraph)[0]
        self.assertEqual(first_field.line_number, 2)
        self.assertEqual(first_field.name, "Files")
        self.assertEqual(list(first_field)[0], " foobar.foo\n")
        second_field = list(first_paragraph)[1]
        self.assertEqual(second_field.line_number, 3)
        self.assertEqual(second_field.name, "Copyright")
        self.assertEqual(list(second_field)[0], " Foo Bar <foo@bar.com>\n")
        third_field = list(first_paragraph)[2]
        self.assertEqual(third_field.line_number, 4)
        self.assertEqual(third_field.name, "License")
        self.assertEqual(list(third_field)[0], " Beerware\n")

    def test_two_paragraph_one_token(self):
        tokenizer = Tokenizer()
        data = """Files: foobar.foo

Copyright: Foo Bar <foo@bar.com>"""
        tokenized_data = tokenizer.get_paragraphs(data.splitlines(True))
        self.assertEqual(len(tokenized_data), 2)
        first_paragraph = tokenized_data[0]
        self.assertEqual(len(first_paragraph), 1)
        first_field = list(first_paragraph)[0]
        self.assertEqual(first_field.line_number, 1)
        self.assertEqual(first_field.name, "Files")
        self.assertEqual(list(first_field)[0], " foobar.foo\n")

    def test_two_paragraph_three_tokens(self):
        tokenizer = Tokenizer()
        data = """

Files: foobar.foo
Copyright: Foo Bar <foo@bar.com>
License: Beerware


Files: sara.sa
Copyright: Sara Sa <sara@sa.com>
License: Vaporware

"""
        tokenized_data = tokenizer.get_paragraphs(data.splitlines(True))
        self.assertEqual(len(tokenized_data), 2)
        first_paragraph = tokenized_data[0]
        self.assertEqual(len(first_paragraph), 3)
        first_field = list(first_paragraph)[0]
        self.assertEqual(first_field.line_number, 3)
        self.assertEqual(first_field.name, "Files")
        self.assertEqual(list(first_field)[0], " foobar.foo\n")
        second_field = list(first_paragraph)[1]
        self.assertEqual(second_field.line_number, 4)
        self.assertEqual(second_field.name, "Copyright")
        self.assertEqual(list(second_field)[0], " Foo Bar <foo@bar.com>\n")
        third_field = list(first_paragraph)[2]
        self.assertEqual(third_field.line_number, 5)
        self.assertEqual(third_field.name, "License")
        self.assertEqual(list(third_field)[0], " Beerware\n")

        second_paragraph = tokenized_data[1]
        self.assertEqual(len(second_paragraph), 3)
        first_field = list(second_paragraph)[0]
        self.assertEqual(first_field.line_number, 8)
        self.assertEqual(first_field.name, "Files")
        self.assertEqual(list(first_field)[0], " sara.sa\n")
        second_field = list(second_paragraph)[1]
        self.assertEqual(second_field.line_number, 9)
        self.assertEqual(second_field.name, "Copyright")
        self.assertEqual(list(second_field)[0], " Sara Sa <sara@sa.com>\n")
        third_field = list(second_paragraph)[2]
        self.assertEqual(third_field.line_number, 10)
        self.assertEqual(third_field.name, "License")
        self.assertEqual(list(third_field)[0], " Vaporware\n")
