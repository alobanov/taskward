"""The app's palettes, each in the light and the dark, taken one to one from its code
(lib/theme/palette_schemes.dart, and Analog from lib/theme/polk_theme.dart) with their names
in both languages, into tool/palettes.json, which tool/build.py lays out as palettes.css and
the swatches. Run again when the app's palettes change:

    python3 tool/palettes.py
"""

import json
import re
from pathlib import Path

APP = Path.home() / 'Development' / 'polk'
OUT = Path(__file__).with_name('palettes.json')

# Analog as the app draws it on its default desk and ink (polk_theme.dart: _deskLight sage,
# the cards' own papers, graphite ink; in the dark the sage desk's dark, AppDarkTextColor.white).
ANALOG = (
    {'desk': 'FFB4C2C3', 'white': 'FFF4F5F6', 'cream': 'FFF5EBD7', 'kraft': 'FFD9CDB6',
     'grey': 'FFE4E3DF', 'ink': 'FF45454F', 'seal': 'FFC8463D', 'dusk': 'FF7E68CF',
     'highlight': '6BF6C945'},
    {'desk': 'FF1D2426', 'white': 'FF2A2B30', 'cream': 'FF332E25', 'kraft': 'FF3B3429',
     'grey': 'FF252525', 'ink': 'FFF4F4F6', 'seal': 'FFC8463D', 'dusk': 'FFA592EC',
     'highlight': '59F6C945'},
)


def main():
    src = (APP / 'lib/theme/palette_schemes.dart').read_text()
    named = dict(re.findall(r'static const (_\w+) = Color\(0x([0-9A-Fa-f]{8})\)', src))

    def scheme(body):
        out = {}
        for key, value in re.findall(r'(\w+): (Color\(0x[0-9A-Fa-f]{8}\)|_\w+|[0-9.]+),', body):
            if value.startswith('Color'):
                out[key] = value[8:16].upper()
            elif value.startswith('_'):
                out[key] = named[value].upper()
            else:
                out[key] = float(value)
        return out

    palettes = {'analog': ANALOG}
    for m in re.finditer(r'PaletteChoice\.(\w+): \(\s*PaletteScheme\((.*?)\),\s*PaletteScheme\((.*?)\),\s*\)',
                         src, re.S):
        palettes[m[1]] = (scheme(m[2]), scheme(m[3]))
    names = {}
    for lang in ('en', 'ru'):
        words = json.loads((APP / f'assets/translations/{lang}.json').read_text())['settings']
        names[lang] = {'palettes': words['palettes'], 'light': words['in_light'], 'dark': words['in_dark']}
    OUT.write_text(json.dumps({'palettes': palettes, 'names': names}, ensure_ascii=False, indent=1) + '\n')
    print(f'{len(palettes)} palettes → {OUT}')


if __name__ == '__main__':
    main()
