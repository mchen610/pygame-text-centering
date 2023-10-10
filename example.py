#example.py

import pygame
from pgcenteredbutton import Button, BadButton 

if __name__ == "__main__":
    
    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((1000, 1000))
    button_color = (200, 200, 200)
    button_center = (350, 500)
    button_dim = (300, 100)
    
    good_button = Button(screen = screen, text = 'GOOD', color = button_color, center = button_center, dim = button_dim)
    good_button.draw()

    bad_button_center = (650, 500)
    bad_button = BadButton(screen = screen, text = 'BAD', color = button_color, center = bad_button_center, dim = button_dim)
    bad_button.draw()

    while good_button.clicked is False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if good_button.is_clicked(event):
                print('Goodbye world')

            if bad_button.is_clicked(event):
                print('I don\'t matter!')
                
        clock.tick(60)
        pygame.display.update()
    
    pygame.quit()
    exit()

