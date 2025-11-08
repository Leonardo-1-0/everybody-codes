from dataclasses import dataclass
from functools import cmp_to_key
from typing import Literal

swords: dict[int, list] = {}
for line in open(0).readlines():
    key, values = line.split(":")
    swords[int(key)] = list(map(int, values.split(",")))


@dataclass
class Bone:
    center: int
    left: int | None = None
    right: int | None = None

    def __repr__(self) -> str:
        return f"{self.left or ''}-{self.center}-{self.right or ''}"

    def get_score(self) -> int:
        return int(f"{self.left or ''}{self.center}{self.right or ''}")


def get_fishbone(values: list[int]) -> list[Bone]:
    fishbone: list[Bone] = []
    for num in values:
        for bone in fishbone:
            if num < bone.center and not bone.left:
                bone.left = num
                break
            elif num > bone.center and not bone.right:
                bone.right = num
                break
        else:
            fishbone.append(Bone(center=num))
    return fishbone


def get_quality(fishbone: list[Bone]) -> str:
    return "".join(str(bone.center) for bone in fishbone)


quality: dict[int, list[Bone]] = {}
for key, values in swords.items():
    quality[key] = get_fishbone(values)


def cmp_swords(
    a: tuple[int, list[Bone]], b: tuple[int, list[Bone]]
) -> Literal[0, 1, -1]:
    qa, qb = int(get_quality(a[1])), int(get_quality(b[1]))
    if qa > qb:
        return 1
    elif qa < qb:
        return -1

    for la, lb in zip(a[1], b[1]):
        qa, qb = la.get_score(), lb.get_score()
        if qa > qb:
            return 1
        elif qa < qb:
            return -1

    return 1 if a[0] > b[0] else -1


sorted_swords = dict(sorted(quality.items(), key=cmp_to_key(cmp_swords), reverse=True))

checksum = 0
for i, key in enumerate(sorted_swords, 1):
    checksum += i * key

print(checksum)
