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

# Generates encodings.cc from ../../public/encodings.h
from __future__ import print_function

import re

_TMPL = '''
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//

// Machine generated. Edit gen_enc.py to alter

#include <cstdio>
#include <cstring>
#include "compact_lang_det.h"
#include "encodings.h"

struct cld_encoding {
  const char *name;
  CLD2::Encoding encoding;
};

extern const cld_encoding cld_encoding_info[] = {
%(encodings)s
};

CLD2::Encoding EncodingFromName(const char *name) {
  for(int i=0;i<CLD2::NUM_ENCODINGS;i++) {
    if (!strcasecmp(cld_encoding_info[i].name, name)) {
      return cld_encoding_info[i].encoding;
    }
  }

  return CLD2::UNKNOWN_ENCODING;
}
'''


def generate_encodings(encoding_header, output_file):
    """ Generate encoding LUT for the given cld encodings.h

        Parameters
        ----------
        encoding_header : str
            Location of the encodings

        output_file : str
            Where to save encodings to
    """
    with open(encoding_header) as encodings:
        regex = re.compile(r'\s*(.*?)\s+=\s*(\d+),')
        lines = []
        for line in encodings:
            line = line.strip()
            match = regex.match(line)
            if match is not None:
                name = match.group(1)
                if name == 'NUM_ENCODINGS':
                    continue
                lines.append('  {"%s", CLD2::%s},' % (name, name))

        enc_table = _TMPL % {'encodings': '\n'.join(lines)}

        with open(output_file, 'w') as output:
            output.write(enc_table)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print('Usage <prog>: input_file output_file')
        sys.exit(1)
    generate_encodings(sys.argv[1], sys.argv[2])
