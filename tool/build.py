"""Writes the site's pages, English at / and Russian at /ru/, from one set of templates:
the landing page, the privacy policy and support.

    python3 tool/build.py
"""
import json
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
URL = 'https://alobanov.github.io/taskward/'
MAIL = 'katleta5000@gmail.com'
BETA = 'https://testflight.apple.com/join/h82fp1R4'
import hashlib
VERSION = hashlib.md5((SITE / 'style.css').read_bytes() + (SITE / 'app.js').read_bytes()).hexdigest()[:8]
UPDATED = {'en': 'October 27, 2026', 'ru': '27 октября 2026'}

T = {
    'en': {
        'title': 'Taskward: a calm to-do list on paper cards',
        'desc': 'A calm to-do list for iPhone and Mac. Every list is a paper card on your desk: '
                'Today in front, the rest in a wooden holder behind it.',
        'nav': ['Lists', 'Smart dates', 'iPhone and Mac', 'Privacy', 'Support'],
        'other': ('Русский', 'ru/'),
        'h1': 'Your day,<br>on one card.',
        'lede': 'Taskward is a calm to-do list for iPhone and Mac. Every list is a paper card on '
                'your desk.',
        'cta': 'Join the beta on TestFlight',
        'small': 'Free, no account. Coming to the App Store soon.',
        'then': 'Draw a card out of the holder and it lies on your desk. Work right on it.',
        'today': 'Today', 'upcoming': 'Upcoming', 'anytime': 'Anytime', 'someday': 'Someday',
        'date': '27.10.26',
        'tasks': [
            ('Sharpen the sword', '', True),
            ('Call the smith about the shield', 'Friday|21:30|1/3', False),
            ('Pay the rent', 'due:Today', False),
            ('Plan the ride to the coast', '2/5', False),
        ],
        'evening': 'This Evening',
        'evening_tasks': ['Read twenty pages'],
        'check': 'Check off',
        'lists_h': 'Every list is a card of its own',
        'lists_say': 'Things come in, get a day or wait for one, and end up done. Each list has its own paper, so you always know where you are.',
        'lists': [
            ('export', 'Inbox', 'white', 'Whatever comes to mind, before you decide what it is.'),
            ('favoriteFilled', 'Today', 'white', 'What you take on today, and this evening under it.'),
            ('today', 'Upcoming', 'cream', 'The days ahead, with your calendar beside them.'),
            ('list', 'Anytime', 'cream', 'Your stock of things to do, there when you are ready.'),
            ('archive', 'Someday', 'kraft', 'Put off, not forgotten. Looked through now and then.'),
            ('check', 'Logbook', 'grey', 'Everything done, kept in the order you did it.'),
        ],
        'ticket_h': 'A task opens as a ticket',
        'ticket_say': 'Notes, a checklist, tags, a deadline and a reminder, on a card torn off '
                      'along a dashed line. Only what you have added shows; the rest waits as a '
                      'pencil mark at its foot.',
        'ticket': {
            'title': 'Call the smith about the shield',
            'notes': 'The old one is cracked along the rim. Ask if he can match the boss.',
            'steps': [('Measure the old one', True), ('Find the sketch', False), ('Ask the price', False)],
            'tags': ['Armoury', 'Errand'], 'when': 'Today',
        },
        'signals_h': 'More than done or not done',
        'signals_say': 'Hold a task’s circle and mark how it stands. Delegated and waiting fade '
                       'into pencil, out of your way.',
        'signals_note': 'Mark',
        'signals': ['Done', 'In progress', 'Delegated', 'Meeting', 'Important', 'Waiting'],
        'smart_h': 'Write it as you’d say it',
        'smart_say': 'Type “Gym tomorrow at 9am” and the day and the reminder set themselves; the '
                     'words leave the title. Tap the highlight if you meant the words.',
        'smart_hint': 'Notes',
        'smart_blank': 'When',
        'phrases': [
            ('Gym ', 'tomorrow at 9am', 'today', 'Tomorrow', '09:00'),
            ('Movie night ', 'on friday evening', 'darkThemeFilled', 'Friday', ''),
            ('Dentist ', 'Nov 12 at 14:30', 'today', 'Nov 12', '14:30'),
        ],
        'more_h': 'And a little more',
        'more': [
            ('paperLines', 'Zen', 'Open a card edge to edge when a day needs all of you. Draw it down and it is back on the desk.'),
            ('search', 'Quick Find', 'Draw Today down on home, or press ⌘F on a Mac: lists, projects, tags and tasks, as you type.'),
            ('notebook', 'Notes', 'A card of its own for what isn’t a task. Move a note into your tasks, or a task back into notes.'),
        ],
        'zen_h': 'One card, the whole screen',
        'zen_say': 'When a day needs all of you, open its card edge to edge: no bar, no desk, '
                   'nothing else. Draw it down and it is back on the desk.',
        'real_h': 'The real app, on iPhone and Mac',
        'real_say': 'The same lists on both, kept in step through your iCloud. On a Mac, a '
                    'sidebar and Quick Find on ⌘F.',
        'shots_alt': 'Taskward on iPhone',
        'mac_alt': 'Taskward on a Mac',
        'yours_h': 'Your desk, your ink',
        'yours_say': 'Pick the desk the cards lie on, the ink you write in, how a done task is '
                     'struck through, and smooth or toothy paper. Try a desk here:',
        'desk_h': 'Desk', 'ink_h': 'Ink',
        'desks': [('default', 'Sage', '#b4c2c3'), ('olive', 'Olive', '#4a5040'),
                  ('walnut', 'Walnut', '#5b4636'), ('charcoal', 'Charcoal', '#2f2f2d'),
                  ('paper', 'Paper', '#e9e5da'), ('mono', 'Monochrome', '#f2f3f5')],
        'inks': [('default', 'Graphite', '#45454f'), ('blue', 'Blue', '#2b3ac9'),
                 ('black', 'Black', '#141417'), ('espresso', 'Espresso', '#3a201c')],
        'kept_h': 'Nothing of yours leaves your hands',
        'kept': ['No account to make.', 'No ads, no tracking, no analytics.',
                 'Your tasks live on your devices and in your own iCloud, which we can’t read.'],
        'kept_link': 'Read the privacy policy',
        'knight_h': 'New to getting things done?',
        'knight_say': 'On first launch a little knight hands you a pile of errands and shows you '
                      'how to sort an inbox, one task at a time. Skip it whenever you like.',
        'support': 'Support', 'privacy': 'Privacy policy', 'by': 'Made by Aleksei Lobanov',
        'back': 'Taskward',
    },
    'ru': {
        'title': 'Taskward: спокойный список дел на бумажных карточках',
        'desc': 'Спокойный список дел для iPhone и Mac. Каждый список — бумажная карточка на '
                'столе: «Сегодня» впереди, остальные в деревянной подставке за ней.',
        'nav': ['Списки', 'Умная дата', 'iPhone и Mac', 'Приватность', 'Поддержка'],
        'other': ('English', '../'),
        'h1': 'Весь день —<br>на одной карточке.',
        'lede': 'Taskward — спокойный список дел для iPhone и Mac. Каждый список — бумажная '
                'карточка на твоём столе.',
        'cta': 'Попробовать бету в TestFlight',
        'small': 'Бесплатно и без аккаунта. Скоро в App Store.',
        'then': 'Вытяни карточку из подставки — она ляжет на стол. Работай прямо на ней.',
        'today': 'Сегодня', 'upcoming': 'Планы', 'anytime': 'В любое время', 'someday': 'Когда-нибудь',
        'date': '27.10.26',
        'tasks': [
            ('Наточить меч', '', True),
            ('Позвонить кузнецу насчёт щита', 'Пятница|21:30|1/3', False),
            ('Заплатить за жильё', 'due:Сегодня', False),
            ('Спланировать поездку к морю', '2/5', False),
        ],
        'evening': 'Этим вечером',
        'evening_tasks': ['Прочитать двадцать страниц'],
        'check': 'Отметить',
        'lists_h': 'У каждого списка своя карточка',
        'lists_say': 'Дела приходят во входящие, получают свой день или ждут его — и уходят в журнал. У каждого списка своя бумага, так что сразу видно, где ты.',
        'lists': [
            ('export', 'Входящие', 'white', 'Всё, что пришло в голову, пока не решил, что это.'),
            ('favoriteFilled', 'Сегодня', 'white', 'То, что берёшь на сегодня, и вечер под ним.'),
            ('today', 'Планы', 'cream', 'Ближайшие дни, и календарь рядом с ними.'),
            ('list', 'В любое время', 'cream', 'Запас дел, который ждёт, когда будешь готов.'),
            ('archive', 'Когда-нибудь', 'kraft', 'Отложено, а не забыто. Иногда стоит пересмотреть.'),
            ('check', 'Журнал', 'grey', 'Всё сделанное, в том порядке, как делал.'),
        ],
        'ticket_h': 'Задача открывается билетом',
        'ticket_say': 'Заметки, чек-лист, теги, срок и напоминание — на карточке с отрывным '
                      'корешком. Видно только то, что добавил; остальное ждёт карандашной меткой '
                      'внизу.',
        'ticket': {
            'title': 'Позвонить кузнецу насчёт щита',
            'notes': 'Старый треснул по краю. Спросить, подберёт ли он умбон.',
            'steps': [('Измерить старый', True), ('Найти эскиз', False), ('Узнать цену', False)],
            'tags': ['Оружейная', 'В городе'], 'when': 'Сегодня',
        },
        'signals_h': 'Больше, чем сделано или нет',
        'signals_say': 'Зажми кружок задачи и отметь, как она: в работе, поручено, жду ответа. '
                       'Поручённое и ожидание уходят в карандаш, чтобы не мешать.',
        'signals_note': 'Отметить',
        'signals': ['Выполнено', 'В работе', 'Поручено', 'Встреча', 'Важно', 'Жду ответа'],
        'smart_h': 'Пиши, как говоришь',
        'smart_say': 'Напиши «Тренировка завтра в 9 утра» — день и напоминание поставятся сами, '
                     'а слова уйдут из названия. Тап по подсветке — если имел в виду просто слова.',
        'smart_hint': 'Заметки',
        'smart_blank': 'Когда',
        'phrases': [
            ('Тренировка ', 'завтра в 9 утра', 'today', 'Завтра', '09:00'),
            ('Кино ', 'в пятницу вечером', 'darkThemeFilled', 'Пятница', ''),
            ('Визит к врачу ', '12 ноября в 14:30', 'today', '12 нояб.', '14:30'),
        ],
        'more_h': 'И ещё немного',
        'more': [
            ('paperLines', 'Дзен', 'Разверни карточку на весь экран, когда день требует всего внимания. Потяни вниз — и она снова на столе.'),
            ('search', 'Быстрый поиск', 'Потяни «Сегодня» вниз на главном или нажми ⌘F на Маке: списки, проекты, теги и задачи прямо по мере ввода.'),
            ('notebook', 'Заметки', 'Отдельная карточка для того, что не задача. Заметку можно сделать задачей, а задачу — заметкой.'),
        ],
        'zen_h': 'Одна карточка на весь экран',
        'zen_say': 'Когда день требует всего внимания, разверни его карточку от края до края: '
                   'без панели, без стола, без лишнего. Потяни вниз — и она снова на столе.',
        'real_h': 'Настоящее приложение, на iPhone и Mac',
        'real_say': 'Одни и те же списки на обоих, синхронно через твой iCloud. На Маке — '
                    'боковая панель и быстрый поиск по ⌘F.',
        'shots_alt': 'Taskward на iPhone',
        'mac_alt': 'Taskward на Маке',
        'yours_h': 'Твой стол, твои чернила',
        'yours_say': 'Выбери стол, на котором лежат карточки, цвет чернил, как зачёркивается '
                     'сделанное, и гладкую или фактурную бумагу. Попробуй стол прямо здесь:',
        'desk_h': 'Стол', 'ink_h': 'Чернила',
        'desks': [('default', 'Шалфей', '#b4c2c3'), ('olive', 'Олива', '#4a5040'),
                  ('walnut', 'Орех', '#5b4636'), ('charcoal', 'Уголь', '#2f2f2d'),
                  ('paper', 'Бумага', '#e9e5da'), ('mono', 'Монохром', '#f2f3f5')],
        'inks': [('default', 'Графит', '#45454f'), ('blue', 'Синие', '#2b3ac9'),
                 ('black', 'Чёрные', '#141417'), ('espresso', 'Эспрессо', '#3a201c')],
        'kept_h': 'Твоё остаётся у тебя',
        'kept': ['Не нужно заводить аккаунт.', 'Ни рекламы, ни слежки, ни аналитики.',
                 'Задачи живут на твоих устройствах и в твоём iCloud — мы их не видим.'],
        'kept_link': 'Политика конфиденциальности',
        'knight_h': 'Впервые слышишь про GTD?',
        'knight_say': 'При первом запуске маленький рыцарь вручит тебе ворох поручений и покажет, '
                      'как разобрать входящие, задачу за задачей. Пропустить можно в любой момент.',
        'support': 'Поддержка', 'privacy': 'Политика конфиденциальности',
        'by': 'Сделал Алексей Лобанов', 'back': 'Taskward',
    },
}


