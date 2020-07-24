import pygame
from backend.engine import Engine


class Text:

    render_order = -6

    def __init__(self, text, x_position=0, y_position=0, size=32, text_color=(255, 255, 255), hidden=False, render_order=-6, font_type='freesansbold.ttf'):
        self.pos_x = x_position
        self.pos_y = y_position
        self.size = size
        self.text_color = text_color
        self.font_type = font_type
        self.hidden = hidden
        self.render_order = render_order
        self.destroyed = False

        self.font = pygame.font.Font(self.font_type, self.size)
        self.text = self.font.render(text, True, self.text_color)

        self.screen = Engine.instance.screen
        Engine.instance.add_object(self)

    def change_text(self, new_text):
        self.text = self.font.render(new_text, True, self.text_color)

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    def destroy(self):
        Engine.instance.remove_object(self)
        self.destroyed = True

    def render(self):
        if not self.hidden:
            self.screen.blit(self.text, (self.pos_x, self.pos_y))
