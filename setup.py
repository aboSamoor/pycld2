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

from distutils.core import Command
from setuptools import setup
from setuptools.command.install import install
from distutils.command.build import build

from gen_enc import generate_encodings

import subprocess
import sys
import os

__VERSION__ = '0.1.0'


# Test suite
class cldtest(Command):
    # user_options, initialize_options and finalize_options must be overriden.
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        errno = subprocess.call([sys.executable, 'tests/cld_test.py'])
        raise SystemExit(errno)


def get_ext_modules():
    import cld2
    return [cld2._full_ffi.verifier.get_extension(),
            cld2._lite_ffi.verifier.get_extension()]


def generate_luts():
    own_dir = os.path.abspath(os.path.dirname(__file__))
    output_file = os.path.join(own_dir, 'cld2', 'encoding_lut.cc')
    enc_header = os.path.join(own_dir, 'cld2', 'public', 'encodings.h')
    generate_encodings(enc_header, output_file)


class CFFIBuild(build):
    def finalize_options(self):
        generate_luts()
        self.distribution.ext_modules = get_ext_modules()
        build.finalize_options(self)


class CFFIInstall(install):
    def finalize_options(self):
        generate_luts()
        self.distribution.ext_modules = get_ext_modules()
        install.finalize_options(self)


setup(
    name='cld2-cffi',
    version=__VERSION__,
    description='CFFI bindings around Google Chromium\'s embedded ' +
    'compact language detection library (CLD2)',
    long_description=open('README.rst', 'r').read(),
    author='Michael McCandless & Greg Bowyer',
    author_email='mail@mikemccandless.com & gbowyer@fastmail.co.uk',
    packages=['cld2', 'cld2full'],
    tests_require=['tox'],
    install_requires=['cffi==0.9.2', 'six'],
    cmdclass={
        'build': CFFIBuild,
        'install': CFFIInstall,
    },
    setup_requires=['cffi==0.9.2', 'six'],
    include_package_data=False,
    zip_safe=False,
    package_data={
        'cld2': ['*.py', '*.c', '*.h'],
        'cld2full': ['*.py'],
    },
    keywords=['cld2', 'cffi'],
    license='Apache2',
    url='http://github.com/GregBowyer/cld2-cffi/',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: C++',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic'
    ],
)