def icon(name, cls='icon'):
    return f'<svg class="{cls}" aria-hidden="true"><use href="{{base}}img/icons.svg#{name}"/></svg>'


SIGNAL = '<svg viewBox="0 0 24 24"><circle class="ring" cx="12" cy="12" r="9.2"/><circle class="fill" cx="12" cy="12" r="9.2"/></svg>'

# The signals' marks, drawn as the app draws them in the circle.
MARKS = [
    '<circle class="ring solid" cx="15" cy="15" r="11"/>',
    '<circle class="ring" cx="15" cy="15" r="11"/><path class="solid" d="M15 4a11 11 0 0 0 0 22z"/>',
    '<circle class="ring" cx="15" cy="15" r="11"/><path class="mark" d="M4 15h22M15 4v22"/>',
    '<circle class="ring" cx="15" cy="15" r="11"/><path class="mark" d="M15 8v7l5 3"/>',
    '<path class="mark" d="M15 5v20M6.3 10l17.4 10M6.3 20l17.4-10"/>',
    '<circle class="ring" cx="15" cy="15" r="11"/><path class="mark" d="M9 15h.01M15 15h.01M21 15h.01" stroke-width="3"/>',
]


def head(lang, title, desc, path, base):
    other = 'ru' if lang == 'en' else 'en'
    here = URL + ('ru/' if lang == 'ru' else '') + path
    there = URL + ('ru/' if other == 'ru' else '') + path
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{here}">
<link rel="alternate" hreflang="{lang}" href="{here}">
<link rel="alternate" hreflang="{other}" href="{there}">
<link rel="alternate" hreflang="x-default" href="{URL + path}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{URL}img/og-{lang}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#b4c2c3">
<link rel="icon" href="{base}img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="{base}img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Pangolin&amp;subset=cyrillic&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}style.css?v={VERSION}">
<style>:root {{ --grain: url({base}img/grain.webp); }}</style>
<script>try {{ const d = localStorage.getItem('taskward-desk'), i = localStorage.getItem('taskward-ink');
if (d && d !== 'default') document.documentElement.dataset.desk = d;
if (i && i !== 'default') document.documentElement.dataset.ink = i; }} catch (_) {{}}</script>
<script src="{base}app.js?v={VERSION}" defer></script>
</head>
'''


def bar(t, base, lang, home):
    other, href = t['other']
    anchors = ['#lists', '#smart', '#real']
    links = ''.join(
        f'<a class="hide-sm" href="{home}{a}">{name}</a>' for a, name in zip(anchors, t['nav'][:3])
    )
    priv = f'{base}{"ru/" if lang == "ru" else ""}privacy/'
    sup = f'{base}{"ru/" if lang == "ru" else ""}support/'
    return f'''<header class="wrap top">
