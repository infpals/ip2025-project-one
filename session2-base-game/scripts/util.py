type Pos = tuple[int, int] | list[int]
type Grid = list[list[int | str]]

def rotateIp(matrix: Grid, rotation: int) -> None:
    for _ in range(rotation % 4):
        n = len(matrix)
        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        for row in matrix:
            row.reverse()


def rotate90(matrix: Grid) -> Grid:
    rows = len(matrix)
    cols = len(matrix[0])

    rotated = []
    for col in range(cols):
        new_row = []
        for row in range(rows - 1, -1, -1):
            new_row.append(matrix[row][col])
        rotated.append(new_row)

    return rotated

def rotate270(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    rotated = []
    for col in range(cols - 1, -1, -1):
        new_row = []
        for row in range(rows):
            new_row.append(matrix[row][col])
        rotated.append(new_row)

    return rotated


async def getIntegerInput(prompt: str) -> int:
    try:
        return int(input(prompt))
    except ValueError:
        return -1

async def getPosInput() -> Pos:
    return await getIntegerInput("Enter the x position\n> "), await getIntegerInput("Enter the y position\n> ")

prompt_new = \
"""
Enter an option (1-5):
1 > Add a ship
2 > Move a ship
3 > View all ships
4 > View board
5 > Confirm Ships
"""
