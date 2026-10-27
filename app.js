// Taskward's site: tasks checked off at a tap, a day written into a new card's title, and the desk and ink picked.
(() => {
  const root = document.documentElement;
  const still = matchMedia('(prefers-reduced-motion: reduce)');

  // A task's circle: a tap checks it off, and back on.
  document.querySelectorAll('.row .signal').forEach((circle) => {
    circle.addEventListener('click', () => {
      const row = circle.closest('.row');
      const done = row.classList.toggle('done');
      circle.setAttribute('aria-pressed', String(done));
    });
  });

  // A day written into the new card's title: typed out, marked as it is read, and the
  // card's foot set from it — one phrase after another while the card is in sight.
  const card = document.querySelector('.newcard');
  if (card) {
    const phrases = JSON.parse(card.dataset.phrases);
    const typed = card.querySelector('.typed');
    const foot = card.querySelector('.chip');
    const blank = foot.innerHTML;
    const wait = (ms) => new Promise((done) => setTimeout(done, ms));
    let seen = false;
    let running = false;

    const show = (title, phrase, marked) => {
      typed.textContent = '';
      typed.append(title);
      if (phrase) {
        if (marked) {
          const mark = document.createElement('mark');
          mark.textContent = phrase;
          typed.append(mark);
        } else {
          typed.append(phrase);
        }
      }
    };
    const setFoot = (html) => {
      foot.style.opacity = 0;
      setTimeout(() => { foot.innerHTML = html; foot.style.opacity = 1; }, 180);
    };

    const play = async () => {
      if (running) return;
      running = true;
      for (let i = 0; seen; i = (i + 1) % phrases.length) {
        const { title, phrase, foot: html } = phrases[i];
        setFoot(blank);
        for (let n = 0; n <= title.length && seen; n++) {
          show(title.slice(0, n), '', false);
          await wait(70);
        }
        for (let n = 1; n <= phrase.length && seen; n++) {
          show(title, phrase.slice(0, n), false);
          await wait(70);
        }
        if (!seen) break;
        show(title, phrase, true);
        setFoot(html);
        await wait(2600);
        for (let n = title.length + phrase.length; n >= 0 && seen; n -= 2) {
          show(title.slice(0, Math.min(n, title.length)), phrase.slice(0, Math.max(0, n - title.length)), n > title.length + phrase.length - 2);
          await wait(18);
        }
        await wait(300);
      }
      running = false;
    };

    if (still.matches) {
      show(phrases[0].title, phrases[0].phrase, true);
      foot.innerHTML = phrases[0].foot;
    } else {
      new IntersectionObserver(([entry]) => {
        seen = entry.isIntersecting;
        if (seen) play();
      }, { threshold: 0.4 }).observe(card);
    }
  }

  // The desk and the ink picked: the page itself takes them, and keeps them.
  const keep = (key, value) => { try { localStorage.setItem(key, value); } catch (_) { /* none kept */ } };
  const kept = (key) => { try { return localStorage.getItem(key); } catch (_) { return null; } };
  const pick = (group, attr, key) => {
    const buttons = document.querySelectorAll(`[data-${group}]`);
    const named = document.querySelector(`.named[data-for="${group}"]`);
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
})();
