import math
import sys

input_: list[int] = list(map(int, sys.stdin.readlines()))
first, last = input_[0], input_[-1]

res =10_000_000_000_000 * (1 / (first / last))
print(100 * math.ceil(res))
