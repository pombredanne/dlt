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


class Paragraph(object):
    """It's a fields container"""
    def __init__(self, *fields):
        self.type = None
        self._fields = []
        for field in fields:
            self.add_field(field)

    def add_field(self, field):
        """Add a field to the container only if it is a Field instance"""
        if not isinstance(field, Field):
            msg = "{f} is not a Field instance".format(f=repr(field))
            raise self.NotFieldInstance(msg)
        self._fields.append(field)

    def __len__(self):
        return len(self._fields)

    def __contains__(self, field_name):
        return any(field_name in field.name for field in self._fields)

    def __getitem__(self, name):
        for field in self:
            if name == field.name.strip():
                return field

    def next(self):
        """Paragraph instances iterable"""
        return self

    def __iter__(self):
        for field in self._fields:
            yield field

    def __repr__(self):
        txt = "Paragraph type {type}:".format(type=repr(self.type))
        for field in self._fields:
            txt += " {field}".format(field=repr(field))
        return txt

    class NotFieldInstance(BaseException):
        """It's used when the field to add an Paragraph insance is not a Field
        instance"""


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

    def add_content(self, value):
        """Append a value to the content list"""
        value = str(value)
        if not self._content:
            self._content = []
        self._content.append(value)

    @property
    def content(self):
        return "".join((v for v in self))

    def next(self):
        """Field instances iterable"""
        return self

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
