import pygame
from colors import *
from offset_linear_regression import params

def left_click(event: pygame.event.Event):
    return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1

class Button:
    def __init__(self, screen: pygame.Surface, text: str, COLOR: tuple, center: tuple, dim: tuple, thickness = 1, radius = -1, font_size = 0):
        if font_size == 0:
            self.font_size = int(dim[1]*1/.9) 
        else:
            self.font_size = font_size
        font = pygame.font.Font(None, self.font_size)
        self.render = font.render(text, True, COLOR)
        
        self.screen = screen
        self.screen_color = screen.get_at(center)

        self.COLOR = COLOR
        self.brightened = False
        self.was_hovered = False
        self.clicked = False

        self.radius = radius
        self.thickness = thickness
        self.dim = dim # (w, h)
        self.real_rect = pygame.Rect(0, 0, self.dim[0], self.dim[1]) #(left, top, width, height)
        self.real_rect.center = center

        self.font_rect = self.render.get_rect(center=center) #for centering text

        while self.font_rect.w > dim[0] or self.font_rect.h > dim[1]: #manual rect is too small
            self.font_size -= 1
            font = pygame.font.Font(None, self.font_size)
            self.render = font.render(text, True, COLOR)
            self.font_rect = self.render.get_rect(center=center)

        self.font_rect.centery = self.font_rect.centery+self.font_size*params['coef']+params['intercept'] #move text to center

        
    def get_text_bottom(self):
        #bottom of real rect - empty space between bottom and text. font_size/2 is the actual pixel height of the text
         return int(self.real_rect.bottom-(self.real_rect.h-self.font_size//2+1)//2)
    
    def get_text_top(self):
        return int(self.real_rect.top+(self.real_rect.h-self.font_size//2+1)//2)

    def draw_text(self):
        self.screen.blit(self.render, self.font_rect)

    def draw_border(self, extra = 0, color = None):
        if color == None:
            color = self.COLOR
        pygame.draw.rect(self.screen, color, self.real_rect, self.thickness + extra, self.radius)

    def draw(self):
        self.draw_text()
        self.draw_border()

    def draw_hovered(self, color = WHITE):
        self.draw_border(3, color)

    def erase_button(self):
        self.draw_border(-self.thickness, self.screen_color)

    def erase_hovered(self):
        self.draw_hovered(self.screen_color)
        self.draw_border()
    
    def draw_clicked(self):
        brighter_color = tuple([value+(255-value)*0.2 for value in self.screen_color.normalize()[:3]])
        self.draw_border(-self.thickness, brighter_color)
        self.draw_text()
        self.draw_hovered()

    def is_hovered(self):
        return self.real_rect.collidepoint(pygame.mouse.get_pos())

    #dont need event to check, but if there is one, check if its mouseclick
    def check_clicked(self):
        if self.clicked:
            self.clicked = False
            return True
        if self.is_hovered():
            self.draw_hovered()
            pygame.display.update()
            while self.is_hovered():        
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                for event in pygame.event.get():
                    if left_click(event):   
                        self.draw_clicked()
                        pygame.display.update()
                        self.brightened = True
                        while self.is_hovered():  
                            for new_event in pygame.event.get():
                                if new_event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                                    self.erase_button()
                                    self.screen.blit(self.render, self.font_rect)
                                    self.draw_hovered()
                                    pygame.display.update()
                                    self.clicked = True
                                    return True
        
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if self.brightened:
            self.brightened = False
            self.erase_button()
            self.draw()
        else:
            self.erase_hovered()
        pygame.display.update()
        return False
        

