from django.core.management.base import BaseCommand
from BaseApp.styles import registered_styles
from BaseApp.constants import background_colors, background_border_colors
import os


class Command(BaseCommand):
    help = 'Generate a dummy HTML file for Tailwind CSS classes'

    def handle(self, *args, **kwargs):
        # registed_styles is a dictionary of style classes
        styles = []
        for style, style_class in registered_styles.items():
            if style_class.classes is "":
                self.stdout.write(self.style.ERROR(
                    f'{style_class.__name__}.classes is empty! Not Registered!'))
                continue
            styles.append(style_class)
            self.stdout.write(self.style.SUCCESS(
                f'{style} Style Installed.'))

        # Define the path to the templates directory
        file_path = os.path.join(
            'BaseApp', 'templates', 'BaseApp', 'tailwind_dummy.html')

        # Create directories if they don't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w', encoding="utf-8") as file:
            for style in styles:
                file.write(f'<div class="hidden {style.classes}"></div>\n')
            colors = []
            for color in background_colors:
                colors.append(color)
            for color in background_border_colors:
                colors.append(color)
            colors_string = ' '.join(colors)
            file.write(f'<div class="hidden {colors_string}"></div>\n')

        self.stdout.write(self.style.SUCCESS(
            f'Successfully generated {file_path}'))
