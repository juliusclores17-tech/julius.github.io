import pygame #pygame - game engine
import sys  #sys - lets you exit the program
import random #random - used for random positions & dares

#Initializes the game and sound system
pygame.init()
pygame.mixer.init()
#Creates a 600x800 window
width = 600
height = 800
#Sets the title of the window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Save the University")

font = pygame.font.SysFont("Arial", 30) #font - used for displaying text on the screen
bigFont = pygame.font.SysFont("Arial", 60) #bigFont - used for displaying larger text on the screen

clock = pygame.time.Clock() #clock - used to control the frame rate of the game

#Loads and scales the background image, player image, and object image
background = pygame.image.load("pictures/background.jpg")
background = pygame.transform.scale(background, (width, height))
#They are resized using: pygame.transform.scale() to fit the game better.
objectImg = pygame.transform.scale(pygame.image.load("log-removebg-preview.png"), (50, 50)) 
playerImg = pygame.transform.scale(pygame.image.load("image/Chibi_char_pixel2.png"), (120, 100))
#Loads the background music and sound effects, and sets their volumes
pygame.mixer.music.load("sounds/bgMusic.mp3")
pygame.mixer.music.set_volume(0.2)

catchSound = pygame.mixer.Sound("sounds/catchSound.mp3")
catchSound.set_volume(0.5)
loseSound = pygame.mixer.Sound("sounds/gameOver.mp3")
loseSound.set_volume(0.5)
winSound = pygame.mixer.Sound("sounds/win.mp3")
winSound.set_volume(0.5)
#Defines game variables such as player speed and winning score (GAME SETTINGS)
playerSpeed = 15
winScore = 50
#A list of dares that the player will have to do if they lose the game. 
#A random dare is selected at the start of each game.
dares = [
    "Sing a song",
    "Do 20 push-ups",
    "Try to lick your elbow",
    "Kiss your classmate"
]

currentDare = random.choice(dares)
#The resetGame function initializes the player's position, the falling object's position, the score,
#and the speed of the falling object. It is called at the start of the game and whenever the player restarts after winning or losing.
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
#These variables are used to track the state of the game
# (whether it's over, won, or started) and to ensure that the lose and win sounds are only played once when the game ends.
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

#The main game loop handles the different states of the game
# before it starts, during gameplay, when the game is over
# and when the player wins. It updates the player's position based on keyboard input, moves the falling object, checks for collisions, and updates the score.
# It also displays the appropriate images and text based on the game state.
    if not started:
        startKey = ""

        startImg = pygame.transform.scale(pygame.image.load("images/=====.png"), (400, 200))
        screen.blit(startImg, (100, 50))

        startButton = pygame.transform.scale(pygame.image.load("images/startButton.png"), (250, 200))
        screen.blit(startButton, (180, 550))

#The player can start the game by pressing any key.
#Once the game starts, the player controls a character at the bottom of the screen, trying to catch falling objects (logos).
#Each time the player catches an object, their score increases and the falling speed of the objects increases.
#If an object falls past the bottom of the screen, the game is over and a random dare is displayed.
#If the player reaches the winning score, they win the game.
#The player can restart the game by pressing the spacebar after winning or losing.
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

        screen.blit(playerImg, player)
        screen.blit(objectImg, logo)
        screen.blit(font.render(f"Score: {score}/50", True, "black"), (10, 10))
#When the game is over, it displays a "GAME OVER" message along with the dare that the player has to do.
#When the player wins, it displays a "YOU WIN!" message and prompts the player to play again.
#In both cases, the background music stops and the appropriate sound effect is played.
    elif gameOver:
        if not playedLoseSound:
            pygame.mixer.music.stop()
            loseSound.play()
            playedLoseSound = True


        box = pygame.transform.scale(pygame.image.load("pictures/box.png"), (550, 800))
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
    clock.tick(60) #Limits the game to 60 frames per second to ensure smooth gameplay and consistent timing across different devices.
