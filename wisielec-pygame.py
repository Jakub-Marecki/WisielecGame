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

# --- Kolory ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
GRAY = (180, 180, 180)
DARK_GRAY = (100, 100, 100)
LIGHT_GRAY = (220, 220, 220)
SHADOW = (50, 50, 50, 100)

# --- Czcionki ---
FONT = pygame.font.SysFont("arial", 40, bold=True)
SMALL_FONT = pygame.font.SysFont("arial", 25, bold=True)

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
    start_x = 100
    start_y = 400
    odstep = 50
    wiersz = 0
    kolumna = 0

    for litera in litery:
        rect = pygame.Rect(start_x + kolumna * odstep, start_y + wiersz * odstep, 45, 45)
        przyciski.append([litera, rect, True])
        kolumna += 1
        if kolumna > 11:
            kolumna = 0
            wiersz += 1
    return przyciski

# --- Funkcja rysowania przycisku ---
def draw_button(text, x, y, w, h, color, hover_color=None):
    rect = pygame.Rect(x, y, w, h)
    mouse_pos = pygame.mouse.get_pos()
    current_color = hover_color if rect.collidepoint(mouse_pos) and hover_color else color
    pygame.draw.rect(screen, current_color, rect, border_radius=10)
    pygame.draw.rect(screen, DARK_GRAY, rect, 2, border_radius=10)
    label = FONT.render(text, True, BLACK)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)
    return rect

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
        screen.blit(BACKGROUND, (0, 0))

        play_again_btn = draw_button("Restart", 20, 20, 140, 50, LIGHT_GRAY, WHITE)
        quit_btn = draw_button("Exit", 640, 20, 140, 50, RED, (255, 100, 100))

        # Rysowanie szubienicy
        rysuj_wisielca(zycia)

        # Rysowanie zgadywanego słowa
        tekst = " ".join(zaszyfrowane)
        render_slowo = FONT.render(tekst, True, BLACK)
        rect_slowo = render_slowo.get_rect(topleft=(50, 220))
        tlo = pygame.Surface(rect_slowo.inflate(20, 10).size, pygame.SRCALPHA)
        tlo.fill((255, 255, 255, 180)) 
        screen.blit(tlo, rect_slowo.inflate(20, 10))
        screen.blit(render_slowo, rect_slowo)

        # Rysowanie liter
        for litera, rect, aktywna in przyciski:
            if aktywna:
                pygame.draw.ellipse(screen, WHITE, rect)
                pygame.draw.ellipse(screen, BLACK, rect, 2)
                litera_render = SMALL_FONT.render(litera, True, BLACK)
            else:
                pygame.draw.ellipse(screen, GRAY, rect)
                litera_render = SMALL_FONT.render(litera, True, WHITE)
            screen.blit(litera_render, litera_render.get_rect(center=rect.center))

        # Sprawdzenie warunków gry
        if zycia <= 0:
            msg = FONT.render(f"Przegrałeś! Słowo to: {slowo}", True, RED)
            rect_msg = msg.get_rect(center=(WIDTH // 2, 540))
            pygame.draw.rect(screen, WHITE, rect_msg.inflate(40, 20), border_radius=15)
            pygame.draw.rect(screen, RED, rect_msg.inflate(40, 20), 3, border_radius=15)
            screen.blit(msg, rect_msg)

        elif "_" not in zaszyfrowane:
            msg = FONT.render("Brawo! Wygrałeś!", True, GREEN)
            rect_msg = msg.get_rect(center=(WIDTH // 2, 540)) 
            pygame.draw.rect(screen, WHITE, rect_msg.inflate(40, 20), border_radius=15)
            pygame.draw.rect(screen, GREEN, rect_msg.inflate(40, 20), 3, border_radius=15)
            screen.blit(msg, rect_msg)


        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                if play_again_btn.collidepoint(position):
                    return gra()
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
