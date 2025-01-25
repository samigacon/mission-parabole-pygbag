import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Charger les images pour Code 1
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

# Fonction pour dessiner un texte centré
def draw_text_centered(text, font, color, surface, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

# État de l'application
STATE_CODE1 = "code1"
STATE_CODE2 = "code2"
current_state = STATE_CODE1

# Points pour Code 1
origin_x, origin_y = 750, 933
step_x, step_y = 50, 25

def cartesian_to_pixel(x, y):
    px = origin_x + x * step_x
    py = origin_y - y * step_y
    return int(px), int(py)

points = {
    "P1": {"pos": cartesian_to_pixel(-6, 25), "target": [-2.25, 0], "color": WHITE, "radius": 10},
    "P2": {"pos": cartesian_to_pixel(-6, 20), "target": [0, 3.5], "color": WHITE, "radius": 10},
    "P3": {"pos": cartesian_to_pixel(-6, 15), "target": [15.5, 0], "color": WHITE, "radius": 10},
}
selected_point = None

# Position des boutons
instruction_button_rect = pygame.Rect(500, 200, 200, 50)
poursuivre_button_rect = pygame.Rect(500, 300, 200, 50)

# Dessiner les axes pour Code 1
def draw_axes_code1():
    for i in range(-10, 17):
        x = origin_x + i * step_x
        pygame.draw.line(screen, ORANGE, (x, origin_y - 5), (x, origin_y + 5), 1)
    for i in range(-2, 34):
        y = origin_y - i * step_y
        pygame.draw.line(screen, ORANGE, (origin_x - 5, y), (origin_x + 5, y), 1)
    pygame.draw.line(screen, ORANGE, (0, origin_y), (screen_width, origin_y), 2)
    pygame.draw.line(screen, ORANGE, (origin_x, 0), (origin_x, screen_height), 2)

# Simulation (Code 2)
def launch_code2():
    car_image = pygame.image.load("car.png")
    car_image = pygame.transform.scale(car_image, (50, 30))
    car_x, car_y = 750, 814
    car_angle = 45
    car_speed = 5
    inclination_point_x = 620
    landing_point_x = 1526
    simulation_running = True

    while simulation_running:
        screen.fill(BLACK)
        screen.blit(background_image, (0, 0))

        # Mouvement de la voiture
        if car_x < inclination_point_x:
            car_x += car_speed
            car_angle = 0
        elif car_x < landing_point_x:
            car_angle = 45
            car_x += car_speed
        else:
            car_angle = 0
            car_x = landing_point_x
            simulation_running = False

        rotated_car = pygame.transform.rotate(car_image, car_angle)
        screen.blit(rotated_car, (car_x - 25, car_y - 15))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == STATE_CODE1:
                if poursuivre_button_rect.collidepoint(event.pos):
                    current_state = STATE_CODE2

    # Affichage des états
    if current_state == STATE_CODE1:
        screen.fill(BLACK)
        screen.blit(background_image, (0, 0))
        draw_axes_code1()
        pygame.draw.rect(screen, BLUE, poursuivre_button_rect)
        draw_text_centered("Poursuivre", font, WHITE, screen, poursuivre_button_rect.centerx, poursuivre_button_rect.centery)
    elif current_state == STATE_CODE2:
        launch_code2()
        running = False  # Sortir après simulation

    pygame.display.flip()

pygame.quit()
