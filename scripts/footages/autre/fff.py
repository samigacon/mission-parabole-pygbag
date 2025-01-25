import pygame

# Initialisation de Pygame
pygame.init()

# Taille de la fenêtre
screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simulation de Trajectoire")

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 100, 255)
PINK = (255, 105, 180)

# Charger les images
background_image = pygame.image.load("pont.png")
car_image = pygame.image.load("car.png")
car_image = pygame.transform.scale(car_image, (50, 30))

# Charger des boutons pour le simulateur
reset_button_image = pygame.image.load("R.png")
simulation_button_image = pygame.image.load("S.png")
reset_button_image = pygame.transform.scale(reset_button_image, (90, 37))
simulation_button_image = pygame.transform.scale(simulation_button_image, (90, 37))

# Position du repère
origin_x, origin_y = 750, 933
step_x, step_y = 50, 25
xmin, xmax = -9.75, 16.75
ymin, ymax = -1.75, 33

# Police pour affichage
font = pygame.font.Font(None, 32)

# États
MODE_PLACEMENT = "placement"
MODE_SIMULATION = "simulation"
current_mode = MODE_PLACEMENT

# Points pour le placement
points = {
    "P1": {"pos": [origin_x - 300, origin_y - 200], "target": [-6, 25], "placed": False},
    "P2": {"pos": [origin_x - 100, origin_y - 300], "target": [0, 15], "placed": False},
    "P3": {"pos": [origin_x + 200, origin_y - 100], "target": [10, 5], "placed": False},
}
selected_point = None

# Paramètres du simulateur
A, B, C = 0, 1, 0  # Coefficients de la parabole
step_A, step_B, step_C = 0.01, 0.1, 0.25
simulation_active = False

# Fonction pour dessiner le repère
def draw_axes():
    for i in range(int(xmin), int(xmax) + 1):
        x = origin_x + i * step_x
        pygame.draw.line(screen, ORANGE, (x, origin_y - 5), (x, origin_y + 5), 2)
        if i != 0:
            label = font.render(f"{i}", True, ORANGE)
            screen.blit(label, (x - 10, origin_y + 10))

    for i in range(int(ymin), int(ymax) + 1):
        y = origin_y - i * step_y
        pygame.draw.line(screen, ORANGE, (origin_x - 5, y), (origin_x + 5, y), 2)
        if i != 0:
            label = font.render(f"{i}", True, ORANGE)
            screen.blit(label, (origin_x - 30, y - 10))

    pygame.draw.line(screen, ORANGE, (origin_x + xmin * step_x, origin_y), 
                     (origin_x + xmax * step_x, origin_y), 3)
    pygame.draw.line(screen, ORANGE, (origin_x, origin_y - ymin * step_y), 
                     (origin_x, origin_y - ymax * step_y), 3)

# Fonction pour dessiner les points
def draw_points():
    all_placed = True
    for point in points.values():
        color = GREEN if point["placed"] else WHITE
        pygame.draw.circle(screen, color, point["pos"], 10)
        if not point["placed"]:
            all_placed = False
    return all_placed

# Fonction pour dessiner la parabole
def draw_curve():
    global A, B, C
    prev_x, prev_y = None, None
    for x_pixel in range(int(xmin * step_x), int(xmax * step_x)):
        relative_x = x_pixel / step_x
        y = A * relative_x ** 2 + B * relative_x + C
        screen_x = origin_x + relative_x * step_x
        screen_y = origin_y - y * step_y

        if xmin * step_x <= relative_x * step_x <= xmax * step_x and 0 <= y <= ymax:
            if prev_x is not None:
                pygame.draw.line(screen, GREEN, (prev_x, prev_y), (screen_x, screen_y), 2)
            prev_x, prev_y = screen_x, screen_y

# Fonction principale
def main():
    global current_mode, selected_point, A, B, C, simulation_active

    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(BLACK)
        screen.blit(background_image, (0, 0))
        draw_axes()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if current_mode == MODE_PLACEMENT:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for name, point in points.items():
                        if not point["placed"]:
                            dist = ((event.pos[0] - point["pos"][0])**2 + (event.pos[1] - point["pos"][1])**2)**0.5
                            if dist < 10:
                                selected_point = name
                elif event.type == pygame.MOUSEBUTTONUP:
                    if selected_point:
                        # Vérifier si le point est placé correctement
                        target_x, target_y = points[selected_point]["target"]
                        target_px = origin_x + target_x * step_x
                        target_py = origin_y - target_y * step_y
                        dist_to_target = ((points[selected_point]["pos"][0] - target_px)**2 +
                                          (points[selected_point]["pos"][1] - target_py)**2)**0.5
                        if dist_to_target < 15:
                            points[selected_point]["placed"] = True
                        selected_point = None
                elif event.type == pygame.MOUSEMOTION and selected_point:
                    points[selected_point]["pos"] = list(event.pos)

            elif current_mode == MODE_SIMULATION:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Interagir avec les boutons ici
                    pass

        # Mode Placement
        if current_mode == MODE_PLACEMENT:
            all_placed = draw_points()
            if all_placed:
                font_big = pygame.font.Font(None, 40)
                text = font_big.render("Cliquez ici pour commencer la simulation", True, WHITE)
                screen.blit(text, (screen_width // 2 - 200, screen_height // 2))
                if pygame.mouse.get_pressed()[0]:
                    current_mode = MODE_SIMULATION

        # Mode Simulation
        elif current_mode == MODE_SIMULATION:
            draw_curve()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Lancer l'application
main()
