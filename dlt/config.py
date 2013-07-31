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
import os
from . import color
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser


PATH_CONFIG_FILE = '/etc/dlt/dlt.cfg'
if 'DLT_CONFIG' in os.environ:
    PATH_CONFIG_FILE = os.environ['DLT_CONFIG']
if not os.path.exists(PATH_CONFIG_FILE):
    PATH_CONFIG_FILE = None


DEBUG = 10
INFO = 20
WARNING = 30
ERROR = 40
severities = {
    "DEBUG": DEBUG,
    "INFO": INFO,
    "WARNING": WARNING,
    "ERROR": ERROR,
}
log_color = {
    DEBUG: color.white.format("DEBUG"),
    INFO: color.green.format("INFO"),
    WARNING: color.magenta.format("WARNING"),
    ERROR: color.red.format("ERROR"),
}
if PATH_CONFIG_FILE:
    config = ConfigParser()
    config.read(PATH_CONFIG_FILE)
else:
    config = {}
log_level = severities.get(config.get("logger", "level"), WARNING)
