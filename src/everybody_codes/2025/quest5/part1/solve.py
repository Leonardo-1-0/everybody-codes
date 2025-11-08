from dataclasses import dataclass

input_: list[int] = list(map(int, open(0).readline().split(":")[1].split(",")))


@dataclass
class Bone:
    center: int
    left: int | None = None
    right: int | None = None

    def __repr__(self) -> str:
        return f"{self.left or ''}-{self.center}-{self.right or ''}"


fishbone: list[Bone] = []
for num in input_:
    for bone in fishbone:
        if num < bone.center and not bone.left:
            bone.left = num
            break
        elif num > bone.center and not bone.right:
            bone.right = num
            break
    else:
        fishbone.append(Bone(center=num))


print("".join(str(bone.center) for bone in fishbone))
