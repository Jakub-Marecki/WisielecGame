import pygame
import random
import sys

# --- Pygame ---
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wisielec")
clock = pygame.time.Clock()
BACKGROUND = pygame.image.load("C:\\Users\\ASUS ZENBOOK\\Desktop\\repo_github\\Wisielec\\background.png")
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
    # Głowa
    if zycia <= 5:
        pygame.draw.circle(screen, BLACK, (540, 195), 20, 4)

        # Twarz
        if zycia > 0:
            pygame.draw.circle(screen, BLACK, (532, 190), 2)  # lewe oko
            pygame.draw.circle(screen, BLACK, (548, 190), 2)  # prawe oko
            pygame.draw.arc(screen, BLACK, (528, 198, 24, 15), 0, 3.14, 2)  # smutna buźka
        else:
            # Oczy X
            pygame.draw.line(screen, BLACK, (530, 188), (535, 193), 2)
            pygame.draw.line(screen, BLACK, (535, 188), (530, 193), 2)
            pygame.draw.line(screen, BLACK, (545, 188), (550, 193), 2)
            pygame.draw.line(screen, BLACK, (550, 188), (545, 193), 2)
            pygame.draw.arc(screen, BLACK, (528, 198, 24, 15), 0, 3.14, 2)  # smutne usta

    # Tułów
    if zycia <= 4:
        pygame.draw.line(screen, BLACK, (540, 215), (540, 285), 4)

    # Ręce
    if zycia <= 3:
        pygame.draw.line(screen, BLACK, (540, 225), (500, 255), 4)  # lewa ręka
    if zycia <= 2:
        pygame.draw.line(screen, BLACK, (540, 225), (580, 255), 4)  # prawa ręka

    # Nogi
    if zycia <= 1:
        pygame.draw.line(screen, BLACK, (540, 285), (510, 335), 4)  # lewa noga
    if zycia <= 0:
        pygame.draw.line(screen, BLACK, (540, 285), (570, 335), 4)  # prawa noga


# --- Przyciski liter ---
def stworz_alfabet():
    litery = list("ABCDEFGHIJKLMNOPQRSTUWYZ")
    przyciski = []
    start_x = 130
    start_y = 400
    odstep = 45
    wiersz = 0
    kolumna = 0

    for litera in litery:
        rect = pygame.Rect(start_x + kolumna * odstep, start_y + wiersz * odstep, 40, 40)
        przyciski.append([litera, rect, True])
        kolumna += 1
        if kolumna > 11:
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
            
# --- Przyciski Obłusga gry ----
def draw_button(text, x, y, w, h, color):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, color, rect)
    label = FONT.render(text, True, BLACK)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)
    return rect

# --- Główna pętla gry ---
def gra():
    slowo = losowanie_slowa()
    zaszyfrowane = szyfrowanie(slowo)
    zycia = 6
    przyciski = stworz_alfabet()

    running = True
    while running:
        screen.fill(WHITE)
        screen.blit(BACKGROUND, (0,0))
        play_again_btn = draw_button("Restart", 20, 20, 140, 50, GRAY)
        quit_btn = draw_button("Exit", 640, 20, 140, 50, RED)

        # Rysowanie szubienicy
        rysuj_wisielca(zycia)

        # Rysowanie zaszyfrowanego słowa
        tekst = " ".join(zaszyfrowane)
        render_slowo = FONT.render(tekst, True, BLACK)
        screen.blit(render_slowo, (100, 200))

        # Rysowanie liter
        for litera, rect, aktywna in przyciski:
            if aktywna:
                pygame.draw.rect(screen, WHITE, rect)
                pygame.draw.rect(screen, BLACK, rect, 2)
                litera_render = SMALL_FONT.render(litera, True, BLACK)
            else:
                pygame.draw.rect(screen, GRAY, rect)
                litera_render = SMALL_FONT.render(litera, True, WHITE)
            screen.blit(litera_render, (rect.x + 10, rect.y + 5))

        # Sprawdzenie warunków gry
        if zycia <= 0:
            msg = FONT.render(f"Przegrałeś! Słowo to: {slowo}", True, RED)
            screen.blit(msg, (400 - msg.get_width() // 2, 520))
        elif "_" not in zaszyfrowane:
            msg = FONT.render("Brawo! Wygrałeś!", True, GREEN)
            screen.blit(msg, (400 - msg.get_width() // 2, 520))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                if play_again_btn.collidepoint(position):
                    return gra()  # restart gry
                if quit_btn.collidepoint(position):
                    pygame.quit()
                    sys.exit()
                for btn in przyciski:
                    litera, rect, aktywna = btn
                    if aktywna and rect.collidepoint(position):
                        btn[2] = False
                        if litera in slowo:
                            odszyfrowanie_litery(slowo, zaszyfrowane, litera)
                        else:
                            zycia -= 1

        clock.tick(30)

# --- Start ---
if __name__ == "__main__":
    gra()