<a class="brand" href="{home}"><img src="{base}img/icon.png" alt="" width="40" height="40">Taskward</a>
<nav aria-label="Sections">{links}<a class="hide-sm" href="{priv}">{t['nav'][3]}</a><a href="{sup}">{t['nav'][4]}</a><a href="{href}" lang="{'ru' if lang == 'en' else 'en'}">{other}</a></nav>
</header>'''


def foot(t, base, lang):
    other, href = t['other']
    pre = 'ru/' if lang == 'ru' else ''
    return f'''<footer><div class="wrap">
<a href="{base}{pre}support/">{t['support']}</a>
<a href="{base}{pre}privacy/">{t['privacy']}</a>
<a href="{href}">{other}</a>
<span class="by">{t['by']}</span>
</div></footer>'''


def small_print(spec):
    if not spec:
        return ''
    parts = []
    for bit in spec.split('|'):
        if bit.startswith('due:'):
            parts.append(f'<span class="due">{icon("flagFilled")}{bit[4:]}</span>')
        elif ':' in bit:
            parts.append(f'<span>{icon("reminderFilled")}{bit}</span>')
        elif '/' in bit:
            parts.append(f'<span>{bit}</span>')
        else:
            parts.append(f'<span>{icon("flagFilled")}{bit}</span>')
    return f'<div class="print">{"".join(parts)}</div>'


def row(t, title, spec, done):
    pressed = 'true' if done else 'false'
    return (f'<li class="row{" done" if done else ""}"><button class="signal" aria-pressed="{pressed}" '
            f'aria-label="{t["check"]}: {title}">{SIGNAL}</button>'
            f'<div><div class="title">{title}</div>{small_print(spec)}</div></li>')


def landing(lang):
    t = T[lang]
    base = '' if lang == 'en' else '../'
    home = './'
    rows = ''.join(row(t, *task) for task in t['tasks'])
    evening = ''.join(row(t, title, '', False) for title in t['evening_tasks'])
    lists = ''.join(
        f'<div class="paper {paper}" style="--r:{r}deg"><div class="head">'
        f'{icon(mark)}{name}</div><p>{say}</p></div>'
        for (mark, name, paper, say), r in zip(t['lists'], [-1.2, 0.8, -0.4, 1.1, -0.9, 0.5])
    ).replace('<svg class="icon" aria-hidden="true"><use href="{base}img/icons.svg#favoriteFilled"/></svg>',
              '<svg class="icon" style="color:var(--seal)" aria-hidden="true"><use href="{base}img/icons.svg#favoriteFilled"/></svg>')
    tk = t['ticket']
    steps = ''.join(
        f'<li class="{"done" if done else ""}"><span class="box"></span>{s}</li>' for s, done in tk['steps']
    )
    signals = ''.join(
        f'<li class="{"faint" if i == 5 else ""}"><svg viewBox="0 0 30 30" aria-hidden="true">{m}</svg>{name}</li>'
        for i, (m, name) in enumerate(zip(MARKS, t['signals']))
    )
    phrases = json.dumps([
        {'title': title, 'phrase': phrase,
         'foot': (f'{icon(mark)}<span>{day}</span>'
                  + (f'{icon("reminderFilled")}<span>{time}</span>' if time else ''))
         .replace('{base}', base)}
        for title, phrase, mark, day, time in t['phrases']
    ], ensure_ascii=False).replace('"', '&quot;')
    iphones = ''.join(
        f'<img src="{base}img/{lang}-iphone-{i}.webp" alt="{t["shots_alt"]}" width="760" height="1651" loading="lazy">'
        for i in range(1, 9)
    )
    desks = ''.join(
        f'<button class="swatch" style="--c:{c}" data-desk="{k}" aria-label="{n}" aria-pressed="false"></button>'
        for k, n, c in t['desks']
    )
    inks = ''.join(
        f'<button class="blot" style="--c:{c}" data-inkpick="{k}" aria-label="{n}" aria-pressed="false"></button>'
        for k, n, c in t['inks']
    )
    kept = ''.join(f'<li>{line}</li>' for line in t['kept'])
    more = ''.join(
        f'<div class="paper {paper}" style="--r:{r}deg"><div class="head">{icon(mark)}{name}</div><p>{say}</p></div>'
        for (mark, name, say), paper, r in zip(t['more'], ['white', 'cream', 'kraft'], [-0.8, 0.6, -0.4])
    )
    sample_rows = ''.join(row(t, title, '', done) for title, _, done in t['tasks'][:3])
    pre = 'ru/' if lang == 'ru' else ''
    page = head(lang, t['title'], t['desc'], '', base) + f'''<body>
{bar(t, base, lang, home)}
<main>
<section class="hero"><div class="wrap hero-in">
<div class="hero-words">
<h1>{t['h1']}</h1>
<p class="lede">{t['lede']}</p>
<a class="button" href="{BETA}">{icon('add')}{t['cta']}</a>
<p class="small">{t['small']}</p>
</div>
<div class="fan">
<img class="side left" src="{base}img/{lang}-iphone-3.webp" alt="" width="760" height="1651">
<img class="side right" src="{base}img/{lang}-iphone-4.webp" alt="" width="760" height="1651">
<img class="front" src="{base}img/{lang}-iphone-1.webp" alt="{t['shots_alt']}" width="760" height="1651" fetchpriority="high">
</div>
</div></section>

