from pgcenteredbutton import button
import pygame

if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1000,1000))
    easy_button = button.Button(screen, 'EASY', (66, 66, 66), center = (500, 500), dim = (300, 100))
    easy_button.draw()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
        easy_button.check_clicked()

        clock.tick(60) #fps
        pygame.display.update()
