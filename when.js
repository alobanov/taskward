// A day and a time read off a task's title, in Russian and English — the app's own rules
// (lib/utils/when_words.dart), carried over: the first day named, with a time or «вечером»
// next to it; a time alone is today's, tomorrow's once gone by; a weekday is the next one,
// today's a week off; a date gone by this year is next year's.
window.WhenWords = (() => {
  const L = '(?<![\\p{L}\\p{N}])';
  const R = '(?![\\p{L}\\p{N}])';
  const re = (body) => new RegExp(L + body + R, 'giu');

  const ruDays = ['понедельник', 'вторник', 'сред[ау]', 'четверг', 'пятниц[ау]', 'суббот[ау]', 'воскресенье'];
  const enDays = ['mon(?:day)?', 'tue(?:s|sday)?', 'wed(?:nesday)?', 'thu(?:rs|rsday)?', 'fri(?:day)?', 'sat(?:urday)?', 'sun(?:day)?'];
  const allDays = [...ruDays, ...enDays];
  const ruMonths = ['январ', 'феврал', 'март', 'апрел', 'ма', 'июн', 'июл', 'август', 'сентябр', 'октябр', 'ноябр', 'декабр'];
  const enMonths = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'];

  const evening = re('(?:вечером|this evening|tonight|in the evening)');
  const relative = re('(сегодня|завтра|послезавтра|today|tomorrow|tmr|day after tomorrow)');
  const inDays = re('(?:через|in)\\s+(\\d{1,3}|одн[уи]|один|два|две|три|четыре|пять|a|an|one|two|three)?\\s*(дн[еяи]й?|день|дня|недел[юиь]|недели|недель|days?|weeks?)');
  const weekday = re('(?:(?:в|во|on)\\s+)?((?:следующ(?:ий|ую|ее)|next)\\s+)?(' + allDays.map((d) => '(?:' + d + ')').join('|') + ')');
  const ruDate = re('(\\d{1,2})\\s+(января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)');
  const enDate = re('(?:(\\d{1,2})(?:st|nd|rd|th)?\\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*|(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\\s+(\\d{1,2})(?:st|nd|rd|th)?)');
  const dotted = re('(\\d{1,2})\\.(\\d{1,2})(?:\\.(\\d{4}|\\d{2}))?');
  const time = re('(?:(?:в|at|@)\\s*(\\d{1,2})(?:[:.](\\d{2}))?(?:\\s*(утра|дня|вечера|ночи|am|pm|a\\.m\\.|p\\.m\\.))?|(\\d{1,2})(?:[:.](\\d{2}))?\\s*(am|pm|утра|вечера|ночи)|(\\d{1,2}):(\\d{2}))');

  const day0 = (d) => new Date(d.getFullYear(), d.getMonth(), d.getDate());
  const add = (d, n) => new Date(d.getFullYear(), d.getMonth(), d.getDate() + n);
  const weekdayOf = (d) => ((d.getDay() + 6) % 7) + 1; // Monday 1 … Sunday 7

  function on(today, d, month, year) {
    const make = (y) => {
      if (month < 1 || month > 12 || d < 1) return null;
      const date = new Date(y, month - 1, d);
      return date.getMonth() === month - 1 ? date : null;
    };
    if (year != null) return make(year);
    const day = make(today.getFullYear());
    if (!day) return null;
    return day < today ? make(today.getFullYear() + 1) : day;
  }

  function* days(text, today) {
    for (const m of text.matchAll(relative)) {
      const w = m[1].toLowerCase();
      const ahead = w === 'сегодня' || w === 'today' ? 0 : (w === 'завтра' || w === 'tomorrow' || w === 'tmr' ? 1 : 2);
      yield [m.index, m.index + m[0].length, add(today, ahead)];
    }
    for (const m of text.matchAll(inDays)) {
      const w = (m[1] || '').toLowerCase();
      const n = ({ '': 1, a: 1, an: 1, one: 1, 'один': 1, 'одну': 1, 'одни': 1, 'два': 2, 'две': 2, two: 2, 'три': 3, three: 3, 'четыре': 4, 'пять': 5 })[w] ?? (parseInt(w, 10) || 1);
      const unit = m[2].toLowerCase();
      const week = unit.startsWith('недел') || unit.startsWith('week');
      yield [m.index, m.index + m[0].length, add(today, n * (week ? 7 : 1))];
    }
    for (const m of text.matchAll(weekday)) {
      const word = m[2].toLowerCase();
      const index = allDays.findIndex((d) => new RegExp('^(?:' + d + ')$', 'iu').test(word));
      const target = (index % 7) + 1;
      let ahead = (target - weekdayOf(today) + 7) % 7;
      if (ahead === 0) ahead = 7;
      if (m[1] && ahead < 7) ahead += 7;
      yield [m.index, m.index + m[0].length, add(today, ahead)];
    }
    for (const m of text.matchAll(ruDate)) {
      const name = m[2].toLowerCase();
      const month = ruMonths.findIndex((p) => name.startsWith(p)) + 1;
      const day = on(today, parseInt(m[1], 10), month, null);
      if (day) yield [m.index, m.index + m[0].length, day];
    }
    for (const m of text.matchAll(enDate)) {
      const name = (m[2] || m[3]).toLowerCase();
      const day = on(today, parseInt(m[1] || m[4], 10), enMonths.indexOf(name) + 1, null);
      if (day) yield [m.index, m.index + m[0].length, day];
    }
    for (const m of text.matchAll(dotted)) {
      const y = m[3] ? (m[3].length === 2 ? 2000 + parseInt(m[3], 10) : parseInt(m[3], 10)) : null;
      const day = on(today, parseInt(m[1], 10), parseInt(m[2], 10), y);
      if (day) yield [m.index, m.index + m[0].length, day];
    }
  }

  function* times(text) {
    for (const m of text.matchAll(time)) {
      const h = parseInt(m[1] || m[4] || m[7], 10);
      const min = parseInt(m[2] || m[5] || m[8] || '0', 10);
      const part = (m[3] || m[6] || '').toLowerCase();
      if (min > 59) continue;
      let hour = h;
      if (['am', 'a.m.', 'утра'].includes(part)) hour = h === 12 ? 0 : h;
      else if (['pm', 'p.m.', 'вечера', 'дня'].includes(part)) hour = h < 12 ? h + 12 : h;
      else if (part === 'ночи') hour = h >= 6 && h < 12 ? h + 12 : (h === 12 ? 0 : h);
      if (hour > 23 || (part && h > 12)) continue;
      yield [m.index, m.index + m[0].length, hour * 60 + min];
    }
  }

  function find(text, now = new Date(), dismissed = new Set()) {
    const today = day0(now);
    const minutesNow = now.getHours() * 60 + now.getMinutes();
    const kept = (s, e) => !dismissed.has(text.slice(s, e).toLowerCase());
    const ds = [...days(text, today)].filter(([s, e]) => kept(s, e)).sort((a, b) => a[0] - b[0]);
    const ts = [...times(text)].filter(([s, e]) => kept(s, e));
    const es = [...text.matchAll(evening)].map((m) => [m.index, m.index + m[0].length]);
    const next = (end, start) => end <= start && text.slice(end, start).trim() === '';
    if (ds.length) {
      let [start, end, day] = ds[0];
      let isEvening = false;
      let minutes = null;
      for (let grown = true; grown;) {
        grown = false;
        for (const [s, e, m] of ts) {
          if (minutes === null && (next(end, s) || next(e, start))) {
            minutes = m; start = Math.min(s, start); end = Math.max(e, end); grown = true;
          }
        }
        for (const [s, e] of es) {
          if (!isEvening && (next(end, s) || next(e, start))) {
            isEvening = true; start = Math.min(s, start); end = Math.max(e, end); grown = true;
          }
        }
      }
      if (!kept(start, end)) return null;
      return { start, end, day, evening: isEvening, minutes };
    }
    if (ts.length) {
      const [start, end, minutes] = ts[0];
      return { start, end, day: minutes <= minutesNow ? add(today, 1) : today, evening: false, minutes };
    }
    if (es.length) return { start: es[0][0], end: es[0][1], day: today, evening: true, minutes: null };
    return null;
  }

  const without = (text, f) => (text.slice(0, f.start) + ' ' + text.slice(f.end))
    .replace(/\s+/g, ' ').trim().replace(/\s+([,.!?;:])/g, '$1');

  return { find, without, add, day0 };
})();
