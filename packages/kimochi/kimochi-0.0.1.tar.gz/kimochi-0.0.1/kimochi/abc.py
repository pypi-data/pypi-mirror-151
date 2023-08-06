from typing import Dict, Literal

from PIL import Image, ImageDraw, ImageChops, ImageOps

class BaseObject:
    def __init__(self, response: Dict[str, str], type: str):
        self.response = response
        self.type = type
        self.url = response.get('url')

        for key, value in response.items():
            setattr(self, key, value)

    def __repr__(self):
        return f'<{self.type.capitalize()} url: {self.url}>'

