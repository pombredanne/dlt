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
from collections import namedtuple
import abc
from dlt.render import field_to_text, paragraph_to_text
from dlt.color import green
from dlt.scheme import PARAGRAPH_TYPES
from dlt.config import ERROR
from dlt import utils


def get_all_rules():
    return [CheckHasHeader, FieldType, ParagraphType, RepeatedFields,
            FileParagraph]


class Rule(object):
    """Base class for rules"""
    __metaclass__ = abc.ABCMeta

    def __init__(self, data):
        self._msg = []
        self._context = None
        self._data = data
        self.Message = namedtuple("Message",
                                  ["severity",
                                   "line_number",
                                   "position",
                                   "txt",
                                   "context",
                                   "suggestion", ])

    @property
    def messages(self):
        """Return the message queue"""
        return self._msg

    def add_msg(self, severity, line_number, position, msg, context,
                suggestion=""):
        """Put a message into the queue, adding extra data like line number,
        position and context"""
        msg = self.Message(severity, line_number, position, msg, context,
                           suggestion)
        self._msg.append(msg)

    @abc.abstractmethod
    def apply(self):
        """Apply the rule"""


class FieldType(Rule):
    """Checks all fields have a valid type and according to the type,
    check the content field"""
    def __init__(self, paragraphs):
        super(FieldType, self).__init__(paragraphs)
        self.type_checkers = {
            "line_based_lists": self._line_based_lists,
            "formatted_text": self._formatted_text,
            "white_separated_lists": self._white_separated_lists,
            "single_line_values": self._single_line_values,
        }

    def _line_based_lists(self, field):
        return self._single_line_values(field)

    def _formatted_text(self, field):
        return True

    def _white_separated_lists(self, field):
        return True

    def _single_line_values(self, field):
        if "\n " in field.content:
            context, position = self._get_context_single_line_values(field)
            self.add_msg(ERROR, field.line_number, position,
                         "This field doesn't allow multiples lines", context)
            return False
        return True

    def _get_context_single_line_values(self, field):
        field_txt = field_to_text(field)
        position = field_txt.find("\n ")
        txt = "{first}\n{indicator}{rest}"
        txt = txt.format(
            first=field_txt[:position],
            indicator=" " * position + green.format("^"),
            rest=field_txt[position:],
        )
        return (txt, position)

    def _get_context_invalid_type(self, field):
        position = 1
        indicator = green.format("_") + len(field.name) * green.format("~")
        txt = "{indicator}\n{field_render}"
        txt = txt.format(field_render=field_to_text(field),
                         indicator=indicator)
        return (txt, position)

    def apply(self):
        """Apply the rule"""
        success = True
        for paragraph in self._data:
            for field in paragraph:
                if field.type is None:
                    context, position = self._get_context_invalid_type(field)
                    self.add_msg(ERROR, field.line_number, position,
                                 "Invalid Field", context)
                    success = False
                else:
                    success &= self.type_checkers[field.type](field)
        return success