<section class="part" id="lists"><div class="wrap">
<h2>{t['lists_h']}</h2>
<p class="say">{t['lists_say']}</p>
<div class="spread">{lists}</div>
</div></section>

<section class="part" id="ticket"><div class="wrap split">
<div><h2>{t['ticket_h']}</h2><p class="say">{t['ticket_say']}</p></div>
<div class="ticket-wrap"><div class="paper ticket">
<h3><span class="signal">{SIGNAL}</span>{tk['title']}</h3>
<p class="notes">{tk['notes']}</p>
<ul class="steps">{steps}</ul>
<div class="stub">
<div class="tags">{''.join(f'<span>{x}</span>' for x in tk['tags'])}</div>
<div class="when"><span class="star">{icon('favoriteFilled')}</span>{tk['when']}{icon('reminderFilled')}21:30<span class="marks">{icon('flagFilled')}</span></div>
</div>
</div></div>
</div></section>

<section class="part" id="signals"><div class="wrap split">
<div><h2>{t['signals_h']}</h2><p class="say">{t['signals_say']}</p></div>
<div class="paper signals-note"><p class="note-title">{t['signals_note']}</p><ul class="signals">{signals}</ul></div>
</div></section>

<section class="part" id="smart"><div class="wrap split">
<div class="paper newcard" data-phrases="{phrases}">
<div class="field"><span class="ring"></span><span><span class="typed"></span><span class="caret"></span></span></div>
<p class="hint">{t['smart_hint']}</p>
<div class="foot"><span class="chip"><span class="muted">{icon('today')}</span><span class="muted">{t['smart_blank']}</span></span><span class="marks">{icon('tag')}{icon('paperLines')}{icon('flagFilled')}</span></div>
</div>
<div><h2>{t['smart_h']}</h2><p class="say">{t['smart_say']}</p></div>
</div></section>

