"""Banc de test local : board.html + base factice en memoire, servi sur 127.0.0.1:8765.

    python test/serve.py [--delay] [--port 8765]

--delay : chaque ecriture attend 150 ms + 200 ms par ecriture deja faite, et chaque
          ecriture declenche son propre instantane (pour voir les rendus intermediaires).
"""
import argparse
import http.server
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

STUB = r'''<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}html{scroll-padding-top:env(safe-area-inset-top,0px)}body{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif;background:#faf9f5;color:#141413}img{max-width:100%}[hidden]:not([hidden=until-found i]){display:none!important}</style></head><body>
<script>
(() => {
  const DELAY = __DELAY__;
  const store = { boards: {}, items: {}, contacts: {}, settings: {}, tags: {}, views: {} };
  const subs = { boards: [], items: [], contacts: [], settings: [], tags: [], views: [] };
  const uid = () => Math.random().toString(36).slice(2, 10);
  const snap = (name) => ({ docs: Object.entries(store[name]).sort((a, z) => (a[1].order ?? 0) - (z[1].order ?? 0)).map(([id, d]) => ({ id, data: () => ({ ...d }) })) });
  const fire = (name) => subs[name].forEach((cb) => cb(snap(name)));
  window.__store = store; window.__log = []; window.__orders = [];
  addEventListener("DOMContentLoaded", () => new MutationObserver(() =>
    window.__orders.push([...document.querySelectorAll(".tab[data-board]")].map((t) => t.dataset.board).join(">"))
  ).observe(document.querySelector("#tabs"), { childList: true }));
  const col = (name) => ({
    orderBy: () => col(name),
    where: () => ({ get: async () => snap(name) }),
    onSnapshot: (cb) => { subs[name].push(cb); setTimeout(() => cb(snap(name)), 0); },
    add: async (d) => { const id = uid(); store[name][id] = { ...d }; fire(name); return { id }; }
  });
  const db = {
    collection: col,
    doc: (p) => { const [name, id] = p.split("/"); return {
      update: async (d) => {
        window.__log.push([p, d]);
        if (DELAY) await new Promise((r) => setTimeout(r, 150 + 200 * window.__log.length));
        Object.assign(store[name][id], d); fire(name);
      },
      set: async (d) => { store[name][id] = { ...d }; fire(name); },
      delete: async () => { delete store[name][id]; fire(name); }
    }; }
  };
  const cols = [{ id: "todo", label: "A faire", tone: "neutral" }, { id: "doing", label: "En cours", tone: "active" }, { id: "done", label: "Fait", tone: "done" }];
  [["b1", "Tableau 1", 10], ["b2", "Tableau 2", 20], ["b3", "Tableau 3", 30], ["b4", "Tableau 4", 40]].forEach(([id, name, order]) => {
    store.boards[id] = { name, order, preset: "kanban", columns: cols, createdAt: "", updatedAt: "" };
  });
  // Jeu de démonstration : de quoi regarder la page sans rien saisir (cartes,
  // étiquettes, limite de colonne, vues enregistrées). Tableau 1 seulement.
  store.boards.b1.columns = [cols[0], { ...cols[1], limit: 2 }, cols[2]];
  const T = new Date().toISOString();
  // d(n, h) = il y a n jours à h heures, en ISO ; LBL = libellé d'une colonne de la démo.
  const d = (n, h = 10) => { const x = new Date(); x.setDate(x.getDate() - n); x.setHours(h, 0, 0, 0); return x.toISOString(); };
  const LBL = { todo: "A faire", doing: "En cours", done: "Fait" };
  const mv = (n, h, from, to) => ({ at: d(n, h), by: "moi", type: "move", text: LBL[from] + " → " + LBL[to] });
  const cr = (n, col) => ({ at: d(n), by: "moi", type: "create", text: "Créée dans " + LBL[col] });
  const card = (id, title, column, order, extra) => { store.items[id] = { boardId: "b1", title, body: "", column, order, assignee: "", tags: [], links: [], due: "", dueTime: "", priority: 0, activity: [], history: [{ at: T, by: "moi", type: "create", text: "Créée dans " + LBL[column] }], archivedAt: "", archivedBy: "", by: "moi", createdAt: T, updatedAt: T, ...extra }; };
  card("a1", "Mantis 11377 — Suggestions de liens : filtrer par taxonomie", "todo", 1000, { tags: ["Albedo", "mantis"], priority: 1, assignee: "moi", blockedBy: ["a7"], createdAt: d(12), history: [cr(12, "todo")], body: "- [ ] Relire la spec\n- [ ] Chiffrer\n- [x] Accuser réception" });
  card("a2", "Mantis 11378 — Transcription : paragraphes via retour chariot", "todo", 2000, { tags: ["Albedo", "mantis"], priority: 1, assignee: "moi", blockedBy: ["a4"], createdAt: d(9), history: [cr(9, "todo")] });
  card("a3", "Relire le mail de Paul « Rubedo + Redway »", "todo", 3000, { tags: ["RubWay"], priority: 2, assignee: "claude", blockedBy: ["zz"], createdAt: d(3), history: [cr(3, "todo")], links: [{ url: "https://mail.google.com/", label: "Gmail" }] });
  card("a4", "SDP 96786 — Liseuse : liens des grilles de jeux décalés", "doing", 1000, { tags: ["Liseuse", "sdp"], priority: 1, assignee: "moi", due: "2026-10-01", createdAt: d(10), history: [cr(10, "todo"), mv(8, 9, "todo", "doing"), mv(8, 9, "doing", "todo"), mv(7, 14, "todo", "doing")] });
  card("a5", "MEP mensuelle", "doing", 2000, { tags: ["mep"], assignee: "claude", body: "- [x] build\n- [ ] deploy\n- [ ] test", due: "2026-10-20", dueTime: "09:00", createdAt: d(6), history: [cr(6, "todo"), mv(2, 11, "todo", "doing")] });
  card("a6", "Spool2xfr : suivi recette", "doing", 3000, { tags: ["Cloudinary"], assignee: "moi", activity: [{ at: T, by: "claude", text: "Recette passée sur QA, reste la prod." }], createdAt: d(14), history: [cr(14, "todo"), mv(13, 15, "todo", "doing")] });
  card("a7", "Nouveau fichier de config appli V4", "done", 1000, { tags: ["Eidos"], assignee: "claude", doneAt: d(4, 17), createdAt: d(11), history: [cr(11, "todo"), mv(9, 10, "todo", "doing"), mv(4, 17, "doing", "done")] });
  card("a8", "Ancien ticket réglé", "done", 2000, { tags: ["mantis"], createdAt: d(15), doneAt: d(6, 16), archivedAt: d(1, 9), history: [cr(15, "todo"), mv(12, 10, "todo", "doing"), mv(6, 16, "doing", "done"), { at: d(1, 9), by: "moi", type: "archive", text: "Archivée" }] });
  card("a9", "Importé sans historique", "todo", 4000, { tags: ["sdp"], createdAt: d(20), history: [] });
  store.tags.liseuse = { name: "Liseuse", hue: 218, updatedAt: T, by: "moi" };
  store.views.v1 = { boardId: "b1", name: "Albedo", order: 10, state: { view: "cols", q: "Albedo", who: "", late: false, cols: [], prio: [], arch: false, sort: "", dir: "" }, createdAt: T, updatedAt: T, by: "moi" };
  store.views.v2 = { boardId: "b1", name: "P1 en liste", order: 20, state: { view: "list", q: "", who: "", late: false, cols: [], prio: ["1"], arch: false, sort: "updated", dir: "desc" }, createdAt: T, updatedAt: T, by: "moi" };
  store.views.v3 = { boardId: "b1", name: "Pour Claude", order: 30, state: { view: "cols", q: "", who: "claude", late: false, cols: [], prio: [], arch: false, sort: "", dir: "" }, createdAt: T, updatedAt: T, by: "moi" };
  window.claude = { use: async (n) => n === "db" ? db : null };
})();
</script>
'''


def build(delay):
    src = io.open(os.path.join(ROOT, "board.html"), encoding="utf-8").read()
    html = STUB.replace("__DELAY__", "true" if delay else "false") + src
    io.open(os.path.join(HERE, "index.html"), "w", encoding="utf-8", newline="\n").write(html)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--delay", action="store_true")
    ap.add_argument("--port", type=int, default=8765)
    a = ap.parse_args()
    build(a.delay)
    os.chdir(HERE)
    print(f"http://127.0.0.1:{a.port}/  (delay={'on' if a.delay else 'off'})", flush=True)
    try:
        http.server.ThreadingHTTPServer(("127.0.0.1", a.port), http.server.SimpleHTTPRequestHandler).serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
