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
UPDATED = {'en': 'October 27, 2026', 'ru': '27 октября 2026'}

T = {
    'en': {
        'title': 'Taskward: a calm to-do list on paper cards',
        'desc': 'A calm to-do list for iPhone and Mac. Every list is a paper card on your desk: '
                'Today in front, the rest in a wooden holder behind it.',
        'nav': ['Smart dates', 'Lists', 'iPhone and Mac', 'Privacy', 'Support'],
        'other': ('Русский', 'ru/'),
        'h1': 'Your day,<br>on <u>one card</u>.',
        'lede': ('A calm to-do list for iPhone and Mac.',
                 'Every list is a paper card on your desk. Write a task the way you’d say it, and '
                 'work your day from one card.'),
        'small': 'No account · no ads · kept in your own iCloud',
        'cta': 'Coming soon to the App Store',
        # The card under the lede: what Taskward comes to, as tasks on a list, each its small
        # print as the app writes it — {today}, {bell}, {cloud}, {knight} and the signals' marks
        # {s1}, {s2}, {s5} laid in as icons.
        'points_h': 'Why Taskward',
        'why_h': 'Four reasons to try it',
        'why_say': 'A to-do list that keeps out of your way. Each reason is a line on a card, as '
                   'tasks are in the app: tick them off as you read.',
        'points': [
            ('Write it as you’d say it', '“Gym <mark>tomorrow at 9</mark>” → {today}Tomorrow {bell}09:00'),
            ('More than done or not', '{s1}in progress {s2}delegated {s5}waiting'),
            ('The same lists on iPhone and Mac', '{cloud}kept in step through your iCloud'),
            ('A knight to show you the way', '{knight}on first launch, Getting Things Done step by step'),
        ],
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
            'notes': 'The old one is **cracked** along the rim. Ask if he can match the ::boss::.',
            'steps': [('Measure the old one', True), ('Find the sketch', False), ('Ask the price', False)],
            'tags': ['Armoury', 'Errand'], 'when': 'Today',
        },
        'signals_h': 'More than done or not done',
        'signals_say': 'Hold a task’s circle and mark how it stands. Delegated and waiting fade '
                       'into pencil, out of your way.',
        'signals_note': ('Mark it', 'Complete', 'Signals…'),
        'md_h': 'Notes in Markdown',
        'md_say': 'Headings, bold, highlights, lists, boxes to tick, links, even tables. The marks '
                  'stay where you wrote them, in pencil; what they mark takes its look at once.',
        'md': ['Heading', 'bold', 'highlight', 'to do', 'link', 'table'],
        'signals': ['In progress', 'Delegated', 'Appointment', 'Important'],
        # Written in pen round the phone, each pointing at its place on the screen.
        'float': {'smart': ('Gym ', 'tomorrow at 9'), 'when': 'Tomorrow', 'progress': 'In progress',
                  'tag': 'Armoury'},
        'notes': ['the other lists, standing behind', 'Today in front: work right on it',
                  'a deadline today, in red', 'a tap, and a new task',
                  'Inbox, projects and notes, on the oak'],
        'gtd_h': 'Built on Getting Things Done',
        'gtd_say': 'David Allen’s method for a clear head: get everything out of it and into a trusted place, then decide, one thing at a time. Taskward’s lists are its steps.',
        'gtd': [('Capture', 'Everything goes into the Inbox, as it comes.'),
                ('Clarify', 'What is it? Do it now, give it a day, put it off, or keep it as a note.'),
                ('Organise', 'Today, Upcoming, Anytime, Someday, projects and areas.'),
                ('Reflect', 'Look Someday through now and then; the Logbook keeps what’s done.'),
                ('Engage', 'Work from one card: Today.')],
        'gtd_knight': 'On first launch a little knight walks you through it with a pile of errands.',
        'cap': {
            'shots': 'The real app',
            'try': 'Type a task with a day in it and press Return.',
            'ticket': ('A task opens as a ticket', 'Notes, a checklist, tags, a deadline, a reminder.'),
            'signals': ('More than done', 'Hold a task’s circle to mark how it stands.'),
            'lists': ('Every list, its own card', 'Each on its own paper, behind Today.'),
            'mac': ('On a Mac too', 'A sidebar, Quick Find on ⌘F, kept in step through iCloud.'),
            'yours': ('Your desk, your ink', 'Try a desk on this page:'),
        },
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
            ('paperLines', 'Zen', 'A card edge to edge when a day needs all of you.'),
            ('search', 'Quick Find', 'Draw Today down, or ⌘F on a Mac.'),
            ('today', 'Calendar', 'Your calendars’ events in Today and Upcoming, beside your to-dos. Only read, never changed.'),
        ],
        'more_say': 'Small things that make a calm day calmer.',
        # What each card shows: Zen's tasks, the word typed into Quick Find and what it finds,
        # the day's events (time, title, its calendar's colour) as Today lists them.
        'more_demo': {
            'zen': ['Sharpen the sword', 'Call the smith', 'Pay the rent'],
            'find': ('sadd', ['Oil the <mark>sadd</mark>le', 'Mend the <mark>sadd</mark>le bags']),
            'cal': [('07:30', 'Morning ride', '#7cc9f2'), ('10:30', 'Council at the keep', '#f5a03c'),
                    ('19:00', 'Supper with Masha', '#3aa0e8')],
        },
        'zen_h': 'One card, the whole screen',
        'zen_say': 'When a day needs all of you, open its card edge to edge: no bar, no desk, '
                   'nothing else. Draw it down and it is back on the desk.',
        'real_h': 'The real app, on iPhone and Mac',
        'real_say': 'The same lists on both, kept in step through your iCloud. On a Mac the '
                    'holder stands in a window of its own, by day or by night, and Quick Find is '
                    'one key away: ⌘F.',
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
        'knight_say': 'A little knight shows you how to sort an inbox on first launch.',
        'support': 'Support', 'privacy': 'Privacy policy', 'by': 'Made by Aleksei Lobanov',
        'back': 'Taskward',
    },
    'ru': {
        'title': 'Taskward: спокойный список дел на бумажных карточках',
        'desc': 'Спокойный список дел для iPhone и Mac. Каждый список — бумажная карточка на '
                'столе: «Сегодня» впереди, остальные в деревянной подставке за ней.',
        'nav': ['Умная дата', 'Списки', 'iPhone и Mac', 'Приватность', 'Поддержка'],
        'other': ('English', '../'),
        'h1': 'Весь день —<br>на <u>одной карточке</u>.',
        'lede': ('Спокойный список дел для iPhone и Mac.',
                 'Каждый список — бумажная карточка на твоём столе. Пиши задачу, как говоришь, '
                 'и веди весь день с одной карточки.'),
        'small': 'Без аккаунта · без рекламы · в твоём iCloud',
        'cta': 'Скоро в App Store',
        'points_h': 'Почему Taskward',
        'why_h': 'Четыре причины попробовать',
        'why_say': 'Список дел, который не мешает. Каждая причина — строка на карточке, как '
                   'задачи в приложении: отмечай их по ходу чтения.',
        'points': [
            ('Пиши, как говоришь', '«Тренировка <mark>завтра в 9</mark>» → {today}Завтра {bell}09:00'),
            ('Не только «сделано»', '{s1}в работе {s2}поручено {s5}жду ответа'),
            ('Одни списки на iPhone и Mac', '{cloud}синхронно через твой iCloud'),
            ('Рыцарь проведёт по методу', '{knight}при первом запуске, GTD шаг за шагом'),
        ],
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
        'hints': [
            ('export', 'Входящие', 'white', '#4AA8F0', '#487ba8', 'Всё сюда — разберёшь потом', 'Всё, что пришло в голову. Раз в день разбирай.'),
            ('today', 'Планы', 'cream', '#FF6B5E', '#ab5a57', 'То, у чего есть свой день', 'Задачи с датой ждут здесь и сами придут в «Сегодня» в свой день.'),
            ('list', 'В любое время', 'cream', '#3FB27F', '#428169', 'Следующие шаги', 'Опустело «Сегодня» — возьми отсюда следующее.'),
            ('archive', 'Когда-нибудь', 'kraft', '#FFA23A', '#a85900', 'Мечты и «потом»', 'То, чего хочется, но не сейчас. Загляни раз в неделю.'),
            ('project', 'Проекты', 'white', '#8B6CF0', '#6c5aa8', 'Проекты и области', 'Проект — цель из нескольких шагов, область — часть жизни: работа, дом, здоровье.'),
            ('notebook', 'Заметки', 'white', '#F6C945', '#a68e4a', 'Не задача, просто запись', 'Мысли, которые стоит сохранить, — не среди задач. Станет делом — перенеси.'),
        ],
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
            'notes': 'Старый **треснул** по краю. Спросить, подберёт ли он ::умбон::.',
            'steps': [('Измерить старый', True), ('Найти эскиз', False), ('Узнать цену', False)],
            'tags': ['Оружейная', 'В городе'], 'when': 'Сегодня',
        },
        'signals_h': 'Больше, чем сделано или нет',
        'signals_say': 'Зажми кружок задачи и отметь, как она: в работе, поручено, жду ответа. '
                       'Поручённое и ожидание уходят в карандаш, чтобы не мешать.',
        'signals_note': ('Отметить', 'Выполнить', 'Сигналы…'),
        'md_h': 'Заметки в Markdown',
        'md_say': 'Заголовки, жирный, выделение, списки, галочки, ссылки и даже таблицы. Значки '
                  'остаются там, где ты их написал, карандашом, а размеченное сразу меняет вид.',
        'md': ['Заголовок', 'жирный', 'выделение', 'сделать', 'ссылка', 'таблица'],
        'signals': ['В работе', 'Поручено', 'Встреча', 'Важно'],
        'float': {'smart': ('Тренировка ', 'завтра в 9'), 'when': 'Завтра', 'progress': 'В работе',
                  'tag': 'Оружейная'},
        'notes': ['остальные списки стоят позади', '«Сегодня» впереди — работай на нём',
                  'срок сегодня — красным', 'тап — и новая задача',
                  'входящие, проекты и заметки — на дубовой подставке'],
        'gtd_h': 'По методу GTD',
        'gtd_say': 'Метод Дэвида Аллена для ясной головы: выгрузить из неё всё в надёжное место и решать по одному делу за раз. Списки Taskward — это его шаги.',
        'gtd': [('Собрать', 'Всё, что приходит в голову, — во входящие, сразу.'),
                ('Разобрать', 'Что это? Сделать сейчас, назначить день, отложить или оставить заметкой.'),
                ('Разложить', 'Сегодня, Планы, В любое время, Когда-нибудь, проекты и области.'),
                ('Пересмотреть', 'Иногда пролистывать «Когда-нибудь»; сделанное хранит журнал.'),
                ('Делать', 'Работать с одной карточки — «Сегодня».')],
        'gtd_knight': 'При первом запуске маленький рыцарь проведёт по методу на ворохе поручений.',
        'cap': {
            'shots': 'Настоящее приложение',
            'try': 'Напиши задачу с днём и нажми ввод.',
            'ticket': ('Задача — это билет', 'Заметки, чек-лист, теги, срок, напоминание.'),
            'signals': ('Не только «сделано»', 'Зажми кружок и отметь, как задача.'),
            'lists': ('У списка своя карточка', 'Каждый на своей бумаге, позади «Сегодня».'),
            'mac': ('И на Маке', 'Боковая панель, поиск по ⌘F, синхронно через iCloud.'),
            'yours': ('Твой стол, твои чернила', 'Попробуй стол прямо здесь:'),
        },
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
            ('paperLines', 'Дзен', 'Карточка на весь экран, когда нужно сосредоточиться.'),
            ('search', 'Быстрый поиск', 'Потяни «Сегодня» вниз или нажми ⌘F на Маке.'),
            ('today', 'Календарь', 'События твоих календарей — в «Сегодня» и «Планах», рядом с задачами. Только читаются, ничего не меняется.'),
        ],
        'more_say': 'Мелочи, от которых спокойный день становится ещё спокойнее.',
        'more_demo': {
            'zen': ['Наточить меч', 'Позвонить кузнецу', 'Заплатить за жильё'],
            'find': ('седл', ['Смазать <mark>седл</mark>о', 'Починить <mark>седл</mark>ьные сумки']),
            'cal': [('07:30', 'Утренняя прогулка верхом', '#7cc9f2'), ('10:30', 'Совет в замке', '#f5a03c'),
                    ('19:00', 'Ужин с Машей', '#3aa0e8')],
        },
        'zen_h': 'Одна карточка на весь экран',
        'zen_say': 'Когда день требует всего внимания, разверни его карточку от края до края: '
                   'без панели, без стола, без лишнего. Потяни вниз — и она снова на столе.',
        'real_h': 'Настоящее приложение, на iPhone и Mac',
        'real_say': 'Одни и те же списки на обоих, синхронно через твой iCloud. На Маке '
                    'подставка стоит в своём окне, днём и ночью, а быстрый поиск — по ⌘F.',
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
        'knight_say': 'При первом запуске маленький рыцарь покажет, как разобрать входящие.',
        'support': 'Поддержка', 'privacy': 'Политика конфиденциальности',
        'by': 'Сделал Алексей Лобанов', 'back': 'Taskward',
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
SIGNAL_HALF = ('<svg class="icon" viewBox="0 0 30 30" aria-hidden="true"><circle cx="15" cy="15" r="11" '
               'fill="none" stroke="currentColor" stroke-width="1.9"/><path fill="currentColor" '
               'd="M15 4a11 11 0 0 0 0 22z"/></svg>')

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
<script>try {{ const d = localStorage.getItem('taskward-desk'), i = localStorage.getItem('taskward-ink');
if (d && d !== 'default') document.documentElement.dataset.desk = d;
if (i && i !== 'default') document.documentElement.dataset.ink = i; }} catch (_) {{}}</script>
<script src="{base}when.js?v={VERSION}" defer></script>
<script src="{base}app.js?v={VERSION}" defer></script>
</head>
'''


def bar(t, base, lang, home):
    other, href = t['other']
    anchors = ['#smart', '#lists', '#real']
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
        f'<div class="paper {paper} lcard" style="--r:{r}deg;--marker:{marker};--pen:{pen}">'
        f'<div class="head">{icon(mark)}{name}</div>'
        f'<div class="hint"><b>{title}</b><span>{text}</span></div></div>'
        for (mark, name, paper, marker, pen, title, text), r
        in zip(t['hints'], [-1.4, 0.9, -0.6, 1.2, -1.0, 0.7])
    )
    tk = t['ticket']
    mk = lambda m: f'<span class="mk">{m}</span>'
    h, bold, hl, todo, link, table = t['md']
    md = ''.join(f'<li>{x}</li>' for x in [
        f'{mk("#")} <b class="h">{h}</b>', f'{mk("**")}<b>{bold}</b>{mk("**")}',
        f'{mk("::")}<mark>{hl}</mark>{mk("::")}', f'{mk("- [ ]")} {todo}',
        f'{mk("[")}<u>{link}</u>{mk("](…)")}', f'{mk("|")} {table} {mk("|")}',
    ])
    ticket_notes = re.sub(r'::(.+?)::', lambda m: mk('::') + f'<mark>{m[1]}</mark>' + mk('::'),
                          re.sub(r'\*\*(.+?)\*\*', lambda m: mk('**') + f'<b>{m[1]}</b>' + mk('**'), tk['notes']))
    steps = ''.join(
        f'<li class="{"done" if done else ""}"><button class="box" type="button" aria-pressed="{"true" if done else "false"}" aria-label="{t["check"]}: {s}"></button>{s}</li>' for s, done in tk['steps']
    )
    signals = ''.join(
        f'<li>{sig(mark)}{name}</li>'
        for mark, name in zip(['progress', 'delegated', 'appointment', 'important'], t['signals'])
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
    demo = t['more_demo']
    ring = '<span class="o"></span>'
    demos = [
        # Zen: the card edge to edge in a little screen, nothing round it.
        '<div class="demo zen"><div class="screen-mini">'
        + ''.join(f'<p>{ring}<span>{x}</span></p>' for x in demo['zen']) + '<p>' + ring + '</p></div></div>',
        # Quick Find: its field with a word typed, a caret blinking after it, and what it finds.
        f'<div class="demo find"><div class="field">{icon("search")}{demo["find"][0]}<span class="caret"></span></div>'
        + ''.join(f'<p>{ring}<span>{x}</span></p>' for x in demo['find'][1]) + '</div>',
        # Calendar: the day's events by their calendars' dots, a task of the day under them.
        '<div class="demo cal">'
        + ''.join(f'<p><span class="dot" style="background:{c}"></span><span class="at">{at}</span><span>{x}</span></p>' for at, x, c in demo['cal'])
        + '</div>',
    ]
    more = ''.join(
        f'<div class="paper {paper} small"><div class="head">{icon(mark)}{name}</div><p>{say}</p>{d}</div>'
        for (mark, name, say), paper, d in zip(t['more'], ['white', 'cream', 'kraft'], demos)
    )
    try_words = json.dumps({
        'base': t['try_base'], 'evening': t['evening_word'], 'when': t['when_word'],
        'today': t['today_word'], 'tomorrow': t['tomorrow_word'], 'seed': t['try_seed'],
        'icons': {k: icon(v).replace('{base}', base) for k, v in
                  {'today': 'today', 'moon': 'darkThemeFilled', 'bell': 'reminderFilled', 'star': 'favoriteFilled', 'inbox': 'export'}.items()},
    }, ensure_ascii=False).replace('"', '&quot;')
    examples = ''.join(f'<button type="button" class="example">{e}</button>' for e in t['try_examples'])
    marks = {'s1': sig('progress'), 's2': sig('delegated'), 's5': sig('pending')}
    glyphs = {'today': icon('today'), 'bell': icon('reminderFilled'), 'cloud': icon('backup'),
              'knight': icon('knight'), **marks}
    points = ''.join(
        f'<li class="row"><button class="signal" aria-pressed="false" aria-label="{t["check"]}: {title}">'
        f'{SIGNAL}</button><div><div class="title">{title}</div>'
        f'<div class="print">{re.sub(r"(\{\w+\}[^{]*?)(?= ?\{|$)", r"<i>\1</i>", say).format(**glyphs)}</div></div></li>'
        for title, say in t['points']
    )
    notes = ''.join(
        f'<p class="pen-note {side}" style="--x:{x}%;--y:{y}%;--r:{r}deg">{ARROW}<span>{words}</span></p>'
        for words, (side, x, y, r) in zip(t['notes'], NOTES)
    )
    gtd = ''.join(f'<li><b>{name}</b><span>{say}</span></li>' for name, say in t['gtd'])
    sample_rows = ''.join(row(t, title, '', done) for title, _, done in t['tasks'][:3])
    pre = 'ru/' if lang == 'ru' else ''
    page = head(lang, t['title'], t['desc'], '', base) + f'''<body>
{bar(t, base, lang, home)}
<main>
<section class="hero"><div class="wrap hero-in">
<div class="hero-words">
<h1 class="written">{''.join(f'<span class="pen" style="--i:{i}">{line}</span>' for i, line in enumerate(t['h1'].split('<br>'))).replace('<u>', '<span class="under">').replace('</u>', UNDER + '</span>')}</h1>
<p class="lede"><b>{t['lede'][0]}</b> {t['lede'][1]}</p>
<span class="button soon"><svg class="icon" viewBox="0 0 17 20" aria-hidden="true"><path fill="currentColor" d="M14.07 10.63c-.02-2.33 1.9-3.45 1.99-3.51-1.08-1.58-2.77-1.8-3.37-1.82-1.43-.15-2.8.84-3.53.84-.73 0-1.85-.82-3.05-.8-1.57.03-3.02.92-3.83 2.33-1.63 2.83-.42 7.02 1.17 9.32.78 1.12 1.71 2.38 2.93 2.34 1.18-.05 1.62-.76 3.05-.76 1.42 0 1.82.76 3.06.74 1.27-.03 2.07-1.14 2.84-2.27.9-1.31 1.27-2.58 1.29-2.64-.03-.01-2.47-.95-2.49-3.77zM11.77 3.79c.65-.79 1.09-1.88.97-2.97-.94.04-2.07.62-2.74 1.41-.6.7-1.13 1.81-.99 2.88 1.05.08 2.11-.53 2.76-1.32z"/></svg>{t['cta']}</span>
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

