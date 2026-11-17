"""Writes the site's pages, English at / and Russian at /ru/, from one set of templates:
the landing page, the privacy policy and support.

    python3 tool/build.py
"""
import json
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
URL = 'https://alobanov.github.io/taskward/'
MAIL = 'katleta5000@gmail.com'
import hashlib

VERSION = hashlib.md5((SITE / 'style.css').read_bytes() + (SITE / 'app.js').read_bytes() + (SITE / 'when.js').read_bytes()).hexdigest()[:8]
UPDATED = {'en': 'November 4, 2026', 'ru': '4 ноября 2026'}

T = {
    'en': {
        'title': 'Taskward: a calm to-do list on paper cards',
        'desc': 'A calm to-do list for iPhone and Mac. Every list is a paper card on your desk: '
                'Today in front, the rest in a wooden holder behind it.',
        'nav': ['Features', 'Pro', 'iPhone and Mac', 'Privacy', 'Support'],
        'other': ('Русский', 'ru/'),
        'h1': 'Your day,<br>on <u>one card</u>.',
        'lede': ('A calm to-do list for iPhone and Mac.',
                 'Every list is a paper card on your desk. Write a task the way you’d say it, and '
                 'work your day from one card.'),
        'small': 'No account · no ads · kept in your own iCloud',
        'cta': 'Coming soon to the App Store',
        'upcoming': 'Upcoming',
        'check': 'Check off',
        # Each list's card with the hint the app shows under its head (list_hint in the app's
        # translations), its words cut short for the page: (icon, name, paper, marker, pen, title, text);
        # the pen is the marker taken toward the ink, as ListHint writes in it.
        'hints': [
            ('export', 'Inbox', 'white', '#4AA8F0', '#487ba8', 'Catch it all here', 'Whatever comes to mind. Sort it once a day.'),
            ('today', 'Upcoming', 'cream', '#FF6B5E', '#ab5a57', 'What has a day of its own', "Dated tasks wait here and come up in Today on their day."),
            ('list', 'Anytime', 'cream', '#3FB27F', '#428169', 'Next steps', 'When Today is done, take the next one from here.'),
            ('archive', 'Someday', 'kraft', '#FFA23A', '#a85900', 'Dreams and later', "What you’d like to do, just not now. Look in once a week."),
            ('project', 'Projects', 'white', '#8B6CF0', '#6c5aa8', 'Projects and areas', 'A project is a goal of several steps; an area, a part of life: work, home, health.'),
            ('notebook', 'Notes', 'white', '#F6C945', '#a68e4a', 'Not a to-do, just written down', 'Thoughts worth keeping, out of your to-dos. A note becomes a task once it is one.'),
        ],
        'ticket': {
            'title': 'Call the smith about the shield',
            'notes': 'The old one is **cracked** along the rim. Ask if he can match the ::boss::.',
            'steps': [('Measure the old one', True), ('Find the sketch', False), ('Ask the price', False)],
            'tags': ['Armoury', 'Errand'], 'when': 'Today',
        },
        'signals_note': ('Mark it', 'Complete', 'Signals…'),
        'signals': ['In progress', 'Delegated', 'Appointment', 'Important'],
        # Written in pen round the phone, each pointing at its place on the screen.
        'float': {'smart': ('Gym ', 'tomorrow at 9'), 'when': 'Tomorrow', 'progress': 'In progress',
                  'tag': 'Armoury'},
        'notes': ['the other lists, standing behind', 'Today in front: work right on it',
                  'a deadline today, in red', 'a tap, and a new task',
                  'Inbox, projects and notes, on the oak'],
        'smart_h': 'Write it as you’d say it',
        'try_say': 'Type a task with a day in it, the way you would say it, and press Return. '
                   'The day and the reminder set themselves, and the task lands on its card.',
        'try_ph': 'Gym tomorrow at 9am',
        'try_add': 'Put it on its card',
        'try_examples': ['tomorrow at 9am', 'on friday evening', 'in 3 days', 'Nov 12 at 14:30'],
        'try_base': 'Gym ',
        'inbox': 'Inbox', 'evening_word': 'This Evening', 'when_word': 'When',
        'today_word': 'Today', 'tomorrow_word': 'Tomorrow',
        'try_seed': {'inbox': ['Buy a new pen'], 'today': ['Sharpen the sword'], 'upcoming': ['Tournament at the castle']},
        # Quick Find's little scene: the word typed and what it finds.
        'find_demo': ('sadd', ['Oil the <mark>sadd</mark>le', 'Mend the <mark>sadd</mark>le bags']),
        # The Day demo: its title, then its rows — an event (time, title, end, length, colour,
        # over), now, free time (from, words), a task (time, title), a crowd (two events, +N).
        'day_demo': {
            'title': 'Monday, 19 October',
            'rows': [
                ('event', '07:30', 'Morning ride', '08:30', '1 h', '#7cc9f2', True),
                ('now', 'now'),
                ('free', '', '49 min left free'),
                ('event', '10:30', 'Council at the keep', '11:30', '1 h', '#f5a03c', False),
                ('free', '11:30', '2 h 30 min free'),
                ('crowd', '14:00', [('Archery practice', '#b65ce0'), ('Letters', '#7cc9f2')], '+2'),
                ('free', '15:00', '3 h 30 min free'),
                ('task', '18:30', 'Call the smith about the shield'),
                ('event', '19:00', 'Supper with Masha', '21:00', '2 h', '#3aa0e8', False),
            ],
        },
        'notes_demo': {
            'title': 'Notes',
            'parts': [
                (None, ['What the smith said', 'Names for the horse']),
                ('Songs', ['Verses for the feast', 'A ballad of the sea']),
                ('Ideas', ['A sundial for the yard']),
            ],
            'diary': ('Diary', 'Sunday, 18 October', ['Oil the hinges', 'Reply to Masha', 'Pack the saddle']),
            'slip': 'Ideas',
        },
        'cal_empty': 'Nothing on this day',
        # The demo's days, by how far each is from today: its events (time, or none for all
        # day; title; its calendar's colour) and its tasks (title, done).
        'cal_days': [
            (-2, [('09:00', 'Market day', '#3fbf5a')], [('Oil the saddle', True)]),
            (0, [('07:30', 'Morning ride', '#7cc9f2'), ('10:30', 'Council at the keep', '#f5a03c'),
                 ('19:00', 'Supper with Masha', '#3aa0e8')],
             [('Sharpen the sword', True), ('Pay the rent', False)]),
            (1, [('13:00', 'Joust heats', '#b65ce0')], [('Call the smith about the shield', False)]),
            (2, [], [('Plan the ride to the coast', False)]),
            (4, [('', 'Feast of St Luke', '#3fbf5a')], []),
            (6, [('18:00', 'Tourney feast', '#f5a03c'), ('20:00', 'Night watch', '#3aa0e8')], []),
            (9, [], [('Visit the far north', False)]),
        ],
        'shots_alt': 'Taskward on iPhone',
        'mac_alt': 'Taskward on a Mac',
        'kept_h': 'Nothing of yours leaves your hands',
        'kept': ['No account to make.', 'No ads, no tracking. Anonymous usage statistics you can turn off.',
                 'Your tasks live on your devices and in your own iCloud, which we can’t read.'],
        'kept_link': 'Read the privacy policy',
        # Everything it does, at a glance: a tile for each, linking to where it is shown —
        # (anchor, icon, name, one line, a Pro mark or none). Only what the app does
        # (the app's docs/*.md); Pro's as docs/pro.md has it: a tile all Pro's marked by its
        # name, one only in part by {pro} in its line, right after what is Pro's.
        'all_h': 'Everything it does',
        'all_say': 'A calm to-do list with more in it than it shows. Tap one to see it at work.',
        'tiles': [
            ('speak', 'voice', 'Write as you speak', 'Type “gym tomorrow at 9”, or say your whole day aloud {pro}', ''),
            ('claude', 'magic', 'Plans from Claude', 'Ask for a plan; it lands in your lists as projects and tasks.', 'Pro · Mac'),
            ('day', 'time', 'Your day by the hour', 'Events and tasks on one clock, and the month on a card.', 'Pro'),
            ('paper', 'cardFile', 'Lists on paper cards', 'Today in front, the rest in an oak holder. Many themes {pro}', ''),
            ('ticket', 'note', 'All in one task', 'Notes in Markdown, a checklist; a deadline and a reminder {pro}', ''),
            ('signals', '', 'More than done', 'In progress, delegated, waiting: mark how a task stands. Every signal {pro}', ''),
            ('repeat', 'repeat', 'Repeating tasks', 'Every week, or the 2nd Tuesday {pro}: the next comes when one is done.', ''),
            ('find', 'search', 'Quick Find', 'Pull Today down, or ⌘F: lists, projects, tags, tasks.', ''),
            ('notes', 'notebook', 'Notes and a diary', 'Notes apart from tasks, and a diary that writes itself.', 'Pro'),
            ('focus', 'tomato', 'Focus timer', 'One tomato at a time for the task at hand, on the Lock Screen too.', ''),
            ('mac', 'backup', 'iPhone and Mac in step', 'Your own iCloud, no account. On a Mac, the day in the menu bar {pro}', ''),
            ('widgets', 'paperDots', 'Widgets', 'Today, what’s next and the month on your Lock Screen, and Home Screen {pro}', ''),
        ],
        # The four told large, each beside a short film of the app in a phone.
        'voice_h': 'Or say your whole day',
        'voice_say': 'Tap the microphone beside Today’s plus and talk: “call the bank at ten, gym in '
                     'the evening, a present for Anna on Friday.” It comes back as separate tasks with '
                     'their days and times, and the ones you gave no time are fitted into the gaps '
                     'between your events. Look them over, then add.',
        'voice_note': 'Dictating is part of Pro, on iPhone and Mac.',
        'claude_h': 'Plans from Claude, right in your lists',
        'claude_say': 'Tell Claude what you’re up to. It looks at your areas and projects and writes a '
                      'plan in: a project with headings, tasks with their days, deadlines and checklists. '
                      'Or ask it to sort your Inbox. Whatever it does, one Undo takes back.',
        'claude_note': 'On a Mac with Pro, and on your iPhone a moment later through iCloud.',
        'claude_link': 'How to connect Claude',
        'day_h': 'Your day by the hour',
        'day_say': 'Switch the calendar to Day: your events and the tasks with a time lie out by the '
                   'clock, side by side where they overlap. The free time between them takes one line '
                   'and says how long it really is, so the whole day fits one screen. The month puts a '
                   'dot under each day for its events and tasks: tap a day to see it.',
        'day_note': 'Your calendars are read on the device, never copied. The calendar is part of Pro.',
        'paper_h': 'Every list, a paper card on your desk',
        'paper_say': 'Today lies in front and you work right on it; Upcoming, Anytime and Someday '
                     'stand behind it in an oak holder. Draw one out and it lies on the desk. Each list '
                     'has its own paper and a word on what it’s for, so you always know where you are.',
        'yours_h': 'Make it yours',
        'yours_say': 'Light or dark, a palette for each, the desk under the cards, the ink you write in, '
                     'how a done task is struck through, smooth or toothy paper. Or open a list edge '
                     'to edge, nothing round it.',
        # The rest, smaller: four with a little scene each, then four in a line or two.
        'rest_h': 'And everything else',
        'rest_say': 'Small things that make a calm day calmer.',
        'ticket_h': 'Notes, checklist and reminder in one task',
        'ticket_say': 'A task opens as a ticket: notes in Markdown, a checklist, tags, a deadline and a '
                      'reminder. Only what you’ve added shows; the rest waits as a pencil mark at its foot.',
        'signals_h': 'Mark how a task stands, not just done',
        'signals_say': 'Hold a task’s circle: in progress, delegated, an appointment, waiting, a '
                       'question… Delegated and waiting fade to pencil, out of your way.',
        'find_h': 'Find anything in a keystroke',
        'find_say': 'Pull Today down on your phone, or press ⌘F on a Mac: lists, projects, tags and '
                    'tasks by their names. One more tap looks in notes and checklists too.',
        'notes_h': 'Notes apart from your tasks',
        'notes_say': 'Thoughts worth keeping get a card of their own, under headings; move one to your '
                     'tasks once it is one. Turn on the diary, and every day leaves a note of what you '
                     'got done.',
        'small_cards': [
            ('repeat', 'repeat', 'Tasks that come back', 'Every day, week or month, after it’s done or '
             'on a schedule. The next one comes as you check this one off.'),
            ('focus', 'tomato', 'A focus timer', 'Wind the knob and work one tomato at a time, a break '
             'between. It runs on the Lock Screen and rings at the end.'),
            ('widgets', 'paperDots', 'Your day at a glance', 'Today, what’s next, the week and the month '
             'on your Home Screen; on the Lock Screen too, with New Task a tap away.'),
            ('gtd', 'knight', 'Getting Things Done, built in', 'Inbox, Today, Upcoming, Anytime and '
             'Someday are the method’s steps. On first launch a little knight shows you how.'),
        ],
        'mac_h': 'On a Mac too, in step through iCloud',
        'mac_say': 'The same lists on iPhone and Mac, kept in step through your own iCloud: no account '
                   'to make. On a Mac the holder stands in a window of its own with a sidebar, every '
                   'list a key away — ⌘1 to ⌘6, ⌘N for a task, ⌘F to find — and with Pro today’s date '
                   'sits in the menu bar, your day a click under it.',
        # Free and Pro, as docs/pro.md has them ("What is Pro's", "Free, and to stay so"), and
        # the prices in the USA.
        'pro_h': 'Free to use. Pro for more.',
        'pro_say': 'No trial clock, no paywall at launch: the free app is a whole to-do list, for good. '
                   'Pro adds the rest, and keeps one person making Taskward.',
        'free_h': 'Free, for good',
        'free': ['Every list, and projects and areas without limit', 'Days and reminders written as you’d say them — “tomorrow at 9”',
                 'Checklists, and notes in Markdown on any task', 'Processing the Inbox, the Logbook, the Trash',
                 'Quick Find', 'Plain repeats', 'Four signals', 'The focus timer',
                 'iCloud sync between iPhone and Mac', 'Lock Screen widgets and New Task',
                 'Light or dark, the inks, the font, the text size'],
        'procol_h': 'Pro',
        'pro': ['Deadlines, and reminders set by hand', 'Tags, and lists filtered by them',
                'Fuller repeats: the 2nd Tuesday, an end, a deadline on each copy',
                'The calendar with your events; a task put in your Calendar', 'Dictating your day',
                'Plans from Claude, on a Mac', 'Notes, and the diary of the day', 'Every signal',
                'Home Screen widgets', 'Your day in a Mac’s menu bar',
                'Every palette, desk and paper; app icons; lists in full screen'],
        'prices': [('Month', '$2.99', 'a month'), ('Year', '$29.99', 'a year'), ('Lifetime', '$69.99', 'once')],
        'price_note': 'Month and Year start with 7 days free. Prices in the US App Store; other '
                      'countries have their own. If Pro ends, what you set stays: deadlines, reminders '
                      'and tags go on working.',
        'support': 'Support', 'privacy': 'Privacy policy', 'by': 'Made by Aleksei Lobanov',
    },
    'ru': {
        'title': 'Taskward: спокойный список дел на бумажных карточках',
        'desc': 'Спокойный список дел для iPhone и Mac. Каждый список — бумажная карточка на '
                'столе: «Сегодня» впереди, остальные в деревянной подставке за ней.',
        'nav': ['Возможности', 'Pro', 'iPhone и Mac', 'Приватность', 'Поддержка'],
        'other': ('English', '../'),
        'h1': 'Весь день —<br>на <u>одной карточке</u>.',
        'lede': ('Спокойный список дел для iPhone и Mac.',
                 'Каждый список — бумажная карточка на твоём столе. Пиши задачу, как говоришь, '
                 'и веди весь день с одной карточки.'),
        'small': 'Без аккаунта · без рекламы · в твоём iCloud',
        'cta': 'Скоро в App Store',
        'upcoming': 'Планы',
        'check': 'Отметить',
        'hints': [
            ('export', 'Входящие', 'white', '#4AA8F0', '#487ba8', 'Всё сюда — разберёшь потом', 'Всё, что пришло в голову. Раз в день разбирай.'),
            ('today', 'Планы', 'cream', '#FF6B5E', '#ab5a57', 'То, у чего есть свой день', 'Задачи с датой ждут здесь и сами придут в «Сегодня» в свой день.'),
            ('list', 'В любое время', 'cream', '#3FB27F', '#428169', 'Следующие шаги', 'Опустело «Сегодня» — возьми отсюда следующее.'),
            ('archive', 'Когда-нибудь', 'kraft', '#FFA23A', '#a85900', 'Мечты и «потом»', 'То, чего хочется, но не сейчас. Загляни раз в неделю.'),
            ('project', 'Проекты', 'white', '#8B6CF0', '#6c5aa8', 'Проекты и области', 'Проект — цель из нескольких шагов, область — часть жизни: работа, дом, здоровье.'),
            ('notebook', 'Заметки', 'white', '#F6C945', '#a68e4a', 'Не задача, просто запись', 'Мысли, которые стоит сохранить, — не среди задач. Станет делом — перенеси.'),
        ],
        'ticket': {
            'title': 'Позвонить кузнецу насчёт щита',
            'notes': 'Старый **треснул** по краю. Спросить, подберёт ли он ::умбон::.',
            'steps': [('Измерить старый', True), ('Найти эскиз', False), ('Узнать цену', False)],
            'tags': ['Оружейная', 'В городе'], 'when': 'Сегодня',
        },
        'signals_note': ('Отметить', 'Выполнить', 'Сигналы…'),
        'signals': ['В работе', 'Поручено', 'Встреча', 'Важно'],
        'float': {'smart': ('Тренировка ', 'завтра в 9'), 'when': 'Завтра', 'progress': 'В работе',
                  'tag': 'Оружейная'},
        'notes': ['остальные списки стоят позади', '«Сегодня» впереди — работай на нём',
                  'срок сегодня — красным', 'тап — и новая задача',
                  'входящие, проекты и заметки — на дубовой подставке'],
        'smart_h': 'Пиши, как говоришь',
        'try_say': 'Напиши задачу с днём, как сказал бы вслух, и нажми ввод. День и напоминание '
                   'поставятся сами, а задача ляжет на свою карточку.',
        'try_ph': 'Тренировка завтра в 9 утра',
        'try_add': 'Положить на карточку',
        'try_examples': ['завтра в 9 утра', 'в пятницу вечером', 'через 3 дня', '12 ноября в 14:30'],
        'try_base': 'Тренировка ',
        'inbox': 'Входящие', 'evening_word': 'Этим вечером', 'when_word': 'Когда',
        'today_word': 'Сегодня', 'tomorrow_word': 'Завтра',
        'try_seed': {'inbox': ['Купить новое перо'], 'today': ['Наточить меч'], 'upcoming': ['Турнир в замке']},
        'find_demo': ('седл', ['Смазать <mark>седл</mark>о', 'Починить <mark>седл</mark>ьные сумки']),
        'day_demo': {
            'title': 'Понедельник, 19 октября',
            'rows': [
                ('event', '07:30', 'Прогулка верхом', '08:30', '1 ч', '#7cc9f2', True),
                ('now', 'сейчас'),
                ('free', '', 'ещё 49 мин свободно'),
                ('event', '10:30', 'Совет в замке', '11:30', '1 ч', '#f5a03c', False),
                ('free', '11:30', 'свободно 2 ч 30 мин'),
                ('crowd', '14:00', [('Тренировка лучников', '#b65ce0'), ('Письма', '#7cc9f2')], '+2'),
                ('free', '15:00', 'свободно 3 ч 30 мин'),
                ('task', '18:30', 'Позвонить кузнецу насчёт щита'),
                ('event', '19:00', 'Ужин с Машей', '21:00', '2 ч', '#3aa0e8', False),
            ],
        },
        'notes_demo': {
            'title': 'Заметки',
            'parts': [
                (None, ['Что сказал кузнец', 'Имена для коня']),
                ('Песни', ['Стихи к пиру', 'Баллада о море']),
                ('Идеи', ['Солнечные часы во двор']),
            ],
            'diary': ('Дневник', 'Воскресенье, 18 октября', ['Смазать петли', 'Ответить Маше', 'Собрать седло']),
            'slip': 'Идеи',
        },
        'cal_empty': 'На этот день ничего',
        'cal_days': [
            (-2, [('09:00', 'Ярмарка', '#3fbf5a')], [('Смазать седло', True)]),
            (0, [('07:30', 'Утренняя прогулка верхом', '#7cc9f2'), ('10:30', 'Совет в замке', '#f5a03c'),
                 ('19:00', 'Ужин с Машей', '#3aa0e8')],
             [('Наточить меч', True), ('Заплатить за жильё', False)]),
            (1, [('13:00', 'Отборочные поединки', '#b65ce0')], [('Позвонить кузнецу насчёт щита', False)]),
            (2, [], [('Спланировать поездку к морю', False)]),
            (4, [('', 'День святого Луки', '#3fbf5a')], []),
            (6, [('18:00', 'Пир после турнира', '#f5a03c'), ('20:00', 'Ночной дозор', '#3aa0e8')], []),
            (9, [], [('Съездить на дальний север', False)]),
        ],
        'shots_alt': 'Taskward на iPhone',
        'mac_alt': 'Taskward на Маке',
        'kept_h': 'Твоё остаётся у тебя',
        'kept': ['Не нужно заводить аккаунт.', 'Ни рекламы, ни слежки. Анонимная статистика, которую можно выключить.',
                 'Задачи живут на твоих устройствах и в твоём iCloud — мы их не видим.'],
        'kept_link': 'Политика конфиденциальности',
        'all_h': 'Что умеет Taskward',
        'all_say': 'Спокойный список дел, в котором больше, чем видно сразу. Нажми, чтобы посмотреть в деле.',
        'tiles': [
            ('speak', 'voice', 'Пиши, как говоришь', '«Тренировка завтра в 9» — или надиктуй весь день голосом {pro}', ''),
            ('claude', 'magic', 'Планы от Claude', 'Попроси план — он ляжет в списки проектами и задачами.', 'Pro · Mac'),
            ('day', 'time', 'День по часам', 'События и задачи на одних часах и месяц на карточке.', 'Pro'),
            ('paper', 'cardFile', 'Списки на бумаге', '«Сегодня» впереди, остальные в дубовой подставке. Много тем {pro}', ''),
            ('ticket', 'note', 'Всё в одной задаче', 'Заметки в Markdown, чек-лист; срок и напоминание {pro}', ''),
            ('signals', '', 'Не только «сделано»', 'В работе, поручено, жду ответа: отметь, как идёт дело. Все сигналы {pro}', ''),
            ('repeat', 'repeat', 'Повторы', 'Каждую неделю или во второй вторник {pro}: следующая придёт сама.', ''),
            ('find', 'search', 'Быстрый поиск', 'Потяни «Сегодня» вниз или ⌘F: списки, проекты, теги, задачи.', ''),
            ('notes', 'notebook', 'Заметки и дневник', 'Заметки отдельно от задач и дневник, который пишется сам.', 'Pro'),
            ('focus', 'tomato', 'Таймер фокуса', 'Помидор за помидором для одной задачи, и на экране блокировки.', ''),
            ('mac', 'backup', 'iPhone и Mac заодно', 'Твой iCloud, без аккаунта. На Маке — день в строке меню {pro}', ''),
            ('widgets', 'paperDots', 'Виджеты', '«Сегодня», ближайшее дело и месяц на экране блокировки и на «Домой» {pro}', ''),
        ],
        'voice_h': 'Или надиктуй весь день',
        'voice_say': 'Нажми микрофон рядом с плюсом в «Сегодня» и просто говори: «позвонить в банк в '
                     'десять, вечером спортзал, в пятницу подарок Ане». Вернутся отдельные задачи со '
                     'своими днями и временем, а те, где время не прозвучало, встанут в окна между '
                     'событиями. Проверь список — и добавь.',
        'voice_note': 'Диктовка входит в Pro, на iPhone и Mac.',
        'claude_h': 'Планы от Claude — прямо в твоих списках',
        'claude_say': 'Расскажи Claude, что задумал. Он посмотрит твои области и проекты и запишет '
                      'план: проект с заголовками, задачи с днями, сроками и чек-листами. Или попроси '
                      'разобрать входящие. Что бы он ни сделал, одно «Отменить» вернёт всё как было.',
        'claude_note': 'На Маке с Pro, а через миг и на iPhone — через iCloud.',
        'claude_link': 'Как подключить Claude',
        'day_h': 'День по часам',
        'day_say': 'Переключи календарь на «День»: события и задачи со временем разложатся по часам, '
                   'пересекающиеся — рядом. Свободное время между ними занимает одну строку и говорит, '
                   'сколько его на самом деле, так что весь день помещается на экран. В месяце под '
                   'каждым днём точки за события и задачи — нажми на день, чтобы его увидеть.',
        'day_note': 'Календари читаются на устройстве и никуда не копируются. Календарь входит в Pro.',
        'paper_h': 'Каждый список — бумажная карточка на столе',
        'paper_say': '«Сегодня» лежит впереди, и работаешь прямо на нём; «Планы», «В любое время» и '
                     '«Когда-нибудь» стоят за ним в дубовой подставке. Вытяни любую — и она ляжет на '
                     'стол. У каждого списка своя бумага и подсказка, зачем он, так что всегда видно, где ты.',
        'yours_h': 'Сделай своим',
        'yours_say': 'Светлая или тёмная тема и палитра для каждой, стол под карточками, цвет чернил, '
                     'как зачёркивается сделанное, гладкая или фактурная бумага. Или открой список во '
                     'весь экран, без ничего вокруг.',
        'rest_h': 'И всё остальное',
        'rest_say': 'Мелочи, от которых спокойный день становится ещё спокойнее.',
        'ticket_h': 'Заметки, чек-лист и напоминание в одной задаче',
        'ticket_say': 'Задача открывается билетом: заметки в Markdown, чек-лист, теги, срок и '
                      'напоминание. Видно только то, что добавил; остальное ждёт карандашной меткой внизу.',
        'signals_h': 'Отмечай, как идёт дело, а не только «сделано»',
        'signals_say': 'Зажми кружок задачи: в работе, поручено, встреча, жду ответа, вопрос… '
                       'Поручённое и ожидание уходят в карандаш, чтобы не мешать.',
        'find_h': 'Найти что угодно за секунду',
        'find_say': 'Потяни «Сегодня» вниз на телефоне или нажми ⌘F на Маке: списки, проекты, теги и '
                    'задачи по названию. Ещё одно касание — и поиск заглянет в заметки и чек-листы.',
        'notes_h': 'Заметки отдельно от задач',
        'notes_say': 'Мысли, которые стоит сохранить, живут на своей карточке, по разделам; станет '
                     'делом — перенеси в задачи. Включи дневник, и каждый день оставит заметку о том, '
                     'что ты успел.',
        'small_cards': [
            ('repeat', 'repeat', 'Задачи, которые возвращаются', 'Каждый день, неделю или месяц — после '
             'выполнения или по расписанию. Следующая появится, как только отметишь эту.'),
            ('focus', 'tomato', 'Таймер фокуса', 'Поверни ручку и работай помидор за помидором, с '
             'перерывами. Таймер идёт и на экране блокировки и звенит в конце.'),
            ('widgets', 'paperDots', 'День одним взглядом', '«Сегодня», ближайшее дело, неделя и месяц на '
             'экране «Домой»; и на экране блокировки — с новой задачей в одно касание.'),
            ('gtd', 'knight', 'GTD внутри', 'Входящие, «Сегодня», «Планы», «В любое время» и '
             '«Когда-нибудь» — шаги метода. При первом запуске маленький рыцарь покажет, как ими пользоваться.'),
        ],
        'mac_h': 'И на Маке — синхронно через iCloud',
        'mac_say': 'Одни и те же списки на iPhone и Mac, синхронно через твой собственный iCloud: '
                   'аккаунт заводить не нужно. На Маке подставка стоит в своём окне с боковой панелью, '
                   'любой список — на клавише: ⌘1–⌘6, ⌘N для задачи, ⌘F для поиска. А с Pro '
                   'сегодняшняя дата живёт в строке меню, и весь день — в клике под ней.',
        'pro_h': 'Бесплатно — насовсем. Pro — для большего.',
        'pro_say': 'Без счётчика пробных дней и без стены оплаты при запуске: бесплатное приложение — '
                   'полноценный список дел, навсегда. Pro добавляет остальное и помогает одному '
                   'человеку делать Taskward дальше.',
        'free_h': 'Бесплатно, навсегда',
        'free': ['Все списки, проекты и области без ограничений', 'Дни и напоминания словами — «завтра в 9»',
                 'Чек-листы и заметки в Markdown в любой задаче', 'Разбор входящих, журнал и корзина',
                 'Быстрый поиск', 'Простые повторы', 'Четыре сигнала', 'Таймер фокуса',
                 'Синхронизация iPhone и Mac через iCloud', 'Виджеты экрана блокировки и «Новая задача»',
                 'Светлая или тёмная тема, чернила, шрифт, размер текста'],
        'procol_h': 'Pro',
        'pro': ['Сроки и напоминания, поставленные вручную', 'Теги и списки, отфильтрованные по ним',
                'Сложные повторы: второй вторник, конец, срок у каждой копии',
                'Календарь с твоими событиями; задача — в Календарь', 'Диктовка дня',
                'Планы от Claude, на Маке', 'Заметки и дневник дня', 'Все сигналы',
                'Виджеты экрана «Домой»', 'День в строке меню Мака',
                'Все палитры, столы и бумага; иконки приложения; списки во весь экран'],
        'prices': [('Месяц', '$2.99', 'в месяц'), ('Год', '$29.99', 'в год'), ('Навсегда', '$69.99', 'один раз')],
        'price_note': 'Месяц и год начинаются с 7 бесплатных дней. Цены американского App Store, в '
                      'других странах свои. Если Pro закончится, всё, что ты поставил, останется: '
                      'сроки, напоминания и теги продолжат работать.',
        'support': 'Поддержка', 'privacy': 'Политика конфиденциальности',
        'by': 'Сделал Алексей Лобанов',
    },
}


