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

# Fonction pour dessiner les boutons
def draw_buttons():
    buttons = [
        {"label": "+", "rect": pygame.Rect(10, 10, 40, 30), "action": "A_up"},
        {"label": "-", "rect": pygame.Rect(60, 10, 40, 30), "action": "A_down"},
        {"label": "+", "rect": pygame.Rect(10, 50, 40, 30), "action": "B_up"},
        {"label": "-", "rect": pygame.Rect(60, 50, 40, 30), "action": "B_down"},
        {"label": "+", "rect": pygame.Rect(10, 90, 40, 30), "action": "C_up"},
        {"label": "-", "rect": pygame.Rect(60, 90, 40, 30), "action": "C_down"}
    ]

    if curve_validated:
        buttons.append({"label": "Réinitialiser", "rect": pygame.Rect(10, 130, 100, 30), "action": "reset"})
        buttons.append({"label": "Lancer la simulation", "rect": pygame.Rect(120, 130, 200, 30), "action": "launch"})

    for button in buttons:
        pygame.draw.rect(screen, GRAY, button["rect"])
        label = font.render(button["label"], True, BLACK)
        screen.blit(label, (button["rect"].x + 10, button["rect"].y + 5))

    value_A = font.render(f"A: {A:.3f}", True, WHITE)
    value_B = font.render(f"B: {B:.1f}", True, WHITE)
    value_C = font.render(f"C: {C:.2f}", True, WHITE)
    screen.blit(value_A, (110, 15))
    screen.blit(value_B, (110, 55))
    screen.blit(value_C, (110, 95))
    return buttons

# Gestion des clics
def handle_button_click(mouse_pos, buttons):
    global A, B, C, car_x, car_y, car_angle, simulation_active
    for button in buttons:
        if button["rect"].collidepoint(mouse_pos):
            if button["action"] == "A_up":
                A += step_A
            elif button["action"] == "A_down":
                A -= step_A
            elif button["action"] == "B_up":
                B += step_B
            elif button["action"] == "B_down":
                B -= step_B
            elif button["action"] == "C_up":
                C += step_C
            elif button["action"] == "C_down":
                C -= step_C
            elif button["action"] == "reset":
                car_x, car_y = initial_car_x, initial_car_y
                car_angle = 45  # Retour à l'angle initial (incliné)
                simulation_active = False
            elif button["action"] == "launch":
                simulation_active = True
                car_x, car_y = simulation_start_x, simulation_start_y  # Point de départ de la simulation
                print(f"Simulation lancée depuis : car_x={car_x}, car_y={car_y}")  # Debug

# Boucle principale
running = True
simulation_active = False
while running:
    screen.fill(BLACK)
    screen.blit(background, (0, 0))
    draw_axes()
    curve_validated = draw_curve()
    buttons = draw_buttons()

    if not simulation_active:
        rotated_car = pygame.transform.rotate(car_image, car_angle)
        screen.blit(rotated_car, (car_x - 25, car_y - 15))  # Afficher la voiture à sa position initiale

    if simulation_active:
        if car_x < inclination_point_x:
            # Mouvement horizontal jusqu'au point d'inclinaison
            car_x += car_speed
            car_y = simulation_start_y
            car_angle = 0
        elif car_x >= inclination_point_x and car_x < landing_point_x:
            # Inclinaison progressive de la voiture à 45° et montée suivant la parabole
            car_angle = 45
            relative_x = (car_x - origin_x) / step_x
            car_y = origin_y - (A * relative_x ** 2 + B * relative_x + C) * step_y - vertical_offset
            car_x += car_speed
        else:
            # Transition progressive vers l'horizontale à l'atterrissage
            if car_angle > 0:
                car_angle -= 1  # Transition encore plus lente
            car_x += car_speed
            relative_x = (car_x - origin_x) / step_x
            car_y = origin_y - (A * relative_x ** 2 + B * relative_x + C) * step_y - vertical_offset

            if car_x >= landing_point_x:
                car_angle = 0
                car_x, car_y = landing_point_x, landing_point_y  # Ajusté pour l'atterrissage final
                simulation_active = False

        rotated_car = pygame.transform.rotate(car_image, car_angle)
        screen.blit(rotated_car, (car_x - 25, car_y - 15))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_button_click(event.pos, buttons)

pygame.quit()
