# Intro to Pygame

# pip install pygame
import pygame

# Initialize Pygame
pygame.init()

# Colours
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Create the screen
size = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Beginner Pygame Example")

# Clock to control frame rate
clock = pygame.time.Clock()

# Circle properties
circle_pos = [size[0] // 2, size[1] // 2]
circle_radius = 30
circle_color = blue

# Fonts
my_font_name = pygame.font.get_default_font()
my_font = pygame.font.Font(my_font_name, 30)
my_text = my_font.render(" ", True, black)

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Change circle colour when clicked
            if event.button == 1:  # Left click
                circle_color = red
            elif event.button == 3:  # Right click
                circle_color = blue
        elif event.type == pygame.MOUSEMOTION:
            # Move circle with mouse
            circle_pos = list(event.pos)
        elif event.type == pygame.KEYDOWN:
            # If character pressed is alphanumeric, change the text.
            if event.unicode.isalnum():
                my_text = my_font.render(event.unicode, True, black)

    # Clear screen
    screen.fill(white)

    # Draw the shapes
    pygame.draw.circle(screen, circle_color, circle_pos, circle_radius)
    pygame.draw.rect(screen, black, (50, 50, 200, 100), 2)

    # Draw the text
    screen.blit(my_text, (500, 400))

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

# Close pygame
pygame.quit()
