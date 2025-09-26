import pygame
import random
import sys

# --- Pygame ---
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wisielec")
clock = pygame.time.Clock()

# --- Ścieżki ---
DICT_PATH = "C:\\Users\\ASUS ZENBOOK\\Desktop\\repo_github\\Wisielec\\slownik.txt"
BACKGROUND_PATH = "C:\\Users\\ASUS ZENBOOK\\Desktop\\repo_github\\Wisielec\\background.png"

BACKGROUND = pygame.image.load(BACKGROUND_PATH)

# --- Kolory ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
GRAY = (180, 180, 180)
DARK_GRAY = (100, 100, 100)
LIGHT_GRAY = (220, 220, 220)

# --- Czcionki ---
FONT = pygame.font.SysFont("arial", 40, bold=True)
SMALL_FONT = pygame.font.SysFont("arial", 25, bold=True)


# --- Klasa ogólnego przycisku UI ---
class UIbutton:
    def __init__(self, text, x, y, w, h, color, hover_color, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, DARK_GRAY, self.rect, 2, border_radius=10)
        label = FONT.render(self.text, True, BLACK)
        screen.blit(label, label.get_rect(center=self.rect.center))

    def check_click(self, pos):
        if self.rect.collidepoint(pos) and self.action:
            self.action()


# --- Klasa przycisku litery ---
class LetterButton:
    def __init__(self, litera, rect):
        self.litera = litera
        self.rect = rect
        self.aktywna = True

    def draw(self, screen):
        if self.aktywna:
            pygame.draw.ellipse(screen, WHITE, self.rect)
            pygame.draw.ellipse(screen, BLACK, self.rect, 2)
            render = SMALL_FONT.render(self.litera, True, BLACK)
        else:
            pygame.draw.ellipse(screen, GRAY, self.rect)
            render = SMALL_FONT.render(self.litera, True, WHITE)
        screen.blit(render, render.get_rect(center=self.rect.center))

    def check_click(self, pos):
        return self.aktywna and self.rect.collidepoint(pos)


# --- Funkcje pomocnicze ---
def load_words():
    slownik = []
    with open(DICT_PATH, 'r') as plik:
        for line in plik:
            word = line.strip().upper()
            if word not in slownik:
                slownik.append(word)
    return slownik


def losowanie_slowa(slownik):
    return random.choice(slownik)


def rysuj_wisielca(zycia):
    if zycia <= 5:
        pygame.draw.circle(screen, BLACK, (540, 195), 20, 4)
        if zycia > 0:
            pygame.draw.circle(screen, BLACK, (532, 190), 2)
            pygame.draw.circle(screen, BLACK, (548, 190), 2)
            pygame.draw.arc(screen, BLACK, (528, 198, 24, 15), 0, 3.14, 2)
        else:
            pygame.draw.line(screen, BLACK, (530, 188), (535, 193), 2)
            pygame.draw.line(screen, BLACK, (535, 188), (530, 193), 2)
            pygame.draw.line(screen, BLACK, (545, 188), (550, 193), 2)
            pygame.draw.line(screen, BLACK, (550, 188), (545, 193), 2)
            pygame.draw.arc(screen, BLACK, (528, 198, 24, 15), 0, 3.14, 2)

    if zycia <= 4:
        pygame.draw.line(screen, BLACK, (540, 215), (540, 285), 4)
    if zycia <= 3:
        pygame.draw.line(screen, BLACK, (540, 225), (500, 255), 4)
    if zycia <= 2:
        pygame.draw.line(screen, BLACK, (540, 225), (580, 255), 4)
    if zycia <= 1:
        pygame.draw.line(screen, BLACK, (540, 285), (510, 335), 4)
    if zycia <= 0:
        pygame.draw.line(screen, BLACK, (540, 285), (570, 335), 4)


def sprawdz_wynik(zycia, slowo, zaszyfrowane):
    if zycia <= 0:
        return f"Przegrałeś! Słowo to: {slowo}", RED
    elif "_" not in zaszyfrowane:
        return "Brawo! Wygrałeś!", GREEN
    return None, None


# --- Klasa gry ---
class HangmanGame:
    def __init__(self, slownik):
        self.slownik = slownik
        self.reset()

    def reset(self):
        self.slowo = losowanie_slowa(self.slownik)
        self.zaszyfrowane = ["_"] * len(self.slowo)
        self.zycia = 6
        self.przyciski = self.stworz_alfabet()

    def stworz_alfabet(self):
        litery = list("ABCDEFGHIJKLMNOPQRSTUWYZ")
        przyciski = []
        start_x, start_y, odstep = 100, 400, 50
        wiersz = kolumna = 0
        for litera in litery:
            rect = pygame.Rect(start_x + kolumna * odstep, start_y + wiersz * odstep, 45, 45)
            przyciski.append(LetterButton(litera, rect))
            kolumna += 1
            if kolumna > 11:
                kolumna, wiersz = 0, wiersz + 1
        return przyciski

    def check_letter(self, pos):
        for button in self.przyciski:
            if button.check_click(pos):
                button.aktywna = False
                if button.litera in self.slowo:
                    for i, l in enumerate(self.slowo):
                        if l == button.litera:
                            self.zaszyfrowane[i] = l
                else:
                    self.zycia -= 1

    def draw_word(self):
        tekst = " ".join(self.zaszyfrowane)
        render = FONT.render(tekst, True, BLACK)
        rect = render.get_rect(topleft=(50, 220))
        tlo = pygame.Surface(rect.inflate(20, 10).size, pygame.SRCALPHA)
        tlo.fill((255, 255, 255, 180))
        screen.blit(tlo, rect.inflate(20, 10))
        screen.blit(render, rect)

    def draw_buttons(self):
        for button in self.przyciski:
            button.draw(screen)


# --- Pętla główna ---
def gra():
    slownik = load_words()
    game = HangmanGame(slownik)

    # Przyciski UI
    restart_btn = UIbutton("Restart", 20, 20, 140, 50, LIGHT_GRAY, WHITE, action=game.reset)
    exit_btn = UIbutton("Exit", 640, 20, 140, 50, RED, (255, 100, 100), action=lambda: sys.exit())

    running = True
    while running:
        screen.blit(BACKGROUND, (0, 0))

        # Rysuj szubienicę i elementy
        rysuj_wisielca(game.zycia)
        game.draw_word()
        game.draw_buttons()

        # Rysuj przyciski
        restart_btn.draw(screen)
        exit_btn.draw(screen)

        # Sprawdź warunki końca gry
        msg, color = sprawdz_wynik(game.zycia, game.slowo, game.zaszyfrowane)
        if msg:
            render = FONT.render(msg, True, color)
            rect_msg = render.get_rect(center=(WIDTH // 2, 540))
            pygame.draw.rect(screen, WHITE, rect_msg.inflate(40, 20), border_radius=15)
            pygame.draw.rect(screen, color, rect_msg.inflate(40, 20), 3, border_radius=15)
            screen.blit(render, rect_msg)

        pygame.display.flip()

        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                game.check_letter(pos)
                restart_btn.check_click(pos)
                exit_btn.check_click(pos)

        clock.tick(30)

    pygame.quit()


# --- Start ---
if __name__ == "__main__":
    gra()
