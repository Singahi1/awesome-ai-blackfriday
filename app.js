/* Awesome AI Deals — progressive enhancement for the generated static pages */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));

  const TODAY = new Date(document.body.dataset.snapshot || '2026-11-25T00:00:00');
  TODAY.setHours(0, 0, 0, 0);
  const VIEW = document.body.dataset.view || 'home';
  const CAMPAIGN = document.body.dataset.campaign || null;
  const state = { q: '', cat: 'All', sort: 'useful', hideStale: false };
  let DATA = null;

  const daysLeft = (iso) => iso ? Math.round((new Date(iso + 'T00:00:00') - TODAY) / 86400000) : null;
  const fmtDate = (iso, year = false) => {
    if (!iso) return '';
    return new Date(iso + 'T12:00:00').toLocaleDateString('en-GB', {
      day: 'numeric', month: 'short', ...(year ? { year: 'numeric' } : {})
    });
  };
  const endCls = (d) => {
    const n = daysLeft(d.valid_until);
    if (d.lifecycle === 'expired' || (n !== null && n < 0)) return 'gone';
    if (n === 0 || n === 1) return 'hot';
    if (n !== null && n <= 7) return 'warm';
    return n === null ? 'open' : '';
  };
  const endLabel = (d) => {
    const n = daysLeft(d.valid_until);
    if (d.lifecycle === 'expired') return 'Ended ' + fmtDate(d.valid_until);
    if (n === 0) return 'Ends today';
    if (n === 1) return 'Ends tomorrow';
    if (n !== null && n < 0) return 'Ended ' + fmtDate(d.valid_until);
    if (n !== null && n <= 14) return n + ' days left';
    return d.valid_until ? 'Ends ' + fmtDate(d.valid_until) : 'No end date';
  };

  fetch('data/deals.json', { cache: 'no-cache' })
    .then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); })
    .catch(() => {
      if (window.DEALS) return window.DEALS;
      throw new Error('no dataset');
    })
    .then((d) => { DATA = d; init(d); })
    .catch((e) => {
      $('#count').textContent = 'Could not load the deal data (' + e.message + ').';
      $('#grid').innerHTML = '<p class="empty">Serve the folder instead: <code>python3 -m http.server</code></p>';
    });

  function baseDeals(all) {
    if (VIEW === 'archive') return all.filter((d) => ['expired', 'archived'].includes(d.lifecycle));
    if (VIEW === 'campaign') return all.filter((d) => d.campaign === CAMPAIGN && ['live', 'announced'].includes(d.lifecycle));
    return all.filter((d) => d.lifecycle === 'live');
  }

  function init(data) {
    const meta = data.meta;
    const base = baseDeals(data.deals);
    $('#updated').textContent = 'Snapshot ' + fmtDate(meta.generated, true);
    $('#window') && ($('#window').textContent = meta.checked_window);
    $('#foot-date').textContent = fmtDate(meta.generated, true);
    $('#bf-date').textContent = fmtDate(meta.black_friday) + ' 2026';
    $('#cm-date').textContent = fmtDate(meta.cyber_monday) + ' 2026';

    const live = base.filter((d) => d.lifecycle === 'live');
    const top = [...live].sort((a, b) => (b.useful || 0) - (a.useful || 0))[0] || {};
    const ending = live.filter((d) => { const n = daysLeft(d.valid_until); return n !== null && n >= 0 && n <= 7; });
    const stale = live.filter((d) => d.verification === 'stale');
    let items;
    if (VIEW === 'archive') {
      items = [
        { v: base.length, l: 'expired offers' },
        { v: new Set(base.map((d) => d.campaign || 'other')).size, l: 'campaigns' },
        { v: fmtDate(base.map((d) => d.valid_until).filter(Boolean).sort().at(-1)), l: 'latest expiry', acid: true },
        { v: fmtDate(base.map((d) => d.valid_until).filter(Boolean).sort()[0]), l: 'oldest expiry' },
      ];
    } else if (VIEW === 'campaign') {
      items = [
        { v: live.length, l: 'live offers' },
        { v: top.useful || '—', l: 'top pick: ' + (top.name || '—'), acid: true },
        { v: ending.length, l: 'ending in 7 days' },
        { v: base.filter((d) => d.lifecycle === 'announced').length, l: 'announced' },
      ];
    } else {
      items = [
        { v: live.length, l: 'live deals' },
        { v: top.useful || '—', l: 'top pick: ' + (top.name || '—'), acid: true },
        { v: ending.length, l: 'ending in 7 days' },
        { v: stale.length, l: 'recheck due' },
      ];
    }
    $('#stats').innerHTML = items.map((s) => `<div class="stat${s.acid ? ' acid' : ''}"><b>${esc(s.v)}</b><span>${esc(s.l)}</span></div>`).join('');

    const tick = [...base].sort((a, b) => (b.useful || 0) - (a.useful || 0)).slice(0, 9);
    const line = tick.map((d) => `<span><b>${esc(d.useful || '—')}</b> ${esc(d.name)}</span>`).join('');
    $('#ticker').innerHTML = `<div class="ticker-track">${line}${line}</div>`;

    const counts = base.reduce((acc, d) => ({ ...acc, [d.category]: (acc[d.category] || 0) + 1 }), {});
    $('#cats').innerHTML = [`<button class="chip" data-cat="All" aria-pressed="true">All<small>${base.length}</small></button>`]
      .concat(data.categories.filter((c) => counts[c]).map((c) => `<button class="chip" data-cat="${esc(c)}" aria-pressed="false">${esc(c)}<small>${counts[c]}</small></button>`))
      .join('');
    $$('#cats .chip').forEach((b) => b.addEventListener('click', () => {
      state.cat = b.dataset.cat;
      $$('#cats .chip').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
      render();
    }));

    if ($('#nodeal-table tbody')) {
      $('#nodeal-table tbody').innerHTML = data.no_deal.map((n) => `<tr><td><a href="${esc(n.url)}" target="_blank" rel="noopener">${esc(n.name)}</a></td><td>${esc(n.note)}</td><td>${esc(fmtDate(n.last_verified))}</td></tr>`).join('');
    }
    if ($('#watchlist')) {
      $('#watchlist').innerHTML = data.watchlist.map((w) => `<li><b><a href="${esc(w.url)}" target="_blank" rel="noopener">${esc(w.name)}</a></b>${esc(w.note)}</li>`).join('');
    }
    if ($('#always-on')) {
      $('#always-on').innerHTML = data.always_on.map((a) => `<li><b><a href="${esc(a.url)}" target="_blank" rel="noopener">${esc(a.name)}</a></b><span class="kind">${esc(a.kind)}</span><br>${esc(a.note)}</li>`).join('');
    }

    $('#q').addEventListener('input', (e) => { state.q = e.target.value.trim().toLowerCase(); render(); });
    $('#sort').addEventListener('change', (e) => { state.sort = e.target.value; render(); });
    if ($('#hide-stale')) $('#hide-stale').addEventListener('change', (e) => { state.hideStale = e.target.checked; render(); });
    $('#reset').addEventListener('click', () => {
      state.q = ''; state.cat = 'All'; state.hideStale = false;
      $('#q').value = '';
      if ($('#hide-stale')) $('#hide-stale').checked = false;
      $$('#cats .chip').forEach((x) => x.setAttribute('aria-pressed', String(x.dataset.cat === 'All')));
      render();
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === '/' && document.activeElement !== $('#q')) { e.preventDefault(); $('#q').focus(); }
      if (e.key === 'Escape' && document.activeElement === $('#q')) $('#q').blur();
    });
    render();
  }

  function render() {
    if (!DATA) return;
    const base = baseDeals(DATA.deals);
    let list = base.slice();
    if (state.hideStale) list = list.filter((d) => d.verification !== 'stale');
    if (state.cat !== 'All') list = list.filter((d) => d.category === state.cat);
    if (state.q) {
      list = list.filter((d) => [d.name, d.what, d.deal, d.category, d.code, d.eligibility, d.campaign, (d.tags || []).join(' '), (d.regions || []).join(' ')]
        .filter(Boolean).join(' ').toLowerCase().includes(state.q));
    }
    const weight = (d) => typeof d.discount === 'number' ? ((d.tags || []).includes('first-month') ? d.discount * .5 : d.discount) : -1;
    const sorters = {
      useful: (a, b) => (b.useful || 0) - (a.useful || 0) || a.name.localeCompare(b.name),
      discount: (a, b) => weight(b) - weight(a) || a.name.localeCompare(b.name),
      ending: (a, b) => {
        const da = daysLeft(a.valid_until), db = daysLeft(b.valid_until);
        if (da === null) return 1; if (db === null) return -1; return da - db;
      },
      az: (a, b) => a.name.localeCompare(b.name),
      verified: (a, b) => (b.last_verified || '').localeCompare(a.last_verified || ''),
    };
    list.sort(sorters[state.sort] || sorters.useful);
    const noun = VIEW === 'archive' ? 'expired offers' : VIEW === 'campaign' ? 'campaign offers' : 'live deals';
    $('#count').textContent = `${list.length} of ${base.length} ${noun}` + (state.cat !== 'All' ? ` · ${state.cat}` : '') + (state.q ? ` · “${state.q}”` : '');
    $('#reset').hidden = !(state.cat !== 'All' || state.q || state.hideStale);
    $('#empty').hidden = list.length > 0;
    $('#grid').innerHTML = list.map(card).join('');
    $$('.code').forEach((btn) => btn.addEventListener('click', async () => {
      try { await navigator.clipboard.writeText(btn.dataset.code); }
      catch {
        const ta = document.createElement('textarea'); ta.value = btn.dataset.code;
        document.body.appendChild(ta); ta.select(); document.execCommand('copy'); ta.remove();
      }
      const hint = $('.hint', btn); btn.classList.add('copied'); hint.textContent = 'copied';
      setTimeout(() => { btn.classList.remove('copied'); hint.textContent = 'copy code'; }, 1600);
    }));
  }

  function card(d) {
    const cls = endCls(d);
    const disc = typeof d.discount === 'number'
      ? `<div class="disc">${d.discount}%<span style="font-size:11px;opacity:.6"> off</span></div>`
      : `<div class="disc na">${esc(d.offer_type || 'no %')}</div>`;
    const price = (d.price_before || d.price_after) ? `<div class="price">${d.price_before ? `<span class="before">${esc(d.price_before)}</span><span class="arrow">→</span>` : ''}<span class="after">${esc(d.price_after || '')}</span></div>` : '';
    const code = d.code ? `<div class="code-row"><button class="code" data-code="${esc(d.code)}" title="Click to copy"><span>${esc(d.code)}</span><span class="hint">copy code</span></button></div>` : '';
    const pills = [];
    if (d.sponsored) pills.push('<span class="tagpill pick">Partner</span>');
    if (d.lifecycle === 'announced') pills.push('<span class="tagpill">announced</span>');
    if (d.verification === 'stale') pills.push('<span class="tagpill stale">recheck due</span>');
    if (d.verification === 'conflicting') pills.push('<span class="tagpill stale">conflicting</span>');
    (d.tags || []).filter((t) => !['announced', 'partner', 'perk', 'expired'].includes(t)).forEach((t) => pills.push(t === 'editor-pick' ? '<span class="tagpill pick">Editor’s pick</span>' : `<span class="tagpill">${esc(t)}</span>`));
    if ((d.regions || []).length) pills.push(`<span class="tagpill">${esc(d.regions.join(', '))}</span>`);
    const evidenceType = (d.evidence || [{}])[0].type || 'tracker';
    const evidenceLabel = evidenceType.startsWith('vendor_') ? 'vendor' : 'tracker';
    return `<article class="card${cls === 'hot' || cls === 'warm' ? ' ending' : ''}${d.lifecycle === 'expired' ? ' expired-card' : ''}${d.verification === 'stale' ? ' stale-card' : ''}${d.sponsored ? ' sponsored' : ''}">
      <a class="stretched" href="${esc(d.url)}" target="_blank" rel="noopener" aria-label="Open ${esc(d.name)} offer"></a>
      <div class="card-head"><span class="cat">${esc(d.category)}</span>${disc}</div>
      <h3>${esc(d.name)}</h3><p class="what">${esc(d.what)}</p><p class="deal">${esc(d.deal)}</p>
      ${price}${code}${d.renewal ? `<p class="renewal">${esc(d.renewal)}</p>` : ''}
      <div class="meta"><span class="ends ${cls}" title="${esc(d.ends_note || '')}">${esc(endLabel(d))}</span>${pills.join('')}</div>
      <p class="src"><a href="${esc(d.url)}" target="_blank" rel="noopener">vendor ↗</a><a href="${esc(d.source)}" target="_blank" rel="noopener">source · ${esc(fmtDate(d.last_verified))} (${evidenceLabel})</a></p>
    </article>`;
  }
})();
