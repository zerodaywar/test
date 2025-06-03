import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Spinning Hexagon")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Hexagon properties
HEX_RADIUS = 200  # Radius of the hexagon
HEX_CENTER = (WIDTH // 2, HEIGHT // 2)  # Center of the hexagon
HEX_ROTATION_SPEED = 1  # Degrees per frame

# Ball properties
BALL_RADIUS = 20
BALL_COLOR = RED
ball_pos = [HEX_CENTER[0], HEX_CENTER[1] - HEX_RADIUS + BALL_RADIUS]  # Start at top
ball_vel = [2, 0]  # Initial velocity (x, y)
GRAVITY = 0.2  # Gravity effect
FRICTION = 0.99  # Friction effect

# Clock for controlling frame rate
clock = pygame.time.Clock()

def rotate_point(point, center, angle):
    """Rotate a point around a center by a given angle (in degrees)."""
    angle_rad = math.radians(angle)
    x, y = point
    cx, cy = center
    dx = x - cx
    dy = y - cy
    new_x = cx + dx * math.cos(angle_rad) - dy * math.sin(angle_rad)
    new_y = cy + dx * math.sin(angle_rad) + dy * math.cos(angle_rad)
    return (new_x, new_y)

def get_hexagon_points(center, radius, rotation):
    """Get the vertices of a hexagon."""
    points = []
    for i in range(6):
        angle_deg = 60 * i + rotation
        angle_rad = math.radians(angle_deg)
        x = center[0] + radius * math.cos(angle_rad)
        y = center[1] + radius * math.sin(angle_rad)
        points.append((x, y))
    return points

def check_collision(ball_pos, ball_vel, hex_points):
    """Check for collision between the ball and the hexagon walls."""
    for i in range(len(hex_points)):
        p1 = hex_points[i]
        p2 = hex_points[(i + 1) % len(hex_points)]
        
        # Vector of the wall
        wall_vec = (p2[0] - p1[0], p2[1] - p1[1])
        wall_length = math.hypot(wall_vec[0], wall_vec[1])
        wall_unit_vec = (wall_vec[0] / wall_length, wall_vec[1] / wall_length)
        
        # Vector from ball to wall start
        ball_to_wall = (ball_pos[0] - p1[0], ball_pos[1] - p1[1])
        
        # Project ball_to_wall onto wall_unit_vec
        projection = (ball_to_wall[0] * wall_unit_vec[0] + ball_to_wall[1] * wall_unit_vec[1])
        closest_point = (p1[0] + projection * wall_unit_vec[0], p1[1] + projection * wall_unit_vec[1])
        
        # Distance from ball to closest point on the wall
        distance = math.hypot(ball_pos[0] - closest_point[0], ball_pos[1] - closest_point[1])
        
        if distance <= BALL_RADIUS:
            # Calculate reflection
            normal_vec = (-wall_unit_vec[1], wall_unit_vec[0])  # Perpendicular to the wall
            dot_product = ball_vel[0] * normal_vec[0] + ball_vel[1] * normal_vec[1]
            ball_vel[0] -= 2 * dot_product * normal_vec[0]
            ball_vel[1] -= 2 * dot_product * normal_vec[1]
            
            # Move ball outside the wall to avoid sticking
            overlap = BALL_RADIUS - distance
            ball_pos[0] += overlap * normal_vec[0]
            ball_pos[1] += overlap * normal_vec[1]
            
            # Apply friction
            ball_vel[0] *= FRICTION
            ball_vel[1] *= FRICTION

# Main loop
rotation = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update rotation
    rotation += HEX_ROTATION_SPEED
    if rotation >= 360:
        rotation -= 360

    # Update ball position and velocity
    ball_vel[1] += GRAVITY  # Apply gravity
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Get hexagon points
    hex_points = get_hexagon_points(HEX_CENTER, HEX_RADIUS, rotation)

    # Check for collisions
    check_collision(ball_pos, ball_vel, hex_points)

    # Clear screen
    screen.fill(WHITE)

    # Draw hexagon
    pygame.draw.polygon(screen, BLACK, hex_points, 2)

    # Draw ball
    pygame.draw.circle(screen, BALL_COLOR, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)

    # Update display
    pygame.display.flip()

    # Cap frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()