def icon(name, cls='icon'):
    return f'<svg class="{cls}" aria-hidden="true"><use href="{{base}}img/icons.svg#{name}"/></svg>'


SIGNAL = '<svg viewBox="0 0 24 24"><circle class="ring" cx="12" cy="12" r="9.2"/><circle class="fill" cx="12" cy="12" r="9.2"/></svg>'

def knight_sticker():
    """The app's knight as a sticker on the desk: his paths from the icons' sprite, laid
    three times — thick in white for the sticker's edge and the shield filled white under
    it, then in the icon's navy over them."""
    import re
    sprite = (SITE / 'img/icons.svg').read_text()
    start = sprite.index('<symbol id="knight"')
    body = sprite[sprite.index('>', start) + 1:sprite.index('</symbol>', start)]
    tags = re.findall(r'<path [^>]*/>', body)
    lines = [re.search(r'd="([^"]+)"', p).group(1) for p in tags if 'fill="#000"' not in p]
    eyes = [re.search(r'd="([^"]+)"', p).group(1) for p in tags if 'fill="#000"' in p]
    edge = ''.join(f'<path d="{d}"/>' for d in lines)
    ink = ''.join(f'<path d="{d}"/>' for d in lines) + ''.join(f'<path class="eye" d="{d}"/>' for d in eyes)
    return (f'<svg class="sticker" viewBox="-3 -3 46 46" aria-hidden="true">'
            f'<g class="edge">{edge}<path class="body" d="{lines[0]}"/></g>'
            f'<path class="shield" d="{lines[0]}"/><g class="ink">{ink}</g></svg>')


