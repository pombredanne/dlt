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
from dlt.field import Field


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

    def __getitem__(self, value):
        name = None
        index = None
        try:
            index = int(value)
        except ValueError:
            name = value
        for i, field in enumerate(self):
            if name is not None and name == field.name.strip():
                return field
            elif index is not None and index == i:
                return field

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
