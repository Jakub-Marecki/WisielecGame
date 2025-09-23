import pygame
import random
import sys

# --- Inicjalizacja ---
pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wisielec")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)

FONT = pygame.font.SysFont("arial", 40)

# --- Lista słów ---
slownik = []


with open("C:\\Users\\ASUS ZENBOOK\\Desktop\\repo_github\\Wisielec\\slownik.txt", 'r') as plik:
    for line in plik:
        clear = line.strip()
        if clear not in slownik:
            slownik.append(clear)

# --- Funkcje ---
def rysuj_wisielca(lives):
    # prosty rysunek wisielca
    # bazowy stojak
    # Szubienica
    pygame.draw.line(WIN, BLACK, (150, 350), (350, 350), 5)  # podstawa
    pygame.draw.line(WIN, BLACK, (250, 350), (250, 50), 5)  # pion
    pygame.draw.line(WIN, BLACK, (250, 50), (400, 50), 5)  # poziom
    pygame.draw.line(WIN, BLACK, (400, 50), (400, 100), 5)  # sznur

    # Głowa
    if lives <= 5:
        pygame.draw.circle(WIN, BLACK, (400, 130), 30, 3)  # głowa
        
        #Twarz
        if lives > 0:
            # normalne oczy
            pygame.draw.circle(WIN, BLACK, (390, 125), 3)  # lewe oko
            pygame.draw.circle(WIN, BLACK, (410, 125), 3)  # prawe oko
            pygame.draw.arc(WIN, BLACK, (385, 130, 30, 20), 3.14, 0, 2) # usta (łuk do dołu)
        else:
            # oczy X jeśli zmarł
            pygame.draw.line(WIN, BLACK, (387, 122), (393, 128), 2)  # lewe X
            pygame.draw.line(WIN, BLACK, (393, 122), (387, 128), 2)
            pygame.draw.line(WIN, BLACK, (407, 122), (413, 128), 2)  # prawe X
            pygame.draw.line(WIN, BLACK, (413, 122), (407, 128), 2)
            pygame.draw.arc(WIN, BLACK, (385, 135, 30, 20),0 , 3.14, 2)

    # Tułów
    if lives <= 4:
        pygame.draw.line(WIN, BLACK, (400, 160), (400, 250), 3)

    # Ręce
    if lives <= 3:
        pygame.draw.line(WIN, BLACK, (400, 180), (360, 220), 3)
    if lives <= 2:
        pygame.draw.line(WIN, BLACK, (400, 180), (440, 220), 3)

    # Nogi
    if lives <= 1:
        pygame.draw.line(WIN, BLACK, (400, 250), (360, 300), 3)
    if lives <= 0:
        pygame.draw.line(WIN, BLACK, (400, 250), (440, 300), 3)


def pokaz_slowo(slowo, trafione):
    wyswietl = ""
    for litera in slowo:
        if litera in trafione:
            wyswietl += litera + " "
        else:
            wyswietl += "_ "
    tekst = FONT.render(wyswietl, True, BLACK)
    WIN.blit(tekst, (100, 500))

def game():
    slowo = random.choice(slownik)
    trafione = []
    lives = 6
    running = True

    while running:
        WIN.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                litera = event.unicode.lower()
                if litera.isalpha() and litera not in trafione:
                    if litera in slowo:
                        trafione.append(litera)
                    else:
                        lives -= 1

        # Rysowanie
        rysuj_wisielca(lives)
        pokaz_slowo(slowo, trafione)

        # Sprawdzenie końca gry
        if lives <= 0:
            tekst = FONT.render(f"Przegrana! Słowo to: {slowo}", True, RED)
            WIN.blit(tekst, (100, 100))
        elif all(l in trafione for l in slowo):
            tekst = FONT.render("Brawo! Wygrałeś!", True, GREEN)
            WIN.blit(tekst, (100, 100))

        pygame.display.update()

# --- Start gry ---
if __name__ == "__main__":
    game()