<section class="part" id="real"><div class="wrap">
<div class="shelf">{iphones}</div>
</div></section>

<section class="part features"><div class="wrap">

<article class="feature flip" id="why">
<div class="say"><h2>{t['why_h']}</h2><p>{t['why_say']}</p></div>
<div class="show"><div class="paper why"><div class="why-head">{icon('favoriteFilled')}{t['points_h']}<span class="count">{len(t['points'])}</span></div><ul class="rows">{points}</ul></div>
</div>
</article>

<article class="feature" id="smart">
<div class="say"><h2>{t['smart_h']}</h2><p>{t['try_say']}</p></div>
<div class="show">
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
</article>

<article class="feature flip" id="ticket">
<div class="say"><h2>{t['ticket_h']}</h2><p>{t['ticket_say']}</p>
<h3>{t['md_h']}</h3><p>{t['md_say']}</p><ul class="md">{md}</ul></div>
<div class="show">
<div class="ticket-wrap"><div class="paper ticket">
<h4 class="row"><button class="signal" type="button" aria-pressed="false" aria-label="{t['check']}: {tk['title']}">{SIGNAL}</button><span class="title">{tk['title']}</span></h4>
<p class="notes">{ticket_notes}</p>
<ul class="steps">{steps}</ul>
<div class="stub">
<div class="tags">{''.join(f'<span>{x}</span>' for x in tk['tags'])}</div>
<div class="when"><span class="star">{icon('favoriteFilled')}</span>{tk['when']}{icon('reminderFilled')}21:30<span class="marks">{icon('flagFilled')}</span></div>
</div>
</div></div>
</div>
</article>

