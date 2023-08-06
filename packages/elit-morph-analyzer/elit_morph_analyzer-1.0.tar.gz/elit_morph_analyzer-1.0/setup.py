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

__author__ = 'Jinho D. Choi'

import setuptools

with open('README.md') as fh:
    long_description = fh.read()

setuptools.setup(
    name='elit_morph_analyzer',
    version='1.0',
    scripts=[],
    author='Jinho D. Choi',
    author_email='jinho.choi@emory.edu',
    description='English Morphological Analyzer from ELIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/emorynlp/elit-morph_analyzer',
    packages=setuptools.find_packages(),
    install_requires=['marisa-trie'],
    tests_require=['pytest'],
    classifiers=[
         'Programming Language :: Python :: 3',
         'License :: OSI Approved :: Apache Software License',
         'Operating System :: OS Independent',
    ],
    package_data={'elit_tokenizer': ['resources/english/*.txt', 'resources/english/*.json']},
    include_package_data=True
 )