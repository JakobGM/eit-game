from settings import ScreenSettings
from typing import Callable
import pygame as pg
from settings import Color


class Text:
    def __init__(
        self,
        x: int,
        y: int,
        text: str = "",
        callable_text: Callable = None,
        color=Color(255, 255, 255),
        antialias=False,
    ):
        pg.font.init()
        self.x = x
        self.y = y
        self.text = text
        self.callable_text = callable_text
        self.font = pg.font.SysFont(ScreenSettings.font, ScreenSettings.font_size)
        self.color = color
        self.antialias = antialias

    def get_element(self):
        if self.callable_text is not None:
            text = self.callable_text()
            if type(text) is float:
                return self.font.render(
                    self.text + str(int(text)), self.antialias, self.color
                )
            return self.font.render(self.text + str(text), self.antialias, self.color)
        return self.font.render(self.text, self.antialias, self.color)