<section class="part" id="more"><div class="wrap">
<h2>{t['more_h']}</h2>
<div class="trio">{more}</div>
</div></section>

<section class="part" id="real"><div class="wrap">
<h2>{t['real_h']}</h2>
<p class="say">{t['real_say']}</p>
<div class="shelf">{iphones}</div>
<div class="macs">
<img src="{base}img/{lang}-mac-1.webp" alt="{t['mac_alt']}" width="2240" height="1400" loading="lazy">
</div>
</div></section>

<section class="part" id="yours"><div class="wrap">
<h2>{t['yours_h']}</h2>
<p class="say">{t['yours_say']}</p>
<div class="picks">
<div><h3>{t['desk_h']}</h3><div class="swatches">{desks}</div><p class="named" data-for="desk" aria-live="polite"></p></div>
<div><h3>{t['ink_h']}</h3><div class="swatches">{inks}</div><p class="named" data-for="inkpick" aria-live="polite"></p></div>
<div class="paper sample" aria-hidden="true"><div class="head"><svg class="icon" aria-hidden="true"><use href="{base}img/icons.svg#favoriteFilled"/></svg>{t['today']}</div><ul class="rows">{sample_rows}</ul></div>
</div>
</div></section>

<section class="part" id="kept"><div class="wrap">
<div class="paper kept">
{icon('lock', 'icon big')}
<div><h2>{t['kept_h']}</h2><ul>{kept}</ul><p><a href="{base}{pre}privacy/">{t['kept_link']}</a></p></div>
</div>
</div></section>

