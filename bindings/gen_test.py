# coding=utf-8

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

# Generates test.py from ../../internal/cld2_unittest.cc and ../../internal/unittest_data.h

import re

# NOTE: this generates just a starting point; I had to fixup a few
# tests by hand for silly diffs like Korean vs KOREAN

CLD_PATH = '../cld2'

r = re.compile(r'const char\* (.*?)\s+=\s+"(.*?)";')
testData = {}
f = open('%s/internal/unittest_data.h' % CLD_PATH)
for line in f.readlines():
  if line.find('#else') != -1:
    break
  m = r.search(line)
  if m is not None:
    testData[m.group(1).strip()] = m.group(2)
f.close()

# Carried over from internal/cld2_unittest.cc:

testData['kTeststr_en'] = 'confiscation of goods is assigned as the penalty part most of the courts consist of members and when it is necessary to bring public cases before a jury of members two courts combine for the purpose the most important cases of all are brought jurors or'

#testData['kTeststr_ks'] = 'नेपाल एसिया मंज अख मुलुक राजधानी काठ माडौं नेपाल अधिराज्य पेरेग्वाय दक्षिण अमेरिका महाद्वीपे मध् यक्षेत्रे एक देश अस् ति फणीश्वर नाथ रेणु फिजी छु दक्षिण प्रशान् त महासागर मंज अख देश बहामास छु केरेबियन मंज अख मुलुख राजधानी नसौ सम् बद्घ विषय बुरुंडी अफ्रीका महाद्वीपे मध् यक्षेत्रे देश अस् ति सम् बद्घ विषय'

# Manually extracted from internal/unittest_data.h:
#testData['kTeststr_fr_en_Latn'] = 'A acc\xC3\xA8s aux chiens et aux frontaux qui lui ont \xC3\xA9t\xC3\xA9 il peut consulter et modifier ses collections et exporter This article is about the country. France is the largest country in Western Europe and the third-largest in Europe as a whole. Cet article concerne le pays europ\xC3\xA9\x65n aujourd\xE2\x80\x99hui appel\xC3\xA9 R\xC3\xA9publique fran\xC3\xA7\x61ise. Pour d\xE2\x80\x99\x61utres usages du nom France, Motoring events began soon after the construction of the first successful gasoline-fueled automobiles. The quick brown fox jumped over the lazy dog'
testData['kTeststr_fr_en_Latn'] = "France is the largest country in Western Europe and the third-largest in Europe as a whole. " + \
                                  "A accès aux chiens et aux frontaux qui lui ont été il peut consulter et modifier ses collections et exporter " + \
                                  "Cet article concerne le pays européen aujourd’hui appelé République française. Pour d’autres usages du nom France, " + \
                                  "Pour une aide rapide et effective, veuiller trouver votre aide dans le menu ci-dessus. " + \
                                  "Motoring events began soon after the construction of the first successful gasoline-fueled automobiles. The quick brown fox jumped over the lazy"

r = re.compile(r'\{(.*?), (.*?)\},')

count = 0

doFull = True

if doFull:
  f = open('%s/internal/cld2_unittest_full.cc' % CLD_PATH)
else:
  f = open('%s/internal/cld2_unittest.cc' % CLD_PATH)

small = set()
if doFull:
  import test
  for lang, data in test.testData:
    small.add((lang, data))

reComment = re.compile(r'/\*.*?\*/')

langs = set()
for line in f.readlines():
  m = r.search(line)
  if m is not None and not line.strip().startswith('//'):
    lang = m.group(1)
    if lang == 'UNKNOWN_LANGUAGE':
      break

    lang = reComment.sub('', lang).strip()

    if lang == 'CHINESE':
      lang = 'Chinese'
    elif lang == 'CHINESE_T':
      lang = 'ChineseT'
    elif lang == 'JAPANESE':
      lang = 'Japanese'
    elif lang == 'KOREAN':
      lang = 'Korean'

    testDataVar = m.group(2).strip()
    s = testData[testDataVar].replace('\'', '\\\'')
    if not doFull or (lang, s) not in small:
      print('  (\'%s\', \'%s\'),' % (lang, s))
      count += 1

    langs.add(lang)
    
    if False:
      print('')
      print('  def test_%s(self):' % testDataVar[9:])
      print('    self.runOne(\'%s\', \'%s\')' % (lang, testData[testDataVar].replace('\'', '\\\'')))

print('%d langs, %d cases' % (len(langs), count))

