// Taskward's site: tasks checked off at a tap, a day written into a new card's title, and the desk and ink picked.
(() => {
  const root = document.documentElement;
  const still = matchMedia('(prefers-reduced-motion: reduce)');

  // A ticket's steps, checked off and back on.
  document.querySelectorAll('.ticket .steps .box').forEach((box) => {
    box.addEventListener('click', () => {
      const done = box.closest('li').classList.toggle('done');
      box.setAttribute('aria-pressed', String(done));
    });
  });

  // A task's circle: a tap checks it off, and back on.
  document.querySelectorAll('.row .signal').forEach((circle) => {
    circle.addEventListener('click', () => {
      const row = circle.closest('.row');
      const done = row.classList.toggle('done');
      circle.setAttribute('aria-pressed', String(done));
    });
  });

  // Try it: a task written on the new card, its day read as it is written — the app's own
  // rules (when.js) — marked under the highlighter, set at the card's foot, and on Return
  // the task laid on its card: the Inbox with no day, Today for today, Upcoming for later.
  const tryIt = document.querySelector('.try');
  if (tryIt) {
    const words = JSON.parse(tryIt.dataset.words);
    const lang = tryIt.dataset.lang;
    const form = tryIt.querySelector('form');
    const input = form.querySelector('.title');
    const mirror = form.querySelector('.mirror');
    const chip = form.querySelector('.chip');
    const lists = Object.fromEntries([...tryIt.querySelectorAll('.mini')].map((m) => [m.dataset.list, m]));
    const dismissed = new Set();
    let found = null;
    const esc = (t) => t.replace(/&/g, '&amp;').replace(/</g, '&lt;');
    const pad = (n) => String(n).padStart(2, '0');
    const clock = (m) => `${pad(Math.floor(m / 60))}:${pad(m % 60)}`;
    const today = () => WhenWords.day0(new Date());
    const dayName = (d) => {
      const ahead = Math.round((d - today()) / 864e5);
      if (ahead === 0) return words.today;
      if (ahead === 1) return words.tomorrow;
      const f = ahead < 7
        ? new Intl.DateTimeFormat(lang, { weekday: 'long' }).format(d)
        : new Intl.DateTimeFormat(lang, { day: 'numeric', month: 'short' }).format(d);
      return f.charAt(0).toUpperCase() + f.slice(1);
    };
    const whenOf = (f) => {
      if (!f) return `<span class="muted">${words.icons.today}${words.when}</span>`;
      const isToday = Math.round((f.day - today()) / 864e5) === 0;
      const icon = f.evening ? words.icons.moon : (isToday ? `<span class="star">${words.icons.star}</span>` : words.icons.today);
      const name = f.evening && isToday ? words.evening : dayName(f.day);
      const bell = f.minutes != null ? `${words.icons.bell}<span>${clock(f.minutes)}</span>` : '';
      return `${icon}<span>${name}</span>${bell}`;
    };
    const draw = () => {
      const text = input.value;
      found = WhenWords.find(text, new Date(), dismissed);
      mirror.innerHTML = found
        ? esc(text.slice(0, found.start)) + '<mark>' + esc(text.slice(found.start, found.end)) + '</mark>' + esc(text.slice(found.end))
        : esc(text);
      mirror.scrollLeft = input.scrollLeft;
      chip.innerHTML = whenOf(found);
      form.classList.toggle('dated', !!found);
    };
    const place = (title, f, fresh) => {
      const ahead = f ? Math.round((f.day - today()) / 864e5) : null;
      const list = ahead === null ? 'inbox' : (ahead <= 0 ? 'today' : 'upcoming');
      const li = document.createElement('li');
      li.className = 'row' + (fresh ? ' fresh' : '');
      const print = f ? `<div class="print">${list === 'upcoming' ? `<span>${esc(dayName(f.day))}</span>` : ''}${f.evening ? `<span>${words.icons.moon}</span>` : ''}${f.minutes != null ? `<span>${words.icons.bell}${clock(f.minutes)}</span>` : ''}</div>` : '';
      li.innerHTML = `<button class="signal" type="button" aria-pressed="false"><svg viewBox="0 0 24 24"><circle class="ring" cx="12" cy="12" r="9.2"/><circle class="fill" cx="12" cy="12" r="9.2"/></svg></button><div><div class="title">${esc(title)}</div>${print}</div>`;
      li.querySelector('.signal').addEventListener('click', () => {
        li.setAttribute('aria-pressed', String(li.classList.toggle('done')));
      });
      const rows = lists[list].querySelector('.rows');
      rows.prepend(li);
      while (rows.children.length > 4) rows.lastElementChild.remove();
      if (fresh) {
        lists[list].classList.remove('lifted');
        void lists[list].offsetWidth;
        lists[list].classList.add('lifted');
      }
    };
    for (const [list, titles] of Object.entries(words.seed)) {
      for (const title of titles) lists[list].querySelector('.rows').append(Object.assign(document.createElement('li'), {
        className: 'row', innerHTML: `<span class="signal"><svg viewBox="0 0 24 24"><circle class="ring" cx="12" cy="12" r="9.2"/><circle class="fill" cx="12" cy="12" r="9.2"/></svg></span><div><div class="title">${esc(title)}</div></div>`,
      }));
    }
    input.addEventListener('input', () => { dismissed.clear(); draw(); });
    input.addEventListener('scroll', () => { mirror.scrollLeft = input.scrollLeft; });
    // A tap in the words marked: they are a title's words again.
    input.addEventListener('click', () => {
      const at = input.selectionStart;
      if (found && input.selectionStart === input.selectionEnd && at > found.start && at < found.end) {
        dismissed.add(input.value.slice(found.start, found.end).toLowerCase());
        draw();
      }
    });
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const text = input.value.trim();
      if (!text) { input.focus(); return; }
      const title = found ? (WhenWords.without(input.value, found) || text) : text;
      place(title, found, true);
      input.value = '';
      dismissed.clear();
      draw();
    });
    tryIt.querySelectorAll('.example').forEach((b) => b.addEventListener('click', () => {
      input.value = words.base + b.textContent;
      dismissed.clear();
      draw();
      input.focus({ preventScroll: true });
      input.setSelectionRange(input.value.length, input.value.length);
    }));
    draw();
  }

  // The desk and the ink picked: the page itself takes them, and keeps them.
  const keep = (key, value) => { try { localStorage.setItem(key, value); } catch (_) { /* none kept */ } };
  const kept = (key) => { try { return localStorage.getItem(key); } catch (_) { return null; } };
  const pick = (group, attr, key) => {
    const buttons = document.querySelectorAll(`[data-${group}]`);
    const named = document.querySelector(`[data-for="${group}"]`);
    const choose = (value) => {
      if (value === 'default') delete root.dataset[attr]; else root.dataset[attr] = value;
      buttons.forEach((b) => {
        const on = b.dataset[group] === value;
        b.setAttribute('aria-pressed', String(on));
        if (on && named) named.textContent = b.getAttribute('aria-label');
      });
    };
    buttons.forEach((b) => b.addEventListener('click', () => {
      choose(b.dataset[group]);
      keep(key, b.dataset[group]);
    }));
    choose(kept(key) || 'default');
  };
  pick('desk', 'desk', 'taskward-desk');
  pick('inkpick', 'ink', 'taskward-ink');

  // The calendar: this month on a card, its days marked by the demo's events and tasks, put
  // by how far each is from today; a day tapped is ringed, and what it holds is shown under
  // the tear line — the old faded out, then the new in.
  const month = document.querySelector('.month');
  if (month) {
    const { days, empty } = JSON.parse(month.dataset.cal);
    const lang = month.dataset.lang;
    const first = lang === 'ru' ? 1 : 0;
    const day0 = (d) => new Date(d.getFullYear(), d.getMonth(), d.getDate());
    const today = day0(new Date());
    const key = (d) => `${d.getFullYear()}-${d.getMonth()}-${d.getDate()}`;
    const plus = (d, n) => new Date(d.getFullYear(), d.getMonth(), d.getDate() + n);
    const held = new Map(days.map(([off, ev, tasks]) => [key(plus(today, off)), { ev, tasks }]));
    const cap = (w) => w.charAt(0).toUpperCase() + w.slice(1);
    const el = (tag, cls, text) => {
      const e = document.createElement(tag);
      if (cls) e.className = cls;
      if (text != null) e.textContent = text;
      return e;
    };
    const head = month.querySelector('.month-head');
    head.querySelector('b').textContent = cap(new Intl.DateTimeFormat(lang, { month: 'long' }).format(today));
    head.querySelector('span').textContent = String(today.getFullYear());
    const grid = month.querySelector('.days');
    const start = new Date(today.getFullYear(), today.getMonth(), 1);
    const back = (start.getDay() - first + 7) % 7;
    const weekday = new Intl.DateTimeFormat(lang, { weekday: 'short' });
    const weekend = (d) => d.getDay() === 0 || d.getDay() === 6;
    for (let i = 0; i < 7; i++) {
      const d = plus(start, i - back);
      grid.append(el('div', 'wd' + (weekend(d) ? ' we' : ''), cap(weekday.format(d).replace('.', ''))));
    }
    const dayView = month.querySelector('.day');
    const named = new Intl.DateTimeFormat(lang, { weekday: 'long', month: 'long', day: 'numeric' });
    let picked = null;
    const show = (d) => {
      const it = held.get(key(d)) || { ev: [], tasks: [] };
      dayView.querySelector('h4').textContent = cap(named.format(d));
      const list = dayView.querySelector('ul');
      list.replaceChildren();
      it.ev.forEach(([at, title, c]) => {
        const li = el('li');
        const dot = el('span', 'dot');
        dot.style.background = c;
        li.append(dot, el('span', 'at', at), el('span', null, title));
        list.append(li);
      });
      it.tasks.forEach(([title, done]) => {
        const li = el('li', done ? 'done' : null);
        li.append(el('span', 'o'), el('span', null, title));
        list.append(li);
      });
      if (!it.ev.length && !it.tasks.length) list.append(el('li', 'none', empty));
    };
    const pickDay = (cell, d) => {
      if (picked === cell) return;
      picked?.classList.remove('picked');
      picked?.setAttribute('aria-selected', 'false');
      cell.classList.add('picked');
      cell.setAttribute('aria-selected', 'true');
      const opening = picked === null;
      picked = cell;
      if (opening || still.matches) return show(d);
      dayView.classList.add('gone');
      setTimeout(() => { show(d); dayView.classList.remove('gone'); }, 160);
    };
    for (let i = 0; i < 42; i++) {
      const d = plus(start, i - back);
      const cell = el('button', 'd');
      cell.type = 'button';
      cell.setAttribute('role', 'gridcell');
      cell.setAttribute('aria-label', named.format(d));
      if (d.getMonth() !== today.getMonth()) cell.classList.add('out');
      if (weekend(d)) cell.classList.add('we');
      if (+d === +today) cell.classList.add('now');
      const dots = el('span', 'dots');
      const it = held.get(key(d));
      if (it) {
        [...new Set(it.ev.map((e) => e[2]))].slice(0, it.tasks.length ? 2 : 3).forEach((c) => {
          const dot = el('i');
          dot.style.background = c;
          dots.append(dot);
        });
        if (it.tasks.length) dots.append(el('i', it.tasks.some((t) => !t[1]) ? null : 'idle'));
      }
      cell.append(el('span', 'n', String(d.getDate())), dots);
      cell.addEventListener('click', () => pickDay(cell, d));
      grid.append(cell);
      if (+d === +today) pickDay(cell, d);
    }
  }
})();
