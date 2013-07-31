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

"""The scheme defined in DEP5"""


FIELD_TYPES = {
    "white_separated_lists": ["Files"],
    "line_based_lists": ["Upstream-Contact"],
    "single_line_values": [
        "Format",
        "Upstream-Name",
    ],
    "formatted_text": [
        "License",
        "Copyright",
        "Source",
        "Comment",
        "Disclaimer",
    ],
}


# True if the field is mandatory otherwise is optional
PARAGRAPH_TYPES = {
    "header": {
        "Format": True,
        "Upstream-Name": False,
        "Upstream-Contact": False,
        "Source": False,
        "Disclaimer": False,
        "Comment": False,
        "License": False,
        "Copyright": False,
    },
    "files": {
        "Files": True,
        "Copyright": True,
        "License": True,
        "Comment": False,
    },
    "standalone_license": {
        "License": True,
        "Comment": False,
    },
}
