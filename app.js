/* awesome-ai-blackfriday — vanilla JS, no build step */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));

  const TODAY = new Date();
  TODAY.setHours(0, 0, 0, 0);

  const state = { q: '', cat: 'All', sort: 'discount', hideExpired: true };

  const daysLeft = (iso) => {
    if (!iso) return null;
    const d = new Date(iso + 'T00:00:00');
    return Math.round((d - TODAY) / 86400000);
  };

  const fmtDate = (iso) => {
    if (!iso) return '';
    const d = new Date(iso + 'T12:00:00');
    return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short' });
  };

  const endCls = (d) => {
    if (d === null) return 'open';
    if (d < 0) return 'gone';
    if (d <= 2) return 'hot';
    if (d <= 7) return 'warm';
    return '';
  };

  const endLabel = (deal) => {
    const d = daysLeft(deal.ends);
    if (deal.ends && d < 0) return 'Ended ' + fmtDate(deal.ends);
    if (d === 0) return 'Ends today';
    if (d === 1) return 'Ends tomorrow';
    if (d !== null && d <= 14) return d + ' days left';
    if (deal.ends) return 'Ends ' + fmtDate(deal.ends);
    return 'No end date';
  };

  let DATA = null;

  /* ------------------------------------------------------------- boot */
  // try the JSON (keeps one source of truth), fall back to the generated
  // script when the page is opened from disk and fetch() is blocked
  fetch('data/deals.json', { cache: 'no-cache' })
    .then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); })
    .catch(() => {
      if (window.DEALS) return window.DEALS;
      throw new Error('no dataset');
    })
    .then((d) => { DATA = d; init(d); })
    .catch((e) => {
      $('#count').textContent = 'Could not load the deal data (' + e.message + ').';
      $('#grid').innerHTML = '<p class="empty">Serve the folder instead: <code>python3 -m http.server</code> then open localhost:8000.</p>';
    });

  function init(data) {
    const meta = data.meta;
    const deals = data.deals;

    $('#updated').textContent = 'Snapshot ' + new Date(meta.generated + 'T12:00:00')
      .toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
    $('#window').textContent = meta.checked_window;
    $('#foot-date').textContent = new Date(meta.generated + 'T12:00:00')
      .toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
    $('#bf-date').textContent = fmtDate(meta.black_friday) + ' 2026';
    $('#cm-date').textContent = fmtDate(meta.cyber_monday) + ' 2026';

    // stats
    const live = deals.filter((d) => d.status !== 'expired');
    const withDisc = live.filter((d) => typeof d.discount === 'number');
    // headline stats skip first-month teasers ($0.29 for a month isn't a real discount)
    const headline = withDisc.filter((d) => !(d.tags || []).includes('first-month'));
    const maxDisc = headline.reduce((a, b) => (b.discount > a.discount ? b : a), headline[0] || {});
    const endingSoon = live.filter((d) => { const n = daysLeft(d.ends); return n !== null && n >= 0 && n <= 7; });
    const avg = Math.round(headline.reduce((s, d) => s + d.discount, 0) / (headline.length || 1));
    const stats = [
      { v: live.length, l: 'deals tracked' },
      { v: avg + '%', l: 'average discount' },
      { v: (maxDisc.discount || 0) + '%', l: 'biggest: ' + (maxDisc.name || '—'), acid: true },
      { v: endingSoon.length, l: 'ending in 7 days' },
    ];
    $('#stats').innerHTML = stats.map((s) => `
      <div class="stat${s.acid ? ' acid' : ''}">
        <b>${esc(s.v)}</b><span>${esc(s.l)}</span>
      </div>`).join('');

    // ticker: top 8 by discount
    const tick = withDisc.slice().sort((a, b) => b.discount - a.discount).slice(0, 9);
    const line = tick.map((d) => `<span><b>${d.discount}%</b> ${esc(d.name)}</span>`).join('');
    $('#ticker').innerHTML = `<div class="ticker-track">${line}${line}</div>`;

    // category chips
    const cats = ['All', ...data.categories];
    const counts = cats.map((c) => (c === 'All' ? live.length : live.filter((d) => d.category === c).length));
    $('#cats').innerHTML = cats.map((c, i) => `
      <button class="chip" data-cat="${esc(c)}" aria-pressed="${c === 'All'}">${esc(c)}<small>${counts[i]}</small></button>`
    ).join('');
    $$('#cats .chip').forEach((b) => b.addEventListener('click', () => {
      state.cat = b.dataset.cat;
      $$('#cats .chip').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
      render();
    }));

    // tables
    $('#nodeal-table tbody').innerHTML = data.no_deal.map((n) => `
      <tr>
        <td><a href="${esc(n.url)}" target="_blank" rel="noopener">${esc(n.name)}</a></td>
        <td>${esc(n.note)}</td>
        <td>${esc(fmtDate(n.checked))}</td>
      </tr>`).join('');

    $('#watchlist').innerHTML = data.watchlist.map((w) => `
      <li><b><a href="${esc(w.url)}" target="_blank" rel="noopener">${esc(w.name)}</a></b>${esc(w.note)}</li>`
    ).join('');

    $('#always-on').innerHTML = data.always_on.map((a) => `
      <li><b><a href="${esc(a.url)}" target="_blank" rel="noopener">${esc(a.name)}</a></b>
      <span class="kind">${esc(a.kind)}</span><br>${esc(a.note)}</li>`
    ).join('');

    // controls
    $('#q').addEventListener('input', (e) => { state.q = e.target.value.trim().toLowerCase(); render(); });
    $('#sort').addEventListener('change', (e) => { state.sort = e.target.value; render(); });
    $('#hide-expired').addEventListener('change', (e) => { state.hideExpired = e.target.checked; render(); });
    $('#reset').addEventListener('click', () => {
      state.q = ''; state.cat = 'All';
      $('#q').value = '';
      $$('#cats .chip').forEach((x) => x.setAttribute('aria-pressed', String(x.dataset.cat === 'All')));
      render();
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === '/' && document.activeElement !== $('#q')) { e.preventDefault(); $('#q').focus(); }
      if (e.key === 'Escape' && document.activeElement === $('#q')) { $('#q').blur(); }
    });

    render();
  }

  /* ------------------------------------------------------------- render */
  function render() {
    if (!DATA) return;
    const all = DATA.deals;
    let list = all.slice();

    if (state.hideExpired) {
      list = list.filter((d) => { const n = daysLeft(d.ends); return n === null || n >= 0; });
    }
    if (state.cat !== 'All') list = list.filter((d) => d.category === state.cat);
    if (state.q) {
      const q = state.q;
      list = list.filter((d) =>
        [d.name, d.what, d.deal, d.category, d.code, d.audience, (d.tags || []).join(' ')]
          .filter(Boolean).join(' ').toLowerCase().includes(q));
    }

    // first-month teasers are ranked at half their headline number so a $0.29-for-30-days
    // offer doesn't outrank a year-long 55% cut
    const weight = (d) => {
      if (typeof d.discount !== 'number') return -1;
      return (d.tags || []).includes('first-month') ? d.discount * 0.5 : d.discount;
    };
    const sorters = {
      discount: (a, b) => weight(b) - weight(a) || a.name.localeCompare(b.name),
      ending: (a, b) => {
        const da = daysLeft(a.ends), db = daysLeft(b.ends);
        if (da === null) return 1; if (db === null) return -1;
        return da - db;
      },
      az: (a, b) => a.name.localeCompare(b.name),
      verified: (a, b) => (b.verified || '').localeCompare(a.verified || ''),
    };
    list.sort(sorters[state.sort] || sorters.discount);

    $('#count').textContent = `${list.length} of ${all.length} deals` +
      (state.cat !== 'All' ? ` · ${state.cat}` : '') +
      (state.q ? ` · “${state.q}”` : '');

    const filtered = state.cat !== 'All' || state.q || !state.hideExpired;
    $('#reset').hidden = !filtered;
    $('#empty').hidden = list.length > 0;

    $('#grid').innerHTML = list.map(card).join('');

    $$('.code').forEach((btn) => {
      btn.addEventListener('click', async () => {
        const code = btn.dataset.code;
        try {
          await navigator.clipboard.writeText(code);
        } catch {
          const ta = document.createElement('textarea');
          ta.value = code; document.body.appendChild(ta); ta.select();
          document.execCommand('copy'); ta.remove();
        }
        const hint = $('.hint', btn);
        btn.classList.add('copied');
        hint.textContent = 'copied';
        setTimeout(() => { btn.classList.remove('copied'); hint.textContent = 'copy code'; }, 1600);
      });
    });
  }

  function card(d) {
    const dl = daysLeft(d.ends);
    const cls = endCls(dl);
    const disc = typeof d.discount === 'number'
      ? `<div class="disc">${d.discount}%<span style="font-size:11px;opacity:.6"> off</span></div>`
      : `<div class="disc na">${d.status === 'perk' ? 'perk' : 'no %'}</div>`;

    const price = (d.price_before || d.price_after)
      ? `<div class="price">
           ${d.price_before ? `<span class="before">${esc(d.price_before)}</span><span class="arrow">→</span>` : ''}
           <span class="after">${esc(d.price_after || '')}</span>
         </div>` : '';

    const code = d.code
      ? `<div class="code-row"><button class="code" data-code="${esc(d.code)}" title="Click to copy">
           <span>${esc(d.code)}</span><span class="hint">copy code</span>
         </button></div>` : '';

    const tags = (d.tags || []).map((t) => t === 'editor-pick'
      ? '<span class="tagpill pick">Editor’s pick</span>'
      : `<span class="tagpill">${esc(t)}</span>`).join('');

    const endsTxt = d.ends_note && !d.ends ? d.ends_note : endLabel(d);
    const title = d.ends_note && d.ends ? ` title="${esc(d.ends_note)}"` : '';

    return `<article class="card${cls === 'hot' || cls === 'warm' ? ' ending' : ''}">
      <div class="card-head">
        <span class="cat">${esc(d.category)}</span>
        ${disc}
      </div>
      <h3>${esc(d.name)}</h3>
      <p class="what">${esc(d.what)}</p>
      <p class="deal">${esc(d.deal)}</p>
      ${price}
      ${code}
      ${d.renewal ? `<p class="renewal">${esc(d.renewal)}</p>` : ''}
      <div class="meta">
        <span class="ends ${cls}"${title}>${esc(endsTxt)}</span>
        ${tags}
      </div>
      <p class="src">
        <a href="${esc(d.url)}" target="_blank" rel="noopener">vendor ↗</a>
        <a href="${esc(d.source)}" target="_blank" rel="noopener">source · ${esc(fmtDate(d.verified))}</a>
      </p>
    </article>`;
  }
})();