# Where the notes round the phone point, in hundredths of the phone: the stack of cards
# behind Today, Today's head, the rent due today, the plus, the oak's Inbox.
NOTES = [('l', 11.4, 19.5, 4), ('r', 92.5, 31.3, -7), ('l', 9.0, 52.9, -3), ('r', 89.6, 83.6, -6),
         ('l', 11.0, 92.0, -2)]
# A stroke of the pen under a word, a little uphill, its end flicked back.
UNDER = ('<svg viewBox="0 0 300 24" preserveAspectRatio="none" aria-hidden="true">'
         '<path d="M4 17 C 70 11, 170 9, 292 8 C 230 12, 170 15, 120 19"/></svg>')
# A hand-drawn arrow, its head at the right middle; a note on the right turns it round.
ARROW = ('<svg class="arrow" viewBox="0 0 64 40" aria-hidden="true">'
         '<path d="M3 31 C 17 36, 41 33, 61 20"/><path d="M51 17.5 L 61.5 19.8 L 55.5 28.5"/></svg>')
# The signals' marks as the app draws them (lib/widgets/pen_signal.dart): in its 24, the
# ring of 8.6 the first stroke, the mark in it; the asterisk stands alone.
RING = '<circle class="ring" cx="12" cy="12" r="8.6"/>'
SIG = {
    'done': RING + '<circle class="solid" cx="12" cy="12" r="8.6"/>',
    'progress': RING + '<path class="solid" d="M12 3.4a8.6 8.6 0 0 0 0 17.2z"/>',
    'delegated': RING + '<path class="line" d="M12 3.4v17.2M3.4 12h17.2M15.2 7.2l5.4 4.8-5.4 4.8"/>',
    'appointment': RING + '<path class="line" d="M12 3.4v17.2M3.4 12h17.2"/>',
    'important': '<path class="line" stroke-width="2.2" d="M12 4v16M18.93 8 5.07 16M18.93 16 5.07 8"/>',
    'pending': RING + '<path class="line" d="M8.6 7.4h6.8M8.6 7.4l6.8 9.2M15.4 7.4l-6.8 9.2M8.6 16.6h6.8"/>',
}


