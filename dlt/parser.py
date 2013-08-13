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
import sys
import operator
from collections import OrderedDict
from dlt.scheme import FIELD_TYPES, PARAGRAPH_TYPES
from dlt.rules import get_all_rules
from dlt.config import log_level, log_color
from dlt.color import blue


class Parser(object):
    """Parser to debian copyright file machine readable. Try to parse the
    described here
    http://www.debian.org/doc/packaging-manuals/copyright-format/1.0/"""
    def __init__(self):
        self._rules = []

    def process(self, paragraphs):
        """Parse a list of paragraphs"""
        self._guess_types(paragraphs)
        for rule in get_all_rules():
            rule_inst = rule(paragraphs)
            self._rules.append(rule_inst)
            if not rule_inst.apply():
                return False
        return True

    def _print_message(self, message):
        msg = "{level}: {msg} in line {line}:{position}\n\n{context}\n{sug}"
        context = ""
        if message.context:
            context = '\t{0}'.format("\n\t".join(message.context.split("\n")))
            context = blue.format(context)
        msg = msg.format(
            level=log_color[message.severity],
            msg=message.txt,
            line=message.line_number,
            position=message.position,
            context=context,
            sug=message.suggestion,
        )
        print(msg)

    def show_msg(self):
        """Show the messages of each rule"""
        for rule in self._rules:
            for message in rule.messages:
                if message.severity >= log_level:
                    self._print_message(message)

    def _guess_types(self, paragraphs):
        for paragraph in paragraphs:
            paragraph.type = self._get_paragraph_type(paragraph)
            for field in paragraph:
                field.type = self._get_field_type(field)

    def _get_paragraph_type(self, paragraph):
        """Receive a parsed paragraph and try to establish the type applying
        the constraints defined in format 1.0 of machine-readable document"""
        type_scores = {}
        paragraph_type_sorted = OrderedDict(sorted(PARAGRAPH_TYPES.items()))
        count = len(paragraph_type_sorted)
        for paragraph_type, field_names in paragraph_type_sorted.items():
            step = sys.float_info.epsilon * count
            count -= 1
            step += 1.0 / len(paragraph_type_sorted[paragraph_type])
            type_scores[paragraph_type] = 0.0
            for field_name in field_names.keys():
                if field_name in paragraph:
                    type_scores[paragraph_type] += step
        tag, score = max(type_scores.items(), key=operator.itemgetter(1))
        return tag if score > 0 else None

    def _get_field_type(self, field):
        """Try to tag as is in DEP5"""
        for field_type, field_names in FIELD_TYPES.items():
            if field.name.strip() in field_names:
                return field_type
