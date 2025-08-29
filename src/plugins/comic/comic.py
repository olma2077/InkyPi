from plugins.base_plugin.base_plugin import BasePlugin
from PIL import Image, ImageDraw, ImageFont

import requests

from .comic_parser import COMICS, get_panel


class Comic(BasePlugin):
    def generate_settings_template(self):
        template_params = super().generate_settings_template()
        template_params['comics'] = list(COMICS)
        return template_params

    def generate_image(self, settings, device_config):
        comic = settings.get("comic")
        if not comic or comic not in COMICS:
            raise RuntimeError("Invalid comic provided.")

        comic_panel = get_panel(comic)
        image_url = comic_panel["url"]
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
            if comic_panel["title"]:
                height += 20
            if comic_panel["caption"]:
                height += 20
            background = Image.new("RGB", (width, height), "white")
            font = ImageFont.truetype("DejaVuSans.ttf", size=20)
            draw = ImageDraw.Draw(background)
            if comic_panel["title"]:
                draw.text((0, 0), comic_panel["title"], font=font)
            if comic_panel["caption"]:
                draw.text((0, height - 20), comic_panel["caption"], font=font)
            background.paste(img, ((width - img.width) // 2, (height - img.height) // 2))
            return background