<article class="feature" id="signals">
<div class="say"><h2>{t['signals_h']}</h2><p>{t['signals_say']}</p></div>
<div class="show">
<div class="taped"><span class="tape"></span><p class="note-title">{t['signals_note'][0]}</p>
<p class="complete">{sig('done')}{t['signals_note'][1]}</p><ul class="sigs">{signals}</ul><p class="more">{t['signals_note'][2]}</p></div>
</div>
</article>

<article class="feature wide" id="lists">
<div class="say"><h2>{t['lists_h']}</h2><p>{t['lists_say']}</p></div>
<div class="deck">{lists}</div>
</article>

<article class="feature trio">
<h2>{t['more_h']}</h2><p class="lead">{t['more_say']}</p>
<div class="cards3">{more}</div>
</article>

<article class="feature" id="mac">
<div class="say"><h2>{t['cap']['mac'][0]}</h2><p>{t['real_say']}</p></div>
<div class="show"><div class="macs">
<img src="{base}img/{lang}-mac-5.webp" alt="" width="2240" height="1400" loading="lazy">
<img src="{base}img/{lang}-mac-2.webp" alt="" width="2240" height="1400" loading="lazy">
<img src="{base}img/{lang}-mac-1.webp" alt="{t['mac_alt']}" width="2240" height="1400" loading="lazy">
</div></div>
</article>

