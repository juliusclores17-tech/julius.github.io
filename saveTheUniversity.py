import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

width = 600
height = 800

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Save the University")

smallPixelFont = pygame.font.Font("font/pixelatedElegance.ttf", 20)
bigPixelFont = pygame.font.Font("font/pixelatedElegance.ttf", 50)

clock = pygame.time.Clock()

background = pygame.image.load("pictures/newBackground.png")
background = pygame.transform.scale(background, (width, height))

objectImg = pygame.transform.scale(pygame.image.load("pictures/UddLogo.png"), (50, 50))

playerImg = pygame.transform.scale(pygame.image.load("pictures/Chibi char.png"), (120, 100))

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
    "Kiss your classmate",
    "Borrow money from stranger",
    "Confess to your crush"
]

currentDare = random.choice(dares)

def resetGame():
    global currentDare
    currentDare = random.choice(dares)
    return (
        pygame.Rect(250, 700, 120, 60),
        pygame.Rect(random.randint(0, width-50), 0, 50, 50),0, 5
    )

player, logo, score, speed = resetGame()

gameOver = False
won = False
started = False

playedLoseSound = False
playedWinSound = False
#angelo, johnbern, porbile
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

        startImg = pygame.transform.scale(pygame.image.load("pictures/introPic.png"), (400, 200))
        screen.blit(startImg, (100, 50))

        startButton = pygame.transform.scale(pygame.image.load("pictures/startButton.png"), (250, 200))
        screen.blit(startButton, (180, 550))

    elif not gameOver and not won:
        spikes = pygame.transform.scale(pygame.image.load("pictures/spikes.png"), (700, 500))
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
#Clores, Danan
        if logo.top > height: 
            gameOver = True

        if score == winScore:
            won = True
        
        spikes =  pygame.Rect(0, 780, 700, 500)
        if logo.colliderect(spikes):
            gameOver = True

        screen.blit(playerImg, player)
        screen.blit(objectImg, logo)
        screen.blit(smallPixelFont.render(f"Score: {score}/50", True, "black"), (10, 10))

    elif gameOver:
        if not playedLoseSound:
            pygame.mixer.music.stop()
            loseSound.play()
            playedLoseSound = True

        box = pygame.transform.scale(pygame.image.load("pictures/box.png"), (550, 600))
        screen.blit(box, (30, 80))

        screen.blit(bigPixelFont.render("GAME OVER", False, "red"), (130, 150))
        screen.blit(smallPixelFont.render("Your Dare:", False, "black"), (70, 230))
        screen.blit(smallPixelFont.render(currentDare, False, "black"), (100, 280))
        screen.blit(smallPixelFont.render("Press SPACE to Restart", False, "black"), (160, 550))
        
    elif won:
        if not playedWinSound:
            pygame.mixer.music.stop()
            winSound.play()
            playedWinSound = True

        box = pygame.transform.scale(pygame.image.load("pictures/box.png"), (550, 600))
        screen.blit(box, (30, 80))

        screen.blit(bigPixelFont.render("YOU WIN!", False, "Green"), (170, 150))
        screen.blit(smallPixelFont.render("You caught all 50!", False, "black"), (180, 280))
        screen.blit(smallPixelFont.render("Press SPACE to Play Again", False, "black"), (130, 550))

    pygame.display.flip()
    clock.tick(60)
#MJ, Marivic
