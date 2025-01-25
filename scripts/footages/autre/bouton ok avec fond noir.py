import pygame

# Initialisation de Pygame
pygame.init()

# Charger l'image du fond
background = pygame.image.load("pont.png")
screen_width, screen_height = background.get_size()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simulation de Trajectoire avec Repère et Parabole")

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
PINK = (255, 105, 180)
GRAY = (200, 200, 200)

# Position initiale de la voiture et paramètres de mouvement
car_x, car_y = 750, 814  # Position initiale au bord du pont, inclinée à 45°
car_speed = 5  # Vitesse horizontale
initial_car_x, initial_car_y = car_x, car_y  # Sauvegarde de la position initiale
car_angle = 45  # Angle initial de la voiture (inclinaison au départ)

# Points clés de la simulation
simulation_start_x, simulation_start_y = 268, 920  # Point de départ
inclination_point_x, inclination_point_y = 620, 930  # Point d'inclinaison à 45°
landing_point_x, landing_point_y = 1526, 925  # Point d'atterrissage

# Charger et redimensionner l'image de la voiture
car_image = pygame.image.load("car.png")
car_image = pygame.transform.scale(car_image, (50, 30))  # Redimensionner la voiture

# Centre et échelle du repère
origin_x, origin_y = 750, 933  # Centre du repère
step_x, step_y = 50, 25  # Taille des unités
xmin, xmax = -9.75, 16.75  # Limites des abscisses
ymin, ymax = -1.75, 33  # Limites des ordonnées

# Paramètres de la courbe
A, B, C = 0, 1, 0  # Départ avec une droite
step_A, step_B, step_C = 0.001, 0.1, 0.25
curve_validated = False

# Décalage vertical pour que la voiture reste au-dessus de la parabole
vertical_offset = 30

# Police pour affichage
font = pygame.font.Font(None, 24)

# Chargement des images des boutons
button_a_image = pygame.image.load("A.png")
button_b_image = pygame.image.load("B.png")
button_c_image = pygame.image.load("C.png")
button_a_image = pygame.transform.scale(button_a_image, (90, 150))
button_b_image = pygame.transform.scale(button_b_image, (90, 150))
button_c_image = pygame.transform.scale(button_c_image, (90, 150))

# Positions des boutons
button_a_rect = button_a_image.get_rect(topleft=(300, 150))
button_b_rect = button_b_image.get_rect(topleft=(300, 300))
button_c_rect = button_c_image.get_rect(topleft=(300, 450))

# Dimensions et position de l'écran central
ecran_width, ecran_height = 842, 505
ecran_rect = pygame.Rect((screen_width - ecran_width) // 2, 50, ecran_width, ecran_height)

# Fonction pour dessiner les axes
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

# Fonction pour dessiner la courbe
def draw_curve():
    prev_x, prev_y = None, None
    curve_color = GREEN if round(A, 3) == -0.098 and round(B, 1) == 1.3 and round(C, 2) == 3.5 else RED

    for x_pixel in range(int(xmin * step_x), int(xmax * step_x)):
        relative_x = x_pixel / step_x
        y = A * relative_x ** 2 + B * relative_x + C
        screen_x = origin_x + relative_x * step_x
        screen_y = origin_y - y * step_y

        if xmin * step_x <= relative_x * step_x <= xmax * step_x and 0 <= y <= ymax:
            if prev_x is not None:
                pygame.draw.line(screen, curve_color, (prev_x, prev_y), (screen_x, screen_y), 2)
            prev_x, prev_y = screen_x, screen_y

    return curve_color == GREEN

# Fonction pour dessiner les boutons avec arrière-plan
def draw_buttons():
    # Dessin du rectangle noir avec angles arrondis
    rect_width = 120
    rect_height = 480
    rect_x = 288
    rect_y = 140
    pygame.draw.rect(screen, BLACK, (rect_x, rect_y, rect_width, rect_height), border_radius=20)

    # Dessiner les boutons
    screen.blit(button_a_image, button_a_rect)
    screen.blit(button_b_image, button_b_rect)
    screen.blit(button_c_image, button_c_rect)

# Fonction pour dessiner l'écran central
def draw_screen():
    pygame.draw.rect(screen, GRAY, ecran_rect, border_radius=20)
    text_general = font.render("f(x) = a x² + b x + c", True, WHITE)
    text_values = font.render(f"f(x) = {A:.3f} x² + {B:.1f} x + {C:.2f}", True, WHITE)
    screen.blit(text_general, (ecran_rect.x + 20, ecran_rect.y + 20))
    screen.blit(text_values, (ecran_rect.x + 20, ecran_rect.y + 60))

# Gestion des clics
def handle_button_click(mouse_pos):
    global A, B, C
    if button_a_rect.collidepoint(mouse_pos):
        if mouse_pos[0] < button_a_rect.centerx:
            A += step_A
        else:
            A -= step_A
    elif button_b_rect.collidepoint(mouse_pos):
        if mouse_pos[0] < button_b_rect.centerx:
            B += step_B
        else:
            B -= step_B
    elif button_c_rect.collidepoint(mouse_pos):
        if mouse_pos[0] < button_c_rect.centerx:
            C += step_C
        else:
            C -= step_C

# Boucle principale
running = True
while running:
    screen.fill(BLACK)
    screen.blit(background, (0, 0))
    draw_axes()
    draw_curve()
    draw_buttons()
    draw_screen()

    rotated_car = pygame.transform.rotate(car_image, car_angle)
    screen.blit(rotated_car, (car_x - 25, car_y - 15))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_button_click(event.pos)

pygame.quit()
