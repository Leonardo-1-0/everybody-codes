from dataclasses import dataclass

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


quality: dict[int, int] = {}
for key, values in swords.items():
    quality[key] = int(get_quality(get_fishbone(values)))

worst, *_, best = sorted(quality.items(), key=lambda item: item[1])
print(best[1] - worst[1])
