# ========================================================================
# Copyright 2022 Emory University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========================================================================
import json
import logging
import re
from typing import Set

__author__ = 'Jinho D. Choi'


def read_word_set(filename) -> Set[str]:
    """
    :param filename: the name of the file containing one key per line.
    :return: a set containing all keys in the file.
    """
    with open(filename, encoding='utf-8') as fin:
        s = set(line.strip() for line in fin)
    logging.info('Init: %s (keys = %d)' % (filename, len(s)))
    return s


class NoIndent(object):
    def __init__(self, value):
        self.value = value


class NoIndentEncoder(json.JSONEncoder):
    REGEX = re.compile(r'@@@(\d+)@@@')

    def __init__(self, *args, **kwargs):
        super(NoIndentEncoder, self).__init__(*args, **kwargs)
        self.kwargs = dict(kwargs)
        del self.kwargs['indent']
        self._replacements = {}

    def default(self, o):
        if isinstance(o, NoIndent):
            key = len(self._replacements)
            self._replacements[key] = json.dumps(o.value, **self.kwargs)
            return "@@@%d@@@" % key
        else:
            return super(NoIndentEncoder, self).default(o)

    def encode(self, o):
        result = super(NoIndentEncoder, self).encode(o)
        out = []
        m = self.REGEX.search(result)
        while m:
            key = int(m.group(1))
            out.append(result[:m.start(0) - 1])
            out.append(self._replacements[key])
            result = result[m.end(0) + 1:]
            m = self.REGEX.search(result)
        return ''.join(out)
