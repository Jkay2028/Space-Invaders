import pygame


class InputBox:
    def __init__(self, x, y, width, height, text='', enter_handler=None, destroy_on_enter=False, font_size=32, active_color=(30, 144, 255), inactive_color=(135, 206, 250), hidden=False, render_order=-8, font_type='freesansbold.ttf'):
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.font = pygame.font.Font(font_type, font_size)
        self.original_width = width
        self.rect = pygame.Rect(x, y, width, height)
        self.color = self.inactive_color
        self.text = text
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
        self.render_order = render_order
        self.destroyed = False
        self.hidden = False
        self.enter_handler = enter_handler
        self.destroy_on_enter = destroy_on_enter
        from backend.engine import Engine
        self.engine = Engine.instance
        self.screen = self.engine.screen
        self.engine.add_input_box(self)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.hidden:
            click_inside = self.rect.collidepoint(event.pos)
            if self.active != click_inside:
                self.active = click_inside
                if self.active:
                    self.color = self.active_color
                else:
                    self.color = self.inactive_color
                self.render_txt_surface()
        if event.type == pygame.KEYDOWN and not self.hidden:
            if self.active:
                if event.key == pygame.K_RETURN:
                    if self.enter_handler is not None:
                        self.enter_handler()
                    if self.destroy_on_enter:
                        self.destroy()
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.render_txt_surface()
        width = max(self.original_width, self.txt_surface.get_width()+10)
        self.rect.w = width

    def render_txt_surface(self):
        self.txt_surface = self.font.render(
            self.text, True, self.color)

    def render(self):
        if not self.hidden:
            pygame.draw.rect(self.screen, (255, 255, 255), self.rect)
            self.screen.blit(self.txt_surface,
                             (self.rect.x + 5, self.rect.y + 5))

    def show(self):
        self.hidden = False

    def hide(self):
        self.hidden = True

    def destroy(self):
        self.engine.remove_input_box(self)
        self.destroyed = True
        self = None
