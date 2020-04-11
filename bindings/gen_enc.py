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

import re

s = open('../../public/encodings.h').read()


r = re.compile(r'\s*(.*?)\s+=\s*(\d+),')
l = []
for line in s.split('\n'):
  line = line.strip()
  m = r.match(line)
  if m is not None:
    l.append((m.group(1), int(m.group(2))))

print()
print('''struct cld_encoding {
  const char# name;
  CLD2::Encoding encoding;
};''')

print('const cld_encoding cld_encoding_info[] = {')

for k, v in l:
  print('  {"%s", CLD2::%s},' % (k, k))
print('};')