<section class="part" id="knight"><div class="wrap knight">
{icon('knight', 'icon big')}
<div><h2>{t['knight_h']}</h2><p class="say">{t['knight_say']}</p>
<p><a class="button" href="{BETA}">{icon('add')}{t['cta']}</a></p></div>
</div></section>
</main>
{foot(t, base, lang)}
</body>
</html>
'''
    return page.replace('{base}', base)


PRIVACY = {
    'en': ('Privacy policy', '''
<p>Taskward is a to-do list for iPhone and Mac made by Aleksei Lobanov. This policy says what
happens to what you write in it. In short: nothing you write reaches us.</p>
<h2>What we collect</h2>
<p>Nothing. Taskward has no account, no ads, no analytics and no tracking, and it sends nothing
to us or to anyone else. Its App Store privacy label is “Data Not Collected”.</p>
<h2>Where your tasks are kept</h2>
<p>Your lists, tasks, notes, tags and settings are kept in a database on your device. If iCloud
is on for Taskward, they are also kept in your own iCloud account, in its private database, so
your iPhone and Mac stay in step. That database belongs to your Apple Account: we cannot see,
read or change it. Apple keeps it under the
<a href="https://www.apple.com/legal/privacy/">Apple Privacy Policy</a>.</p>
<h2>Your calendars and reminders</h2>
<p>If you let it, Taskward reads the events of your calendars to show them next to your
day’s tasks. They are read on your device and are never copied anywhere. Reminders you set are
scheduled as notifications by your device itself.</p>
<h2>Crashes</h2>
<p>If you have chosen to share analytics with Apple, Apple may send us anonymous crash reports
for the app. They contain no tasks or other things you have written.</p>
<h2>Deleting your data</h2>
<p>Delete a task, a list or everything in the app and it is gone from your device and your
iCloud. Deleting the app removes what it kept on the device. To remove what it kept in iCloud,
open Settings, tap your name, then iCloud, Manage Storage, Taskward, and delete its data.</p>
<h2>Children</h2>
<p>Taskward collects nothing from anyone, children included.</p>
<h2>Changes</h2>
<p>If this policy changes, the new one is published here with its date.</p>
<h2>Contact</h2>
<p>Questions: <a href="mailto:{mail}">{mail}</a>.</p>
'''),
    'ru': ('Политика конфиденциальности', '''
