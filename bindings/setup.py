#!/usr/bin/env python

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
#

from distutils.core import setup, Extension
import distutils.core
import platform
import subprocess
import sys
import os
import shutil

if os.path.exists('build'):
    shutil.rmtree('build')
    
# NOTE: change this to point to where you checked out the CLD2
# sources:
CLD2_PATH = '../cld2'

# Test suite
class cldtest(distutils.core.Command):
    # user_options, initialize_options and finalize_options must be overriden.
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass

    def run(self):
        errno = subprocess.call([sys.executable, 'tests/cld_test.py'])
        raise SystemExit(errno)

module = Extension('cld2',
                   language='c++',
                   include_dirs = ['%s/public' % CLD2_PATH, '%s/internal' % CLD2_PATH],
                   libraries = ['cld2'],
                   sources=['pycldmodule.cc', 'encodings.cc'],
                   )

setup(name='chromium_compact_language_detector',
      version='2.0',
      author='Michael McCandless',
      author_email='mail@mikemccandless.com',
      description='Python bindings around Google Chromium\'s embedded compact language detection library (CLD2)',
      ext_modules = [module],
      license = 'Apache2',
      url = 'http://code.google.com/p/chromium-compact-language-detector/',
      classifiers = [
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: C++',
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic'
        ],
      )
