import math
import re
import sys

input_: str = re.sub(r"\s+", "", "/".join(sys.stdin.readlines()))

revs = 100
for ratio in input_.split("|"):
    revs *= eval(ratio)

print(math.floor(revs))
