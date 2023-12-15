import os
import re

def walkDir(dname, filt=r".*"):
  result = []
  for root, dnames, fnames in os.walk(dname):
    for fname in fnames:
      if re.search(filt, fname):
        foo = root + "/" + fname
        foo = re.sub(r"[/\\]+", "/", foo)
        result.append(foo)
  return result
