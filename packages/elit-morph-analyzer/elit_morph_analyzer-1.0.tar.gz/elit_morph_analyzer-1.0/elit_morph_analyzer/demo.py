# ========================================================================
# Copyright 2021 Emory University
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

from elit_morph_analyzer import EnglishMorphAnalyzer

__author__ = 'Jinho D. Choi'

analyzer = EnglishMorphAnalyzer()

# default
tokens = ['I', 'bought', 'books', 'for', 'studying', 'earlier']
postags = ['PRP', 'VBD', 'NNS', 'IN', 'VBG', 'JJR']
print(analyzer.decode(tokens, postags))

tp = []

# verb: 3rd-person singular
tp.append((['pushes', 'pushes', 'takes'], ['VBZ', 'VBZ', 'VBZ']))

# verb: gerund
tp.append((['lying', 'feeling', 'taking', 'running'], ['VBG', 'VBG', 'VBG', 'VBG']))

# past (participle)
tp.append((['denied', 'zipped', 'heard', 'written', 'clung'], ['VBD', 'VBD', 'VBD', 'VBN', 'VBN']))

# verb: irregular
tp.append((['bit', 'bound', 'took', 'slept', 'spoken'], ['VBD', 'VBD', 'VBD', 'VBD', 'VBN']))

# noun: plural
tp.append((['crosses', 'men', 'vertebrae', 'foci', 'optima'], ['NNS', 'NNS', 'NNS', 'NNS', 'NNS']))

# noun: irregular
tp.append((['indices', 'wolves', 'knives', 'quizzes'], ['NNS', 'NNS', 'NNS', 'NNS']))

# adjective: comparative, superative
tp.append((['easier', 'larger', 'smallest', 'biggest'], ['JJR', 'JJR', 'JJS', 'JJS']))

# adverb: comparative, superative
tp.append((['earlier', 'sooner', 'largest'], ['RBR', 'RBR', 'JJS']))

# adjective/adverb: irregular
tp.append((['worse', 'further', 'best'], ['JJR', 'RBR', 'JJS']))

for tokens, postags in tp:
    print(analyzer.decode(tokens, postags, baseonly=False))

tp = []

# verb: 'fy'
tp.append((['glorify', 'qualify', 'simplify', 'liquefy'], ['VB', 'VB', 'VB', 'VB']))

# verb: 'ize'
tp.append((['hospitalize', 'theorize', 'crystallize', 'dramatize'], ['VB', 'VB', 'VB', 'VB']))

# verb: 'en'
tp.append((['strengthen', 'brighten'], ['VB', 'VB']))

# noun: 'age'
tp.append((['marriage', 'passage', 'mileage'], ['NN', 'NN', 'NN']))

# noun: 'al'
tp.append((['denial', 'approval'], ['NN', 'NN']))

# noun: 'ance'
tp.append((['annoyance', 'insurance', 'relevance', 'difference', 'accuracy'], ['NN', 'NN', 'NN', 'NN', 'NN']))

# noun: 'ant'
tp.append((['applicant', 'assistant', 'servant', 'immigrant', 'resident'], ['NN', 'NN', 'NN', 'NN', 'NN']))

# noun: 'dom'
tp.append((['freedom', 'kingdom'], ['NN', 'NN']))

# noun: 'ee'
tp.append((['employee', 'escapee'], ['NN', 'NN']))

# noun: 'er'
tp.append((['carrier', 'lawyer', 'writer', 'liar', 'actor'], ['NN', 'NN', 'NN', 'NN', 'NN']))

# noun: 'hood'
tp.append((['likelihood', 'childhood'], ['NN', 'NN']))

# adjective: 'ing'
tp.append((['building'], ['NN']))

# noun: 'ism'
tp.append((['witticism', 'baptism', 'capitalism', 'bimetallism'], ['NN', 'NN', 'NN', 'NN']))

# noun: 'ist'
tp.append((['capitalist', 'machinist', 'panellist', 'environmentalist'], ['NN', 'NN', 'NN', 'NN']))

