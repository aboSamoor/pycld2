import time
import re

USE_FULL_TABLES = True

if USE_FULL_TABLES:
  import cld2full as cld2detect
else:
  import cld2 as cld2detect

reOneLine = re.compile('^Samp ([^] ]+) /(.*?)/ (.*)$')
lineCount = 0

# NOTE: some lines have \r in them and we want to NOT make a new line for that:
def readlines(f):
  buf = bytearray()
  while True:
    c = f.read(1)
    if len(c) == 0:
      return
    buf.append(c[0])
    if c == b'\n': 
      yield buf.decode('utf-8')
      buf = bytearray()

correct = 0
wrong = 0
t0 = time.time()
with open('../cld2/internal/test_shuffle_1000_48_666.utf8', 'rb') as f:
  for lineCount, line in enumerate(readlines(f)):
    m = reOneLine.match(line)
    if m is None:
      raise RuntimeError('malformed line %d: %s' % (lineCount, line))
    lang = m.group(1)
    source = m.group(2)
    text = m.group(3)

    # Ignore odd combinations:
    if lang in ('ar-Latn',  # Arabic
                'hr-Cyrl',  # Croatian
                'ko-Latn',  # Korean
                'fa-Latn'):
      print('NOTE: skip odd lang/script combination %s: source=%s, text=%s' % (lang, source, text))
      continue
    
    isReliable, textBytesFound, details = cld2detect.detect(text, isPlainText=True)
    langCode = lang.split('-')[0]
    if langCode == details[0][1]:
    #if langCode in [x[1] for x in details]:
      correct += 1
    else:
      wrong += 1
      print("wrong: %s vs %s: %s" % (langCode, details, text))
    #print('%s: %s, %s' % (lang, isReliable, details))
    #print('%s: %s' % (lang, source))

t1 = time.time()
total = correct + wrong
print('Took %.1f sec (%.3f msec per test); %d correct of %d total: %.3f %% accuracy' % \
      (t1-t0,
       1000*(t1-t0)/total,
       correct,
       total,
       100.*correct/total))
