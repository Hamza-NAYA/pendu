import pygame
import random
import easygui
# Utilisation de la bibliothèque easygui pour utiliser des messagesbox
# pour installer cette bibliothèque : pip install easygui

# Initialisation de Pygame
pygame.init()

# Définition de quelques constantes
WIDTH, HEIGHT = 1000, 800
FPS = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT_SIZE = 22
LETTER_GAP = 20

# Initialisation de la fenêtre Pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu du Pendu")
clock = pygame.time.Clock()
font = pygame.font.Font("Merriweather-Black.ttf", FONT_SIZE)

# Chargement des mots depuis le fichier "mots.txt"
with open("mots.txt", "r") as file:
    mots = file.read().splitlines()

# Chargement des scores depuis le fichier "scores.txt"
scores = {}
try:
    with open("scores.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            name, score = line.strip().split(":")
            scores[name] = int(score)
except FileNotFoundError:
    pass

# Fonction pour choisir un mot aléatoire en fonction de la difficulté
def choisir_mot(difficulte):
    mots_difficulte = [mot for mot in mots if difficulte[0] <= len(mot) <= difficulte[1]]
    return random.choice(mots_difficulte).upper()

# Fonction pour afficher le mot caché avec des underscores pour les lettres non trouvées
def afficher_mot_cache(mot, lettres_trouvees):
    mot_cache = ""
    for lettre in mot:
        if lettre in lettres_trouvees:
            mot_cache += lettre + " "
        else:
            mot_cache += "_ "
    return mot_cache.strip()

# Fonction pour afficher le pendu
def afficher_pendu(erreurs):
    pendu_images = ["images/pendu01.png", "images/pendu02.png", "images/pendu03.png",
                    "images/pendu04.png", "images/pendu05.png", "images/pendu06.png",
                    "images/pendu07.png"]
    if erreurs < len(pendu_images):
        pendu_img = pygame.image.load(pendu_images[erreurs])
        screen.blit(pendu_img, (WIDTH // 2 - pendu_img.get_width() // 2, 20))

# Nouvelle fonction pour afficher un message dans l'interface graphique
def afficher_message(message, delay=0):
    screen.fill(WHITE)
    message_text = font.render(message, True, BLACK)
    screen.blit(message_text, (WIDTH // 2 - message_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    if delay > 0:
        pygame.time.wait(delay)

# Fonction principale du jeu
def jouer(difficulte):
    mot = choisir_mot(difficulte)
    lettres_trouvees = set()
    lettres_incorrectes = set()
    erreurs = 0

    while True:
        screen.fill(WHITE)

        mot_cache = afficher_mot_cache(mot, lettres_trouvees)
        mot_text = font.render(mot_cache, True, BLACK)
        screen.blit(mot_text, (WIDTH // 2 - mot_text.get_width() // 2, HEIGHT - 100))

        if erreurs < 7:
            afficher_pendu(erreurs)
        else:
            afficher_message(f"Dommage ! Le mot était {mot}.", 2000)
            break

        lettres_incorrectes_text = font.render(f"Lettres incorrectes: {' '.join(lettres_incorrectes)}", True, BLACK)
        screen.blit(lettres_incorrectes_text, (WIDTH // 2 - lettres_incorrectes_text.get_width() // 2, HEIGHT - 50))

        pygame.display.flip()

        if "_" not in mot_cache:
            afficher_message(f"Félicitations ! Vous avez trouvé le mot : {mot}", 2000)
            nom_joueur = obtenir_nom_joueur()
            scores[nom_joueur] = scores.get(nom_joueur, 0) + 1
            with open("scores.txt", "a") as file:
                file.write(f"{nom_joueur}:{scores[nom_joueur]}\n")
            break

        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

            if event.key in range(pygame.K_a, pygame.K_z + 1):
                lettre = chr(event.key).upper()
                if lettre not in lettres_incorrectes and lettre not in lettres_trouvees:
                    if lettre not in mot:
                        erreurs += 1
                        lettres_incorrectes.add(lettre)
                    else:
                        lettres_trouvees.add(lettre)

# Fonction pour obtenir le nom du joueur avec une boîte de dialogue
def obtenir_nom_joueur():
    nom_joueur = easygui.enterbox("Entrez votre nom :")
    return nom_joueur

# Fonction pour afficher le tableau des scores
def afficher_scores():
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    y = 100
    for i, (name, score) in enumerate(sorted_scores):
        score_text = font.render(f"{i+1}. {name}: {score}", True, BLACK)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, y))
        y += FONT_SIZE

# Fonction pour choisir la difficulté
def choisir_difficulte():
    while True:
        screen.fill(WHITE)

        diff_text = font.render("Choisissez la difficulté : Facile(1) | Moyen(2) | Difficile(3)", True, BLACK)
        screen.blit(diff_text, (WIDTH // 2 - diff_text.get_width() // 2, HEIGHT // 2 - FONT_SIZE))

        pygame.display.flip()

        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                return (4, 5)  # Taille des mots pour la difficulté Facile
            elif event.key == pygame.K_2:
                return (6, 8)  # Taille des mots pour la difficulté Moyen
            elif event.key == pygame.K_3:
                return (9, 15)  # Taille des mots pour la difficulté Difficile

# Fonction pour effacer le tableau des scores
def effacer_scores():
    global scores
    scores = {}  # Réinitialisation du dictionnaire des scores
    with open("scores.txt", "w") as file:
        file.write("")
    afficher_scores()  # Ajout de cet appel pour rafraîchir l'affichage

# Fonction principale pour le menu
def menu():
    while True:
        screen.fill(WHITE)

        menu_text = font.render("Jouer(1) | Tableau des scores(2)  | Effacer le tableau des scores(3) | Quitter(4)", True, BLACK)
        screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 - FONT_SIZE))

        pygame.display.flip()

        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                difficulte = choisir_difficulte()
                jouer(difficulte)
            elif event.key == pygame.K_2:
                afficher_scores()
                pygame.display.flip()
                pygame.time.wait(3000)  # Attendre 5 secondes pour afficher les scores
            elif event.key == pygame.K_3:
                effacer_scores()
            elif event.key == pygame.K_4:
                pygame.quit()
                exit()

# Boucle principale du programme
menu()
pygame.quit()
