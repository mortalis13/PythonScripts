
# Python 3

import re

def tokenize(text, match1=re.compile("([idel])|(\d+):|(-?\d+)").match):
  i = 0
  while i < len(text):
    m = match1(text, i)
    if m != None:
      # print(m)
      s = m.group(m.lastindex)
      i = m.end()
      if m.lastindex == 2:
        yield "s"
        yield text[i:i+int(s)]
        i = i + int(s)
      else:
        yield s


def decode_item(next, token):
  if token == "i":
    # integer: "i" value "e"
    data = int(next())
    if next() != "e":
      raise ValueError
  elif token == "s":
    # string: "s" value (virtual tokens)
    data = next()
  elif token == "l" or token == "d":
    # container: "l" (or "d") values "e"
    data = []
    tok = next()
    while tok != "e":
      data.append(decode_item(next, tok))
      tok = next()
    if token == "d":
      data = dict(zip(data[0::2], data[1::2]))
  else:
    raise ValueError
  return data


def decode(text):
  # f=open('c:/t.txt', 'w', encoding='latin1')
  # f.write(text)
  # f.close()
  
  # m1=re.compile("([idel])|(\d+):|(-?\d+)").match
  # res=m1(text, 0)
  # print(res)
  # return
  
  try:
    src = tokenize(text)
    print(src)
    # data = decode_item(src.next, src.next())
    data = decode_item(src.__next__, next(src))
    
    for token in src: # look for more tokens
      raise SyntaxError("trailing junk")
  except (AttributeError, ValueError, StopIteration):
    raise SyntaxError("syntax error")
  return data
