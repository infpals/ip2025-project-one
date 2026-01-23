# Background

from scripts import *
import json
import asyncio


if __name__ == '__main__':
    with open("scripts/ships.json") as f:
        ships = json.load(f)
    p = Player("Test", ships)
    asyncio.run(p.new())
