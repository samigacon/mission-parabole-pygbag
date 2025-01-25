import pygame

# Initialisation de Pygame
pygame.init()

# Charger l'image du fond
background = pygame.image.load("./scripts/footages/pont.png")
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

intro_active = True  # Variable pour afficher l'introduction au démarrage


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
car_image = pygame.image.load("./scripts/footages/car.png")
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
font = pygame.font.Font(None, 20)

# Chargement des images des boutons
button_a_image = pygame.image.load("./scripts/footages/A.png")
button_b_image = pygame.image.load("./scripts/footages/B.png")
button_c_image = pygame.image.load("./scripts/footages/C.png")
button_a_image = pygame.transform.scale(button_a_image, (90, 150))
button_b_image = pygame.transform.scale(button_b_image, (90, 150))
button_c_image = pygame.transform.scale(button_c_image, (90, 150))

# Positions des boutons
button_a_rect = button_a_image.get_rect(topleft=(300, 200))
button_b_rect = button_b_image.get_rect(topleft=(300, 380))
button_c_rect = button_c_image.get_rect(topleft=(300, 550))

# Charger l'image de l'écran central
ecran_image = pygame.image.load("./scripts/footages/ecran.png")
ecran_image = pygame.transform.scale(ecran_image, (300, 180))
ecran_rect = ecran_image.get_rect(center=(screen_width // 1.75, 300))

# Charger et redimensionner les images des boutons R et S
reset_button_image = pygame.image.load("./scripts/footages/R.png")
simulation_button_image = pygame.image.load("./scripts/footages/S.png")
reset_button_image = pygame.transform.scale(reset_button_image, (90, 37))
simulation_button_image = pygame.transform.scale(simulation_button_image, (90, 37))

# Position des boutons R et S sous le bouton C
reset_button_rect = reset_button_image.get_rect(topleft=(button_c_rect.left, button_c_rect.bottom + 60))
simulation_button_rect = simulation_button_image.get_rect(topleft=(reset_button_rect.left, reset_button_rect.bottom + 10))

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
    global curve_color
    prev_x, prev_y = None, None

    for x_pixel in range(int(xmin * step_x), int(xmax * step_x)):
        relative_x = x_pixel / step_x
        y = A * relative_x ** 2 + B * relative_x + C
        screen_x = origin_x + relative_x * step_x
        screen_y = origin_y - y * step_y

        if xmin * step_x <= relative_x * step_x <= xmax * step_x and 0 <= y <= ymax:
            if prev_x is not None:
                pygame.draw.line(screen, curve_color, (prev_x, prev_y), (screen_x, screen_y), 2)
            prev_x, prev_y = screen_x, screen_y

# Fonction pour dessiner les boutons
def draw_buttons():
    # Dessin du rectangle noir avec angles arrondis pour les boutons A, B, C
    rect_width = 120
    rect_height = 730
    rect_x = 288
    rect_y = 140
    pygame.draw.rect(screen, BLACK, (rect_x, rect_y, rect_width, rect_height), border_radius=20)

    # Dessiner le texte "Coefficients"
    coefficients_text = font.render("Coefficients", True, WHITE)
    coefficients_text_rect = coefficients_text.get_rect(center=(button_a_rect.centerx, button_a_rect.top - 30))
    screen.blit(coefficients_text, coefficients_text_rect)

    # Dessiner les boutons A, B, C
    screen.blit(button_a_image, button_a_rect)
    screen.blit(button_b_image, button_b_rect)
    screen.blit(button_c_image, button_c_rect)

    # Dessiner les boutons R et S avec texte
    pygame.draw.rect(screen, BLACK, (reset_button_rect.x - 10, reset_button_rect.y - 5, 110, 45), border_radius=10)
    pygame.draw.rect(screen, BLACK, (simulation_button_rect.x - 10, simulation_button_rect.y - 5, 110, 45), border_radius=10)
    screen.blit(reset_button_image, reset_button_rect.topleft)
    screen.blit(simulation_button_image, simulation_button_rect.topleft)

    # Texte des boutons R et S
    reset_label = font.render("Réinitialiser", True, WHITE)
    simulation_label = font.render("Simulation", True, BLACK)
    screen.blit(reset_label, (reset_button_rect.x + 10, reset_button_rect.y + 10))
    screen.blit(simulation_label, (simulation_button_rect.x + 10, simulation_button_rect.y + 10))

# Fonction pour dessiner l'écran central
def draw_screen():
    screen.blit(ecran_image, ecran_rect.topleft)
# Fonction pour dessiner l'écran central
def draw_screen():
    screen.blit(ecran_image, ecran_rect.topleft)

    # Affichage du titre "Fonction polynomiale de degré 2"
    title_text = font.render("Fonction polynomiale de degré 2", True, WHITE)
    title_text_rect = title_text.get_rect(center=(ecran_rect.centerx, ecran_rect.top + 40))
    screen.blit(title_text, title_text_rect)

    # Affichage de la fonction générale
    text_general = font.render("f(x) = ", True, WHITE)
    a_text = font.render("A", True, ORANGE)
    x2_text = font.render("x² + ", True, WHITE)
    b_text = font.render("B", True, GREEN)
    x_text = font.render("x + ", True, WHITE)
    c_text = font.render("C", True, PINK)

    screen.blit(text_general, (ecran_rect.x + 20, ecran_rect.y + 65))
    screen.blit(a_text, (ecran_rect.x + 95, ecran_rect.y + 65))
    screen.blit(x2_text, (ecran_rect.x + 110, ecran_rect.y + 65))
    screen.blit(b_text, (ecran_rect.x + 150, ecran_rect.y + 65))
    screen.blit(x_text, (ecran_rect.x + 165, ecran_rect.y + 65))
    screen.blit(c_text, (ecran_rect.x + 200, ecran_rect.y + 65))

    # Affichage de la fonction avec les valeurs actuelles
    text_values = font.render("f(x) = ", True, WHITE)
    a_value = font.render(f"{A:.3f}", True, ORANGE)
    x2_value = font.render("x² + ", True, WHITE)
    b_value = font.render(f"{B:.1f}", True, GREEN)
    x_value = font.render("x + ", True, WHITE)
    c_value = font.render(f"{C:.2f}", True, PINK)

    # Positionnement des éléments
    screen.blit(text_values, (ecran_rect.x + 20, ecran_rect.y + 95))
    screen.blit(a_value, (ecran_rect.x + 90, ecran_rect.y + 95))
    screen.blit(x2_value, (ecran_rect.x + 140, ecran_rect.y + 95))
    screen.blit(b_value, (ecran_rect.x + 170, ecran_rect.y + 95))
    screen.blit(x_value, (ecran_rect.x + 195, ecran_rect.y + 95))
    screen.blit(c_value, (ecran_rect.x + 230, ecran_rect.y + 95))


def draw_message(message, success=True):
    # Définir les dimensions et la position de l'encadré
    message_width = 500
    message_height = 150
    message_x = (screen_width - message_width) // 2
    message_y = (screen_height - message_height) // 2
    message_rect = pygame.Rect(message_x, message_y, message_width, message_height)

    # Couleur pour le texte
    text_color = WHITE  # Le texte d'erreur est aussi en blanc
    background_color = BLACK  # L'encadré reste noir

    # Dessiner l'encadré
    pygame.draw.rect(screen, background_color, message_rect)
    pygame.draw.rect(screen, WHITE, message_rect, 3)  # Bordure blanche

    # Affichage du texte
    message_text = font.render(message, True, text_color)
    screen.blit(
        message_text,
        (message_x + (message_width - message_text.get_width()) // 2,
         message_y + (message_height - message_text.get_height()) // 2),
    )


# Gestion des clics
def handle_button_click(mouse_pos):
    global A, B, C, buttons_active
    if not buttons_active or show_error_message:  # Désactiver les boutons si erreur
        return

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




def handle_simulation_buttons(mouse_pos):
    global A, B, C, car_x, car_y, car_angle, simulation_active, show_success_message, show_error_message, buttons_active, curve_color

    if reset_button_rect.collidepoint(mouse_pos):
        # Réinitialiser les paramètres
        A, B, C = 0, 1, 0  # Valeurs par défaut
        car_x, car_y = initial_car_x, initial_car_y
        car_angle = 45
        simulation_active = False
        curve_color = RED  # Réinitialiser la couleur de la courbe à rouge
        show_success_message = False  # Supprimer les messages de succès
        show_error_message = False  # Supprimer les messages d'erreur
        buttons_active = True  # Réactiver les boutons
        print("Simulation réinitialisée.")  # Debug

    elif simulation_button_rect.collidepoint(mouse_pos) and not show_error_message:
        # Lancer la simulation uniquement si pas d'erreur
        simulation_active = True
        car_x, car_y = simulation_start_x, simulation_start_y
        print("Simulation lancée.")  # Debug

def draw_intro():
    intro_text = (
        "Retrouvez la trajectoire de la voiture afin de réaliser la cascade correctement et sans danger.\n\n"
        "Faites varier les paramètres A, B, et C de la fonction polynomiale de degré 2.\n\n"
        "N'oubliez pas que la trajectoire doit passer par les points que vous avez placés précédemment.\n\n"
        "Pour savoir lesquels, consultez votre feuille de route."
    )
    screen.fill(BLACK)  # Fond noir
    font_intro = pygame.font.Font(None, 40)  # Taille de la police pour l'intro
    lines = intro_text.split("\n")
    y_offset = screen_height // 2 - len(lines) * 20  # Centrer verticalement
    for line in lines:
        text_surface = font_intro.render(line, True, WHITE)
        text_rect = text_surface.get_rect(center=(screen_width // 2, y_offset))
        screen.blit(text_surface, text_rect)
        y_offset += 40  # Espacement entre les lignes


# Boucle principale
running = True
simulation_active = False
show_success_message = False
show_error_message = False
curve_color = RED  # La courbe est rouge par défaut
buttons_active = True  # Les boutons A, B, C sont actifs par défaut

while running:
    screen.fill(BLACK)

    if intro_active:
        draw_intro()  # Affiche l'introduction si active
    else:
        screen.blit(background, (0, 0))
        draw_axes()
        draw_curve()  # Dessine la courbe avec la couleur actuelle
        draw_buttons()
        draw_screen()

        if simulation_active:
            if car_x < inclination_point_x:
                # Mouvement horizontal jusqu'au point d'inclinaison
                car_x += car_speed
                car_y = simulation_start_y
                car_angle = 0
            elif car_x >= inclination_point_x and car_x < landing_point_x:
                # Inclinaison progressive suivant la parabole
                car_angle = 45
                relative_x = (car_x - origin_x) / step_x
                car_y = origin_y - (A * relative_x ** 2 + B * relative_x + C) * step_y - vertical_offset
                car_x += car_speed
            else:
                # Transition progressive à l'atterrissage
                if car_angle > 0:
                    car_angle -= 1
                car_x += car_speed
                relative_x = (car_x - origin_x) / step_x
                car_y = origin_y - (A * relative_x ** 2 + B * relative_x + C) * step_y - vertical_offset
                
                if car_x >= landing_point_x:
                    car_angle = 0
                    car_x, car_y = landing_point_x, landing_point_y
                    simulation_active = False

                    # Vérification des paramètres après la simulation
                    if round(A, 3) == -0.098 and round(B, 1) == 1.3 and round(C, 2) == 3.5:
                        curve_color = GREEN  # La courbe devient verte
                        show_success_message = True
                        show_error_message = False
                        buttons_active = False  # Désactiver les boutons
                    else:
                        curve_color = RED  # Réinitialiser à rouge en cas d'erreur
                        show_error_message = True
                        show_success_message = False

        rotated_car = pygame.transform.rotate(car_image, car_angle)
        screen.blit(rotated_car, (car_x - 25, car_y - 15))

        if show_success_message:
            draw_message("Simulation Réussie, les paramètres sont corrects", success=True)

        if show_error_message:
            draw_message("Erreur dans la simulation, recommencez", success=False)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if intro_active:
                intro_active = False  # Désactiver l'introduction au clic
            else:
                handle_button_click(event.pos)
                handle_simulation_buttons(event.pos)

pygame.quit()


