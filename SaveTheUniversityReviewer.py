import pygame # pip install pygame
import sys  # for sys.exit()
import random # for random.randint() and random.choice()

pygame.init() # Initialize Pygame
pygame.mixer.init() # Initialize the mixer for sound
# Set up the display
width = 600
height = 800
# Create the game window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Save the University")
# Load fonts
smallPixelFont = pygame.font.Font("font/pixelatedElegance.ttf", 20)
bigPixelFont = pygame.font.Font("font/pixelatedElegance.ttf", 50)

clock = pygame.time.Clock() # Create a clock to control the frame rate

background = pygame.image.load("pictures/newBackground.png") # Load and scale the background image to fit the window
background = pygame.transform.scale(background, (width, height)) 
# Load and scale the object and player images
objectImg = pygame.transform.scale(pygame.image.load("pictures/UddLogo.png"), (50, 50))

playerImg = pygame.transform.scale(pygame.image.load("pictures/Chibi char.png"), (120, 100))
# Load and set up sounds
pygame.mixer.music.load("sounds/bgMusic.mp3")
pygame.mixer.music.set_volume(0.2)
# Load sound effects and set their volume
catchSound = pygame.mixer.Sound("sounds/catchSound.mp3")
catchSound.set_volume(0.5)
loseSound = pygame.mixer.Sound("sounds/gameOver.mp3")
loseSound.set_volume(0.5)
winSound = pygame.mixer.Sound("sounds/win.mp3")
winSound.set_volume(0.5)
# Game variables
playerSpeed = 15
winScore = 50
# List of dares for the game over screen
dares = [
    "Sing a song",
    "Do 20 push-ups",
    "Try to lick your elbow",
    "Kiss your classmate",
    "Borrow money from stranger",
    "Confess to your crush"
]
# Randomly select a dare for the game over screen
currentDare = random.choice(dares)
# Function to reset the game state, including player and logo positions, score, and speed
def resetGame():
    global currentDare
    currentDare = random.choice(dares)
    return (
        pygame.Rect(250, 700, 120, 60),
        pygame.Rect(random.randint(0, width-50), 0, 50, 50),0, 5
    )
# Initialize the player, logo, score, and speed using the resetGame function
player, logo, score, speed = resetGame()
# Flags to track game state
gameOver = False
won = False
started = False
# Flags to ensure the lose and win sounds are played only once
playedLoseSound = False
playedWinSound = False
# Main game loop
while True:
    screen.blit(background, (0, 0))
# Handle events such as quitting the game and key presses
    for event in pygame.event.get():    # Check for events
        if event.type == pygame.QUIT: # Quit the game if the window is closed
            pygame.quit()   # Quit Pygame
            sys.exit() # Exit the program
# Start the game when any key is pressed, and reset the game if it's over or won and the space key is pressed
        if not started and event.type == pygame.KEYDOWN: # Start the game on any key press
            started = True # Set the started flag to True
            player, logo, score, speed = resetGame() # Reset the game state
            pygame.mixer.music.play(-1, 0.0, 3000) # Start playing background music in a loop with a fade-in effect
# Reset the game when space is pressed after a game over or win
        elif (gameOver or won) and event.type == pygame.KEYDOWN: # Check if the game is over or won and a key is pressed
            if event.key == pygame.K_SPACE: # Check if the space key is pressed
                player, logo, score, speed = resetGame() # Reset the game state
                gameOver = False # Reset the game over flag
                won = False # Reset the won flag
                playedLoseSound = False # Reset the lose sound flag
                playedWinSound = False # Reset the win sound flag
                pygame.mixer.music.play(-1, 0.0, 3000) # Start playing background music in a loop with a fade-in effect
# Game logic and rendering based on the current game state
    if not started: # If the game hasn't started, display the intro screen with the start button
        startKey = "" # Variable to hold the key prompt for starting the game
      
        startImg = pygame.transform.scale(pygame.image.load("pictures/introPic.png"), (400, 200))
        screen.blit(startImg, (100, 50))

        startButton = pygame.transform.scale(pygame.image.load("pictures/startButton.png"), (250, 200))
        screen.blit(startButton, (180, 550))
#         Display the prompt to start the game
    elif not gameOver and not won:
        spikes = pygame.transform.scale(pygame.image.load("pictures/spikes.png"), (700, 500))
        screen.blit(spikes, (0, 545))
        
        keys = pygame.key.get_pressed() # Get the current state of all keyboard keys

        if keys[pygame.K_LEFT]: # Move the player left if the left arrow key is pressed
            player.x -= playerSpeed # Move the player left by subtracting playerSpeed from the player's x-coordinate
        if keys[pygame.K_RIGHT]:
            player.x += playerSpeed
# Ensure the player stays within the bounds of the window
        player.x = max(0, min(width - player.width, player.x))
# Move the logo down the screen by increasing its y-coordinate by the speed variable
        logo.y += speed
# Check for collision between the logo and the player, and update the score, logo position, and speed if a collision occurs
        if logo.colliderect(player):# Check if the logo collides with the player
            catchSound.play() # Play the catch sound effect
            score += 1 # Increment the score by 1
            logo.topleft = (random.randint(0, width-50), 0) # Reset the logo to a new random position at the top of the screen
            speed += 0.3 # Increase the speed of the logo slightly to make the game more challenging
# Check if the logo has fallen below the bottom of the screen, and set the game over flag if it has

        if logo.top > height:  # Check if the logo has fallen below the bottom of the screen
            gameOver = True # Set the game over flag to True if the logo has fallen below the bottom of the screen

        if score == winScore:
            won = True
        # Check for collision between the logo and the spikes, and set the game over flag if a collision occurs
        spikes =  pygame.Rect(0, 780, 700, 500) # Create a rectangle for the spikes area at the bottom of the screen
        if logo.colliderect(spikes): # Check if the logo collides with the spikes
            gameOver = True # Set the game over flag to True if the logo collides with the spikes
# Draw the player, logo, and score on the screen
        screen.blit(playerImg, player) # Draw the player image at the player's current position
        screen.blit(objectImg, logo) # Draw the logo image at the logo's current position
        screen.blit(smallPixelFont.render(f"Score: {score}/50", True, "black"), (10, 10)) # Draw the score in the top-left corner of the screen 

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
