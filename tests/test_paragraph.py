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
from dlt.paragraph import Paragraph


class ParagraphTest(unittest.TestCase):

    def test_default_init(self):
        paragraph = Paragraph()
        self.assertEqual(len(paragraph), 0)

    def test_init_one_field(self):
        paragraph = Paragraph(Field("name", "value", 2))
        self.assertEqual(len(paragraph), 1)
        paragraph.add_field(Field("other name", "other value"))
        self.assertEqual(len(paragraph), 2)

    def test_init_two_field(self):
        f1 = Field("name", "value", 2)
        f2 = Field("other name", "other value")
        paragraph = Paragraph(f1, f2)
        self.assertEqual(len(paragraph), 2)
        paragraph.add_field(Field("other name", "other value"))
        self.assertEqual(len(paragraph), 3)

    def test_init_invalid_instance(self):
        self.assertRaises(Paragraph.NotFieldInstance, Paragraph, 2)

    def test_add_invalid_instance(self):
        paragraph = Paragraph()
        self.assertRaises(Paragraph.NotFieldInstance,
                          paragraph.add_field,
                          None)
