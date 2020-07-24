import pygame
from backend.engine import Engine


class Button:

    render_order = -5

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    def destroy(self):
        Engine.instance.remove_object(self)
        self.destroyed = True

    def mouse_is_over(self):
        mouse_pos = pygame.mouse.get_pos()

        return self.pos_x + self.width > mouse_pos[0] > self.pos_x and self.pos_y + self.height > mouse_pos[1] > self.pos_y

    def check_mouse_click(self, pos_x, pos_y):
        if self.mouse_is_over():
            self.handler()
            if self.destroy_on_click:
                self.destroy()

    def __init__(self, pos_x, pos_y, width, height, handler=None, text="", font_size=32, hidden=False, font_color=(0, 0, 0), button_color=(255, 255, 255), hover_color=None, destroy_on_click=False, render_order=-5, font_type='freesansbold.ttf'):
        self.button_color = button_color
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.font_type = font_type
        self.font_size = font_size
        self.render_order = render_order
        if hover_color == None:
            self.hover_color = button_color
        else:
            self.hover_color = hover_color
        self.hidden = hidden
        self.handler = handler
        self.destroy_on_click = destroy_on_click
        self.destroyed = False

        self.font = pygame.font.Font(self.font_type, self.font_size)
        self.text = self.font.render(text, True, font_color)
        self.text_rect = self.text.get_rect(center=(self.pos_x + self.width /
                                                    2, self.pos_y + self.height / 2))

        Engine.instance.add_object(self)
        if self.handler is not None:
            Engine.instance.on_mouse_click(self.check_mouse_click)

    def render(self):
        if not self.hidden:
            if self.mouse_is_over():
                pygame.draw.rect(Engine.instance.screen, self.hover_color,
                                 (self.pos_x, self.pos_y, self.width, self.height))

            else:
                pygame.draw.rect(Engine.instance.screen, self.button_color,
                                 (self.pos_x, self.pos_y, self.width, self.height))

            Engine.instance.screen.blit(self.text, self.text_rect)
