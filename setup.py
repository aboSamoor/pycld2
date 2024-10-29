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
import platform

import setuptools

# See internal/compile_libs.sh for some detail.  Note that this is *not*
# simply internal/*.cc.  Issue #23: keep these relative for manifest.
src_files = [
    path.join("cld2/internal/", i)
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
src_files.extend(["bindings/pycldmodule.cc", "bindings/encodings.cc"])
for i in src_files:
    if not path.exists(i):
        raise RuntimeError("Missing source file: %s" % i)

include_dirs = ["cld2/internal", "cld2/public"]

extra_compile_args = ["-w", "-O2", "-fPIC"]
if platform.machine() == 'x86_64':
    extra_compile_args.append('-m64')
elif platform.machine() == 'aarch64':
    extra_compile_args.append('-march=armv8-a')

module = setuptools.Extension(
    # First arg (name) is the full name of the extension, including
    # any packages - ie. not a filename or pathname, but Python dotted
    # name.
    "pycld2._pycld2",
    sources=src_files,
    include_dirs=include_dirs,
    language="c++",
    extra_compile_args=extra_compile_args,
)

# We define version as PYCLD2_VERSION in the C++ module.
# Note: we could also use `define_macros` arg to setup()
with io.open("bindings/pycldmodule.cc", encoding="utf-8") as fr:
    VERSION = re.search(
        r'^#define\s+PYCLD2_VERSION\s+"([^"]+)"$', fr.read(), re.M
    ).group(1)

with io.open("README.md", encoding="utf-8") as fr:
    long_description = fr.read()

if __name__ == "__main__":
    setuptools.setup(
        name="pycld2",
        version=VERSION,
        author="Rami Al-Rfou",
        author_email="rmyeid@gmail.com",
        maintainer="Brad Solomon",
        maintainer_email="brad.solomon.1124@gmail.com",
        description="Python bindings around Google Chromium's embedded compact language detection library (CLD2)",
        long_description=long_description,
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
