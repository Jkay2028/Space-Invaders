from backend.text import Text
import pygame


class Table:
    def __init__(self, x, y, columns, column_width, row_height, background_color=(255, 255, 255), font_color=(0, 0, 0), font_size=32, render_order=-10, font_type='freesansbold.ttf'):
        self.x = x
        self.y = y
        self.rows = 0
        self.columns = columns
        self.row_height = row_height
        self.column_width = column_width
        self.background_color = background_color
        self.texts = []
        self.font_color = font_color
        self.font_size = font_size
        self.render_order = render_order
        self.font_type = font_type
        self.update_rect()
        from backend.engine import Engine
        self.engine = Engine.instance
        self.screen = self.engine.screen
        self.engine.add_object(self)

    def update_rect(self):
        self.widths = []
        width = 0
        if isinstance(self.column_width, int) or isinstance(self.column_width, float):
            width = self.columns * self.column_width
            for i in range(self.columns):
                self.widths.append(self.x + i * self.column_width)
        else:
            if len(self.column_width) == self.columns:
                for i in range(self.columns):
                    self.widths.append(self.x + width)
                    width += self.column_width[i]
            else:
                print("Column Width List does not have a correct length")
        height = self.rows * self.row_height
        self.rect = (self.x, self.y, width, height)

    def add_row(self, text_list):
        self.rows += 1
        self.update_rect()
        if len(text_list) != self.columns:
            print("The text list length does not match the column length")
        else:
            for i in range(self.columns):
                new_text = Text(text_list[i], self.widths[i], self.y + (self.rows - 1) * self.row_height,
                                self.font_size, self.font_color, False, self.render_order, self.font_type)
                self.texts.append(new_text)

    def render(self):
        pygame.draw.rect(self.screen, self.background_color, self.rect)
        for text in self.texts:
            text.render()

    def destroy(self):
        self.engine.remove_object(self)
        for text in self.texts:
            text.destroy()
