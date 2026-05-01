import pygame
import sys
import random

pygame.init()


WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Save The University")


BLACK = (0, 0, 0)
BLUE = (0, 120, 255)


font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 60)

clock = pygame.time.Clock()


background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))


object_img = pygame.transform.scale(pygame.image.load("log-removebg-preview.png"), (50, 50))
player_img = pygame.transform.scale(pygame.image.load("Chibi_char_pixel2.png"), (120, 100))


player_speed = 10
WIN_SCORE = 50


dares = [
    "Sing a song ",
    "Do 20 push-ups ",
    "Try to lick your elbow."
]

current_dare = random.choice(dares)

def reset_game():
    global current_dare
    current_dare = random.choice(dares)
    return (
        pygame.Rect(250, 700, 120, 60),
        pygame.Rect(random.randint(0, WIDTH-50), 0, 50, 50),
        0,
        5
    )

player, obj, score, speed = reset_game()
game_over = False
won = False

while True:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if (game_over or won) and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player, obj, score, speed = reset_game()
                game_over = False
                won = False

    if not game_over and not won:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player.x += player_speed

        player.x = max(0, min(WIDTH - player.width, player.x))

        obj.y += speed

        if obj.colliderect(player):
            score += 1
            obj.topleft = (random.randint(0, WIDTH-50), 0)
            speed += 0.3

        if obj.top > HEIGHT:
            game_over = True

        if score == WIN_SCORE:
            won = True

        screen.blit(player_img, player)
        screen.blit(object_img, obj)
        screen.blit(font.render(f"Score: {score}/50", True, BLACK), (10, 10))

    elif game_over:
        screen.blit(big_font.render("GAME OVER", True, BLACK), (150, 250))
        screen.blit(font.render("Your Dare:", True, BLACK), (230, 320))

       
        screen.blit(font.render(current_dare, True, BLACK), (160, 360))

        screen.blit(font.render("Press SPACE to Restart", True, BLACK), (150, 420))

    elif won:
        screen.blit(big_font.render("YOU WIN!", True, BLUE), (180, 250))
        screen.blit(font.render("You caught all 50!", True, BLACK), (180, 320))
        screen.blit(font.render("Press SPACE to Play Again", True, BLACK), (130, 400))

    pygame.display.flip()
    clock.tick(60)