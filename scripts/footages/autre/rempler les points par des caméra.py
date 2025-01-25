import pygame

# Initialisation de Pygame
pygame.init()

# Charger les images
background_image = pygame.image.load("pont.png")  # Image pour la simulation principale
image_lm = pygame.image.load("LM.png")  # Image pour afficher en haut, redimensionnée
image_st = pygame.image.load("ST.png")  # Nouvelle image pour l'étape intermédiaire

# Redimensionner l'image LM
image_lm = pygame.transform.scale(image_lm, (150, 100))  # Ajuster la taille

# Taille de la fenêtre
screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simulation de Trajectoire")

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)

# Police pour les textes
font = pygame.font.Font(None, 36)

# États de l'application
STATE_INTRO = "intro"
STATE_SIMULATION = "simulation"
current_state = STATE_INTRO

# Zone interactive
interactive_zone = {"x": 845, "y": 882, "width": 300, "height": 100}

# Repère
origin_x, origin_y = 750, 933
step_x, step_y = 50, 25
xmin, xmax = -9.75, 16.75
ymin, ymax = -1.75, 33

# Points à placer
points = {
    "P1": {"pos": [100, 200], "target": [-2.25, 0], "color": WHITE, "radius": 10},
    "P2": {"pos": [100, 300], "target": [0, 3.5], "color": WHITE, "radius": 10},
    "P3": {"pos": [100, 400], "target": [15.5, 0], "color": WHITE, "radius": 10},
}
selected_point = None

# Fonction pour convertir les coordonnées cartésiennes en pixels
def cartesian_to_pixel(x, y):
    px = origin_x + x * step_x
    py = origin_y - y * step_y
    return int(px), int(py)

# Fonction pour afficher du texte centré
def draw_text_centered(text, font, color, surface, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

# Fonction pour dessiner les axes du repère
def draw_axes():
    for i in range(int(xmin), int(xmax) + 1):
        x = origin_x + i * step_x
        pygame.draw.line(screen, ORANGE, (x, origin_y - 5), (x, origin_y + 5), 1)
        if i != 0:
            label = font.render(f"{i}", True, ORANGE)
            screen.blit(label, (x - 10, origin_y + 10))

    for i in range(int(ymin), int(ymax) + 1):
        y = origin_y - i * step_y
        pygame.draw.line(screen, ORANGE, (origin_x - 5, y), (origin_x + 5, y), 1)
        if i != 0:
            label = font.render(f"{i}", True, ORANGE)
            screen.blit(label, (origin_x - 30, y - 10))

    pygame.draw.line(screen, ORANGE, (origin_x + xmin * step_x, origin_y),
                     (origin_x + xmax * step_x, origin_y), 2)
    pygame.draw.line(screen, ORANGE, (origin_x, origin_y - ymin * step_y),
                     (origin_x, origin_y - ymax * step_y), 2)

# Fonction principale
def main():
    global current_state, selected_point

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_state == STATE_INTRO:
                    if (interactive_zone["x"] - interactive_zone["width"] // 2 <= event.pos[0] <= interactive_zone["x"] + interactive_zone["width"] // 2 and
                        interactive_zone["y"] - interactive_zone["height"] // 2 <= event.pos[1] <= interactive_zone["y"] + interactive_zone["height"] // 2):
                        current_state = STATE_SIMULATION
                elif current_state == STATE_SIMULATION:
                    for name, point in points.items():
                        distance = ((event.pos[0] - point["pos"][0])**2 + (event.pos[1] - point["pos"][1])**2)**0.5
                        if distance <= point["radius"]:
                            selected_point = name
            elif event.type == pygame.MOUSEBUTTONUP:
                selected_point = None
            elif event.type == pygame.MOUSEMOTION and selected_point:
                points[selected_point]["pos"] = list(event.pos)

        # Nouvelle étape intermédiaire
        if current_state == STATE_INTRO:
            screen.blit(image_st, (screen_width // 2 - image_st.get_width() // 2, screen_height // 2 - image_st.get_height() // 2))
            screen.blit(image_lm, ((screen_width // 2) - (image_lm.get_width() // 2), 10))  # Centrer en haut de l'écran

        # Simulation principale
        elif current_state == STATE_SIMULATION:
            screen.blit(background_image, (0, 0))
            draw_axes()
            draw_text_centered("Simulation en cours", font, WHITE, screen, screen_width // 2, 30)

            all_correct = True
            for name, point in points.items():
                target_px, target_py = cartesian_to_pixel(*point["target"])
                distance = ((target_px - point["pos"][0])**2 + (target_py - point["pos"][1])**2)**0.5
                if distance >= 10:
                    all_correct = False

                point["color"] = GREEN if all_correct else WHITE

                pygame.draw.circle(screen, point["color"], point["pos"], point["radius"])
                cart_x, cart_y = point["target"]
                draw_text_centered(f"{name}({cart_x};{cart_y})", font, point["color"], screen, point["pos"][0] + 70, point["pos"][1] - 20)

            draw_text_centered("Placez les points sur le repère", font, WHITE, screen, screen_width // 2, 70)

            if all_correct:
                pygame.draw.rect(screen, WHITE, (screen_width - 250, 50, 200, 50), border_radius=15)
                draw_text_centered("Poursuivre", font, BLACK, screen, screen_width - 150, 75)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Lancer l'application
main()
