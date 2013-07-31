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
"""Run all tests auto discovered by unittest.TestLoader"""

import unittest
import sys


if __name__ == "__main__":
    all_tests = unittest.TestLoader().discover('tests')
    verbosity = 1
    for argv in sys.argv:
        if "-v" in argv:
            verbosity = argv.count("v") + 1
    unittest.TextTestRunner(verbosity=verbosity).run(all_tests)