def sig(name):
    return f'<svg class="sig" viewBox="0 0 24 24" aria-hidden="true">{SIG[name]}</svg>'


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
<script src="{base}when.js?v={VERSION}" defer></script>
<script src="{base}app.js?v={VERSION}" defer></script>
</head>
'''


def bar(t, base, lang, home):
    other, href = t['other']
    anchors = ['#all', '#pro', '#mac']
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
<a href="{base}{pre}assistants/">{'Ассистенты' if lang == 'ru' else 'Assistants'}</a>
<a href="{base}{pre}privacy/">{t['privacy']}</a>
<a href="{href}">{other}</a>
<span class="by">{t['by']}</span>
</div></footer>'''


APPLE = ('<svg class="icon" viewBox="0 0 17 20" aria-hidden="true"><path fill="currentColor" d="M14.07 10.63c-.02-2.33 1.9-3.45 1.99-3.51-1.08-1.58-2.77-1.8-3.37-1.82-1.43-.15-2.8.84-3.53.84-.73 0-1.85-.82-3.05-.8-1.57.03-3.02.92-3.83 2.33-1.63 2.83-.42 7.02 1.17 9.32.78 1.12 1.71 2.38 2.93 2.34 1.18-.05 1.62-.76 3.05-.76 1.42 0 1.82.76 3.06.74 1.27-.03 2.07-1.14 2.84-2.27.9-1.31 1.27-2.58 1.29-2.64-.03-.01-2.47-.95-2.49-3.77zM11.77 3.79c.65-.79 1.09-1.88.97-2.97-.94.04-2.07.62-2.74 1.41-.6.7-1.13 1.81-.99 2.88 1.05.08 2.11-.53 2.76-1.32z"/></svg>')


def vphone(lang, clip):
    """A short film of the app, looping in a phone as the hero's is held: the store's frame, its
    screen masked. Till the film and its poster are there, the screen shows the paper."""
    return (f'<div class="vphone" aria-hidden="true"><div class="phone"><div class="screen">'
            f'<video autoplay muted loop playsinline preload="metadata" poster="{{base}}img/{lang}-v-{clip}.webp">'
            f'<source src="{{base}}img/{lang}-v-{clip}.mp4" type="video/mp4"></video></div>'
            f'<div class="glass"></div></div></div>')


