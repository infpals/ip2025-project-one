from scripts.util import *

class ShipOld:
    def __init__(self, id: int, shape: list[str]):
        self.id = id
        self.shape = shape
        self.rotated = False
        self.spaces = sum(sum(val == "#" for val in row) for row in shape)
        self.pos = None

    def __str__(self):
        return f"Ship({self.id})"

    def __repr__(self):
        shape = "\n\t".join("|" + "".join(line) + "|" for line in self.getShapeAsArrays())
        return f"Ship:\n- id={self.id}\n- shape:\n\t{shape}\n- spaces={self.spaces}\n- pos={self.pos}"

    def getShapeAsArrays(self):
        return [[val for val in line] for line in self.shape]

    def rotate(self):
        if self.rotated:
            self.shape = rotate90(self.getShapeAsArrays())
        else:
            self.shape = rotate270(self.getShapeAsArrays())
        self.rotated = not self.rotated

    def isAtPos(self, pos: Pos) -> bool:
        if self.pos is None:
            raise ValueError("Position not set")
        for ship_pos in self.getPoss():
            if ship_pos == pos:
                return True
        return False

    def getPoss(self) -> list[Pos]:
        if self.pos is None:
            raise ValueError("Position not set")
        poss = []
        for dy, row in enumerate(self.getShapeAsArrays()):
            for dx, val in enumerate(row):
                test_pos = self.pos[0] + dx, self.pos[1] + dy
                if val == "#":
                    poss.append(test_pos)
        return poss

    def hit(self) -> None:
        self.spaces -= 1

    def isDead(self) -> bool:
        return self.spaces <= 0


class Ship:
    def __init__(self, id: int, shape: list[str]):
        self.id = id
        self.shape = shape
        self.spaces = sum(row.count("#") for row in shape)
        self.pos = None
        self.placed = False

    def getShape(self):
        return [[c for c in row] for row in self.shape]

    def rotate(self):
        self.shape = ["".join(row) for row in zip(*self.shape[::-1])]

    def getPoss(self, pos_override=None):
        pos = pos_override if pos_override else self.pos
        if pos is None:
            return []

        poss = []
        for dy, row in enumerate(self.getShape()):
            for dx, val in enumerate(row):
                if val == "#":
                    poss.append((pos[0] + dx, pos[1] + dy))
        return poss

    def isAtPos(self, pos):
        return pos in self.getPoss()

    def hit(self):
        self.spaces -= 1

    def isDead(self):
        return self.spaces <= 0


def getTestShip(id: int) -> ShipOld:
    if 'json' not in locals() and 'json' not in globals():
        import json
    with open("ships.json") as f:
        ships = json.load(f)
    return ShipOld(id, ships[str(id)]["shape"])

if __name__ == '__main__':
    for i in range(1, 5):
        ship = getTestShip(i)
        print(repr(ship))
