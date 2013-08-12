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

from os.path import abspath, expanduser, normpath, join, exists, isfile


def find_debian_copyright_file(deb_src_dir):
    """Try to find the debian copyright file, may be this piece of source
    was hacked many times..."""
    deb_src_dir = normpath(abspath(expanduser(deb_src_dir)))
    paths_to_lookup = [join(deb_src_dir, "debian", "copyright"),
                       join(deb_src_dir, "copyright"),
                       deb_src_dir, ]
    for path in paths_to_lookup:
        if exists(path) and isfile(path):
            return path


def get_by_type(paragraphs, type):
    """Filter the paragraphs by type"""
    for paragraph in paragraphs:
        if paragraph.type == type:
            yield paragraph
