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
from tempfile import mkdtemp
import os
import unittest
from dlt.tokenizer import Tokenizer
from dlt.parser import Parser
from dlt.coverage import Coverage
from copyright import two_fp_without_header


class CoverageTest(unittest.TestCase):
    def setUp(self):
        self.tokenizer = Tokenizer()
        self.parser = Parser()
        self.test_dir = mkdtemp()
        self.debian_dir = os.path.join(self.test_dir, "debian")
        self.copyright_file_path = os.path.join(self.debian_dir, "copyright")
        os.makedirs(self.debian_dir)

    def fake_file(self, filename, dir=None):
        if dir is None:
            dir = self.test_dir
        with open(os.path.join(dir, filename), 'w'):
            pass

    def get_paragraphs(self, txt):
        open(self.copyright_file_path, 'w').write("".join(txt))
        paragraphs = self.tokenizer.get_paragraphs(txt)
        self.parser._guess_types(paragraphs)
        self.parser.process(paragraphs)
        return paragraphs

    def test_test(self):
        self.fake_file("foobar.foo")
        self.fake_file("sara.sa", self.debian_dir)
        paragraphs = self.get_paragraphs(two_fp_without_header)
        coverage = Coverage(paragraphs, self.test_dir)
        #coverage.apply()
