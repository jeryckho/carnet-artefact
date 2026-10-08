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

STUB = r'''<!doctype html><meta charset="utf-8"><script>
(() => {
  const DELAY = __DELAY__;
  const store = { boards: {}, items: {}, contacts: {}, settings: {} };
  const subs = { boards: [], items: [], contacts: [], settings: [] };
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
