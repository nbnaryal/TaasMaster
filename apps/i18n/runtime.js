/* TaasMaster Nepali layer for the tracker apps.
   The apps stay exactly as written; this swaps their on-screen English for Nepali as they draw.
   Dictionary: window.TM_I18N = { exact: {en: ne}, patterns: [[enWith{0}, neWith{0}], ...] } */
(function () {
  'use strict';
  var D = window.TM_I18N || { exact: {}, patterns: [] };
  var exact = {}, pats = [];
  var norm = function (s) { return s.replace(/\s+/g, ' ').trim(); };
  Object.keys(D.exact).forEach(function (k) { exact[norm(k)] = D.exact[k]; });
  var esc = function (s) { return s.replace(/[.*+?^$()|[\]\\]/g, '\\$&'); };
  (D.patterns || []).forEach(function (p) {
    // {0} matches any text; {0#} matches a number only (so "{0#} players" never swallows a sentence)
    var order = [], src = norm(p[0]).split(/(\{\d+#?\})/).map(function (part) {
      var m = part.match(/^\{(\d+)(#?)\}$/);
      if (m) { order.push(m[1]); return m[2] ? '([-+−]?[\\d.,]+)' : '(.+?)'; }
      return esc(part);
    }).join('');
    try { pats.push({ re: new RegExp('^' + src + '$'), order: order, to: p[1] }); } catch (e) {}
  });
  // Longer patterns first so the most specific one wins.
  pats.sort(function (a, b) { return b.re.source.length - a.re.source.length; });

  function one(core) {
    var out = null;
    {
      for (var i = 0; i < pats.length; i++) {
        var m = core.match(pats[i].re);
        if (m) {
          var vals = {};
          pats[i].order.forEach(function (n, k) { vals[n] = tr(m[k + 1]) || m[k + 1]; });
          out = pats[i].to.replace(/\{(\d+)\}/g, function (_, n) { return vals[n] != null ? vals[n] : ''; });
          break;
        }
      }
    }
    return out;
  }
  var MONTHS = { Jan: 'जनवरी', Feb: 'फेब्रुअरी', Mar: 'मार्च', Apr: 'अप्रिल', May: 'मे', Jun: 'जुन', Jul: 'जुलाई', Aug: 'अगस्ट', Sep: 'सेप्टेम्बर', Oct: 'अक्टोबर', Nov: 'नोभेम्बर', Dec: 'डिसेम्बर' };
  var money = function (t) {
    return t.replace(/\bRs\b\.?/g, 'रु.').replace(/\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* (\d{1,2}), (\d{4})/g, function (_, m, d, y) { return MONTHS[m] + ' ' + d + ', ' + y; });
  };
  function tr(s) {
    var core = norm(s);
    if (!core || !/[A-Za-z]/.test(core)) return null;
    var out = exact[core];
    // Several sentences in one piece of text: translate each one
    if (out == null) {
      var sents = core.split(/(?<!\bRs\.|e\.g\.)(?<=[.!?।])\s+(?=\S)/);
      if (sents.length > 1) {
        var got = false;
        out = sents.map(function (x) { var t = tr(x); if (t != null) { got = true; return t.trim(); } return x; }).join(' ');
        if (!got) out = null;
      }
    }
    if (out == null) out = one(core);
    // Parts joined with " · ": translate each part
    if (out == null && core.indexOf(' · ') > 0) {
      var any = false;
      out = core.split(' · ').map(function (x) { var t = x ? tr(x) : null; if (t != null) { any = true; return t.trim(); } return x; }).join(' · ');
      if (!any) out = null;
    }
    if (out == null && /\bRs\b|\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d/.test(core)) out = money(core);
    else if (out != null) out = money(out);
    if (out == null || out === core) return null;
    var lead = s.match(/^\s*/)[0], trail = s.match(/\s*$/)[0];
    return lead + out + trail;
  }
  window.TM_tr = function (s) { var t = tr(String(s)); return t == null ? String(s) : t; };

  var SKIP = { SCRIPT: 1, STYLE: 1, TEXTAREA: 1, CODE: 1, PRE: 1 };
  var ATTRS = ['placeholder', 'title', 'aria-label', 'alt'];
  function doText(n) {
    var p = n.parentNode;
    if (!p || SKIP[p.nodeName] || (p.closest && p.closest('[data-no-tr],[contenteditable="true"]'))) return;
    var t = tr(n.nodeValue);
    if (t != null) n.nodeValue = t;
  }
  function doEl(el) {
    if (SKIP[el.nodeName] || el.hasAttribute('data-no-tr')) return;
    for (var i = 0; i < ATTRS.length; i++) {
      var v = el.getAttribute(ATTRS[i]);
      if (v) { var t = tr(v); if (t != null) el.setAttribute(ATTRS[i], t); }
    }
    if (el.nodeName === 'INPUT' && (el.type === 'button' || el.type === 'submit') && el.value) { var tv = tr(el.value); if (tv != null) el.value = tv; }
  }
  function walk(root) {
    if (root.nodeType === 3) return doText(root);
    if (root.nodeType !== 1 || SKIP[root.nodeName]) return;
    doEl(root);
    var w = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT, null);
    var n;
    while ((n = w.nextNode())) {
      if (n.nodeType === 3) doText(n); else doEl(n);
    }
  }
  var obs = new MutationObserver(function (list) {
    for (var i = 0; i < list.length; i++) {
      var m = list[i];
      if (m.type === 'characterData') doText(m.target);
      else if (m.type === 'attributes') doEl(m.target);
      else for (var j = 0; j < m.addedNodes.length; j++) walk(m.addedNodes[j]);
    }
  });
  obs.observe(document.documentElement, { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: ATTRS });
  document.addEventListener('DOMContentLoaded', function () { walk(document.body); });

  // Native dialogs the apps may use
  ['alert', 'confirm', 'prompt'].forEach(function (f) {
    var orig = window[f];
    if (!orig) return;
    window[f] = function (msg) {
      var a = Array.prototype.slice.call(arguments);
      if (typeof msg === 'string') a[0] = msg.split('\n').map(function (l) { return window.TM_tr(l); }).join('\n');
      return orig.apply(window, a);
    };
  });
})();
