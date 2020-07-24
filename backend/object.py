import pygame


class Object:

    img = None
    pos_x = 0
    pos_y = 0
    render_order = 0

    def __init__(self, img_path, x, y, scale=1.0, rotation=0.0, destroy_on_screen_exit=False, destroy_handler=None, render_order=0, hidden=False):
        self.img = pygame.image.load(img_path)
        self.pos_x = x
        self.pos_y = y
        self.hidden = hidden
        self.render_order = render_order
        self.scale = scale
        self.rotation = rotation
        self.destroyed = False
        self.destroy_on_screen_exit = destroy_on_screen_exit
        self.destroy_handler = destroy_handler

        from backend.engine import Engine
        self.engine = Engine.instance

        self.screen = self.engine.screen

        self.engine.add_object(self)

        self.img = pygame.transform.scale(
            self.img, (int(self.img.get_rect()[2] * scale), int(self.img.get_rect()[3] * scale)))
        self.img = pygame.transform.rotate(self.img, self.rotation)

        self.width = int(self.img.get_rect()[2])
        self.height = int(self.img.get_rect()[3])

    def destroy(self):
        self.engine.remove_object(self)
        self.destroyed = True
        self = None

    def render(self):
        if self.destroy_on_screen_exit:
            if (self.pos_x + self.width < 0) or (self.pos_x > self.engine.screen_width) or (self.pos_y + self.width < 0) or (self.pos_y > self.engine.screen_height):
                if self.destroy_handler is not None:
                    self.destroy_handler(self)

                self.destroy()

        if not self.hidden:
            self.screen.blit(self.img, (self.pos_x, self.pos_y))

    def check_collision(self, obj):
        selfRect = self.img.get_rect().copy()
        selfRect = selfRect.move(self.pos_x, self.pos_y)
        objRect = obj.img.get_rect().copy()
        objRect = objRect.move(obj.pos_x, obj.pos_y)
        return selfRect.colliderect(objRect)

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False
