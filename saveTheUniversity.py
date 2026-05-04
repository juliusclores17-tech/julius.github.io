import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

width = 600
height = 800

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Save the University")

font = pygame.font.SysFont("Arial", 30)
bigFont = pygame.font.SysFont("Arial", 60)

clock = pygame.time.Clock()

background = pygame.image.load("images/newBackground.png")
background = pygame.transform.scale(background, (width, height))

objectImg = pygame.transform.scale(pygame.image.load("images/UddLogo.png"), (50, 50))

playerImg = pygame.transform.scale(pygame.image.load("images/Chibi_char.png"), (120, 100))

pygame.mixer.music.load("sounds/bgMusic.mp3")
pygame.mixer.music.set_volume(0.2)

catchSound = pygame.mixer.Sound("sounds/catchSound.mp3")
catchSound.set_volume(0.5)
loseSound = pygame.mixer.Sound("sounds/gameOver.mp3")
loseSound.set_volume(0.5)
winSound = pygame.mixer.Sound("sounds/win.mp3")
winSound.set_volume(0.5)

playerSpeed = 15
winScore = 50

dares = [
    "Sing a song",
    "Do 20 push-ups",
    "Try to lick your elbow",
    "Kiss your classmate"
]

currentDare = random.choice(dares)

def resetGame():
    global currentDare
    currentDare = random.choice(dares)
    return (
        pygame.Rect(250, 700, 120, 60),
        pygame.Rect(random.randint(0, width-50), 0, 50, 50),
        0,
        5
    )

player, logo, score, speed = resetGame()

gameOver = False
won = False
started = False

playedLoseSound = False
playedWinSound = False

while True:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not started and event.type == pygame.KEYDOWN:
            started = True
            player, logo, score, speed = resetGame()
            pygame.mixer.music.play(-1, 0.0, 3000)

        elif (gameOver or won) and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player, logo, score, speed = resetGame()
                gameOver = False
                won = False
                playedLoseSound = False
                playedWinSound = False
                pygame.mixer.music.play(-1, 0.0, 3000)

    if not started:
        startKey = ""

        startImg = pygame.transform.scale(pygame.image.load("images/introPic.png"), (400, 200))
        screen.blit(startImg, (100, 50))

        startButton = pygame.transform.scale(pygame.image.load("images/startButton.png"), (250, 200))
        screen.blit(startButton, (180, 550))

    elif not gameOver and not won:
        spikes = pygame.transform.scale(pygame.image.load("images/spikes.png"), (700, 500))
        screen.blit(spikes, (0, 545))
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player.x -= playerSpeed
        if keys[pygame.K_RIGHT]:
            player.x += playerSpeed

        player.x = max(0, min(width - player.width, player.x))

        logo.y += speed
    
        if logo.colliderect(player):
            catchSound.play()
            score += 1
            logo.topleft = (random.randint(0, width-50), 0)
            speed += 0.3

        if logo.top > height: 
            gameOver = True

        if score == winScore:
            won = True
        
        spikes =  pygame.Rect(0, 780, 700, 500)
        if logo.colliderect(spikes):
            gameOver = True
    
        screen.blit(playerImg, player)
        screen.blit(objectImg, logo)
        screen.blit(font.render(f"Score: {score}/50", True, "black"), (10, 10))

    elif gameOver:
        if not playedLoseSound:
            pygame.mixer.music.stop()
            loseSound.play()
            playedLoseSound = True
       
        box = pygame.transform.scale(pygame.image.load("images/box.png"), (550, 800))
        screen.blit(box, (40, 80))

        screen.blit(bigFont.render("GAME OVER", True, "red"), (160, 200))
        screen.blit(font.render("Your Dare:", True, "black"), (130, 270))
        screen.blit(font.render(currentDare, True, "black"), (150, 320))
        screen.blit(font.render("Press SPACE to Restart", True, "black"), (190, 550))
        
    elif won:
        if not playedWinSound:
            pygame.mixer.music.stop()
            winSound.play()
            playedWinSound = True

        screen.blit(bigFont.render("YOU WIN!", True, "blue"), (180, 250))
        screen.blit(font.render("You caught all 50!", True, "black"), (180, 320))
        screen.blit(font.render("Press SPACE to Play Again", True, "black"), (130, 400))
        screen.blit(box, (100, 100))

    pygame.display.flip()
    clock.tick(60)