def landing(lang):
    t = T[lang]
    base = '' if lang == 'en' else '../'
    home = './'
    pre = 'ru/' if lang == 'ru' else ''
    # Every list's card on its own paper, with the hint the app lays under its head.
    lists = ''.join(
        f'<div class="paper {paper} lcard" style="--r:{r}deg;--marker:{marker};--pen:{pen}">'
        f'<div class="head">{icon(mark)}{name}</div>'
        f'<div class="hint"><b>{title}</b><span>{text}</span></div></div>'
        for (mark, name, paper, marker, pen, title, text), r
        in zip(t['hints'], [-1.4, 0.9, -0.6, 1.2, -1.0, 0.7])
    )
    tk = t['ticket']
    mk = lambda m: f'<span class="mk">{m}</span>'
    ticket_notes = re.sub(r'::(.+?)::', lambda m: mk('::') + f'<mark>{m[1]}</mark>' + mk('::'),
                          re.sub(r'\*\*(.+?)\*\*', lambda m: mk('**') + f'<b>{m[1]}</b>' + mk('**'), tk['notes']))
    steps = ''.join(
        f'<li class="{"done" if done else ""}"><button class="box" type="button" aria-pressed="{"true" if done else "false"}" aria-label="{t["check"]}: {s}"></button>{s}</li>' for s, done in tk['steps']
    )
    signals = ''.join(
        f'<li>{sig(mark)}{name}</li>'
        for mark, name in zip(['progress', 'delegated', 'appointment', 'important'], t['signals'])
    )
    iphones = ''.join(
        f'<img src="{base}img/{lang}-iphone-{i}.webp" alt="{t["shots_alt"]}" width="760" height="1651" loading="lazy">'
        for i in range(1, 9)
    )
    kept = ''.join(f'<li>{line}</li>' for line in t['kept'])
    ring = '<span class="o"></span>'
    find_word, found = t['find_demo']
    find = (f'<div class="demo find"><div class="field">{icon("search")}{find_word}<span class="caret"></span></div>'
            + ''.join(f'<p>{ring}<span>{x}</span></p>' for x in found) + '</div>')
    cal = json.dumps({'days': t['cal_days'], 'empty': t['cal_empty']},
                     ensure_ascii=False).replace('"', '&quot;')
    try_words = json.dumps({
        'base': t['try_base'], 'evening': t['evening_word'], 'when': t['when_word'],
        'today': t['today_word'], 'tomorrow': t['tomorrow_word'], 'seed': t['try_seed'],
        'icons': {k: icon(v).replace('{base}', base) for k, v in
                  {'today': 'today', 'moon': 'darkThemeFilled', 'bell': 'reminderFilled', 'star': 'favoriteFilled', 'inbox': 'export'}.items()},
    }, ensure_ascii=False).replace('"', '&quot;')
    examples = ''.join(f'<button type="button" class="example">{e}</button>' for e in t['try_examples'])
    notes = ''.join(
        f'<p class="pen-note {side}" style="--x:{x}%;--y:{y}%;--r:{r}deg">{ARROW}<span>{words}</span></p>'
        for words, (side, x, y, r) in zip(t['notes'], NOTES)
    )
    # Everything it does: a tile each, its mark, its name and a line, Pro's marked so.
    # {pro} in a line: a mark after the word before it, never put on a line of its own.
    def pro_in(say):
        return re.sub(r'(\S+) \{pro\}', r'<em class=keep>\1 <i class=pro>Pro</i></em>', say)

    tiles = ''.join(
        f'<li><a class="tile" href="#{anchor}">{icon(mark) if mark else sig("progress")}'
        f'<b>{name}{f" <i class=pro>{pro}</i>" if pro else ""}</b>'
        f'<span>{pro_in(say)}</span></a></li>'
        for anchor, mark, name, say, pro in t['tiles']
    )
    smalls = ''.join(
        f'<div class="small-card" id="{anchor}">{icon(mark)}<h3>{name}</h3><p>{say}</p></div>'
        for anchor, mark, name, say in t['small_cards']
    )
    free = ''.join(f'<li>{icon("check")}<span>{x}</span></li>' for x in t['free'])
    pro = ''.join(f'<li>{icon("check")}<span>{x}</span></li>' for x in t['pro'])
    prices = ''.join(f'<li><span>{name}</span><b>{price}</b><i>{per}</i></li>' for name, price, per in t['prices'])
    dd = t['day_demo']

    def plan_row(r):
        kind = r[0]
        if kind == 'event':
            _, at, title, till, length, colour, over = r
            return (f'<div class="dp-row"><span class="t">{at}</span><div class="blk{" over" if over else ""}" '
                    f'style="--c:{colour}"><b>{title}</b><i>{at}–{till} · {length}</i></div></div>')
        if kind == 'now':
            return f'<div class="dp-now"><span class="t">{r[1]}</span><span class="line"></span></div>'
        if kind == 'free':
            return f'<div class="dp-free"><span class="t">{r[1]}</span><span class="dots"></span><span>{r[2]}</span></div>'
        if kind == 'task':
            return (f'<div class="dp-row"><span class="t">{r[1]}</span><div class="blk task">'
                    f'<span class="o"></span><b>{r[2]}</b></div></div>')
        _, at, pair, more = r
        return (f'<div class="dp-row"><span class="t">{at}</span><div class="crowd">'
                + ''.join(f'<div class="blk" style="--c:{c}"><b>{x}</b></div>' for x, c in pair)
                + f'<div class="blk more">{more}</div></div></div>')
    dayplan = ''.join(plan_row(r) for r in dd['rows'])
    nd = t['notes_demo']
    note_parts = ''.join(
        (f'<p class="tapehead">{h}</p>' if h else '')
        + ''.join(f'<p class="n"><span class="dash"></span>{x}</p>' for x in notes_list)
        for h, notes_list in nd['parts']
    )
    dh, dtitle, ddone = nd['diary']
    diary = (f'<p class="tapehead">{dh}</p><div class="n diary"><span class="dash"></span><div>'
             f'<b>{dtitle}</b>' + ''.join(f'<span>☑ {x}</span>' for x in ddone) + '</div></div>')
    # A dash for each heading on the card, the one on the slip in ink.
    heads = [h for h, _ in nd['parts'] if h] + [dh]
    outline = ''.join(f'<span class="{"lit" if h == nd["slip"] else ""}"></span>' for h in heads)
    # Claude's plan, as the Assistants page shows it: asked for, and landed on a card.
    a = A[lang]
    c = a['card']
    plan = (f'<div class="paper grey ask"><span class="chev">›</span>{a["prompt"]}</div>{ARROW}'
            f'<div class="paper plan-card"><div class="plan-head">{icon("project")}<span>{c["project"]}</span>'
            f'<span class="due">{icon("flagFilled")}{c["due"]}</span></div>'
            f'<ul class="rows">{"".join(_plan_row(*r) for r in c["loose"])}</ul>'
            + ''.join(f'<h4 class="plan-heading">{h}</h4><ul class="rows">{"".join(_plan_row(*r) for r in rows)}</ul>'
                      for h, rows in c['headings'])
            + f'<p class="from">{icon("knight")}{c["from"]}</p></div>')
    page = head(lang, t['title'], t['desc'], '', base) + f'''<body>
{bar(t, base, lang, home)}
<main>
<section class="hero"><div class="wrap hero-in">
<div class="hero-words">
<img class="hero-icon" src="{base}img/icon.png" alt="Taskward" width="112" height="112">
<h1 class="written">{''.join(f'<span class="pen" style="--i:{i}">{line}</span>' for i, line in enumerate(t['h1'].split('<br>'))).replace('<u>', '<span class="under">').replace('</u>', UNDER + '</span>')}</h1>
<p class="lede"><b>{t['lede'][0]}</b> {t['lede'][1]}</p>
<span class="button soon">{APPLE}{t['cta']}</span>
<p class="small">{t['small']}</p>
</div>
<div class="scene" aria-hidden="true">
<div class="rig">
<div class="phone"><div class="screen"><img src="{base}img/{lang}-home.webp" alt="" width="786" height="1708" fetchpriority="high">
<div class="bar"><b>9:41</b><svg viewBox="0 0 52 12"><g fill="#f4f1e8"><rect x="0" y="8" width="3" height="4" rx="1"/><rect x="4.5" y="6" width="3" height="6" rx="1"/><rect x="9" y="3.5" width="3" height="8.5" rx="1"/><rect x="13.5" y="1" width="3" height="11" rx="1"/><rect x="36.5" y="1.5" width="13" height="9" rx="2.5" fill="none" stroke="#f4f1e8" stroke-opacity=".5"/><rect x="38" y="3" width="10" height="6" rx="1.3"/></g></svg></div></div>
<div class="glass"></div></div>
<div class="pen-notes">{notes}</div>
</div>
<div class="float paper chip smart" style="--r:-4deg;top:35%;left:-5%"><span class="ring"></span>{t['float']['smart'][0]}<mark>{t['float']['smart'][1]}</mark></div>
<div class="float paper chip when" style="--r:3deg;top:51%;right:-5%;animation-delay:-2s">{icon('today')}{t['float']['when']}{icon('reminderFilled')}09:00</div>
<div class="float paper chip progress" style="--r:2deg;top:69%;left:-3%;animation-delay:-4s"><svg viewBox="0 0 30 30" class="sig"><circle class="ring" cx="15" cy="15" r="11"/><path class="solid" d="M15 4a11 11 0 0 0 0 22z"/></svg>{t['float']['progress']}</div>
<div class="float tag" style="--r:-6deg;top:3%;left:8%;animation-delay:-3s">{t['float']['tag']}</div>
<span class="float doodle star" style="--r:12deg;top:2%;right:9%;animation-delay:-1s">{icon('favoriteFilled')}</span>
<span class="float doodle flag" style="--r:-10deg;top:66%;right:4%;animation-delay:-5s">{icon('flagFilled')}</span>
<span class="knight">{knight_sticker()}</span>
</div>
</div></section>

<section class="part" id="all"><div class="wrap">
<h2 class="part-h">{t['all_h']}</h2><p class="part-say">{t['all_say']}</p>
<ul class="tiles">{tiles}</ul>
</div></section>

<section class="part features"><div class="wrap">

<article class="feature hl" id="speak">
<div class="say"><h2>{t['smart_h']}</h2><p>{t['try_say']}</p>
<h3>{t['voice_h']}</h3><p>{t['voice_say']}</p><p class="aside">{t['voice_note']}</p></div>
{vphone(lang, 'speak')}
<div class="hl-demo">
<div class="try" data-lang="{lang}" data-words="{try_words}">
<form class="paper newcard" autocomplete="off">
<label class="field"><span class="ring" aria-hidden="true"></span>
<span class="line"><span class="mirror" aria-hidden="true"></span>
<input class="title" type="text" maxlength="70" enterkeyhint="done" aria-label="{t['try_ph']}" placeholder="{t['try_ph']}"></span></label>
<div class="foot"><span class="chip"></span><button class="put" type="submit">{t['try_add']}</button></div>
</form>
<div class="examples">{examples}</div>
<div class="desk3">
<div class="paper mini" data-list="inbox"><div class="head">{icon('export')}{t['inbox']}</div><ul class="rows"></ul></div>
<div class="paper mini" data-list="today"><div class="head"><svg class="icon" style="color:var(--seal)" aria-hidden="true"><use href="{base}img/icons.svg#favoriteFilled"/></svg>{t['today_word']}</div><ul class="rows"></ul></div>
<div class="paper cream mini" data-list="upcoming"><div class="head">{icon('today')}{t['upcoming']}</div><ul class="rows"></ul></div>
</div>
</div>
</div>
</article>

<article class="feature hl flip" id="claude">
<div class="say"><h2>{t['claude_h']}</h2><p>{t['claude_say']}</p>
<p class="aside">{t['claude_note']}</p>
<p class="more-link"><a href="{base}{pre}assistants/">{t['claude_link']} →</a></p></div>
{vphone(lang, 'claude')}
<div class="hl-demo plan">{plan}</div>
</article>

<article class="feature hl" id="day">
<div class="say"><h2>{t['day_h']}</h2><p>{t['day_say']}</p><p class="aside">{t['day_note']}</p></div>
{vphone(lang, 'day')}
<div class="hl-demo cal2">
<div class="paper dayplan"><h4 data-today>{dd['title']}</h4>{dayplan}</div>
<div class="paper month" data-lang="{lang}" data-cal="{cal}">
<div class="month-head"><b></b><span></span></div>
<div class="days" role="grid"></div>
<div class="tear" aria-hidden="true"></div>
<div class="day" aria-live="polite"><h4></h4><ul></ul></div>
</div>
</div>
</article>

<article class="feature hl flip" id="paper">
<div class="say"><h2>{t['paper_h']}</h2><p>{t['paper_say']}</p>
<h3>{t['yours_h']}</h3><p>{t['yours_say']}</p></div>
{vphone(lang, 'paper')}
<div class="hl-demo"><div class="deck">{lists}</div></div>
</article>

</div></section>

<section class="part" id="real"><div class="wrap">
<div class="shelf">{iphones}</div>
</div></section>

<section class="part rest"><div class="wrap">
<h2 class="part-h">{t['rest_h']}</h2><p class="part-say">{t['rest_say']}</p>
<div class="grid2">

<article class="card2" id="ticket">
<h3>{t['ticket_h']}</h3><p>{t['ticket_say']}</p>
<div class="ticket-wrap"><div class="paper ticket">
<h4 class="row"><button class="signal" type="button" aria-pressed="false" aria-label="{t['check']}: {tk['title']}">{SIGNAL}</button><span class="title">{tk['title']}</span></h4>
<p class="notes">{ticket_notes}</p>
<ul class="steps">{steps}</ul>
<div class="stub">
<div class="tags">{''.join(f'<span>{x}</span>' for x in tk['tags'])}</div>
<div class="when"><span class="star">{icon('favoriteFilled')}</span>{tk['when']}{icon('reminderFilled')}21:30<span class="marks">{icon('flagFilled')}</span></div>
</div>
</div></div>
</article>

<article class="card2" id="notes">
<h3>{t['notes_h']}</h3><p>{t['notes_say']}</p>
<div class="paper notesdemo"><div class="head">{icon('notebook')}{nd['title']}</div>
{note_parts}{diary}
<div class="outline" aria-hidden="true">{outline}<span class="slip">{nd['slip']}</span></div>
</div>
</article>

<article class="card2" id="find">
<h3>{t['find_h']}</h3><p>{t['find_say']}</p>
<div class="paper cream small">{find}</div>
</article>

<article class="card2" id="signals">
<h3>{t['signals_h']}</h3><p>{t['signals_say']}</p>
<div class="taped"><span class="tape"></span><p class="note-title">{t['signals_note'][0]}</p>
<p class="complete">{sig('done')}{t['signals_note'][1]}</p><ul class="sigs">{signals}</ul><p class="more">{t['signals_note'][2]}</p></div>
</article>

</div>
<div class="smalls">{smalls}</div>
</div></section>

<section class="part features"><div class="wrap">
<article class="feature" id="mac">
<div class="say"><h2>{t['mac_h']}</h2><p>{t['mac_say']}</p></div>
<div class="show"><div class="macs">
<img src="{base}img/{lang}-mac-5.webp" alt="" width="2240" height="1400" loading="lazy">
<img src="{base}img/{lang}-mac-2.webp" alt="" width="2240" height="1400" loading="lazy">
<img src="{base}img/{lang}-mac-1.webp" alt="{t['mac_alt']}" width="2240" height="1400" loading="lazy">
</div></div>
</article>
</div></section>

<section class="part" id="pro"><div class="wrap">
<h2 class="part-h">{t['pro_h']}</h2><p class="part-say">{t['pro_say']}</p>
<div class="plans">
<div class="plan free"><h3>{t['free_h']}</h3><ul>{free}</ul></div>
<div class="paper plan pro"><h3>{icon('pro')}{t['procol_h']}</h3><ul>{pro}</ul>
<ul class="prices">{prices}</ul><p class="price-note">{t['price_note']}</p></div>
</div>
</div></section>

<section class="part"><div class="wrap">
<div class="closing">
<div class="paper kept">
<h3>{icon('lock')}{t['kept_h']}</h3><ul>{kept}</ul><p><a href="{base}{pre}privacy/">{t['kept_link']}</a></p>
</div>
<div class="closing-cta">{icon('knight', 'icon big')}<span class="button soon">{APPLE}{t['cta']}</span><p class="small">{t['small']}</p></div>
</div>
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
<p>Nothing of what you write. Taskward has no account, no ads and no tracking. Two things leave
your device for someone other than Apple: what is needed to sell Taskward Pro, and usage statistics
and crash reports, which you can turn off. Both are described below, and its App Store privacy label
says the same.</p>
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
<p>You can also make calendar events in Taskward: a new one from the plus, or a task put in your
Calendar. On an iPhone this opens the system’s own event editor, which runs apart from Taskward:
the event is saved only if you save it there, and Taskward is given no access to your calendars
for it. On a Mac, Taskward asks for access to your calendars, saves the event to your default
calendar and opens it in the Calendar; Undo takes it out again. An event made so is kept by your
calendar like any other and synced by that calendar’s own account, such as iCloud. Taskward keeps
no copy of it and sends it nowhere.</p>
<h2>Purchases</h2>
<p>Taskward Pro is sold through the App Store. Apple handles the payment: we never see your card,
your name or your Apple Account.</p>
<p>To know whether Pro is yours and to give it back on a new device, Taskward uses
<a href="https://www.revenuecat.com/privacy/">RevenueCat</a>. Each time it starts, the app asks
RevenueCat what you hold, under a random identifier made for the installation, not for you, so this
happens whether or not you ever buy anything. If you buy, RevenueCat receives the receipt from
Apple: which plan, when, at what price, in which country, and whether it renews. No task or
anything else you wrote is ever sent. As with any service on the internet, its servers see the
network address a request comes from. RevenueCat handles this on our behalf, and it is needed for
Pro to work, so it cannot be turned off.</p>
<h2>Usage statistics and crash reports</h2>
<p>To see what is used and what breaks, Taskward sends usage statistics to
<a href="https://mixpanel.com/legal/privacy-policy/">Mixpanel</a> and crash reports to
<a href="https://firebase.google.com/support/privacy">Google Firebase Crashlytics</a>. This is on
unless you turn it off: Settings, Help improve Taskward. After that nothing more is sent.</p>
<p>Usage statistics say what was done, for example that a task was added or a list opened, a
purchase and its plan and price, and how the app is set up: its look, its language, the plan held.
With them go the app’s version, your device’s model and system, and the country of your App Store
account. Crash reports say what kind of error it was, where in the app, and on what device and
system. Both come under a random identifier made for the installation, not for you. No task, note,
tag, project name or search is ever sent.</p>
<p>The country and city may be worked out from the network address a request comes from. We ask
for this not to happen, but it can, for example when something sent before the app last closed goes
out as it starts. Your exact location is never collected.</p>
<h2>Where the data goes</h2>
<p>RevenueCat is a company in the United States, so purchase records may be processed there. It
works under the European Commission’s standard contractual clauses, which bind it to protect them
as they would be protected in the EU. Purchase records are needed to give you the Pro you paid
for, so they are processed to perform that purchase.</p>
<p>Usage statistics are kept by Mixpanel in the European Union. Crash reports are processed by
Google, in the United States among other places, under the same clauses. Both are processed for
our legitimate interest in keeping the app working and knowing what to improve, and you can object
at any time with the switch in Settings.</p>
<p>If you have chosen to share analytics with Apple, Apple may also send us anonymous crash reports
for the app. They contain no tasks or other things you have written.</p>
<h2>Deleting your data</h2>
<p>Delete a task, a list or everything in the app and it is gone from your device and your
iCloud. Deleting the app removes what it kept on the device. To remove what it kept in iCloud,
open Settings, tap your name, then iCloud, Manage Storage, Taskward, and delete its data.</p>
<h2>Your rights</h2>
<p>Depending on where you live, including under the EU and UK GDPR, you have the right to ask what
data about you is held, to have it corrected or deleted, to restrict or object to its use, and to
receive a copy of it. Write to the address below. As purchase records carry no name or email, we
may not be able to tell which of them is yours. The same goes for statistics and crash reports,
which carry only the installation’s random identifier. A subscription is stopped in your Apple Account’s
settings.</p>
<h2>Children</h2>
<p>Taskward is not directed at children. It collects nothing that identifies anyone, children
included.</p>
<h2>Changes</h2>
<p>If this policy changes, the new one is published here with its date.</p>
<h2>Contact</h2>
<p>Questions: <a href="mailto:{mail}">{mail}</a>.</p>
'''),
    'ru': ('Политика конфиденциальности', '''
<p>Taskward — список дел для iPhone и Mac, его сделал Алексей Лобанов. Здесь написано, что
происходит с тем, что вы в нём пишете. Коротко: ничего из этого к нам не попадает.</p>
<h2>Что мы собираем</h2>
<p>Ничего из того, что вы пишете. В Taskward нет аккаунта, рекламы и слежки. С устройства кому-то,
кроме Apple, уходят две вещи: то, что нужно для продажи Taskward Pro, и статистика использования с
отчётами о сбоях, которые можно выключить. Обе описаны ниже, метка приватности в App Store говорит
то же самое.</p>
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
<p>В Taskward можно и создавать события календаря: новое с плюса или из задачи, отправленной в
Календарь. На iPhone для этого открывается системный редактор событий, который работает отдельно
от Taskward: событие сохраняется, только если вы сохраните его там, и доступа к календарям Taskward
для этого не получает. На Mac Taskward просит доступ к календарям, сохраняет событие в календарь
по умолчанию и открывает его в Календаре; «Отменить» его удаляет. Созданное так событие хранится в
вашем календаре, как любое другое, и синхронизируется его собственной учётной записью, например
iCloud. Taskward не хранит его копию и никуда его не отправляет.</p>
<h2>Покупки</h2>
<p>Taskward Pro продаётся через App Store. Оплатой занимается Apple: мы не видим ни вашу карту, ни
имя, ни аккаунт Apple.</p>
<p>Чтобы знать, есть ли у вас Pro, и вернуть его на новом устройстве, Taskward использует
<a href="https://www.revenuecat.com/privacy/">RevenueCat</a>. При каждом запуске приложение спрашивает
у RevenueCat, что у вас куплено, под случайным идентификатором, созданным для установки, а не для
вас, поэтому это происходит, даже если вы ничего не покупаете. Если вы покупаете, RevenueCat получает
чек от Apple: какой тариф, когда, по какой цене, в какой стране и продлевается ли он. Задачи и всё,
что вы написали, никогда не отправляются. Как и любой сервис в интернете, его серверы видят сетевой
адрес, с которого пришёл запрос. RevenueCat обрабатывает это по нашему поручению; без этого Pro не
работает, поэтому отключить это нельзя.</p>
<h2>Статистика и отчёты о сбоях</h2>
<p>Чтобы видеть, чем пользуются и что ломается, Taskward отправляет статистику использования в
<a href="https://mixpanel.com/legal/privacy-policy/">Mixpanel</a> и отчёты о сбоях в
<a href="https://firebase.google.com/support/privacy">Google Firebase Crashlytics</a>. Это включено,
пока вы не выключите: Настройки, «Помогать улучшать Taskward». После этого больше ничего не
отправляется.</p>
<p>В статистике указано, что было сделано, например что добавлена задача или открыт список, покупка,
её план и цена, и как настроено приложение: оформление, язык, купленный план. Вместе с этим уходят
версия приложения, модель устройства и система, а также страна вашего аккаунта App Store. В отчёте о
сбое указано, что это за ошибка, в каком месте приложения и на каком устройстве и системе. И то и
другое идёт под случайным идентификатором, созданным для установки, а не для вас. Задачи, заметки,
теги, названия проектов и поисковые запросы не отправляются никогда.</p>
<p>Страна и город могут определяться по сетевому адресу, с которого пришёл запрос. Мы просим этого
не делать, но так может случиться, например когда то, что не успело уйти до закрытия приложения,
отправляется при следующем запуске. Точное местоположение не собирается.</p>
<h2>Куда попадают данные</h2>
<p>RevenueCat — компания из США, поэтому данные о покупках могут обрабатываться там. Она работает по
стандартным договорным условиям Европейской комиссии, которые обязывают её защищать данные так же,
как в ЕС. Данные о покупках нужны, чтобы вы получили оплаченный Pro, поэтому они обрабатываются для
исполнения этой покупки.</p>
<p>Статистику хранит Mixpanel в Европейском союзе. Отчёты о сбоях обрабатывает Google, в том числе в
США, на тех же условиях. И то и другое обрабатывается в нашем законном интересе: чтобы приложение
работало и было понятно, что улучшать. Возразить можно в любой момент переключателем в настройках.</p>
<p>Если вы разрешили делиться аналитикой с Apple, Apple может также присылать нам обезличенные
отчёты о сбоях приложения. В них нет задач и ничего из написанного вами.</p>
<h2>Удаление данных</h2>
<p>Удалите задачу, список или всё в приложении — и это исчезнет с устройства и из iCloud. Удаление
приложения стирает то, что оно хранило на устройстве. Чтобы удалить данные из iCloud, откройте
Настройки, нажмите своё имя, затем iCloud, «Управление хранилищем», Taskward и удалите данные.</p>
<h2>Ваши права</h2>
<p>В зависимости от того, где вы живёте, в том числе по GDPR в ЕС и Великобритании, вы вправе узнать,
какие данные о вас хранятся, исправить или удалить их, ограничить их использование или возразить
против него и получить их копию. Напишите на адрес ниже. В данных о покупках нет имени и почты,
поэтому мы можем не суметь определить, какие из них ваши. То же со статистикой и отчётами о сбоях:
в них только случайный идентификатор установки. Подписка отменяется в настройках аккаунта
Apple.</p>
<h2>Дети</h2>
<p>Taskward не предназначен для детей. Он не собирает ничего, что позволяет определить человека, в
том числе ребёнка.</p>
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
<h2>Can Claude plan into Taskward?</h2>
<p>Yes, on a Mac with Pro: Claude and other AI assistants read your lists and write plans into them.
See <a href="../assistants/">Assistants</a>.</p>
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
<h2>Может ли Claude планировать в Taskward?</h2>
<p>Да, на Маке с Pro: Claude и другие ИИ-ассистенты читают ваши списки и записывают в них планы.
Смотрите <a href="../assistants/">Ассистенты</a>.</p>
<h2>Как удалить всё?</h2>
<p>Смотрите <a href="../privacy/">политику конфиденциальности</a>: что удалить в приложении и в iCloud.</p>
'''),
}


