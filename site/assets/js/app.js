/* Environmental Acoustic Intelligence — client-side loader.
   Renders the abstract, presenters, outline, downloads, and references from the
   JSON under assets/data/ (synced from /content by build/sync_content.py).
   Vanilla JS, no dependencies. Served over HTTP (GitHub Pages); fetch() will not
   work from a file:// URL — use a local server for preview. */
(function () {
  "use strict";

  const DATA = "assets/data/";
  const $ = (sel, root = document) => root.querySelector(sel);

  const esc = (s) =>
    String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");

  // "Woon-Seng Gan" -> "W.-S. Gan"
  function abbrev(name) {
    const parts = String(name).trim().split(/\s+/);
    const surname = parts.pop();
    const initials = parts.join(" ").split(/[\s-]+/).filter(Boolean)
      .map((w) => w[0].toUpperCase()).join(".-");
    return (initials ? initials + ". " : "") + surname;
  }

  async function getJSON(name) {
    const res = await fetch(DATA + name, { cache: "no-cache" });
    if (!res.ok) throw new Error(`${name}: HTTP ${res.status}`);
    return res.json();
  }

  /* -------------------------------------------------------- renderers ----- */

  function renderAbstract(meta) {
    const wrap = $("#abstractBody");
    if (!wrap || !meta.abstract) return;
    const draft = meta.abstract.draft
      ? ' <span class="badge-draft" title="Draft — to be confirmed by presenters">draft</span>' : "";
    // Split abstract into lead sentence + rest for a little hierarchy.
    const text = meta.abstract.text.trim();
    const cut = text.indexOf(". ") + 1;
    const lead = cut > 1 ? text.slice(0, cut) : text;
    const rest = cut > 1 ? text.slice(cut).trim() : "";
    wrap.innerHTML =
      `<p class="prose lead">${esc(lead)}${draft}</p>` +
      (rest ? `<p class="prose">${esc(rest)}</p>` : "");
  }

  function renderOutcomes(meta) {
    const ol = $("#outcomesList");
    if (!ol || !meta.learning_outcomes) return;
    ol.innerHTML = meta.learning_outcomes.items.map((o) => `<li>${esc(o)}</li>`).join("");
  }

  function renderHeroMeta(meta) {
    const foot = $("#footMeta");
    if (foot) foot.textContent =
      `${meta.event.conference} · ${meta.event.tutorial_number} · Updated ${meta.last_updated || ""}`.trim();
  }

  function renderPeople(people) {
    const host = $("#people");
    if (!host) return;
    const initials = (n) => n.split(/\s+/).map((w) => w[0]).join("").slice(0, 2).toUpperCase();
    const linkLabel = { profile: "Profile", scholar: "Scholar", researchgate: "ResearchGate", website: "Website" };
    host.innerHTML = people.people.map((p) => {
      const photo = p.headshot
        ? `<img class="person__photo" src="${esc(p.headshot)}" alt="Portrait of ${esc(p.display_name)}" width="88" height="88" loading="lazy">`
        : `<div class="person__photo person__photo--ph" aria-hidden="true">${esc(initials(p.name))}</div>`;
      const links = Object.entries(p.links || {}).map(([k, v]) =>
        `<a href="${esc(v)}" rel="noopener">${esc(linkLabel[k] || k)} ↗</a>`).join("");
      const research = p.research
        ? `<p class="person__research"><span class="lbl">Research:</span> ${esc(p.research)}</p>` : "";
      return `<article class="person">
        ${photo}
        <span class="person__rule" aria-hidden="true"></span>
        <div class="person__content">
          <div class="person__name">${esc(p.display_name)}</div>
          <p class="person__cred">${esc(p.credentials)}</p>
          ${research}
          ${links ? `<div class="person__links">${links}</div>` : ""}
        </div>
      </article>`;
    }).join("");
  }

  const chev = '<svg class="sec__chev" width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M9 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';

  function renderOutline(outline) {
    const host = $("#outline-list");
    if (!host) return;

    host.innerHTML = outline.sections.map((s, i) => {
      const framing = s.kind === "framing";
      const open = s.id === "1" ? " open" : "";
      const subs = (s.subsections || []).map((sub) =>
        `<div class="sub"><p class="sub__t">${esc(sub.title)}</p><ul>${
          (sub.points || []).map((pt) => `<li>${esc(pt)}</li>`).join("")}</ul></div>`).join("");
      return `<details class="sec${framing ? " sec--framing" : ""}"${open}>
        <summary>
          <span class="sec__no${framing ? " sec__no--framing" : ""}">${esc(s.number)}</span>
          <span class="sec__title">${esc(s.title)}</span>
          <span class="sec__meta"><span>Slides ${esc(s.slides)}</span></span>
          ${chev}
        </summary>
        <div class="sec__body">
          <p>${esc(s.summary || "")}</p>
          <div class="subs">${subs}</div>
        </div>
      </details>`;
    }).join("");
  }

  const pdfIcon = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="4" y="3" width="16" height="18" rx="2" stroke="currentColor" stroke-width="2"/></svg>';
  const dlIcon = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 3v10m0 0l-4-4m4 4l4-4M5 17v2a2 2 0 002 2h10a2 2 0 002-2v-2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';

  function renderDownloads(meta, people) {
    const host = $("#downloads");
    if (!host || !meta.downloads) return;
    const nameById = {};
    (people.people || []).forEach((p) => (nameById[p.id] = abbrev(p.name)));
    const who = (id) => (id === "all" ? "All" : nameById[id] || id);
    const notice = $("#dlNotice span");
    if (notice && meta.downloads.release_note) {
      notice.innerHTML = `Slides will be available for download <strong>after the session</strong>. ${esc(meta.downloads.release_note)}`;
    }
    host.innerHTML = meta.downloads.items.map((d) => {
      const full = d.id === "full";
      const available = d.status === "available" && d.file;
      const state = available
        ? '<span class="dl__state dl__state--soon">Download</span>'
        : `<span class="dl__state${d.gated ? " dl__state--soon" : ""}">${d.gated ? "After session" : "Pending"}</span>`;
      const inner = `<span class="dl__ic">${full ? dlIcon : pdfIcon}</span>
        <div><div class="dl__t">${esc(d.label)}</div>
        <div class="dl__m">${esc(who(d.presenter))} · ${esc(d.slides)}${full ? " · PDF" : ""}</div></div>${state}`;
      return available
        ? `<a class="dl${full ? " dl--full" : ""}" href="${esc(d.file)}" download>${inner}</a>`
        : `<div class="dl${full ? " dl--full" : ""}">${inner}</div>`;
    }).join("");
  }

  const refChev = '<svg class="refgrp__chev" width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M9 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';

  function citation(r) {
    let s = `${esc(r.authors)}, <span class="t">&ldquo;${esc(r.title)},&rdquo;</span> <span class="v">${esc(r.venue)}</span>`;
    if (r.info) s += `, ${esc(r.info)}`;
    if (r.year) s += `, ${esc(r.year)}`;
    s += ".";
    const chips = [];
    if (r.doi) chips.push(`<a href="https://doi.org/${esc(r.doi)}" rel="noopener">DOI</a>`);
    if (r.arxiv) chips.push(`<a href="https://arxiv.org/abs/${esc(r.arxiv)}" rel="noopener">arXiv</a>`);
    if (!r.doi && !r.arxiv && r.url) chips.push(`<a href="${esc(r.url)}" rel="noopener">Link</a>`);
    if (!r.doi && !r.arxiv && !r.url) chips.push(`<span style="color:var(--faint)">link pending</span>`);
    return s + `<span class="ref__links">${chips.join("")}</span>`;
  }

  function renderReferences(refs) {
    const host = $("#ref-groups");
    if (!host) return;
    const intro = $("#refIntro");
    const total = (refs.counts && refs.counts.total) || refs.references.length;
    if (intro) intro.innerHTML =
      `${total} references in IEEE style, grouped by section, with DOI / arXiv links where available.`;

    const sections = refs.sections || {};
    const order = Object.keys(sections);
    host.innerHTML = order.map((secId, idx) => {
      const items = refs.references.filter((r) => (r.section || []).includes(secId));
      if (!items.length) return "";
      const lis = items.map((r, i) =>
        `<li class="ref"><span class="ref__n">[${i + 1}]</span><span class="ref__body">${citation(r)}</span></li>`
      ).join("");
      return `<details class="refgrp"${idx === 0 ? " open" : ""}>
        <summary><span class="refgrp__no">§${esc(secId)}</span>
          <span class="refgrp__t">${esc(sections[secId])}</span>
          <span class="refgrp__ct">${items.length} refs</span>${refChev}</summary>
        <ul class="refs">${lis}</ul>
      </details>`;
    }).join("");
  }

  function renderContact(meta) {
    const qr = $("#qr");
    if (!qr || !meta.contact) return;
    if (meta.contact.qr) {
      qr.innerHTML = `<img src="${esc(meta.contact.qr)}" alt="QR code linking to this tutorial page" style="width:100%;height:100%;object-fit:contain">`;
      qr.removeAttribute("aria-label");
    }
  }

  function renderError(err) {
    ["#abstractBody", "#refIntro"].forEach((sel) => {
      const n = $(sel);
      if (n) n.innerHTML =
        `<p class="prose" style="color:var(--muted)">Content could not be loaded (${esc(err.message)}). ` +
        `The data files are in <code>assets/data/</code>.</p>`;
    });
  }

  /* --------------------------------------------------------- nav toggle --- */
  function initNav() {
    const btn = $("#navToggle"), links = $("#navLinks");
    if (!btn || !links) return;
    btn.addEventListener("click", () => {
      const open = links.classList.toggle("is-open");
      btn.setAttribute("aria-expanded", String(open));
      btn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
    links.addEventListener("click", (e) => {
      if (e.target.tagName === "A") {
        links.classList.remove("is-open");
        btn.setAttribute("aria-expanded", "false");
        btn.setAttribute("aria-label", "Open menu");
      }
    });
  }

  /* ------------------------------------------------------------- boot ----- */
  async function boot() {
    initNav();
    try {
      const [meta, people, outline, refs] = await Promise.all([
        getJSON("meta.json"), getJSON("people.json"),
        getJSON("outline.json"), getJSON("references.json"),
      ]);
      renderHeroMeta(meta);
      renderAbstract(meta);
      renderOutcomes(meta);
      renderPeople(people);
      renderOutline(outline);
      renderDownloads(meta, people);
      renderReferences(refs);
      renderContact(meta);
    } catch (err) {
      console.error(err);
      renderError(err);
    }
  }

  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
