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
from dlt.field import Field


class FieldTest(unittest.TestCase):
    def test_field_init_without_value(self):
        field = Field("name")
        self.assertEqual(field.name, "name")
        self.assertEqual(len(field), 0)
        self.assertIsNone(field.line_number)
        field.add_content("value content")
        self.assertEqual(len(field), 1)
        self.assertEqual(list(field)[0], "value content")
        field.add_content("other value content")
        self.assertEqual(len(field), 2)
        self.assertEqual(list(field)[1], "other value content")

    def test_field_init_one_value(self):
        field = Field("Files", "foobar.foo")
        self.assertEqual(field.name, "Files")
        self.assertEqual(len(field), 1)
        self.assertIsNone(field.line_number)
        self.assertEqual(list(field)[0], "foobar.foo")
        field.add_content("barfoo.bar")
        self.assertEqual(len(field), 2)
        self.assertEqual(list(field)[1], "barfoo.bar")

    def test_repr_one_value(self):
        field = Field("Files", "foobar.foo")
        txt = ("Name=Files -"
               " Type=None -"
               " Content=['foobar.foo'] -"
               " Line Number=None")
        self.assertEqual(txt, repr(field))

    def test_repr_two_value(self):
        field = Field("Files", ["foobar.foo", "barfoo.bar"])
        field.type = "formatted_text"
        txt = ("Name=Files -"
               " Type=formatted_text -"
               " Content=['foobar.foo', 'barfoo.bar'] -"
               " Line Number=None")
        self.assertEqual(txt, repr(field))

    def test_repr_one_value_with_line_number_set(self):
        field = Field("Files", "foobar.foo", 1)
        txt = "Name=Files - Type=None - Content=['foobar.foo'] - Line Number=1"
        self.assertEqual(txt, repr(field))

    def test_set_line_number(self):
        field = Field("Files", "foobar.foo", 3)
        self.assertEqual(field.line_number, 3)
        field.line_number = 5
        self.assertEqual(field.line_number, 5)