<p>Taskward — список дел для iPhone и Mac, его сделал Алексей Лобанов. Здесь написано, что
происходит с тем, что вы в нём пишете. Коротко: ничего из этого к нам не попадает.</p>
<h2>Что мы собираем</h2>
<p>Ничего. В Taskward нет аккаунта, рекламы, аналитики и слежки, и оно ничего не отправляет ни
нам, ни кому-либо ещё. Метка приватности в App Store — «Данные не собираются».</p>
<h2>Где хранятся задачи</h2>
<p>Списки, задачи, заметки, теги и настройки хранятся в базе данных на вашем устройстве. Если для
Taskward включён iCloud, они хранятся и в вашем личном iCloud, в его закрытой базе, чтобы
iPhone и Mac совпадали. Эта база принадлежит вашему Apple ID: мы не можем её видеть, читать или
менять. Apple хранит её по своей
<a href="https://www.apple.com/ru/legal/privacy/">политике конфиденциальности</a>.</p>
<h2>Календари и напоминания</h2>
<p>Если вы разрешите, Taskward читает события ваших календарей, чтобы показать их рядом с
задачами дня. Они читаются на устройстве и никуда не копируются. Напоминания назначает
уведомлениями само устройство.</p>
<h2>Сбои</h2>
<p>Если вы разрешили делиться аналитикой с Apple, Apple может присылать нам обезличенные отчёты о
сбоях приложения. В них нет задач и ничего из написанного вами.</p>
<h2>Удаление данных</h2>
<p>Удалите задачу, список или всё в приложении — и это исчезнет с устройства и из iCloud. Удаление
приложения стирает то, что оно хранило на устройстве. Чтобы удалить данные из iCloud, откройте
Настройки, нажмите своё имя, затем iCloud, «Управление хранилищем», Taskward и удалите данные.</p>
<h2>Дети</h2>
<p>Taskward ни у кого ничего не собирает, в том числе у детей.</p>
<h2>Изменения</h2>
<p>Если политика изменится, новая версия появится здесь с датой.</p>
<h2>Связь</h2>
<p>Вопросы: <a href="mailto:{mail}">{mail}</a>.</p>
'''),
}

SUPPORT = {
    'en': ('Support', '''
