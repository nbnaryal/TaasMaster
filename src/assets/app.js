/* TaasMaster — score trackers for Call Break, Marriage and Teen Patti.
   Scores are saved in localStorage so a refresh or power cut never wipes a game. */
'use strict';
(function () {
  /* ---------------- Scoring (pure functions, unit-tested) ---------------- */
  const r1 = (x) => Math.round(x * 10) / 10;
  const num = (v) => { const n = parseFloat(v); return Number.isFinite(n) ? n : 0; };
  const sum = (a) => a.reduce((s, x) => s + num(x), 0);

  const Score = {
    /* Call Break: made the call -> call + 0.1 per extra trick; missed -> minus the call. */
    callBreak(bid, won) {
      bid = num(bid); won = num(won);
      return won >= bid ? r1(bid + (won - bid) / 10) : -bid;
    },
    /* Marriage: rows = [{maal, seen}], o = {winner, seenFee, unseenFee, dublee, dubleeBonus}.
       Each player's maal is compared against everyone: net = maal × players − total maal.
       Unseen players' maal does not count. Each loser then pays the winner a fixed fee. */
    marriage(rows, o) {
      const n = rows.length, w = o.winner;
      if (w == null || w < 0 || w >= n) return { error: 'mNeedWinner' };
      if (!rows[w].seen) return { error: 'mWinnerSeen' };
      const eff = rows.map((r) => (r.seen ? num(r.maal) : 0));
      const total = sum(eff);
      const nets = eff.map((m) => m * n - total);
      for (let i = 0; i < n; i++) {
        if (i === w) continue;
        let fee = rows[i].seen ? num(o.seenFee) : num(o.unseenFee);
        if (o.dublee) fee += num(o.dubleeBonus);
        nets[i] -= fee; nets[w] += fee;
      }
      return { nets: nets.map(r1), total };
    },
    /* Teen Patti: winner takes the pot; everyone else loses what they put in. */
    teenPatti(contrib, w) {
      const pot = sum(contrib);
      return contrib.map((c, i) => r1(i === w ? pot - num(c) : -num(c)));
    },
    /* Fewest transfers that square everyone up. */
    settle(totals) {
      const cred = [], debt = [];
      totals.forEach((v, i) => { v = r1(v); if (v > 0) cred.push({ i, v }); else if (v < 0) debt.push({ i, v: -v }); });
      cred.sort((a, b) => b.v - a.v); debt.sort((a, b) => b.v - a.v);
      const out = []; let a = 0, b = 0;
      while (a < debt.length && b < cred.length) {
        const x = r1(Math.min(debt[a].v, cred[b].v));
        if (x > 0) out.push({ from: debt[a].i, to: cred[b].i, amt: x });
        debt[a].v = r1(debt[a].v - x); cred[b].v = r1(cred[b].v - x);
        if (debt[a].v <= 0) a++;
        if (cred[b].v <= 0) b++;
      }
      return out;
    }
  };

  if (typeof document === 'undefined') { if (typeof module !== 'undefined') module.exports = Score; return; }

  /* ---------------- Strings ---------------- */
  const T = {
    en: {
      players: 'Players', addPlayer: '+ Add player', remove: 'Remove', start: 'Start game', newGame: 'New game',
      confirmNew: 'Start a new game? Current scores will be cleared.', undo: 'Undo last', total: 'Total',
      round: 'Round', hand: 'Hand', del: 'Delete', confirmDel: 'Delete this entry?', winner: 'Winner',
      saved: 'Saved on this phone — safe to refresh', namePh: 'Player {n}', settle: 'Settle up', hideSettle: 'Hide settlement',
      settleNone: 'Everyone is square.', owes: '{a} → {b}: {x} pts', history: 'History', options: 'Options',
      install: 'Install', iosHint: 'To install on iPhone: tap Share, then “Add to Home Screen”.',
      minPlayers: 'Add at least {n} players.', noRounds: 'No rounds yet.', scores: 'Scores',
      cbRounds: 'Number of rounds', cbBids: 'Round {n}: calls', cbTricks: 'Round {n}: tricks won', cbLock: 'Lock calls',
      cbSaveRound: 'Save round', cbSum: 'Tricks entered: {s} / 13', cbOver: '{name} wins with {pts} points!',
      cbExtra: 'Play another round', cbFour: 'Call Break is played by exactly 4 players.', cbBidHint: 'Each player calls 1–13.',
      mMaal: 'Maal', mSeen: 'Seen', mUnseen: 'Not seen', mWin: 'Won', mDublee: 'Winner finished with dublee',
      mAddHand: 'Save hand', mSeenFee: 'Seen player pays winner', mUnseenFee: 'Unseen player pays winner',
      mDubleeBonus: 'Extra per player for a dublee win', mTotalMaal: 'Total maal counted: {t}',
      mNeedWinner: 'Pick who won the hand.', mWinnerSeen: 'The winner must have seen the maal.', mPreview: 'This hand',
      mNewHand: 'Hand {n}', mHint: 'Enter maal points, tick who saw the maal, and pick the winner.',
      tpPut: 'Put in', tpPot: 'Pot: {p}', tpWinHand: 'Winning hand', tpSaveRound: 'Save round',
      tpNeedWinner: 'Pick who won the pot.', tpNoPot: 'Enter what each player put into the pot.',
      tpNewRound: 'Round {n}', tpHint: 'Enter the points each player put into the pot, then pick the winner.',
      hands: ['—', 'Trail', 'Pure sequence', 'Sequence', 'Color', 'Pair', 'High card']
    },
    ne: {
      players: 'खेलाडीहरू', addPlayer: '+ खेलाडी थप्नुहोस्', remove: 'हटाउनुहोस्', start: 'खेल सुरु गर्नुहोस्', newGame: 'नयाँ खेल',
      confirmNew: 'नयाँ खेल सुरु गर्ने? अहिलेको स्कोर मेटिनेछ।', undo: 'पछिल्लो फिर्ता', total: 'जम्मा',
      round: 'राउन्ड', hand: 'हात', del: 'मेटाउनुहोस्', confirmDel: 'यो मेटाउने?', winner: 'विजेता',
      saved: 'यही फोनमा सेभ भयो — रिफ्रेस गर्दा पनि हराउँदैन', namePh: 'खेलाडी {n}', settle: 'हिसाब मिलाउनुहोस्', hideSettle: 'हिसाब लुकाउनुहोस्',
      settleNone: 'सबैको हिसाब बराबर छ।', owes: '{a} → {b}: {x} अंक', history: 'इतिहास', options: 'सेटिङ',
      install: 'इन्स्टल', iosHint: 'iPhone मा इन्स्टल गर्न: Share थिचेर “Add to Home Screen” छान्नुहोस्।',
      minPlayers: 'कम्तीमा {n} जना खेलाडी चाहिन्छ।', noRounds: 'अहिलेसम्म कुनै राउन्ड छैन।', scores: 'स्कोर',
      cbRounds: 'राउन्ड संख्या', cbBids: 'राउन्ड {n}: कल', cbTricks: 'राउन्ड {n}: जितेका हात', cbLock: 'कल पक्का गर्नुहोस्',
      cbSaveRound: 'राउन्ड सेभ गर्नुहोस्', cbSum: 'जम्मा हात: {s} / 13', cbOver: '{name} {pts} अंकसहित विजेता!',
      cbExtra: 'अर्को राउन्ड खेल्नुहोस्', cbFour: 'कल ब्रेक ठ्याक्कै ४ जनाले खेलिन्छ।', cbBidHint: 'हरेकले १ देखि १३ सम्म कल गर्छन्।',
      mMaal: 'माल', mSeen: 'देखेको', mUnseen: 'नदेखेको', mWin: 'जित्यो', mDublee: 'विजेताले डबलीबाट खेल सके',
      mAddHand: 'हात सेभ गर्नुहोस्', mSeenFee: 'माल देखेकाले विजेतालाई तिर्ने', mUnseenFee: 'माल नदेखेकाले विजेतालाई तिर्ने',
      mDubleeBonus: 'डबली जितमा प्रति खेलाडी थप', mTotalMaal: 'गनिएको जम्मा माल: {t}',
      mNeedWinner: 'यो हात कसले जित्यो छान्नुहोस्।', mWinnerSeen: 'विजेताले माल देखेको हुनुपर्छ।', mPreview: 'यो हात',
      mNewHand: 'हात {n}', mHint: 'मालको अंक लेख्नुहोस्, कसले माल देख्यो चिन्ह लगाउनुहोस् र विजेता छान्नुहोस्।',
      tpPut: 'हालेको', tpPot: 'पोट: {p}', tpWinHand: 'जित्ने हात', tpSaveRound: 'राउन्ड सेभ गर्नुहोस्',
      tpNeedWinner: 'पोट कसले जित्यो छान्नुहोस्।', tpNoPot: 'प्रत्येकले पोटमा हालेको अंक लेख्नुहोस्।',
      tpNewRound: 'राउन्ड {n}', tpHint: 'प्रत्येकले पोटमा हालेको अंक लेख्नुहोस्, अनि विजेता छान्नुहोस्।',
      hands: ['—', 'ट्रायल', 'प्योर सिक्वेन्स', 'सिक्वेन्स', 'कलर', 'जोडी', 'हाई कार्ड']
    }
  };
  const L = document.documentElement.lang === 'ne' ? 'ne' : 'en';
  const t = (k, v) => {
    let s = T[L][k] != null ? T[L][k] : T.en[k];
    if (v) for (const x in v) s = String(s).split('{' + x + '}').join(v[x]);
    return s;
  };
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const signed = (n) => { n = r1(n); return (n > 0 ? '+' : '') + n; };
  const cls = (n) => (n > 0 ? 'pos' : n < 0 ? 'neg' : '');

  const store = {
    get(k) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : null; } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); return true; } catch (e) { return false; } }
  };

  /* ---------------- PWA: service worker + install button ---------------- */
  if ('serviceWorker' in navigator && location.protocol !== 'file:') {
    window.addEventListener('load', () => { navigator.serviceWorker.register((document.documentElement.dataset.root || '/') + 'sw.js').catch(() => {}); });
  }
  const installBtn = document.getElementById('install');
  let deferred = null;
  window.addEventListener('beforeinstallprompt', (e) => { e.preventDefault(); deferred = e; if (installBtn) installBtn.hidden = false; });
  const standalone = window.matchMedia('(display-mode: standalone)').matches || navigator.standalone;
  const isIOS = /iphone|ipad|ipod/i.test(navigator.userAgent);
  if (installBtn) {
    installBtn.textContent = t('install');
    if (isIOS && !standalone) installBtn.hidden = false;
    installBtn.addEventListener('click', async () => {
      if (deferred) { deferred.prompt(); await deferred.userChoice.catch(() => {}); deferred = null; installBtn.hidden = true; }
      else alert(t('iosHint'));
    });
  }

  /* ---------------- App shell ---------------- */
  const app = document.getElementById('app');
  if (!app) return;
  const game = app.dataset.game;
  const KEY = 'taasmaster:' + game + ':v1';
  const CFG = {
    callbreak: { min: 4, max: 4, def: 4 },
    marriage: { min: 2, max: 6, def: 4 },
    teenpatti: { min: 2, max: 10, def: 4 }
  }[game];
  if (!CFG) return;

  const fresh = (names) => {
    const players = names || Array.from({ length: CFG.def }, () => '');
    const base = { phase: 'setup', players, settle: false };
    if (game === 'callbreak') return Object.assign(base, { rounds: 5, list: [], pend: null });
    if (game === 'marriage') return Object.assign(base, { opts: { seenFee: 3, unseenFee: 10, dubleeBonus: 5 }, list: [], pend: null });
    return Object.assign(base, { list: [], pend: null });
  };
  let st = store.get(KEY) || fresh();
  let msg = '';
  const names = () => st.players;
  const save = () => store.set(KEY, st);

  const newPend = () => {
    const n = st.players.length;
    if (game === 'callbreak') {
      const last = st.list[st.list.length - 1];
      return { bids: last ? last.bids.slice() : Array(n).fill(2), won: null };
    }
    if (game === 'marriage') return { maal: Array(n).fill(''), seen: Array(n).fill(false), w: null, dub: false };
    return { c: Array(n).fill(''), w: null, h: 0 };
  };
  const totals = () => {
    const n = st.players.length, out = Array(n).fill(0);
    st.list.forEach((r) => r.nets.forEach((v, i) => { out[i] = r1(out[i] + v); }));
    return out;
  };

  /* ---------- Shared pieces ---------- */
  const stepper = (k, i, v) =>
    `<div class="step"><button type="button" data-act="step" data-k="${k}" data-i="${i}" data-d="-1" aria-label="−">−</button>` +
    `<output>${v}</output><button type="button" data-act="step" data-k="${k}" data-i="${i}" data-d="1" aria-label="+">+</button></div>`;

  function totalsCard() {
    const tot = totals();
    const max = Math.max(...tot);
    const rows = st.players.map((p, i) => ({ p, v: tot[i], i })).sort((a, b) => b.v - a.v);
    let html = `<div class="card"><h2>${t('scores')}</h2><ul class="totals">` +
      rows.map((r) => `<li class="${r.v === max && st.list.length ? 'lead' : ''}"><span>${esc(r.p)}${r.v === max && st.list.length ? ' <span class="badge">★</span>' : ''}</span><span class="num ${cls(r.v)}">${signed(r.v)}</span></li>`).join('') +
      `</ul>`;
    if (st.list.length) {
      html += `<div class="actions"><button class="btn ghost small" data-act="settle">${st.settle ? t('hideSettle') : t('settle')}</button>` +
        `<button class="btn ghost small" data-act="undo">${t('undo')}</button></div>`;
      if (st.settle) {
        const tr = Score.settle(tot);
        html += `<ul class="totals">` + (tr.length ? tr.map((x) => `<li>${esc(t('owes', { a: st.players[x.from], b: st.players[x.to], x: x.amt }))}</li>`).join('') : `<li>${t('settleNone')}</li>`) + `</ul>`;
      }
    }
    return html + `</div>`;
  }

  function historyCard(label) {
    if (!st.list.length) return '';
    return `<div class="card"><h2>${t('history')}</h2>` +
      st.list.map((r, k) => ({ r, k })).reverse().map(({ r, k }) =>
        `<div class="hist-item"><div><strong>${label} ${k + 1}</strong>${r.h ? ' · ' + esc(t('hands')[r.h]) : ''}<br>` +
        r.nets.map((v, i) => `${esc(st.players[i])} <span class="${cls(v)}">${signed(v)}</span>`).join(' · ') +
        `</div><button class="del" data-act="delete" data-i="${k}">${t('del')}</button></div>`).join('') + `</div>`;
  }

  function footer() {
    return `<button class="btn danger" data-act="new">${t('newGame')}</button><p class="saved" aria-live="polite">✓ ${t('saved')}</p>`;
  }

  /* ---------- Setup ---------- */
  function renderSetup() {
    let h = `<div class="card"><h2>${t('players')}</h2>`;
    if (game === 'callbreak') h += `<p class="note">${t('cbFour')}</p>`;
    st.players.forEach((p, i) => {
      h += `<div class="row field"><input type="text" maxlength="20" autocomplete="off" data-bind="name" data-i="${i}" value="${esc(p)}" placeholder="${esc(t('namePh', { n: i + 1 }))}" aria-label="${esc(t('namePh', { n: i + 1 }))}">` +
        (st.players.length > CFG.min ? `<button class="btn ghost small" style="flex:0" data-act="rm" data-i="${i}" aria-label="${t('remove')}">✕</button>` : '') + `</div>`;
    });
    if (st.players.length < CFG.max) h += `<button class="btn ghost" data-act="add">${t('addPlayer')}</button>`;
    h += `</div>`;
    if (game === 'callbreak') {
      h += `<div class="card"><h2>${t('options')}</h2><div class="prow"><span>${t('cbRounds')}</span>${stepper('rounds', 0, st.rounds)}</div></div>`;
    }
    if (game === 'marriage') {
      const o = st.opts;
      h += `<div class="card"><h2>${t('options')}</h2>` +
        [['seenFee', 'mSeenFee'], ['unseenFee', 'mUnseenFee'], ['dubleeBonus', 'mDubleeBonus']].map(([k, lab]) =>
          `<div class="field"><label for="o-${k}">${t(lab)}</label><input id="o-${k}" inputmode="decimal" data-bind="opt" data-k="${k}" value="${esc(o[k])}"></div>`).join('') + `</div>`;
    }
    h += `<p class="msg">${esc(msg)}</p><button class="btn" data-act="start">${t('start')}</button>`;
    app.innerHTML = h;
  }

  /* ---------- Call Break ---------- */
  function renderCallBreak() {
    const P = st.players, n = st.list.length;
    let h = '';
    const tot = totals();
    // scoreboard: rows = rounds, columns = players
    h += `<div class="card"><h2>${t('scores')}</h2><div class="table-wrap"><table class="sc"><thead><tr><th>#</th>` +
      P.map((p) => `<th>${esc(p)}</th>`).join('') + `</tr></thead><tbody>`;
    for (let r = 0; r < Math.max(st.rounds, n); r++) {
      const row = st.list[r];
      h += `<tr><th>${r + 1}</th>` + P.map((_, i) => row
        ? `<td><span class="${cls(row.nets[i])}">${row.nets[i]}</span><small>${row.bids[i]}/${row.won[i]}</small></td>`
        : `<td>·</td>`).join('') + `</tr>`;
    }
    h += `</tbody><tfoot><tr><td>${t('total')}</td>` + tot.map((v) => `<td class="${cls(v)}">${v}</td>`).join('') + `</tr></tfoot></table></div>`;
    if (n) h += `<div class="actions"><button class="btn ghost small" data-act="undo">${t('undo')}</button><span></span></div>`;
    h += `</div>`;

    if (n >= st.rounds && !st.pend) {
      const best = Math.max(...tot);
      const who = P.filter((_, i) => tot[i] === best).join(' & ');
      h += `<div class="banner">🏆 ${esc(t('cbOver', { name: who, pts: best }))}</div>` +
        `<div class="actions"><button class="btn ghost" data-act="extra">${t('cbExtra')}</button><button class="btn" data-act="new">${t('newGame')}</button></div>`;
      app.innerHTML = h + `<p class="saved">✓ ${t('saved')}</p>`;
      return;
    }
    if (!st.pend) st.pend = newPend();
    const pd = st.pend;
    if (!pd.won) {
      h += `<div class="card"><h2>${t('cbBids', { n: n + 1 })}</h2><p class="note">${t('cbBidHint')}</p>` +
        P.map((p, i) => `<div class="prow"><span class="pname">${esc(p)}</span>${stepper('bids', i, pd.bids[i])}</div>`).join('') +
        `<button class="btn" style="margin-top:12px" data-act="lock">${t('cbLock')}</button></div>`;
    } else {
      const s = sum(pd.won);
      h += `<div class="card"><h2>${t('cbTricks', { n: n + 1 })}</h2>` +
        P.map((p, i) => `<div class="prow"><span class="pname">${esc(p)} <span class="note">(${pd.bids[i]})</span></span>${stepper('won', i, pd.won[i])}</div>`).join('') +
        `<p class="${s === 13 ? 'note' : 'msg'}">${t('cbSum', { s })}</p>` +
        `<div class="actions"><button class="btn ghost" data-act="unlock">← ${t('cbBids', { n: n + 1 })}</button>` +
        `<button class="btn" data-act="saveRound" ${s === 13 ? '' : 'disabled'}>${t('cbSaveRound')}</button></div></div>`;
    }
    app.innerHTML = h + footer();
  }

  /* ---------- Marriage ---------- */
  function marriagePreview() {
    const pd = st.pend;
    const res = Score.marriage(st.players.map((_, i) => ({ maal: pd.maal[i], seen: pd.seen[i] })),
      { winner: pd.w, seenFee: st.opts.seenFee, unseenFee: st.opts.unseenFee, dublee: pd.dub, dubleeBonus: st.opts.dubleeBonus });
    if (res.error) return `<p class="note">${t(res.error)}</p>`;
    return `<p class="note">${t('mTotalMaal', { t: res.total })}</p><ul class="totals">` +
      st.players.map((p, i) => `<li><span>${esc(p)}</span><span class="num ${cls(res.nets[i])}">${signed(res.nets[i])}</span></li>`).join('') + `</ul>`;
  }
  function renderMarriage() {
    if (!st.pend) st.pend = newPend();
    const pd = st.pend;
    let h = totalsCard();
    h += `<div class="card"><h2>${t('mNewHand', { n: st.list.length + 1 })}</h2><p class="note">${t('mHint')}</p>` +
      st.players.map((p, i) => `<div class="mrow"><span class="pname">${esc(p)}</span>` +
        `<input inputmode="decimal" data-bind="maal" data-i="${i}" value="${esc(pd.maal[i])}" placeholder="0" aria-label="${esc(p)} ${t('mMaal')}" ${pd.seen[i] ? '' : 'disabled'}>` +
        `<div class="chips"><label class="chip"><input type="checkbox" data-bind="seen" data-i="${i}" ${pd.seen[i] ? 'checked' : ''}><span>${pd.seen[i] ? '👁 ' + t('mSeen') : t('mUnseen')}</span></label>` +
        `<label class="chip"><input type="radio" name="mw" data-bind="win" data-i="${i}" ${pd.w === i ? 'checked' : ''}><span>🏆 ${t('mWin')}</span></label></div></div>`).join('') +
      `<div class="chips" style="margin-top:10px"><label class="chip"><input type="checkbox" data-bind="dub" ${pd.dub ? 'checked' : ''}><span>${t('mDublee')}</span></label></div>` +
      `<h3>${t('mPreview')}</h3><div id="preview">${marriagePreview()}</div>` +
      `<p class="msg">${esc(msg)}</p><button class="btn" data-act="saveHand">${t('mAddHand')}</button></div>`;
    h += historyCard(t('hand'));
    app.innerHTML = h + footer();
  }

  /* ---------- Teen Patti ---------- */
  function tpPreview() {
    const pd = st.pend, pot = sum(pd.c);
    if (pd.w == null || !pot) return `<p class="note">${t('tpPot', { p: pot })}</p>`;
    const nets = Score.teenPatti(pd.c, pd.w);
    return `<p class="note">${t('tpPot', { p: pot })}</p><ul class="totals">` +
      st.players.map((p, i) => `<li><span>${esc(p)}</span><span class="num ${cls(nets[i])}">${signed(nets[i])}</span></li>`).join('') + `</ul>`;
  }
  function renderTeenPatti() {
    if (!st.pend) st.pend = newPend();
    const pd = st.pend;
    let h = totalsCard();
    h += `<div class="card"><h2>${t('tpNewRound', { n: st.list.length + 1 })}</h2><p class="note">${t('tpHint')}</p>` +
      st.players.map((p, i) => `<div class="mrow"><span class="pname">${esc(p)}</span>` +
        `<input inputmode="decimal" data-bind="c" data-i="${i}" value="${esc(pd.c[i])}" placeholder="0" aria-label="${esc(p)} ${t('tpPut')}">` +
        `<div class="chips"><label class="chip"><input type="radio" name="tw" data-bind="win" data-i="${i}" ${pd.w === i ? 'checked' : ''}><span>🏆 ${t('winner')}</span></label></div></div>`).join('') +
      `<div class="field"><label for="tp-h">${t('tpWinHand')}</label><select id="tp-h" data-bind="h">` +
      t('hands').map((x, k) => `<option value="${k}" ${pd.h === k ? 'selected' : ''}>${esc(x)}</option>`).join('') + `</select></div>` +
      `<div id="preview">${tpPreview()}</div>` +
      `<p class="msg">${esc(msg)}</p><button class="btn" data-act="saveTp">${t('tpSaveRound')}</button></div>`;
    h += historyCard(t('round'));
    app.innerHTML = h + footer();
  }

  function render() {
    if (st.phase === 'setup') renderSetup();
    else if (game === 'callbreak') renderCallBreak();
    else if (game === 'marriage') renderMarriage();
    else renderTeenPatti();
    msg = '';
    save();
  }

  /* ---------- Events ---------- */
  app.addEventListener('click', (e) => {
    const b = e.target.closest('[data-act]');
    if (!b) return;
    const act = b.dataset.act, i = +b.dataset.i;
    switch (act) {
      case 'add': st.players.push(''); break;
      case 'rm': st.players.splice(i, 1); break;
      case 'start': {
        st.players = st.players.map((p, k) => p.trim() || t('namePh', { n: k + 1 }));
        if (st.players.length < CFG.min) { msg = t('minPlayers', { n: CFG.min }); break; }
        st.phase = 'play'; st.list = []; st.pend = null; st.settle = false;
        break;
      }
      case 'step': {
        const d = +b.dataset.d, k = b.dataset.k;
        if (k === 'rounds') st.rounds = Math.min(20, Math.max(1, st.rounds + d));
        else if (k === 'bids') st.pend.bids[i] = Math.min(13, Math.max(1, st.pend.bids[i] + d));
        else if (k === 'won') st.pend.won[i] = Math.min(13, Math.max(0, st.pend.won[i] + d));
        break;
      }
      case 'lock': st.pend.won = st.pend.bids.slice(); break;
      case 'unlock': st.pend.won = null; break;
      case 'saveRound': {
        const pd = st.pend;
        if (sum(pd.won) !== 13) return;
        st.list.push({ bids: pd.bids.slice(), won: pd.won.slice(), nets: pd.bids.map((x, k) => Score.callBreak(x, pd.won[k])) });
        st.pend = null; st.pend = newPend();
        if (st.list.length >= st.rounds) st.pend = null;
        break;
      }
      case 'extra': st.rounds += 1; st.pend = newPend(); break;
      case 'saveHand': {
        const pd = st.pend;
        const res = Score.marriage(st.players.map((_, k) => ({ maal: pd.maal[k], seen: pd.seen[k] })),
          { winner: pd.w, seenFee: st.opts.seenFee, unseenFee: st.opts.unseenFee, dublee: pd.dub, dubleeBonus: st.opts.dubleeBonus });
        if (res.error) { msg = t(res.error); break; }
        st.list.push({ maal: pd.maal.map(num), seen: pd.seen.slice(), w: pd.w, dub: pd.dub, nets: res.nets });
        st.pend = newPend();
        break;
      }
      case 'saveTp': {
        const pd = st.pend;
        if (pd.w == null) { msg = t('tpNeedWinner'); break; }
        if (!sum(pd.c)) { msg = t('tpNoPot'); break; }
        st.list.push({ c: pd.c.map(num), w: pd.w, h: pd.h, nets: Score.teenPatti(pd.c, pd.w) });
        st.pend = newPend();
        break;
      }
      case 'undo': {
        if (game === 'callbreak') {
          if (st.pend && st.pend.won) { st.pend.won = null; break; }
          const last = st.list.pop();
          if (last) st.pend = { bids: last.bids, won: last.won };
        } else if (st.list.length && confirm(t('confirmDel'))) st.list.pop();
        break;
      }
      case 'delete': if (confirm(t('confirmDel'))) st.list.splice(i, 1); break;
      case 'settle': st.settle = !st.settle; break;
      case 'new': if (st.phase === 'setup' || confirm(t('confirmNew'))) { const keep = st.players.slice(); st = fresh(keep); } break;
      default: return;
    }
    render();
  });

  const onInput = (e) => {
    const el = e.target, k = el.dataset.bind;
    if (!k) return;
    const i = +el.dataset.i;
    const pd = st.pend;
    if (k === 'name') { st.players[i] = el.value; save(); return; }
    if (k === 'opt') { st.opts[el.dataset.k] = num(el.value); save(); return; }
    if (k === 'maal') pd.maal[i] = el.value;
    else if (k === 'c') pd.c[i] = el.value;
    else if (k === 'seen') { pd.seen[i] = el.checked; if (!el.checked && pd.w === i) pd.w = null; render(); return; }
    else if (k === 'win') { pd.w = i; if (game === 'marriage') pd.seen[i] = true; render(); return; }
    else if (k === 'dub') pd.dub = el.checked;
    else if (k === 'h') pd.h = +el.value;
    const pv = document.getElementById('preview');
    if (pv) pv.innerHTML = game === 'marriage' ? marriagePreview() : tpPreview();
    save();
  };
  app.addEventListener('input', onInput);
  app.addEventListener('change', (e) => { if (e.target.type === 'checkbox' || e.target.type === 'radio' || e.target.tagName === 'SELECT') onInput(e); });

  // keep other open tabs in sync
  window.addEventListener('storage', (e) => { if (e.key === KEY) { st = store.get(KEY) || fresh(); render(); } });
  render();
})();
