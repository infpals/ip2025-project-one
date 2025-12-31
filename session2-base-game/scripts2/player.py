from util import *
from board import Board
from ship import Ship


class Player:
    def __init__(self, name: str, ship_data: dict) -> None:
        self.name = name
        self.ship_data = ship_data
        self.board = None

    async def new(self):
        self.board = Board()
        confirmed = False
        placed = 0
        ships = []
        for k in self.ship_data:
            for _ in range(int(self.ship_data[k]['count'])):
                ships.append(Ship(int(k), self.ship_data[k]['shape']))

        while not confirmed:
            print(f"\nYou have placed {placed} ships out of {len(ships)}.")
            option = await getIntegerInput(prompt_new)
            if option < 0 or option > 5:
                print("Invalid input. Please try again.")
                continue

            match option:
                case 1:  # Add a ship
                    pick = await getIntegerInput("Enter ship number:\n> ")
                    if pick < 0 or pick > len(ships):
                        print("Invalid input. Please try again.")
                        continue
                    ship = ships[pick]
                    rotate = await getIntegerInput("Rotate ship (0/1):\n> ")
                    if rotate < 0 or rotate > 1:
                        print("Invalid input. Please try again.")
                        continue
                    if rotate:
                        ship.rotate()
                    self.board.addShip(ship, await getPosInput())
                    placed += 1
                case 2:  # Move a ship
                    ship = self.board.getAtPos(await getPosInput())
                    if ship is None:
                        print("Invalid input. Please try again.")
                        continue
                    rotate = await getIntegerInput("Rotate ship (0/1):\n> ")
                    if rotate < 0 or rotate > 1:
                        print("Invalid input. Please try again.")
                        continue
                    if rotate:
                        ship.rotate()
                    print("Enter the new position.")
                    ship.pos = await getPosInput()
                case 3:  # View all ships
                    for i, ship in enumerate(ships):
                        print(f"{i}: {ship}")
                case 4:  # View board
                    print(self.board)
                case 5:  # Confirm Ships
                    if placed < len(ships):
                        print("You have not placed all ships yet.")
                    else:
                        confirmed = True