class ParagraphType(Rule):
    """Checks paragraph according to the type"""
    def __init__(self, paragraphs):
        super(ParagraphType, self).__init__(paragraphs)
        self.type_checkers = {
            "header": self._header_paragraph,
            "files": self._files_paragraph,
            "standalone_license": self._standalone_paragraph,
        }
        self.standalone = set(PARAGRAPH_TYPES["standalone_license"])
        self.files = set(PARAGRAPH_TYPES["files"])
        self.header = set(PARAGRAPH_TYPES["header"])

    def _get_context(self, paragraph, wrong_field):
        txt = ""
        context = ""
        position = 1
        line_number = 1
        for field in paragraph:
            txt += "{0}\n".format(field_to_text(field))
            if field.name == wrong_field:
                ctx = txt[:]
                txt = ""
                length = int(len(field.name))
                line_number = field.line_number
                indicator = green.format("_") + green.format("~") * length
                context = "{indicator}{ctx}".format(ctx=ctx,
                                                    indicator=indicator)
        return "{0}\n{1}".format(context, txt), line_number, position

    def _check_mandatory_fields(self, paragraph):
        if paragraph.type is None:
            return False
        fields = {}
        for field in paragraph:
            fields[field.name] = True
        missed_fields = set(PARAGRAPH_TYPES[paragraph.type]) - set(fields)
        for missed_field in missed_fields:
            if PARAGRAPH_TYPES[paragraph.type][missed_field]:
                message = "Missed field, you forgot the field {0}"
                self.add_msg(ERROR, paragraph[0].line_number, 1,
                             message.format(missed_field),
                             paragraph_to_text(paragraph))
                return False
        return True

    def _header_paragraph(self, paragraph):
        wrong_fields = (self.standalone | self.files) - self.header
        return self._search_incompatible_fields(wrong_fields, paragraph)

    def _search_incompatible_fields(self, wrong_fields, paragraph):
        success = True
        for wrong_field in wrong_fields:
            if wrong_field in paragraph:
                context, line, position = self._get_context(paragraph,
                                                            wrong_field)
                self.add_msg(ERROR, line, position,
                             "Incompatible Field Type", context)
                success = False
        return success

    def _files_paragraph(self, paragraph):
        wrong_fields = (self.standalone | self.header) - self.files
        return self._search_incompatible_fields(wrong_fields, paragraph)

    def _standalone_paragraph(self, paragraph):
        wrong_fields = (self.files | self.header) - self.standalone
        return self._search_incompatible_fields(wrong_fields, paragraph)

    def apply(self):
        """Apply the rule"""
        success = True
        for paragraph in self._data:
            try:
                success &= self.type_checkers[paragraph.type](paragraph)
            except KeyError:
                pass
            success &= self._check_mandatory_fields(paragraph)
        return success


class CheckHasHeader(Rule):
    """Check if has one header paragraph"""
    def __init__(self, paragraphs):
        super(CheckHasHeader, self).__init__(paragraphs)

    def _get_context(self, paragraphs):
        txt = ""
        mark = False
        for paragraph in self._data:
            if paragraph in paragraphs:
                mark = True
            for i, field in enumerate(paragraph):
                if mark and i == 0:
                    txt += '{0}\n'.format(green.format("_" * 40))
                txt += '{0}\n'.format(field_to_text(field))
            if mark:
                txt += '{0}'.format(green.format("^" * 40))
            txt += '\n'
            mark = False
        return txt[:-1]

    def apply(self):
        """Apply the rule"""
        header_paragraphs = []
        for paragraph in self._data:
            if paragraph.type == 'header':
                header_paragraphs.append(paragraph)
        if len(header_paragraphs) == 0:
            suggestion = "Are you sure that the copyright is DEP5 compliant"
            self.add_msg(ERROR, 1, 1,
                         "You need define the header paragraph", suggestion)
            return False
        elif len(header_paragraphs) > 1:
            context = self._get_context(header_paragraphs)
            self.add_msg(ERROR, 1, 1,
                         "Just one header paragraph is allowed", context)
            return False
        return True


class RepeatedFields(Rule):
    """Check if a paragraph has a field repeated"""
    def __init__(self, paragraphs):
        super(RepeatedFields, self).__init__(paragraphs)

    def _get_context(self, field):
        position = 1
        indicator = green.format("^") + len(field.name) * green.format("~")
        txt = "{field_render}\n{indicator}"
        txt = txt.format(field_render=field_to_text(field),
                         indicator=indicator)
        return (txt, position)

    def apply(self):
        for paragraph in self._data:
            fields = {}
            success = True
            for field in paragraph:
                name = field.name.strip()
                fields[name] = fields.get(name, 0) + 1
                if fields[name] > 1:
                    context, position = self._get_context(field)
                    self.add_msg(ERROR, field.line_number, position,
                                 "Field redefinition",
                                 context)
                    success = False
        return success


class FileParagraph(Rule):
    def __init__(self, paragraphs):
        super(FileParagraph, self).__init__(paragraphs)

    def apply(self):
        for paragraph in utils.get_by_type(self._data, "files"):
            if paragraph is None:
                break
            for patterns in paragraph["Files"]:
                paragraph.patterns = []
                for pattern in patterns.split():
                    paragraph.patterns.append(pattern)
        return True