# Assistants: Claude and other AI assistants reading the lists and writing plans into them, over
# MCP from the Mac app (the app's docs/assistants.md). A page of its own, as a guide and a
# reference both: what it is beside a plan landed on a card, three steps to connect, what to
# say, then each tool with its parameters, the formats, and what is safe and private.
from html import escape as _esc

PLAN_JSON = {
    'en': {
        'projects': [{
            'title': 'Run a half marathon', 'deadline': '2027-04-18', 'area_id': '…',
            'notes': 'Spring race, 21.1 km.',
            'tasks': [{'title': 'Pick a training plan', 'when': 'today'}],
            'headings': [
                {'title': 'Gear', 'tasks': [
                    {'title': 'Buy running shoes', 'when': '2026-11-21', 'tags': ['Errand'],
                     'checklist': ['Measure feet', 'Try three pairs']}]},
                {'title': 'Weeks 1–4', 'tasks': [
                    {'title': 'Three easy runs a week', 'when': 'anytime'},
                    {'title': 'Book a physio check', 'reminder': '09:30'}]},
            ],
        }],
        'tasks': [{'title': 'Tell Anna about the race', 'when': 'evening'}],
    },
    'ru': {
        'projects': [{
            'title': 'Пробежать полумарафон', 'deadline': '2027-04-18', 'area_id': '…',
            'notes': 'Весенний забег, 21,1 км.',
            'tasks': [{'title': 'Выбрать план тренировок', 'when': 'today'}],
            'headings': [
                {'title': 'Экипировка', 'tasks': [
                    {'title': 'Купить кроссовки', 'when': '2026-11-21', 'tags': ['Дела'],
                     'checklist': ['Измерить стопу', 'Примерить три пары']}]},
                {'title': 'Недели 1–4', 'tasks': [
                    {'title': 'Три лёгкие пробежки в неделю', 'when': 'anytime'},
                    {'title': 'Записаться к физиотерапевту', 'reminder': '09:30'}]},
            ],
        }],
        'tasks': [{'title': 'Рассказать Ане про забег', 'when': 'evening'}],
    },
}

UPDATE_JSON = {
    'en': {'updates': [
        {'id': '7c1e…', 'project_id': '…', 'heading_id': '…', 'when': 'anytime'},
        {'id': '2f9a…', 'when': 'today', 'tags_add': ['Calls'], 'reminder': '10:00'},
        {'id': 'b04d…', 'trash': True},
    ]},
    'ru': {'updates': [
        {'id': '7c1e…', 'project_id': '…', 'heading_id': '…', 'when': 'anytime'},
        {'id': '2f9a…', 'when': 'today', 'tags_add': ['Звонки'], 'reminder': '10:00'},
        {'id': 'b04d…', 'trash': True},
    ]},
}

COMMAND = ('claude mcp add --transport http taskward http://127.0.0.1:47823/mcp \\\n'
           '  --header "Authorization: Bearer <token>"')

