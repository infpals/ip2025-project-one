from scripts.util import *
from scripts.ship import Ship


class Board:
    size: tuple[int, int] = 8, 6

    def __init__(self) -> None:
        self.ships = []
        self.markers = []

    def __str__(self) -> str:
        board = [[ship.id if (ship := self.getAtPos((x, y))) is not None else 0 for x in range(Board.size[0])] for y in range(Board.size[1])]
        return str("\n".join(str(line) for line in board))

    def getAtPos(self, pos: Pos) -> Ship | None:
        if pos[0] < 0 or pos[0] >= Board.size[0]:
            return None
        if pos[1] < 0 or pos[1] >= Board.size[1]:
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


if __name__ == '__main__':
    if 'getTestShip' not in locals() and 'getTestShip' not in globals():
        from ship import getTestShip
    board = Board()
    print(board)
    ship = getTestShip(1)
    ship.rotate()
    print(ship)
    print(board.addShip(ship, (1, 1)))
    print(board)
