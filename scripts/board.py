from scripts.util import *
from scripts.ship import Ship


class BoardOld:
    size: tuple[int, int] = 8, 6

    def __init__(self) -> None:
        self.ships = []
        self.markers = []

    def __str__(self) -> str:
        board = [[ship.id if (ship := self.getAtPos((x, y))) is not None else 0 for x in range(BoardOld.size[0])] for y in range(BoardOld.size[1])]
        return str("\n".join(str(line) for line in board))

    def getAtPos(self, pos: Pos) -> Ship | None:
        if pos[0] < 0 or pos[0] >= BoardOld.size[0]:
            return None
        if pos[1] < 0 or pos[1] >= BoardOld.size[1]:
            return None
        for ship in self.ships:
            if ship.isAtPos(pos):
                return ship
        return None

    def addShip(self, new_ship: Ship, pos: Pos) -> bool:
        new_ship.pos = pos
        for ship in self.ships:
            for ship_pos in ship.getPoss():
                if new_ship.isAtPos(ship_pos):
                    new_ship.pos = None
                    return False
        self.ships.append(new_ship)
        return True

    def shipsLeft(self) -> int:
        return sum([not ship.isDead for ship in self.ships])

    def addMarker(self, marker: Pos) -> bool:
        hit = False
        for ship in self.ships:
            hit = ship.isAtPos(marker)
        self.markers.append((*marker, hit))
        return hit



class Board:
    size = (10, 8)

    def __init__(self):
        self.ships: list[Ship] = []
        self.markers: list[tuple[int, int, bool]] = []

    def inBounds(self, pos):
        return 0 <= pos[0] < Board.size[0] and 0 <= pos[1] < Board.size[1]

    def alreadyShot(self, pos):
        return any(mx == pos[0] and my == pos[1] for mx, my, _ in self.markers)

    def canPlace(self, ship: Ship, pos: Pos):
        for p in ship.getPoss(pos):
            if not self.inBounds(p):
                return False
            for other in self.ships:
                if p in other.getPoss():
                    return False
        return True

    def addShip(self, ship: Ship, pos: Pos):
        if not self.canPlace(ship, pos):
            return False
        ship.pos = pos
        ship.placed = True
        self.ships.append(ship)
        return True

    def addMarker(self, pos: Pos):
        if self.alreadyShot(pos):
            return None  # invalid shot

        for ship in self.ships:
            if ship.isAtPos(pos):
                ship.hit()
                self.markers.append((*pos, True))
                return True

        self.markers.append((*pos, False))
        return False




if __name__ == '__main__':
    if 'getTestShip' not in locals() and 'getTestShip' not in globals():
        from ship import getTestShip
    board = BoardOld()
    print(board)
    ship = getTestShip(1)
    ship.rotate()
    print(ship)
    print(board.addShip(ship, (1, 1)))
    print(board)