A = {
    'en': {
        'title': 'Assistants', 'desc': 'Let Claude, Codex, Gemini, Grok — any AI agent that speaks MCP — plan into Taskward on your Mac.',
        'kicker': 'Taskward for Mac · Pro',
        'h1': 'Plan with Claude,<br>land it in Taskward',
        'lede': 'Tell Claude what you are up to. It reads your areas and projects, makes a plan — '
                'projects with headings, tasks with their days, deadlines and checklists — and writes '
                'it into Taskward in one go. From the Mac it reaches your iPhone through iCloud. Not only Claude: '
                'Codex, Gemini, Grok — any agent that speaks MCP works the same.',
        'prompt': 'Plan my half marathon in April: gear, the first month of runs, a physio check.',
        'card': {
            'project': 'Run a half marathon', 'due': 'Apr 18',
            'loose': [('Pick a training plan', 'today:Today')],
            'headings': [('Gear', [('Buy running shoes', 'day:Nov 21|tag:Errand|0/2')]),
                         ('Weeks 1–4', [('Three easy runs a week', ''), ('Book a physio check', 'bell:09:30')])],
            'from': 'written by Claude',
        },
        'toc': 'On this page',
        'connect_h': 'Connect in three steps',
        'steps': [
            ('Let assistants in', 'On your Mac, open Taskward’s Settings → <b>Assistants</b> and turn on '
             '<b>Let assistants in</b>. It is part of Pro.'),
            ('Copy the command', 'The page shows a command with your own token in it. Tap <b>Copy the '
             'command</b> and run it once in Terminal:'),
            ('Ask Claude', 'Start Claude Code anywhere and ask for a plan. It calls Taskward by itself; '
             'type <code>/mcp</code> to see it connected.'),
        ],
        'say_h': 'Things to say',
        'says': [
            'Sort my Inbox.',
            'Look at my Inbox and sort it into the projects I already have.',
            'Plan a move to a new flat by March 1: packing, papers, utilities.',
            'What is on my plate today? Put the three most pressing things on this evening.',
            'Make a project for the conference talk with headings for draft, slides and rehearsal.',
        ],
        'tools_h': 'Tools',
        'tools_lede': 'Taskward gives an assistant four tools: two read, one adds a plan, one sorts what is '
                      'there. None of them ever deletes anything for good.',
        'param': ('Parameter', 'Type', 'What it is'),
        'tools': [
            ('get_overview', 'Reads what is there: today’s date, your areas, the open projects with their '
             'headings, deadlines and counts of open tasks, your tags, and how many tasks wait in the '
             'Inbox and Today. An assistant calls it first, so a plan goes where things already are.',
             [], 'No parameters.'),
            ('find_tasks', 'Open tasks of a list, a project or an area, or by words in their titles. '
             'Give one of these:',
             [('list', 'text', '<code>inbox</code>, <code>today</code> (with This Evening), '
               '<code>upcoming</code>, <code>anytime</code> or <code>someday</code>'),
              ('project_id', 'id', 'a project from get_overview'),
              ('area_id', 'id', 'an area from get_overview'),
              ('query', 'text', 'every word matched in the title, big letters or small'),
              ('limit', 'number', 'at most this many; 100 if not given')], ''),
            ('add_plan', 'Writes a plan in one go — all of it, or nothing if any part is wrong. Any of:',
             [('areas', 'list', 'new areas, each with <code>title</code> and its <code>projects</code>; '
               'one named as an area you have is that one'),
              ('projects', 'list', 'new projects: <code>title</code>, <code>notes</code>, <code>when</code>, '
               '<code>deadline</code>, <code>area_id</code>, <code>tasks</code>, and <code>headings</code> — '
               'each a <code>title</code> and its <code>tasks</code>'),
              ('tasks', 'list', 'loose tasks: into the Inbox, onto a day, or into a project, heading or area '
               'you have, by <code>project_id</code>, <code>heading_id</code>, <code>area_id</code>')], ''),
            ('update_tasks', 'Changes tasks already there, many at once — all of it, or nothing if any part is '
             'wrong. For sorting the Inbox and tidying lists. Each update names a task by its '
             '<code>id</code> (from find_tasks) and gives only what changes:',
             [('id', 'id', 'required'),
              ('title', 'text', 'a new title'),
              ('notes', 'text', 'new notes'),
              ('when', 'text', 'as in add_plan; <code>inbox</code> sends it back to the Inbox, out of any project'),
              ('deadline', 'day or null', '<code>YYYY-MM-DD</code>; <code>null</code> takes it off'),
              ('reminder', 'time or null', '<code>HH:MM</code>; <code>null</code> takes it off'),
              ('tags_add', 'list', 'tags to put on, by name'),
              ('tags_remove', 'list', 'tags to take off, by name'),
              ('project_id', 'id or null', 'the project to file it in; <code>null</code> takes it out of its project'),
              ('heading_id', 'id', 'a heading of that project'),
              ('area_id', 'id or null', 'the area to file it in'),
              ('complete', 'true / false', 'done, or open again'),
              ('trash', 'true', 'puts it in the Trash; nothing is deleted for good')], ''),
        ],
        'task_h': 'A task',
        'task_rows': [
            ('title', 'text', 'required'),
            ('notes', 'text', 'Markdown, as the app writes it'),
            ('when', 'text', 'see below'),
            ('deadline', 'day', '<code>YYYY-MM-DD</code>'),
            ('reminder', 'time', '<code>HH:MM</code> on its day; a task with no day is put on today'),
            ('tags', 'list', 'by name; a tag you do not have yet is made'),
            ('checklist', 'list', 'its steps, in order'),
        ],
        'example_h': 'An example: a plan',
        'update_h': 'An example: three Inbox tasks sorted',
        'when_h': 'When',
        'when_rows': [
            ('inbox', 'not sorted yet — the default for a loose task'),
            ('today', 'Today'), ('evening', 'This Evening'),
            ('anytime', 'Anytime — the default inside a project or area'),
            ('someday', 'Someday'),
            ('2026-12-01', 'that day; in Upcoming till then'),
        ],
        'undo_h': 'Undo',
        'undo': 'Whatever an assistant does shows a note at the foot of the window — “An assistant added 6 '
                'tasks”, or that it changed some — with <b>Undo</b>. A plan’s Undo takes out what it made: '
                'tasks, headings, projects, the areas and tags it made. A batch of changes is undone whole, '
                'each task back where and as it was. Nothing is ever deleted for good: a task an assistant '
                'throws out goes to the Trash. Missed the note? The last change waits in Settings → '
                'Assistants as <b>Undo the assistant’s last change</b>.',
        'safe_h': 'Security',
        'safe': [
            'Taskward listens only on the Mac’s own loopback, <code>127.0.0.1:47823</code>: nothing on '
            'your network or the internet can reach it.',
            'Nothing is answered without your token. <b>New token</b> on the same page shuts out every '
            'assistant connected before, until you connect it again.',
            'A request sent by a web page is refused, so no site you visit can reach your tasks.',
            'The door is open only while Taskward is open, the switch is on and Pro is.',
        ],
        'private_h': 'Privacy',
        'private': 'Taskward itself sends nothing anywhere: your tasks stay on your devices and in your '
                   'iCloud. But what an assistant reads from Taskward goes to whoever runs it — Anthropic '
                   'for Claude — as everything you tell it does.',
        'pro_h': 'Pro',
        'pro': 'Letting assistants in is part of Taskward Pro. Without it, the switch opens the offer; if Pro '
               'ends, the door shuts and everything written stays.',
        'faq_h': 'Questions',
        'faq': [
            ('Does it work on iPhone?', 'The door is on the Mac. What is written there reaches your iPhone '
             'through iCloud within seconds.'),
            ('Does Taskward have to be open?', 'Yes: the Mac app is the server. Closed, the assistant is told '
             'it cannot connect.'),
            ('Which assistants?', 'Any agent that speaks MCP over HTTP: Claude Code, Codex, Gemini CLI, '
             'Grok, Cursor and the rest. Claude Code connects with the command above; any other, give it the '
             'address <code>http://127.0.0.1:47823/mcp</code> and the token as a Bearer header. Claude '
             'Desktop runs only local stdio servers; a bridge such as <code>mcp-remote</code> can stand '
             'between.'),
            ('It says it could not open the port.', 'Another app holds port 47823. Quit it, or write to '
             'me.'),
        ],
        'tools_word': 'tool',
    },
    'ru': {
        'title': 'Ассистенты', 'desc': 'Пусть Claude, Codex, Gemini, Grok — любой ИИ-агент с поддержкой MCP — планирует в Taskward на твоём Маке.',
        'kicker': 'Taskward для Mac · Pro',
        'h1': 'Планируй с Claude,<br>а план — сразу в Taskward',
        'lede': 'Расскажи Claude, что задумал. Он посмотрит твои области и проекты, составит план — '
                'проекты с заголовками, задачи с днями, дедлайнами и чек-листами — и запишет его в Taskward '
                'одним махом. С Мака всё приедет на iPhone через iCloud. И не только Claude: Codex, Gemini, Grok — '
                'любой агент с поддержкой MCP работает так же.',
        'prompt': 'Распиши подготовку к полумарафону в апреле: экипировка, первый месяц пробежек, физиотерапевт.',
        'card': {
            'project': 'Пробежать полумарафон', 'due': '18 апр.',
            'loose': [('Выбрать план тренировок', 'today:Сегодня')],
            'headings': [('Экипировка', [('Купить кроссовки', 'day:21 нояб.|tag:Дела|0/2')]),
                         ('Недели 1–4', [('Три лёгкие пробежки в неделю', ''),
                                         ('Записаться к физиотерапевту', 'bell:09:30')])],
            'from': 'записал Claude',
        },
        'toc': 'На странице',
        'connect_h': 'Подключение в три шага',
        'steps': [
            ('Пусти ассистентов', 'На Маке открой Настройки Taskward → <b>Ассистенты</b> и включи '
             '<b>Пускать ассистентов</b>. Это часть Pro.'),
            ('Скопируй команду', 'На странице будет команда с твоим собственным токеном. Нажми '
             '<b>Скопировать команду</b> и один раз выполни её в Терминале:'),
            ('Попроси Claude', 'Запусти Claude Code где угодно и попроси план. Он сам обратится к Taskward; '
             'набери <code>/mcp</code>, чтобы увидеть подключение.'),
        ],
        'say_h': 'Что можно сказать',
        'says': [
            'Разбери мой Inbox.',
            'Посмотри мои Входящие и разложи их по проектам, которые у меня уже есть.',
            'Спланируй переезд в новую квартиру к 1 марта: вещи, документы, коммуналка.',
            'Что у меня на сегодня? Три самых срочных поставь на вечер.',
            'Сделай проект доклада на конференции с заголовками: черновик, слайды, репетиция.',
        ],
        'tools_h': 'Инструменты',
        'tools_lede': 'Taskward даёт ассистенту четыре инструмента: два читают, один добавляет план, один '
                      'разбирает то, что есть. Насовсем ни один из них ничего не удаляет.',
        'param': ('Параметр', 'Тип', 'Что это'),
        'tools': [
            ('get_overview', 'Читает, что есть: сегодняшнюю дату, области, открытые проекты с заголовками, '
             'дедлайнами и числом открытых задач, теги и сколько задач ждёт во Входящих и в Сегодня. '
             'Ассистент вызывает его первым, чтобы план лёг туда, где всё уже лежит.', [], 'Без параметров.'),
            ('find_tasks', 'Открытые задачи списка, проекта или области — или по словам в названии. '
             'Укажи что-то одно:',
             [('list', 'текст', '<code>inbox</code>, <code>today</code> (вместе с Этим вечером), '
               '<code>upcoming</code>, <code>anytime</code> или <code>someday</code>'),
              ('project_id', 'id', 'проект из get_overview'),
              ('area_id', 'id', 'область из get_overview'),
              ('query', 'текст', 'каждое слово ищется в названии, без учёта регистра'),
              ('limit', 'число', 'не больше стольких; по умолчанию 100')], ''),
            ('add_plan', 'Записывает план одним махом — целиком или, если где-то ошибка, никак. Любое из:',
             [('areas', 'список', 'новые области: <code>title</code> и их <code>projects</code>; '
               'область с тем же именем, что у тебя есть, — это она'),
              ('projects', 'список', 'новые проекты: <code>title</code>, <code>notes</code>, <code>when</code>, '
               '<code>deadline</code>, <code>area_id</code>, <code>tasks</code> и <code>headings</code> — '
               'у каждого <code>title</code> и свои <code>tasks</code>'),
              ('tasks', 'список', 'отдельные задачи: во Входящие, на день или в твой проект, заголовок или '
               'область — по <code>project_id</code>, <code>heading_id</code>, <code>area_id</code>')], ''),
            ('update_tasks', 'Меняет задачи, которые уже есть, много сразу — целиком или, если где-то ошибка, '
             'никак. Чтобы разобрать Входящие и навести порядок в списках. Каждое изменение называет задачу '
             'по <code>id</code> (из find_tasks) и даёт только то, что меняется:',
             [('id', 'id', 'обязательно'),
              ('title', 'текст', 'новое название'),
              ('notes', 'текст', 'новые заметки'),
              ('when', 'текст', 'как в add_plan; <code>inbox</code> возвращает во Входящие, из любого проекта'),
              ('deadline', 'день или null', '<code>YYYY-MM-DD</code>; <code>null</code> снимает'),
              ('reminder', 'время или null', '<code>HH:MM</code>; <code>null</code> снимает'),
              ('tags_add', 'список', 'теги, которые надеть, по именам'),
              ('tags_remove', 'список', 'теги, которые снять, по именам'),
              ('project_id', 'id или null', 'проект, куда положить; <code>null</code> вынимает из проекта'),
              ('heading_id', 'id', 'заголовок этого проекта'),
              ('area_id', 'id или null', 'область, куда положить'),
              ('complete', 'true / false', 'выполнена или снова открыта'),
              ('trash', 'true', 'в Корзину; насовсем ничего не удаляется')], ''),
        ],
        'task_h': 'Задача',
        'task_rows': [
            ('title', 'текст', 'обязательно'),
            ('notes', 'текст', 'Markdown, как в приложении'),
            ('when', 'текст', 'см. ниже'),
            ('deadline', 'день', '<code>YYYY-MM-DD</code>'),
            ('reminder', 'время', '<code>HH:MM</code> в её день; задача без дня ставится на сегодня'),
            ('tags', 'список', 'по именам; тега, которого ещё нет, создастся'),
            ('checklist', 'список', 'шаги по порядку'),
        ],
        'example_h': 'Пример: план',
        'update_h': 'Пример: три задачи из Входящих разобраны',
        'when_h': 'Когда',
        'when_rows': [
            ('inbox', 'ещё не разобрано — так по умолчанию для отдельной задачи'),
            ('today', 'Сегодня'), ('evening', 'Этим вечером'),
            ('anytime', 'В любое время — по умолчанию внутри проекта или области'),
            ('someday', 'Когда-нибудь'),
            ('2026-12-01', 'в этот день; до него — в Предстоящих'),
        ],
        'undo_h': 'Отменить',
        'undo': 'Что бы ассистент ни сделал, внизу окна появится записка — «Ассистент добавил 6 задач» или '
                'что он что-то поменял — с кнопкой <b>Отменить</b>. У плана она уберёт всё, что он сделал: '
                'задачи, заголовки, проекты, созданные им области и теги. Пачка изменений отменяется целиком: '
                'каждая задача вернётся туда и такой, какой была. Насовсем ничего не удаляется: выброшенная '
                'ассистентом задача уходит в Корзину. Пропустил записку? Последнее изменение ждёт в '
                'Настройках → Ассистенты: <b>Отменить последнее от ассистента</b>.',
        'safe_h': 'Безопасность',
        'safe': [
            'Taskward слушает только внутренний адрес самого Мака, <code>127.0.0.1:47823</code>: из сети и '
            'из интернета до него не достучаться.',
            'Без твоего токена он ничего не ответит. <b>Новый токен</b> на той же странице отключает всех '
            'подключённых раньше ассистентов, пока ты не подключишь их снова.',
            'Запрос со страницы в браузере отклоняется, так что ни один сайт не доберётся до твоих задач.',
            'Дверь открыта, только пока Taskward открыт, переключатель включён и есть Pro.',
        ],
        'private_h': 'Приватность',
        'private': 'Сам Taskward ничего никуда не отправляет: задачи остаются на твоих устройствах и в твоём '
                   'iCloud. Но то, что ассистент прочтёт в Taskward, уходит тому, кто его запускает, — у '
                   'Claude это Anthropic, — как и всё, что ты ему говоришь.',
        'pro_h': 'Pro',
        'pro': 'Пускать ассистентов — часть Taskward Pro. Без него переключатель откроет предложение Pro; если '
               'Pro закончится, дверь закроется, а всё записанное останется.',
        'faq_h': 'Вопросы',
        'faq': [
            ('А на iPhone работает?', 'Дверь — на Маке. Что записано там, приедет на iPhone через iCloud за '
             'секунды.'),
            ('Taskward должен быть открыт?', 'Да: сервер — это само Мак-приложение. Если оно закрыто, '
             'ассистент скажет, что не может подключиться.'),
            ('Какие ассистенты подходят?', 'Любой агент, который умеет MCP по HTTP: Claude Code, Codex, '
             'Gemini CLI, Grok, Cursor и другие. Claude Code подключается командой выше; любому другому дай '
             'адрес <code>http://127.0.0.1:47823/mcp</code> и токен в заголовке Bearer. Claude Desktop '
             'запускает только локальные stdio-серверы; между ними можно поставить мост вроде '
             '<code>mcp-remote</code>.'),
            ('Пишет, что не смог открыть порт.', 'Порт 47823 занят другим приложением. Закрой его или напиши '
             'мне.'),
        ],
        'tools_word': 'инструмент',
    },
}


