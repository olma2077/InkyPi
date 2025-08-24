from plugins.base_plugin.base_plugin import BasePlugin
from PIL import Image

import requests

from .comic_parser import COMICS


class Comic(BasePlugin):
    def generate_settings_template(self):
        template_params = super().generate_settings_template()
        template_params['comics'] = list(COMICS)
        return template_params

    def generate_image(self, settings, device_config):
        comic = settings.get("comic")
        if not comic or comic not in COMICS:
            raise RuntimeError("Invalid comic provided.")

        comic_panel = COMICS[comic]()
        image_url = comic_panel.url
        if not image_url:
            raise RuntimeError("Failed to retrieve latest comic url.")

        dimensions = device_config.get_resolution()
        if device_config.get_config("orientation") == "vertical":
            dimensions = dimensions[::-1]
        width, height = dimensions

        response = requests.get(image_url, stream=True)
        response.raise_for_status()

        with Image.open(response.raw) as img:
            img.thumbnail((width, height), Image.LANCZOS)
            background = Image.new("RGB", (width, height), "white")
            background.paste(img, ((width - img.width) // 2, (height - img.height) // 2))
            return background
