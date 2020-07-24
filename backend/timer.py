import pygame


class Timer:

    def __init__(self, time, handler, param=None):
        self.time = time
        self.time_left = time
        self.handler = handler
        self.param = param

    def update(self):
        from backend.engine import Engine

        self.time_left -= Engine.instance.delta_time
        if self.time_left <= 0:

            if self.param is None:
                self.handler()
            else:
                self.handler(self.param)

            Engine.instance.remove_timer(self)

    def stop(self):
        from backend.engine import Engine

        Engine.instance.remove_timer(self)
