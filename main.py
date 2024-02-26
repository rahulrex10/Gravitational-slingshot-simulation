 # Import the Pygame module for game development.
import pygame
# Import the math module for mathematical operations.
import math

# Initialize the Pygame module.
pygame.init()
# Set the width and height of the game window.
WIDTH, HEIGHT = 800, 600
# Create a window surface object with the specified width and height.
win = pygame.display.set_mode((WIDTH, HEIGHT))
# Set the title of the window as "Gravitational Slingshot Effect".
pygame.display.set_caption("Gravitational Slingshot Effect")

# Define constants for the mass of the planet, mass of the spacecraft, gravity, frames per second,
# size of the planet, size of objects, and velocity scale.
PLANET_MASS = 100
SHIP_MASS = 5
GRAVITIY = 5
FPS = 60
PLANET_SIZED = 50
OBJECT_SIZE = 5
VELOCITY_SCALE = 100

# Load and scale the background image for the game window.
BACKGROUND = pygame.transform.scale(pygame.image.load("background space.jpg"), (WIDTH, HEIGHT))
# Load and scale the image of the planet.
PLANET = pygame.transform.scale(pygame.image.load("jupiter.png"), (PLANET_SIZED * 2, PLANET_SIZED * 2))
# Define colors for drawing objects.
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# Define a class for the planet with attributes: x-coordinate, y-coordinate, and mass.
class Planet:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass

    # Define a method to draw the planet on the game window.
    def draw(self):
        win.blit(PLANET, (self.x - PLANET_SIZED, self.y - PLANET_SIZED))


# Define a class for the spacecraft with attributes: x-coordinate, y-coordinate, x-velocity,
# y-velocity, and mass.
class Spacecraft:
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass

    # Define methods to calculate the movement of the spacecraft and to draw it on the game window.
    def move(self, planet=None):
        distance = math.sqrt((self.x - planet.x) ** 2 + (self.y - planet.y) ** 2)
        force = (GRAVITIY * self.mass * planet.mass) / distance ** 2

        acceleration = force / self.mass
        angle = math.atan2(planet.y - self.y, planet.x - self.x)
        acceleration_x = acceleration * math.cos(angle)
        acceleration_y = acceleration * math.sin(angle)

        self.vel_x += acceleration_x
        self.vel_y += acceleration_y

        self.x += self.vel_x
        self.y += self.vel_y

    def draw(self):
        pygame.draw.circle(win, RED, (int(self.x), int(self.y)), OBJECT_SIZE)


# Define a function to create a spacecraft object based on the specified location and mouse position.
def create_ship(location, mouse):
    t_x, t_y = location
    m_x, m_y = mouse
    vel_x = (m_x - t_x) / VELOCITY_SCALE
    vel_y = (m_y - t_y) / VELOCITY_SCALE
    obj = Spacecraft(t_x, t_y, vel_x, vel_y, SHIP_MASS)
    return obj


# Define the main function to run the game loop.
def main():
    running = True
    clock = pygame.time.Clock()
    planet = Planet(WIDTH // 2, HEIGHT // 2, PLANET_MASS)
    objects = []
    temp_obj_pos = None

    # Enter the game loop for continuous execution.
    while running:
        # Control the frame rate of the game.
        clock.tick(FPS)
        # Get the current mouse position.
        mouse_pos = pygame.mouse.get_pos()

        # Capture events from the event queue.
        for event in pygame.event.get():
            # If the quit event is triggered, exit the game loop.
            if event.type == pygame.QUIT:
                running = False

            # If the mouse button is pressed:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If a temporary object position exists, create a spacecraft object and append it to the list.
                if temp_obj_pos:
                    obj = create_ship(temp_obj_pos, mouse_pos)
                    objects.append(obj)
                    temp_obj_pos = None
                # Otherwise, update the temporary object position.
                else:
                    temp_obj_pos = mouse_pos

        # Draw the background image on the game window.
        win.blit(BACKGROUND, (0, 0))

        # If there's a temporary object position, draw a line and a circle indicating the object's position.
        if temp_obj_pos:
            pygame.draw.line(win, WHITE, temp_obj_pos, mouse_pos, 1)
            pygame.draw.circle(win, RED, temp_obj_pos, OBJECT_SIZE)

        # Iterate through spacecraft objects:
        for obj in objects[:]:
            # Draw each spacecraft.
            obj.draw()
            # Move the spacecraft based on gravitational forces from the planet.
            obj.move(planet)
            # Remove the spacecraft if it goes off-screen or collides with the planet.
            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            collided = math.sqrt((obj.x - planet.x) ** 2 + (obj.y - planet.y) ** 2) <= PLANET_SIZED
            if off_screen or collided:
                objects.remove(obj)
        # Draw the planet on the game window.
        planet.draw()
        # Update the display.
        pygame.display.update()
    # Quit pygame and exit the program when the game loop ends.
    pygame.quit()


# Entry point of the program.
if __name__ == "__main__":
    main()
