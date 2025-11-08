import math
import sys

input_: list[int] = list(map(int, sys.stdin.readlines()))
first, last = input_[0], input_[-1]

print(math.floor(2025 * (first / last)))