<p>Something not working, or an idea? Write to <a href="mailto:{mail}">{mail}</a> and I’ll
answer, usually within a day or two. Say which device and which version of the app you have
(Settings, at the foot).</p>
<h2>How do my tasks get from iPhone to Mac?</h2>
<p>Through your own iCloud. Sign in to the same Apple Account on both and keep iCloud on for
Taskward. If they fall out of step, open the three dots on home and choose Sync Now.</p>
<h2>Do smart dates work in my language?</h2>
<p>In English and Russian, both at once: “tomorrow at 9am”, “next friday”, “завтра в 9 утра”.
Tap the highlighted words if you meant them as words.</p>
<h2>How do I see my calendar next to my tasks?</h2>
<p>In Settings, turn on calendar events and allow Taskward to read your calendars.</p>
<h2>How do I join the beta?</h2>
<p>Open <a href="{beta}">the TestFlight invitation</a> on your iPhone or Mac.</p>
<h2>How do I delete everything?</h2>
<p>See <a href="../privacy/">the privacy policy</a>: what to delete in the app, and in iCloud.</p>
'''),
    'ru': ('Поддержка', '''
<p>Что-то не работает или есть идея? Напишите на <a href="mailto:{mail}">{mail}</a> — отвечу,
обычно в течение дня-двух. Укажите устройство и версию приложения (Настройки, внизу).</p>
<h2>Как задачи попадают с iPhone на Mac?</h2>
<p>Через ваш iCloud. Войдите в один и тот же Apple ID на обоих и оставьте iCloud для Taskward
включённым. Если что-то разошлось, откройте три точки на главном и выберите «Синхронизировать».</p>
<h2>На каких языках работает умная дата?</h2>
<p>На русском и английском сразу: «завтра в 9 утра», «в следующую пятницу», “tomorrow at 9am”.
Нажмите на подсвеченные слова, если имели в виду просто слова.</p>
<h2>Как увидеть календарь рядом с задачами?</h2>
<p>В Настройках включите события календаря и разрешите Taskward читать календари.</p>
<h2>Как попасть в бету?</h2>
<p>Откройте <a href="{beta}">приглашение в TestFlight</a> на iPhone или Маке.</p>
<h2>Как удалить всё?</h2>
<p>Смотрите <a href="../privacy/">политику конфиденциальности</a>: что удалить в приложении и в iCloud.</p>
'''),
}


def doc(lang, kind, pages):
    t = T[lang]
    title, body = pages[lang]
    depth = '../' if lang == 'en' else '../../'
    home = depth if lang == 'en' else depth + 'ru/'
    body = body.replace('{mail}', MAIL).replace('{beta}', BETA)
    updated = (f'<p class="updated">{"Last updated" if lang == "en" else "Обновлено"}: '
               f'{UPDATED[lang]}</p>') if kind == 'privacy' else ''
    t2 = dict(t)
    t2['other'] = (t['other'][0], (f'../../{kind}/' if lang == 'ru' else f'../ru/{kind}/'))
    page = head(lang, f'{title} · Taskward', t['desc'], f'{kind}/', depth) + f'''<body>
{bar(t2, depth, lang, home)}
<main class="wrap"><article class="paper doc"><h1>{title}</h1>{updated}{body}</article></main>
{foot(t2, depth, lang)}
</body>
</html>
'''
    return page.replace('{base}', depth)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


for lang in ['en', 'ru']:
    pre = SITE if lang == 'en' else SITE / 'ru'
    write(pre / 'index.html', landing(lang))
    write(pre / 'privacy/index.html', doc(lang, 'privacy', PRIVACY))
    write(pre / 'support/index.html', doc(lang, 'support', SUPPORT))
write(SITE / '.nojekyll', '')
write(SITE / '404.html', '<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=/taskward/"><title>Taskward</title>')
write(SITE / 'sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
      + ''.join(f'<url><loc>{URL}{p}</loc></url>' for p in ['', 'privacy/', 'support/', 'ru/', 'ru/privacy/', 'ru/support/'])
      + '</urlset>\n')
print('written')