def _plan_row(title, spec):
    bits = []
    for b in [x for x in spec.split('|') if x]:
        kind, _, val = b.partition(':')
        if kind == 'today':
            bits.append(f'<span class="today">{icon("favoriteFilled")}{val}</span>')
        elif kind == 'day':
            bits.append(f'<span>{icon("today")}{val}</span>')
        elif kind == 'bell':
            bits.append(f'<span>{icon("reminderFilled")}{val}</span>')
        elif kind == 'tag':
            bits.append(f'<span class="tagword">{val}</span>')
        else:
            bits.append(f'<span>{icon("check")}{b}</span>')
    pr = f'<div class="print">{"".join(bits)}</div>' if bits else ''
    return f'<li class="row"><span class="signal static">{SIGNAL}</span><div><div class="title">{title}</div>{pr}</div></li>'


def _table(head, rows):
    th = ''.join(f'<th>{h}</th>' for h in head)
    tr = ''.join('<tr>' + ''.join(
        f'<td>{"<code>" + c + "</code>" if i == 0 else c}</td>' for i, c in enumerate(r)) + '</tr>' for r in rows)
    return f'<div class="table"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def _code(text):
    return f'<pre class="code"><code>{_esc(text)}</code></pre>'


def assistants(lang):
    t = T[lang]
    a = A[lang]
    depth = '../' if lang == 'en' else '../../'
    home = depth if lang == 'en' else depth + 'ru/'
    t2 = dict(t)
    t2['other'] = (t['other'][0], ('../../assistants/' if lang == 'ru' else '../ru/assistants/'))
    c = a['card']
    card = (f'<div class="paper plan-card"><div class="plan-head">{icon("project")}<span>{c["project"]}</span>'
            f'<span class="due">{icon("flagFilled")}{c["due"]}</span></div>'
            f'<ul class="rows">{"".join(_plan_row(*r) for r in c["loose"])}</ul>'
            + ''.join(f'<h4 class="plan-heading">{h}</h4><ul class="rows">{"".join(_plan_row(*r) for r in rows)}</ul>'
                      for h, rows in c['headings'])
            + f'<p class="from">{icon("knight")}{c["from"]}</p></div>')
    prompt = f'<div class="paper grey ask"><span class="chev">›</span>{a["prompt"]}</div>'
    sections = [('connect', a['connect_h']), ('say', a['say_h']), ('tools', a['tools_h']),
                ('formats', a['when_h']), ('undo', a['undo_h']), ('security', a['safe_h']),
                ('privacy', a['private_h']), ('pro', a['pro_h']), ('faq', a['faq_h'])]
    toc = ''.join(f'<li><a href="#{k}">{n}</a></li>' for k, n in sections)
    steps = ''.join(
        f'<li><span class="n">{i}</span><div><h3>{h}</h3><p>{p}</p>{_code(COMMAND) if i == 2 else ""}</div></li>'
        for i, (h, p) in enumerate(a['steps'], 1))
    says = ''.join(f'<li><span class="chev">›</span>{s}</li>' for s in a['says'])
    tools = ''.join(
        f'<section class="tool" id="{name}"><h3><code>{name}</code></h3><p>{say}</p>'
        + (_table(a['param'], params) if params else f'<p class="pencil">{none}</p>') + '</section>'
        for name, say, params, none in a['tools'])
    example = json.dumps(PLAN_JSON[lang], ensure_ascii=False, indent=2)
    # Leaves on one line each — a task, a list of words — so the example reads as the plan does.
    flat = lambda m: re.sub(r'\s*\n\s*', ' ', m[0]).replace('[ ', '[').replace(' ]', ']').replace('{ ', '{').replace(' }', '}')
    example = re.sub(r'\[[^\[\]{}]*\]', flat, example)
    example = re.sub(r'\{[^\[\]{}]*(?:\[[^\[\]{}]*\][^\[\]{}]*)*\}', flat, example)
    update = json.dumps(UPDATE_JSON[lang], ensure_ascii=False, indent=2)
    update = re.sub(r'\{[^\[\]{}]*(?:\[[^\[\]{}]*\][^\[\]{}]*)*\}', flat,
                    re.sub(r'\[[^\[\]{}]*\]', flat, update))
    safe = ''.join(f'<li>{icon("lock")}<span>{s}</span></li>' for s in a['safe'])
    faq = ''.join(f'<details><summary>{q}</summary><p>{ans}</p></details>' for q, ans in a['faq'])
    page = head(lang, f'{a["title"]} · Taskward', a['desc'], 'assistants/', depth) + f'''<body>
{bar(t2, depth, lang, home)}
<main class="wrap assist">
<section class="assist-hero">
<div class="say"><p class="kicker">{a['kicker']}</p><h1>{a['h1']}</h1><p class="lede">{a['lede']}</p></div>
<div class="show">{prompt}{ARROW}{card}</div>
</section>
<article class="paper doc assist-doc">
<nav class="toc" aria-label="{a['toc']}"><b>{a['toc']}</b><ol>{toc}</ol></nav>
<h2 id="connect">{a['connect_h']}</h2>
<ol class="steps">{steps}</ol>
<h2 id="say">{a['say_h']}</h2>
<ul class="says">{says}</ul>
<h2 id="tools">{a['tools_h']}</h2>
<p>{a['tools_lede']}</p>
{tools}
<h3>{a['task_h']}</h3>
{_table(a['param'], a['task_rows'])}
<h3>{a['example_h']}</h3>
{_code(example)}
<h3>{a['update_h']}</h3>
{_code(update)}
<h2 id="formats">{a['when_h']}</h2>
{_table((a['param'][0].replace('Parameter', 'Value').replace('Параметр', 'Значение'), a['param'][2]), a['when_rows'])}
<h2 id="undo">{a['undo_h']}</h2>
<p>{a['undo']}</p>
<h2 id="security">{a['safe_h']}</h2>
<ul class="safe">{safe}</ul>
<h2 id="privacy">{a['private_h']}</h2>
<p>{a['private']}</p>
<h2 id="pro">{a['pro_h']}</h2>
<p>{a['pro']}</p>
<h2 id="faq">{a['faq_h']}</h2>
<div class="faq">{faq.replace('{mail}', MAIL)}</div>
</article>
</main>
{foot(t2, depth, lang)}
</body>
</html>
'''
    return page.replace('{base}', depth)



def doc(lang, kind, pages):
    t = T[lang]
    title, body = pages[lang]
    depth = '../' if lang == 'en' else '../../'
    home = depth if lang == 'en' else depth + 'ru/'
    body = body.replace('{mail}', MAIL)
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
    write(pre / 'assistants/index.html', assistants(lang))
write(SITE / '.nojekyll', '')
write(SITE / '404.html', '<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=/taskward/"><title>Taskward</title>')
write(SITE / 'sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
      + ''.join(f'<url><loc>{URL}{p}</loc></url>' for p in ['', 'privacy/', 'support/', 'assistants/', 'ru/', 'ru/privacy/', 'ru/support/', 'ru/assistants/'])
      + '</urlset>\n')
print('written')
