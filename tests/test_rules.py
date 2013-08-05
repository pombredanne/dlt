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
from dlt.rules import FieldType, ParagraphType, CheckHasHeader, RepeatedFields
from copyright import (two_fp_with_invalid_field, invalid_single_line_values,
                       invalid_header, invalid_file, invalid_standalone,
                       two_headers, two_fp_without_header, header,
                       repeated_fields)


class RuleTest(unittest.TestCase):
    def setUp(self):
        self.tokenizer = Tokenizer()
        self.parser = Parser()

    def get_paragraphs(self, txt):
        paragraphs = self.tokenizer.get_paragraphs(txt)
        self.parser._guess_types(paragraphs)
        return paragraphs

    def print_messages(self, rule):
        for message in rule.messages:
            self.parser._print_message(message)


class FieldTypeTest(RuleTest):
    def test_invalid_field_type(self):
        paragraphs = self.get_paragraphs(two_fp_with_invalid_field)
        rule = FieldType(paragraphs)
        self.assertFalse(rule.apply())
        self.assertEqual(len(rule.messages), 1)
        msg = rule.messages[0]
        self.assertEqual(msg.line_number, 6)
        self.assertEqual(msg.position, 1)
        self.assertEqual(msg.txt, "Invalid Field")

    def test_invalid_single_line_value(self):
        paragraphs = self.get_paragraphs(invalid_single_line_values)
        rule = FieldType(paragraphs)
        self.assertFalse(rule.apply())
        self.assertEqual(len(rule.messages), 1)
        msg = rule.messages[0]
        self.assertEqual(msg.line_number, 2)
        self.assertEqual(msg.position, 73)
        self.assertEqual(msg.txt,
                         "This field doesn't allow multiples lines")


class ParagraphTypeTest(RuleTest):
    def test_invalid_file(self):
        paragraphs = self.get_paragraphs(invalid_file)
        rule = ParagraphType(paragraphs)
        self.assertFalse(rule.apply())
        self.assertEqual(len(rule.messages), 2)
        msg = rule.messages[0]
        self.assertEqual(msg.line_number, 2)
        self.assertEqual(msg.position, 1)
        self.assertEqual(msg.txt, "Incompatible Field Type")

    def test_invalid_header(self):
        paragraphs = self.get_paragraphs(invalid_header)
        rule = ParagraphType(paragraphs)
        self.assertFalse(rule.apply())
        self.assertEqual(len(rule.messages), 1)
        msg = rule.messages[0]
        self.assertEqual(msg.line_number, 6)
        self.assertEqual(msg.position, 1)
        self.assertEqual(msg.txt, "Incompatible Field Type")

    def test_invalid_standalone(self):
        paragraphs = self.get_paragraphs(invalid_standalone)
        rule = ParagraphType(paragraphs)
        self.assertFalse(rule.apply())
        self.assertEqual(len(rule.messages), 1)
        msg = rule.messages[0]
        self.assertEqual(msg.line_number, 2)
        self.assertEqual(msg.position, 1)
        self.assertEqual(msg.txt, "Incompatible Field Type")

    def test_missed_copyright_field(self):
        paragraphs = self.get_paragraphs(invalid_file)
        rule = ParagraphType(paragraphs)
        self.assertFalse(rule.apply())
        self.assertEqual(len(rule.messages), 2)
        msg = rule.messages[1]
        self.assertEqual(msg.line_number, 2)
        self.assertEqual(msg.position, 1)
        self.assertEqual(msg.txt,
                         "Missed field, you forgot the field Copyright")


class CheckHasHeaderTest(RuleTest):
    def test_ok(self):
        data = header + two_fp_without_header
        paragraphs = self.get_paragraphs(data)
        rule = CheckHasHeader(paragraphs)
        self.assertTrue(rule.apply())

    def test_no_headers(self):
        paragraphs = self.get_paragraphs(two_fp_without_header)
        rule = CheckHasHeader(paragraphs)
        self.assertFalse(rule.apply())
        self.assertEqual(len(rule.messages), 1)
        msg = rule.messages[0]
        self.assertEqual(msg.line_number, 1)
        self.assertEqual(msg.position, 1)
        self.assertEqual(msg.txt, "You need define the header paragraph")

    def test_two_headers(self):
        data = two_headers + two_fp_without_header
        paragraphs = self.get_paragraphs(data)
        rule = CheckHasHeader(paragraphs)
        self.assertFalse(rule.apply())
        self.assertEqual(len(rule.messages), 1)
        msg = rule.messages[0]
        self.assertEqual(msg.line_number, 1)
        self.assertEqual(msg.position, 1)
        self.assertEqual(msg.txt, "Just one header paragraph is allowed")


class RepeatedFieldsTest(RuleTest):
    def test_repeated_fields(self):
        paragraphs = self.get_paragraphs(repeated_fields)
        rule = RepeatedFields(paragraphs)
        self.assertFalse(rule.apply())
        self.assertEqual(len(rule.messages), 1)
        msg = rule.messages[0]
        self.assertEqual(msg.line_number, 3)
        self.assertEqual(msg.position, 1)
        self.assertEqual(msg.txt, "Field redefinition")
