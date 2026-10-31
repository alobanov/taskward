"""Lays the site's pictures in from the app's repository: the paper's tooth, the oak, the
app's icon, the hand-drawn icons as one sprite, and the store's screenshots, small."""
import re, sys
from pathlib import Path
from PIL import Image

APP = Path.home() / 'Development/polk'
IMG = Path(__file__).resolve().parent.parent / 'img'

def webp(src, dst, width=None, quality=82):
    im = Image.open(src)
    if width and im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(IMG / dst, 'WEBP', quality=quality, method=6)

webp(APP / 'assets/textures/paper_light.png', 'grain.webp', 384, 70)
webp(APP / 'assets/textures/paper_dark.png', 'grain-dark.webp', 384, 70)
webp(APP / 'assets/textures/oak.jpg', 'oak.webp', 1400, 78)
icon = Image.open(APP / 'tool/app_icon/notebook.png').convert('RGB')
icon.resize((512, 512), Image.LANCZOS).save(IMG / 'icon.png', optimize=True)
icon.resize((180, 180), Image.LANCZOS).save(IMG / 'apple-touch-icon.png', optimize=True)
icon.resize((64, 64), Image.LANCZOS).save(IMG / 'favicon.png', optimize=True)
for lang in ['en', 'ru']:
    for i in range(1, 9):
        webp(APP / f'build/store/{lang}/iphone_{i}.jpg', f'{lang}-iphone-{i}.webp', 760, 90)
    for i in range(1, 6):
        webp(APP / f'build/store/{lang}/mac_{i}.jpg', f'{lang}-mac-{i}.webp', 2240, 90)

# The icons, inked in the page's own colour.
names = ['export', 'favoriteFilled', 'today', 'list', 'archive', 'check', 'flagFilled',
         'reminderFilled', 'tag', 'paperLines', 'darkThemeFilled', 'project', 'notebook',
         'search', 'knight', 'more', 'lock', 'backup', 'success', 'add']
symbols = []
for n in names:
    svg = (APP / f'assets/icons/{n}.svg').read_text()
    box = re.search(r'viewBox="([^"]+)"', svg).group(1)
    body = re.sub(r'^.*?<svg[^>]*>|</svg>\s*$', '', svg, flags=re.S)
    body = re.sub(r'<title>.*?</title>', '', body, flags=re.S)
    body = body.replace('#000000', 'currentColor')
    filled = 'fill="currentColor"' if 'Filled' in n else 'fill="none"'
    symbols.append(f'<symbol id="{n}" viewBox="{box}" {filled} stroke="currentColor" '
                   f'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">{body}</symbol>')
(IMG / 'icons.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg">' + ''.join(symbols) + '</svg>')
print('ok', len(list(IMG.iterdir())), 'files')
