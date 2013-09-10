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


class Field(object):
    """Object representation of a field defined by format 1.0 of Copyright
    machine readable"""
    def __init__(self, name, content=None, line_number=None):
        self.name = name
        self.type = None
        self._content = content
        if not content:
            self._content = []
        self.line_number = line_number
        if content and not type(content) == list:
            self._content = [str(content)]
        self._dict_to_text = {
            "single_line_values": self._to_text_single_line,
            "white_separated_lists": self._separated_list,
        }

    def add_content(self, value):
        """Append a value to the content list"""
        value = str(value)
        if not self._content:
            self._content = []
        self._content.append(value)

    @property
    def content(self):
        return "".join((v for v in self))

    def _separated_list(self):
        txt = '{name}: {content}'
        content = ""
        for v in self:
            content += '{} '.format(v.strip())
        return txt.format(name=self.name,
                          content=content[:-1])

    def _to_text_single_line(self):
        txt = '{name}: {content}'
        return txt.format(name=self.name,
                          content=self.content.strip())

    def to_text(self):
        try:
            return self._dict_to_text[self.type]()
        except KeyError:
            return ""

    def __iter__(self):
        for val in self._content:
            yield val

    def __len__(self):
        return len(self._content)

    def __repr__(self):
        txt = ("Name={name} -"
               " Type={type} -"
               " Content={content} -"
               " Line Number={line}")
        return txt.format(name=self.name,
                          type=self.type,
                          content=repr(self._content),
                          line=repr(self.line_number))