<article class="feature pair">
<div class="say" id="yours"><h2>{t['yours_h']}</h2><p>{t['yours_say']}</p>
<div class="swatches">{desks}</div>
<div class="swatches inks">{inks}</div>
<p class="named"><span data-for="desk" aria-live="polite"></span> · <span data-for="inkpick" aria-live="polite"></span></p>
</div>
<div class="show" id="kept">
<div class="paper kept">
<h3>{icon('lock')}{t['kept_h']}</h3><ul>{kept}</ul><p><a href="{base}{pre}privacy/">{t['kept_link']}</a></p>
</div>
</div>
</article>

<article class="feature gtd-row" id="knight">
<h2>{t['gtd_h']}</h2><p class="lead">{t['gtd_say']}</p>
<ol class="gtd">{gtd}</ol>
<div class="gtd-foot">{icon('knight', 'icon big')}<p>{t['gtd_knight']}</p><span class="button soon"><svg class="icon" viewBox="0 0 17 20" aria-hidden="true"><path fill="currentColor" d="M14.07 10.63c-.02-2.33 1.9-3.45 1.99-3.51-1.08-1.58-2.77-1.8-3.37-1.82-1.43-.15-2.8.84-3.53.84-.73 0-1.85-.82-3.05-.8-1.57.03-3.02.92-3.83 2.33-1.63 2.83-.42 7.02 1.17 9.32.78 1.12 1.71 2.38 2.93 2.34 1.18-.05 1.62-.76 3.05-.76 1.42 0 1.82.76 3.06.74 1.27-.03 2.07-1.14 2.84-2.27.9-1.31 1.27-2.58 1.29-2.64-.03-.01-2.47-.95-2.49-3.77zM11.77 3.79c.65-.79 1.09-1.88.97-2.97-.94.04-2.07.62-2.74 1.41-.6.7-1.13 1.81-.99 2.88 1.05.08 2.11-.53 2.76-1.32z"/></svg>{t['cta']}</span></div>
</article>

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
<h2>Как удалить всё?</h2>
<p>Смотрите <a href="../privacy/">политику конфиденциальности</a>: что удалить в приложении и в iCloud.</p>
'''),
}


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
write(SITE / '.nojekyll', '')
write(SITE / '404.html', '<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=/taskward/"><title>Taskward</title>')
write(SITE / 'sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
      + ''.join(f'<url><loc>{URL}{p}</loc></url>' for p in ['', 'privacy/', 'support/', 'ru/', 'ru/privacy/', 'ru/support/'])
      + '</urlset>\n')
print('written')
