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
import curses


curses.setupterm()
if curses.tigetnum("colors") == 8:
    black = "\033[1;30m{0}\033[0m"
    red = "\033[1;31m{0}\033[0m"
    green = "\033[1;32m{0}\033[0m"
    yellow = "\033[1;33m{0}\033[0m"
    blue = "\033[1;34m{0}\033[0m"
    magenta = "\033[1;35m{0}\033[0m"
    cyan = "\033[1;36m{0}\033[0m"
    white = "\033[1;37m{0}\033[0m"
else:
    black = "{0}"
    red = "{0}"
    green = "{0}"
    yellow = "{0}"
    blue = "{0}"
    magenta = "{0}"
    cyan = "{0}"
    white = "{0}"
