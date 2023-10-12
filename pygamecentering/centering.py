import pygame
from pygamecentering.offset_linear_regression import params

class Text:
    def __init__(self, screen: pygame.Surface, text: str, color: tuple, center: tuple, font_size: int):
        self.screen = screen
        self.screen_color = screen.get_at(center)
        self.text = text
        self.color = color
        self.font_size = font_size
        self.font = pygame.font.Font(None, self.font_size)
        self.render = self.font.render(text, True, color)
        self.font_rect = self.render.get_rect(center=center)
        self.font_rect.centery = self.font_rect.centery+self.font_size*params['coef']+params['intercept']

    def draw(self):
        self.screen.blit(self.render, self.font_rect)

class TextButton(Text):
    def __init__(self, screen: pygame.Surface, text: str, color: tuple, center: tuple, font_size: int):
        super().__init__(screen, text, color, center, font_size)
        self.was_hovered = False
        self.clicked = False

    def __glow(self, factor = 1):
        self.erase_button()
        for i in range(-factor, factor + 1):
            for j in range(-factor, factor + 1):
                glow_surface = self.font.render(self.text, True, (255, 255, 255))
                glow_surface.set_alpha(20)
                self.screen.blit(glow_surface, (self.font_rect.left + i, self.font_rect.top + j))
        self.draw()

    def __draw_hovered(self):
        self.__glow(2)

    def __handle_click_down(self):
        self.__glow(3)
    
    def __handle_click_up(self):
        self.erase_button()
        self.draw()
        self.clicked = True
        self.was_hovered = False

    def __handle_unhovered(self):
        self.was_hovered = False
        self.erase_button()
        self.draw()
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
    #Public methods

    def erase_button(self):
        self.font_rect.inflate_ip(10, 10)
        pygame.draw.rect(self.screen, self.screen_color, self.font_rect, 0)
        self.font_rect.inflate_ip(-10, -10)

    def is_hovered(self):
        return self.font_rect.collidepoint(pygame.mouse.get_pos())

    def is_clicked(self):
        if self.was_hovered is False:
            if self.is_hovered() is True:
                self.was_hovered = True
                self.__draw_hovered()
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                pygame.display.update()
        
        else:
            if self.is_hovered() is True:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                for event in pygame.event.get():     
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.__handle_click_down()
                        pygame.display.update()
                    
                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        self.__handle_click_up()
                        pygame.display.update()
                        return True

            else:
                self.__handle_unhovered()
                pygame.display.update()
                
        return False

class Button():
    def __init__(self, screen: pygame.Surface, text: str, color: tuple, center: tuple, dim: tuple, thickness = 1, radius = -1, adjusted = True):
        self.screen = screen
        self.screen_color = screen.get_at(center)
        self.color = color
        self.font_size = int(dim[1]/.9) 
        self.render = pygame.font.Font(None, self.font_size).render(text, True, color)
        self.radius = radius
        self.thickness = thickness
        self.dim = dim #(w, h)
        self.adjusted = adjusted

        self.real_rect = pygame.Rect(0, 0, dim[0], dim[1]) #(left, top, width, height)
        self.real_rect.center = center
        self.font_rect = self.render.get_rect(center=center)
        while self.font_rect.w > dim[0] or self.font_rect.h > dim[1]:
            self.font_size -= 1
            font = pygame.font.Font(None, self.font_size)
            self.render = font.render(text, True, color)
            self.font_rect = self.render.get_rect(center=center)

        if adjusted:
            self.font_rect.centery = self.font_rect.centery+self.font_size*params['coef']+params['intercept'] #adjust text to center

        self.was_hovered = False
        self.clicked = False
        
    def __draw_text(self):
        self.screen.blit(self.render, self.font_rect)

    def __draw_border(self, extra = 0, color = None):
        color = color or self.color
        pygame.draw.rect(self.screen, color, self.real_rect, self.thickness + extra, self.radius)

    def __draw_hovered(self, color = (255, 255, 255)):
        self.__draw_border(3, color)

    def __handle_unhovered(self):
        self.was_hovered = False
        self.__draw_hovered(self.screen_color)
        self.__draw_border()
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def __handle_click_down(self):
        brighter_color = tuple([value+(255-value)*0.2 for value in self.screen_color.normalize()[:3]])
        self.__draw_border(-self.thickness, brighter_color)
        self.__draw_text()
        self.__draw_hovered()

    def __handle_click_up(self):
        self.erase_button()
        self.screen.blit(self.render, self.font_rect)
        self.__draw_hovered()
        self.clicked = True
        self.was_hovered = False

    #Public methods

    def draw(self):
        self.__draw_text()
        self.__draw_border()

    def erase_button(self):
        self.__draw_border(-self.thickness, self.screen_color)

    def is_hovered(self):
        return self.real_rect.collidepoint(pygame.mouse.get_pos())

    def is_clicked(self):
        if self.was_hovered is False:
            if self.is_hovered() is True:
                self.was_hovered = True
                self.__draw_hovered()
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                pygame.display.update()
        
        else:
            if self.is_hovered() is True:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                for event in pygame.event.get():     
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.__handle_click_down()
                        pygame.display.update()
                    
                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        self.__handle_click_up()
                        pygame.display.update()
                        return True
                    
            else:
                self.__handle_unhovered()
                pygame.display.update()
                
        return False
    
    def move(self, center: tuple):
        self.real_rect.center = center
        self.font_rect.center = center
        if self.adjusted:
            self.font_rect.centery = self.font_rect.centery+self.font_size*params['coef']+params['intercept'] #adjust text to center


class BadButton(Button):
    def __init__(self, screen: pygame.Surface, text: str, color: tuple, center: tuple, dim: tuple, thickness = 1, radius = -1):
        super().__init__(screen, text, color, center, dim, thickness, radius, adjusted = False)        
        