# noun: 'ity'
tp.append((['capability', 'variety', 'normality', 'loyalty'], ['NN', 'NN', 'NN', 'NN']))

# noun: 'man'
tp.append((['chairman', 'chairwoman', 'chairperson'], ['NN', 'NN', 'NN']))

# noun: 'ment'
tp.append((['development', 'abridgment'], ['NN', 'NN']))

# noun: 'ness'
tp.append((['happiness', 'kindness', 'thinness'], ['NN', 'NN', 'NN']))

# noun: 'ship'
tp.append((['friendship'], ['NN']))

# noun: 'sis'
tp.append((['diagnosis', 'analysis'], ['NN', 'NN']))

# noun: 'tion'
tp.append((['verification', 'admiration', 'suspicion', 'addition', 'decision'], ['NN', 'NN', 'NN', 'NN', 'NN']))

# adjective: 'able'
tp.append((['readable', 'irritable', 'flammable', 'visible'], ['JJ', 'JJ', 'JJ', 'JJ']))

# adjective: 'al'
tp.append((['influential', 'accidental', 'universal', 'focal', 'economical'], ['JJ', 'JJ', 'JJ', 'JJ', 'JJ']))

# adjective: 'ant'
tp.append((['applicant', 'relaxant', 'pleasant', 'dominant', 'absorbent'], ['JJ', 'JJ', 'JJ', 'JJ', 'JJ']))

# adjective: 'ary'
tp.append((['cautionary', 'imaginary', 'pupillary', 'monetary'], ['JJ', 'JJ', 'JJ', 'JJ']))

# adjective: 'ed'
tp.append((['diffused', 'shrunk'], ['JJ', 'JJ']))

# adjective: 'ful'
tp.append((['beautiful', 'thoughtful', 'helpful'], ['JJ', 'JJ', 'JJ']))

# adjective: 'ic'
tp.append((['fantastic', 'diagnostic', 'analytic', 'poetic'], ['JJ', 'JJ', 'JJ', 'JJ']))

# adjective: 'ing'
tp.append((['dignifying', 'abiding'], ['JJ', 'JJ']))

# adjective: 'ish'
tp.append((['ticklish', 'reddish', 'boyish', 'mulish'], ['JJ', 'JJ', 'JJ', 'JJ']))

# adjective: 'ive'
tp.append((['talkative', 'adjudicative', 'destructive', 'defensive'], ['JJ', 'JJ', 'JJ', 'JJ']))

# adjective: 'less'
tp.append((['countless', 'speechless'], ['JJ', 'JJ']))

# adjective: 'like'
tp.append((['childlike'], ['JJ']))

# adjective: 'ly'
tp.append((['daily', 'weekly'], ['JJ', 'JJ']))

# adjective: 'most'
tp.append((['innermost'], ['JJ']))

# adjective: 'ous'
tp.append((['glorious', 'wondrous', 'marvellous', 'nervous', 'religious'], ['JJ', 'JJ', 'JJ', 'JJ', 'JJ']))

# adjective: 'some'
tp.append((['worrisome', 'troublesome', 'awesome', 'fulsome'], ['JJ', 'JJ', 'JJ', 'JJ']))

# adjective: 'wise'
tp.append((['clockwise', 'likewise'], ['JJ', 'JJ']))

# adjective: 'y'
tp.append((['clayey', 'grouchy', 'runny', 'rumbly'], ['JJ', 'JJ', 'JJ', 'JJ']))

# adverb: 'ly'
tp.append((['electronically', 'easily', 'sadly', 'incredibly'], ['RB', 'RB', 'RB', 'RB']))

for tokens, postags in tp:
    print(analyzer.decode(tokens, postags, derivation=True, baseonly=False))

tp = []

tp.append((['belittle', 'co-founder', 'super-overlook', 'deuteragonist'], ['VB', 'NN', 'VB', 'NN']))

for tokens, postags in tp:
    print(analyzer.decode(tokens, postags, derivation=True, prefix=2, baseonly=False))
