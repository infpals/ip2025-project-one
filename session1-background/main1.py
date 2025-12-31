from scripts1 import *

if __name__ == '__main__':
    if 'json' not in locals() and 'json' not in globals():
        import json
    if 'asyncio' not in locals() and 'asyncio' not in globals():
        import asyncio
    with open("ships.json") as f:
        ships = json.load(f)
    p = Player("Test", ships)
    asyncio.run(p.new())
