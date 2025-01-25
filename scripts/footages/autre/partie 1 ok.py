import pygame

# Initialisation de Pygame
pygame.init()

# Charger les images
background_image = pygame.image.load("pont.png")  # Image pour la simulation principale
image_lm = pygame.image.load("LM.png")  # Image pour afficher en haut
image_st = pygame.image.load("ST.png")  # Nouvelle image pour l'étape intermédiaire
ecran_image = pygame.image.load("ecran.png")  # Image pour l'écran explicatif

# Taille de la fenêtre
screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simulation de Trajectoire")

# Redimensionner les images
lm_original_width, lm_original_height = 1139, 429
lm_new_width = 400  # Nouvelle largeur souhaitée
lm_new_height = int(lm_new_width * lm_original_height / lm_original_width)  # Calculer la hauteur proportionnelle
image_lm = pygame.transform.scale(image_lm, (lm_new_width, lm_new_height))

ecran_image = pygame.transform.scale(ecran_image, (800, 400))  # Taille ajustée pour centrer le texte
ecran_rect = ecran_image.get_rect(center=(screen_width // 2, screen_height // 2))  # Centré par rapport à "pont"

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 100, 255)

# Police pour les textes
font = pygame.font.Font(None, 32)

# Fonction pour dessiner un texte multi-lignes centré dans l'image "écran"
def draw_screen():
    screen.blit(ecran_image, ecran_rect.topleft)

    # Texte explicatif
    explanation_text = (
        "Bienvenue dans le simulateur de trajectoire.\n\n"
        "Placez trois caméras pour capter la scène de manière impressionnante. "
        "Ces caméras, représentées par des points blancs avec des coordonnées, "
        "serviront également de repères pour tracer la trajectoire.\n\n"
        "Positionnez-les correctement afin de capturer les meilleurs angles pour le tournage."
    )

    # Découpage du texte pour qu'il tienne dans la largeur de l'image "écran"
    wrapped_text = []
    max_width = ecran_rect.width - 80  # Marges intérieures (ajustées)
    for line in explanation_text.split("\n"):
        words = line.split(" ")
        current_line = ""
        for word in words:
            if font.size(current_line + word)[0] <= max_width:
                current_line += word + " "
            else:
                wrapped_text.append(current_line.strip())
                current_line = word + " "
        wrapped_text.append(current_line.strip())

    # Dessin des lignes de texte centrées dans l'image "écran"
    y_offset = ecran_rect.top + 60  # Ajustement pour centrer verticalement
    for line in wrapped_text:
        text_surface = font.render(line, True, WHITE)
        text_rect = text_surface.get_rect(center=(ecran_rect.centerx, y_offset))
        screen.blit(text_surface, text_rect)
        y_offset += 35  # Espacement entre les lignes

# États de l'application
STATE_START = "start"
STATE_INTRO = "intro"
STATE_SIMULATION = "simulation"
STATE_INSTRUCTIONS = "instructions"  # Nouvel état pour afficher les instructions
current_state = STATE_START

# Repère
origin_x, origin_y = 750, 933
step_x, step_y = 50, 25
xmin, xmax = -9.75, 16.75
ymin, ymax = -1.75, 33

# Fonction pour convertir les coordonnées cartésiennes en pixels
def cartesian_to_pixel(x, y):
    px = origin_x + x * step_x
    py = origin_y - y * step_y
    return int(px), int(py)

# Points à placer (alignés verticalement)
points = {
    "P1": {"pos": cartesian_to_pixel(-6, 25), "target": [-2.25, 0], "color": WHITE, "radius": 10},
    "P2": {"pos": cartesian_to_pixel(-6, 20), "target": [0, 3.5], "color": WHITE, "radius": 10},
    "P3": {"pos": cartesian_to_pixel(-6, 15), "target": [15.5, 0], "color": WHITE, "radius": 10},
}
selected_point = None

# Position du bouton "Instructions"
instruction_button_rect = pygame.Rect(
    points["P1"]["pos"][0] - 120,  # Ajustement horizontal pour aligner avec P1
    points["P1"]["pos"][1] - 150,  # Ajustement vertical au-dessus de l'étiquette de P1
    200,  # Largeur
    50    # Hauteur
)

# Position du bouton "Poursuivre" (sous "Instructions")
poursuivre_button_rect = pygame.Rect(
    instruction_button_rect.left,        # Aligné horizontalement avec "Instructions"
    instruction_button_rect.bottom + 20,  # Placé en dessous avec 20px d'espacement
    200,                                # Largeur
    50                                  # Hauteur
)

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
                if current_state == STATE_START:
                    current_state = STATE_INTRO
                elif current_state == STATE_INTRO:
                    current_state = STATE_SIMULATION
                elif current_state == STATE_SIMULATION:
                    if instruction_button_rect.collidepoint(event.pos):  # Bouton "Instructions"
                        current_state = STATE_INSTRUCTIONS
                    for name, point in points.items():
                        distance = ((event.pos[0] - point["pos"][0])**2 + (event.pos[1] - point["pos"][1])**2)**0.5
                        if distance <= point["radius"] and not selected_point:
                            selected_point = name
                elif current_state == STATE_INSTRUCTIONS:
                    current_state = STATE_SIMULATION  # Retour à la simulation
            elif event.type == pygame.MOUSEBUTTONUP:
                selected_point = None
            elif event.type == pygame.MOUSEMOTION and selected_point:
                points[selected_point]["pos"] = list(event.pos)

        # Page de démarrage avec ST et LM
        if current_state == STATE_START:
            screen.blit(image_st, (screen_width // 2 - image_st.get_width() // 2, screen_height // 2 - image_st.get_height() // 2))
            lm_x = (screen_width - lm_new_width) // 2
            lm_y = 50
            screen.blit(image_lm, (lm_x, lm_y))
        
        # Page avec le repère et l'écran explicatif
        elif current_state == STATE_INTRO:
            screen.blit(background_image, (0, 0))
            draw_axes()
            draw_screen()

        # Simulation principale
        elif current_state == STATE_SIMULATION:
            screen.blit(background_image, (0, 0))
            draw_axes()

            # Dessin du bouton "Instructions"
            pygame.draw.rect(screen, BLUE, instruction_button_rect, border_radius=10)
            draw_text_centered("Instructions", font, WHITE, screen, instruction_button_rect.centerx, instruction_button_rect.centery)

            all_correct = True
            for name, point in points.items():
                target_px, target_py = cartesian_to_pixel(*point["target"])
                distance = ((target_px - point["pos"][0])**2 + (target_py - point["pos"][1])**2)**0.5
                if distance >= 10:
                    all_correct = False

                point["color"] = GREEN if all_correct else WHITE
                pygame.draw.circle(screen, point["color"], point["pos"], point["radius"])
                cart_x, cart_y = point["target"]
                draw_text_centered(f"{name}({cart_x};{cart_y})", font, point["color"], screen, point["pos"][0] - 70, point["pos"][1] - 20)

            if all_correct:
                # Dessiner l'onglet "Poursuivre"
                pygame.draw.rect(screen, WHITE, poursuivre_button_rect, border_radius=10)
                draw_text_centered("Poursuivre", font, BLACK, screen, poursuivre_button_rect.centerx, poursuivre_button_rect.centery)

        # Afficher l'écran des instructions
        elif current_state == STATE_INSTRUCTIONS:
            draw_screen()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Lancer l'application
main()
