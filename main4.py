from scripts import *
import pygame, json


class Game:
    SIZE = 800, 600
    CELL = 40

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(Game.SIZE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.running = True

        with open("scripts/ships.json") as f:
            ship_data = json.load(f)

        self.players = [Player("Player A", ship_data), Player("Player B", ship_data)]
        self.current = 0

        self.state = "placement"

        self.dragging_ship: Ship | None = None
        self.mouse_pos = (0, 0)

        self.button_rect = pygame.Rect(700, 500, 150, 50)

    def currentPlayer(self):
        return self.players[self.current]

    def opponent(self):
        return self.players[1 - self.current]

    def gridFromMouse(self, pos):
        return pos[0] // Game.CELL, pos[1] // Game.CELL

    # ------------------ EVENTS ------------------

    def handlePlacementEvents(self, event):
        player = self.currentPlayer()

        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # pick up ship
            for ship in player.ships:
                if not ship.placed:
                    self.dragging_ship = ship
                    self.mouse_pos = event.pos
                    return

            # confirm
            if self.button_rect.collidepoint(mx, my):
                if all(s.placed for s in player.ships):
                    if self.current == 0:
                        self.current = 1
                    else:
                        self.state = "battle"

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging_ship:
                grid = self.gridFromMouse(self.mouse_pos)
                if player.board.canPlace(self.dragging_ship, grid):
                    player.board.addShip(self.dragging_ship, grid)
                self.dragging_ship = None

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.dragging_ship:
                self.dragging_ship.rotate()

    def handleBattleEvents(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # Only allow clicks on RIGHT grid (opponent board)
            if x < 450:
                return

            grid_x = (x - 450) // Game.CELL
            grid_y = y // Game.CELL

            pos = (grid_x, grid_y)

            # Prevent out-of-bounds
            if not self.opponent().board.inBounds(pos):
                return

            result = self.opponent().board.addMarker(pos)

            if result is None:
                return  # duplicate shot

            print("HIT" if result else "MISS")
            self.current = 1 - self.current

    # ------------------ DRAW ------------------

    def drawGrid(self, offset_x=0):
        for y in range(Board.size[1]):
            for x in range(Board.size[0]):
                rect = pygame.Rect(
                    offset_x + x * Game.CELL,
                    y * Game.CELL,
                    Game.CELL,
                    Game.CELL
                )
                pygame.draw.rect(self.screen, "black", rect, 1)

    def drawShips(self, player, hide=False):
        for ship in player.board.ships:
            if hide and not ship.isDead():
                continue
            for x, y in ship.getPoss():
                rect = pygame.Rect(x * Game.CELL, y * Game.CELL, Game.CELL, Game.CELL)
                pygame.draw.rect(self.screen, "grey", rect)

    def drawMarkers(self, board, offset_x=0):
        for x, y, hit in board.markers:
            rect = pygame.Rect(
                offset_x + x * Game.CELL,
                y * Game.CELL,
                Game.CELL,
                Game.CELL
            )
            color = "red" if hit else "blue"
            pygame.draw.circle(self.screen, color, rect.center, 8)

    def drawDraggingShip(self):
        if not self.dragging_ship:
            return

        ship = self.dragging_ship
        grid = self.gridFromMouse(self.mouse_pos)

        valid = self.currentPlayer().board.canPlace(ship, grid)

        for x, y in ship.getPoss(grid):
            rect = pygame.Rect(
                x * Game.CELL,
                y * Game.CELL,
                Game.CELL,
                Game.CELL
            )
            pygame.draw.rect(
                self.screen,
                "green" if valid else "red",
                rect
            )

    def drawPlacement(self):
        player = self.currentPlayer()

        self.drawGrid()
        self.drawShips(player)

        self.drawDraggingShip()

        pygame.draw.rect(self.screen, "green", self.button_rect)
        font = pygame.font.SysFont(None, 24)
        txt = font.render("Confirm", True, "black")
        self.screen.blit(txt, (self.button_rect.x + 20, self.button_rect.y + 15))

    def drawBattle(self):
        self.drawGrid(0)
        # self.drawGrid(450)

        self.drawShips(self.currentPlayer(), hide=True)
        self.drawMarkers(self.currentPlayer().board, 0)

        # self.drawShips(self.opponent(), hide=True)
        # self.drawMarkers(self.opponent().board, 450)

    def drawPlayerLabel(self):
        text = self.font.render(
            f"{self.currentPlayer().name}'s Turn",
            True,
            "black"
        )

        self.screen.blit(text, (10, Game.SIZE[1] - 40))

    # ------------------ LOOP ------------------

    def run(self):
        while self.running:
            self.screen.fill("white")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if self.state == "placement":
                    self.handlePlacementEvents(event)
                elif self.state == "battle":
                    self.handleBattleEvents(event)

            if self.state == "placement":
                self.drawPlacement()
                self.drawPlayerLabel()
            else:
                self.drawBattle()
                self.drawPlayerLabel()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
