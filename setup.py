#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

import io
import re
from os import path

import setuptools

HERE = path.abspath(path.dirname(__file__))
CLD2_PATH = path.join(HERE, "cld2")
BIND_PATH = path.join(HERE, "bindings")


# See internal/compile_libs.sh for some detail.  Note that this is *not*
# simply internal/*.cc
src_files = [
    path.join(CLD2_PATH, "internal/", i)
    for i in (
        "cld2_generated_cjk_compatible.cc",
        "cld2_generated_deltaocta0122.cc",
        "cld2_generated_distinctocta0122.cc",
        "cld2_generated_quad0122.cc",
        "cld_generated_cjk_delta_bi_32.cc",
        "cld_generated_cjk_uni_prop_80.cc",
        "cld_generated_score_quad_octa_0122.cc",
        "cldutil.cc",
        "cldutil_shared.cc",
        "compact_lang_det.cc",
        "compact_lang_det_hint_code.cc",
        "compact_lang_det_impl.cc",
        "debug.cc",
        "fixunicodevalue.cc",
        "generated_distinct_bi_0.cc",
        "generated_entities.cc",
        "generated_language.cc",
        "generated_ulscript.cc",
        "getonescriptspan.cc",
        "lang_script.cc",
        "offsetmap.cc",
        "scoreonescriptspan.cc",
        "tote.cc",
        "utf8statetable.cc",
    )
]
src_files.extend(
    [path.join(BIND_PATH, "pycldmodule.cc"), path.join(BIND_PATH, "encodings.cc")]
)
for i in src_files:
    if not path.exists(i):
        raise RuntimeError("Missing source file: %s" % i)

include_dirs = [path.join(CLD2_PATH, "internal"), path.join(CLD2_PATH, "public")]

module = setuptools.Extension(
    # First arg (name) is the full name of the extension, including
    # any packages - ie. not a filename or pathname, but Python dotted
    # name.
    "pycld2._pycld2",
    sources=src_files,
    include_dirs=include_dirs,
    language="c++",
    # TODO: -m64 may break 32 bit builds
    extra_compile_args=["-w", "-O2", "-m64", "-fPIC"],
)

# We define version as PYCLD2_VERSION in the C++ module.
# Note: we could also use `define_macros` arg to setup()
VERSION = re.search(
    r'^#define\s+PYCLD2_VERSION\s+"([^"]+)"$',
    io.open(path.join(BIND_PATH, "pycldmodule.cc"), encoding="utf-8").read(),
    re.M,
).group(1)

if __name__ == "__main__":
    setuptools.setup(
        name="pycld2",
        version=VERSION,
        author="Rami Al-Rfou",
        author_email="rmyeid@gmail.com",
        maintainer="Brad Solomon",
        maintainer_email="brad.solomon.1124@gmail.com",
        description="Python bindings around Google Chromium's embedded compact language detection library (CLD2)",
        long_description=io.open(
            path.join(HERE, "README.md"),
            encoding="utf-8"
        ).read(),
        long_description_content_type="text/markdown",
        license="Apache2",
        url="https://github.com/aboSamoor/pycld2",
        classifiers=[
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: C++",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Topic :: Text Processing :: Linguistic",
        ],
        packages=["pycld2"],
        ext_modules=[module],
    )
