import random
import pygame
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((1200,800))
pygame.display.set_caption("PINKY BIRD")

imgStovp = pygame.image.load("stovp.png")
imgStovp = pygame.transform.scale(imgStovp, (150, 400))
imgStovpDown = pygame.transform.flip(imgStovp, False, True)

imgBird = pygame.image.load("bird.png")
imgBird = pygame.transform.scale(imgBird, (100,80))

imgBird2 = pygame.image.load("bird2.png")
imgBird2 = pygame.transform.scale(imgBird2, (100,80))

imgBg = pygame.image.load("fon.jpg")
imgBg = pygame.transform.scale(imgBg, (1200, 800))

font = pygame.font.SysFont("Arial", 48, bold=True)
fontSmall = pygame.font.SysFont("Arial", 32)

birdR = imgBird.get_rect()
birdR.center = (300,400)

speed = 0
grav = 0.45
jump = 10

stovp = pygame.sprite.Group()
pinkStovp = pygame.USEREVENT
pygame.time.set_timer(pinkStovp, 1000)

score = 0
game_started = False
game_over = False
btnRect = pygame.Rect(1200//2 - 120, 420, 240, 60)
btnRestart = pygame.Rect(1200//2 - 120, 470, 240, 60)

pygame.mixer.music.load("menu.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
jumpSound = pygame.mixer.Sound("jump.mp3")
jumpSound.set_volume(0.5)

class PinkyBird(pygame.sprite.Sprite):
    def __init__(self, pos, img, is_top=False):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.scored = False
        self.is_top = is_top
    def update(self):
        self.rect.x -= 10
        if self.rect.right < 0:
            self.kill()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_started and not game_over:
                    game_started = True
                    pygame.mixer.music.load("m.mp3")
                    pygame.mixer.music.play(-1)
                elif game_started and not game_over:
                    speed = -jump
                    jumpSound.play()
                elif game_over:
                    score = 0
                    speed = 0
                    birdR.center = (300, 400)
                    stovp.empty()
                    game_over = False
                    game_started = False
                    pygame.mixer.music.load("menu.mp3")
                    pygame.mixer.music.play(-1)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_started and not game_over:
                if btnRect.collidepoint(event.pos):
                    game_started = True
                    pygame.mixer.music.load("m.mp3")
                    pygame.mixer.music.play(-1)
            elif game_started and not game_over:
                    speed = -jump
                    jumpSound.play()
            if game_over:
                if btnRestart.collidepoint(event.pos):
                    score = 0
                    speed = 0
                    birdR.center = (300, 400)
                    stovp.empty()
                    game_over = False
                    game_started = False
                    pygame.mixer.music.load("menu.mp3")
                    pygame.mixer.music.play(-1)

        if event.type == pinkStovp and game_started and not game_over:
            pinkyBird = PinkyBird((1050, random.choice([-90 ,-10, 0])), imgStovp, is_top=True)
            stovp.add(pinkyBird)
            pinkyBird = PinkyBird((1050, random.choice([610,597,630])), imgStovpDown )
            stovp.add(pinkyBird)

    if game_started and not game_over:
        speed += grav
        birdR.centery += int(speed)

        for s in stovp:
            if birdR.colliderect(s.rect):
                 game_over = True
                 pygame.mixer.music.load("gameover.mp3")
                 pygame.mixer.music.play()
        if birdR.top > 800:
            game_over = True
            pygame.mixer.music.load("gameover.mp3")
            pygame.mixer.music.play()
    if game_started and not game_over:
        for s in stovp:
            if not s.scored and s.rect.right < birdR.left and s.is_top:
                s.scored = True
                score += 1

    window.blit(imgBg, (0, 0))
    if speed < 0:
        window.blit(imgBird2, birdR)
    else:
        window.blit(imgBird, birdR)
    if not game_over:
        stovp.update()
    stovp.draw(window)

    if not game_started and not game_over:
        startText = font.render("PINKY BIRD", True, (255, 100, 180))
        window.blit(startText, (1200//2 - startText.get_width()//2, 300))
        pygame.draw.rect(window, (255, 100, 180), btnRect, border_radius=12)
        pygame.draw.rect(window, (255, 255, 255), btnRect, 3, border_radius=12)
        btnText = fontSmall.render("СТАРТ", True, (255, 255, 255))
        window.blit(btnText, (btnRect.centerx - btnText.get_width()//2, btnRect.centery - btnText.get_height()//2))

    if game_over:
        overlay = pygame.Surface((1200, 800), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        window.blit(overlay, (0, 0))
        overText = font.render("ГРА ЗАКІНЧЕНА", True, (255, 100, 180))
        scoreText = font.render(f"Очки: {score}", True, (255, 255, 255))
        window.blit(overText, (1200//2 - overText.get_width()//2, 300))
        window.blit(scoreText, (1200//2 - scoreText.get_width()//2, 380))
        pygame.draw.rect(window, (255, 100, 180), btnRestart, border_radius=12)
        pygame.draw.rect(window, (255, 255, 255), btnRestart, 3, border_radius=12)
        restartText = fontSmall.render("ЗНОВУ", True, (255, 255, 255))
        window.blit(restartText, (btnRestart.centerx - restartText.get_width()//2, btnRestart.centery - restartText.get_height()//2))

    if game_started and not game_over:
        scoreText = font.render(f"Очки: {score}", True, (255, 100, 180))
        window.blit(scoreText, (1200 // 2 - scoreText.get_width() // 2, 20))

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
