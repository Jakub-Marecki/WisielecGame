import pygame
import random
import sys

# --- Pygame ---
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wisielec")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
GRAY = (180, 180, 180)
FONT = pygame.font.SysFont("arial", 40)
SMALL_FONT = pygame.font.SysFont("arial", 25)

# --- Lista słów ---
slownik = []
with open("C:\\Users\\ASUS ZENBOOK\\Desktop\\repo_github\\Wisielec\\slownik.txt", 'r') as plik:
    for line in plik:
        clear = line.strip()
        if clear not in slownik:
            upper_clear = clear.upper()
            slownik.append(upper_clear)

def losowanie_slowa():
    return random.choice(slownik)

# --- Rysowanie szubienicy ---
def rysuj_wisielca(zycia):
    pygame.draw.line(screen, BLACK, (150, 350), (350, 350), 5)  # podstawa
    pygame.draw.line(screen, BLACK, (250, 350), (250, 50), 5)   # pion
    pygame.draw.line(screen, BLACK, (250, 50), (400, 50), 5)    # poziom
    pygame.draw.line(screen, BLACK, (400, 50), (400, 100), 5)   # sznur

    # Głowa
    if zycia <= 5:
        pygame.draw.circle(screen, BLACK, (400, 130), 30, 3)
        # Twarz
        if zycia > 0:
            pygame.draw.circle(screen, BLACK, (390, 125), 3)
            pygame.draw.circle(screen, BLACK, (410, 125), 3)
            pygame.draw.arc(screen, BLACK, (385, 135, 30, 20), 0, 3.14, 2)  # smutna buźka
        else:
            # Oczy X
            pygame.draw.line(screen, BLACK, (387, 122), (393, 128), 2)
            pygame.draw.line(screen, BLACK, (393, 122), (387, 128), 2)
            pygame.draw.line(screen, BLACK, (407, 122), (413, 128), 2)
            pygame.draw.line(screen, BLACK, (413, 122), (407, 128), 2)
            pygame.draw.arc(screen, BLACK, (385, 135, 30, 20), 0, 3.14, 2)  # smutne usta

    # Tułów
    if zycia <= 4:
        pygame.draw.line(screen, BLACK, (400, 160), (400, 250), 3)
    # Ręce
    if zycia <= 3:
        pygame.draw.line(screen, BLACK, (400, 180), (360, 220), 3)
    if zycia <= 2:
        pygame.draw.line(screen, BLACK, (400, 180), (440, 220), 3)
    # Nogi
    if zycia <= 1:
        pygame.draw.line(screen, BLACK, (400, 250), (360, 300), 3)
    if zycia <= 0:
        pygame.draw.line(screen, BLACK, (400, 250), (440, 300), 3)

# --- Przyciski liter ---
def stworz_alfabet():
    litery = list("ABCDEFGHIJKLMNOPRSTUWYZ")
    przyciski = []
    start_x = 50
    start_y = 400
    odstep = 45
    wiersz = 0
    kolumna = 0

    for litera in litery:
        rect = pygame.Rect(start_x + kolumna * odstep, start_y + wiersz * odstep, 40, 40)
        przyciski.append([litera, rect, True])
        kolumna += 1
        if kolumna > 12:
            kolumna = 0
            wiersz += 1
    return przyciski

# --- Szyfrowanie słowa ---
def szyfrowanie(losowe_slowo):
    return ['_'] * len(losowe_slowo)

# --- Odszyfrowanie litery ---
def odszyfrowanie_litery(losowe_slowo, zaszyfrowane, litera):
    for i in range(len(losowe_slowo)):
        if losowe_slowo[i] == litera:
            zaszyfrowane[i] = litera

# --- Główna pętla gry ---
def gra():
    slowo = losowanie_slowa()
    zaszyfrowane = szyfrowanie(slowo)
    zycia = 6
    przyciski = stworz_alfabet()

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                for btn in przyciski:
                    litera, rect, aktywna = btn
                    if aktywna and rect.collidepoint(position):
                        btn[2] = False
                        if litera in slowo:
                            odszyfrowanie_litery(slowo, zaszyfrowane, litera)
                        else:
                            zycia -= 1
    

        # Rysowanie szubienicy
        rysuj_wisielca(zycia)

        # Rysowanie zaszyfrowanego słowa
        tekst = " ".join(zaszyfrowane)
        render_slowo = FONT.render(tekst, True, BLACK)
        screen.blit(render_slowo, (150, 500))

        # Rysowanie dostępnych liter
        for litera, rect, aktywna in przyciski:
            if aktywna:
                pygame.draw.rect(screen, BLACK, rect, 2)
                litera_render = SMALL_FONT.render(litera, True, BLACK)
            else:
                pygame.draw.rect(screen,GRAY,rect)
                litera_render = SMALL_FONT.render(litera, True, WHITE)
            screen.blit(litera_render, (rect.x + 10, rect.y + 5))

        # Sprawdzenie warunków gry
        if zycia <= 0:
            msg = FONT.render(f"Przegrałeś! Słowo to: {slowo}", True, RED)
            screen.blit(msg, (150, 100))
            pygame.display.update()
            pygame.time.wait(3000)
            running = False
        elif "_" not in zaszyfrowane:
            msg = FONT.render("Brawo! Wygrałeś!", True, GREEN)
            screen.blit(msg, (150, 100))
            pygame.display.update()
            pygame.time.wait(3000)
            running = False

        pygame.display.update()
        pygame.time.Clock().tick(30)

# --- Start ---
if __name__ == "__main__":
    gra()
