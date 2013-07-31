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
import os
import shutil
import hashlib
from tempfile import mkdtemp
from dlt.utils import find_debian_copyright_file


class UtilTest(unittest.TestCase):
    def setUp(self):
        self.test_dir = mkdtemp()
        self.debian_dir = os.path.join(self.test_dir, "debian")
        self.copyright_file_path = os.path.join(self.debian_dir, "copyright")
        os.makedirs(self.debian_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_find_debian_copyright_file_inexistent_path(self):
        self.assertIsNone(find_debian_copyright_file(self.debian_dir))

    def test_find_debian_copyright_file_invalid_path(self):
        saraza = hashlib.sha1()
        self.assertIsNone(find_debian_copyright_file(saraza.hexdigest()))

    def test_find_debian_copyright_file_valid_path(self):
        with open(self.copyright_file_path, "w"):
            pass
        self.assertEqual(find_debian_copyright_file(self.debian_dir),
                         self.copyright_file_path)
