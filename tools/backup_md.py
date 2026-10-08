"""Rend une sauvegarde brute (un JSON par document) en notes Markdown lisibles, une par tableau.

    python tools/backup_md.py <dossier de sauvegarde> [--out <dossier>]

Le dossier de sauvegarde contient `boards/<id>.json` et `items/<id>.json` tels que les ecrit
l'outil ArtifactData (parametre out_dir). Sortie par defaut : `<dossier>/md/`, un fichier par
tableau plus un `index.md`. Les fichiers existants du dossier de sortie sont remplaces.
"""
import argparse
import datetime
import glob
import io
import json
import os
import re

TONE_LABEL = {"neutral": "", "active": "en cours", "done": "fait", "alert": "alerte", "info": "info", "wait": "attente", "idle": "sommeil"}


def load_dir(d):
    out = {}
    for f in sorted(glob.glob(os.path.join(d, "*.json"))):
        out[os.path.splitext(os.path.basename(f))[0]] = json.load(io.open(f, encoding="utf-8"))
    return out


def day(iso):
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", iso or "")
    return f"{m[3]}/{m[2]}/{m[1]}" if m else ""


def stamp(iso):
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})", iso or "")
    return f"{m[3]}/{m[2]}/{m[1]} {m[4]}:{m[5]}" if m else day(iso)


def who(a):
    return {"moi": "Moi", "claude": "Claude", "": ""}.get(a, a or "")


def indent(text, prefix="> "):
    return "\n".join(prefix + l if l.strip() else prefix.rstrip() for l in (text or "").rstrip().split("\n"))


def card_md(cid, it):
    p = it.get("priority") or 0
    head = f"### {'P' + str(p) + ' · ' if p else ''}{it.get('title') or '(sans titre)'} `#{cid[:6]}`"
    meta = []
    if it.get("assignee"):
        meta.append(who(it["assignee"]))
    if it.get("due"):
        meta.append("échéance " + day(it["due"]) + (" " + it["dueTime"] if it.get("dueTime") else ""))
    if it.get("tags"):
        meta.append(" ".join("`" + t + "`" for t in it["tags"]))
    links = it.get("links") or ([{"url": it["source"]}] if it.get("source") else [])
    for l in links:
        if l and l.get("url"):
            meta.append(f"[{l.get('label') or l['url']}]({l['url']})")
    if it.get("archivedAt"):
        meta.append("archivée le " + day(it["archivedAt"]))
    if it.get("contactId"):
        meta.append("contact " + it["contactId"])
    lines = [head]
    if meta:
        lines.append("*" + " · ".join(meta) + "*")
    lines.append("")
    if (it.get("body") or "").strip():
        lines.append(indent(it["body"]))
        lines.append("")
    acts = [a for a in it.get("activity") or [] if a]
    hist = [h for h in it.get("history") or [] if h]
    if acts:
        lines.append("**Journal**")
        lines.append("")
        for a in acts:
            lines.append(f"- **{who(a.get('by'))}** · {stamp(a.get('at'))}")
            lines.append(indent(a.get("text"), "  > "))
        lines.append("")
    if hist:
        lines.append("<details><summary>Historique (" + str(len(hist)) + ")</summary>")
        lines.append("")
        for h in hist:
            lines.append(f"- {stamp(h.get('at'))} · {who(h.get('by'))} · {h.get('text', '')}")
        lines.append("")
        lines.append("</details>")
        lines.append("")
    lines.append(f"<sub>créée {stamp(it.get('createdAt'))} · modifiée {stamp(it.get('updatedAt'))}{' par ' + who(it['by']) if it.get('by') else ''}</sub>")
    lines.append("")
    return "\n".join(lines)


def board_md(bid, b, items, src_label):
    cols = b.get("columns") or [{"id": "inbox", "label": "À trier", "tone": "neutral"}]
    known = {c["id"] for c in cols}
    mine = {cid: it for cid, it in items.items() if it.get("boardId") == bid}
    by_order = lambda kv: (kv[1].get("order") or 0, kv[0])
    live = {cid: it for cid, it in mine.items() if not it.get("archivedAt")}
    arch = {cid: it for cid, it in mine.items() if it.get("archivedAt")}
    out = [f"# {b.get('name') or bid}", "",
           f"*Tableau `{bid}` · modèle {b.get('preset', '?')} · {len(live)} carte(s) active(s), {len(arch)} archivée(s) · sauvegarde {src_label}*", ""]
    out.append("| Colonne | Cartes |")
    out.append("|---|---|")
    for c in cols:
        tone = TONE_LABEL.get(c.get("tone"), "")
        tone = f" ({tone})" if tone and tone != c["label"].lower() else ""
        out.append(f"| {c['label']}{tone} | {sum(1 for it in live.values() if it.get('column') == c['id'])} |")
    out.append("")
    groups = [(c["label"], [kv for kv in sorted(live.items(), key=by_order) if kv[1].get("column") == c["id"]]) for c in cols]
    orphans = [kv for kv in sorted(live.items(), key=by_order) if kv[1].get("column") not in known]
    if orphans:
        groups.append(("Hors colonnes", orphans))
    if arch:
        groups.append(("Archivées", sorted(arch.items(), key=lambda kv: kv[1].get("archivedAt") or "", reverse=True)))
    for label, cards in groups:
        out.append(f"## {label} ({len(cards)})")
        out.append("")
        if not cards:
            out.append("*vide*")
            out.append("")
        for cid, it in cards:
            out.append(card_md(cid, it))
    return "\n".join(out).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("backup")
    ap.add_argument("--out")
    a = ap.parse_args()
    boards = load_dir(os.path.join(a.backup, "boards"))
    items = load_dir(os.path.join(a.backup, "items"))
    out = a.out or os.path.join(a.backup, "md")
    os.makedirs(out, exist_ok=True)
    label = os.path.basename(os.path.normpath(a.backup))
    index = [f"# Sauvegarde {label}", "", f"*Rendu le {datetime.date.today().strftime('%d/%m/%Y')} · {len(boards)} tableaux, {len(items)} cartes*", "",
             "| Tableau | Modèle | Actives | Archivées | Fichier |", "|---|---|---|---|---|"]
    for bid, b in sorted(boards.items(), key=lambda kv: (kv[1].get("order") or 0, kv[0])):
        md = board_md(bid, b, items, label)
        io.open(os.path.join(out, bid + ".md"), "w", encoding="utf-8", newline="\n").write(md)
        mine = [it for it in items.values() if it.get("boardId") == bid]
        n_arch = sum(1 for it in mine if it.get("archivedAt"))
        index.append(f"| {b.get('name') or bid} | {b.get('preset', '?')} | {len(mine) - n_arch} | {n_arch} | [{bid}.md]({bid}.md) |")
    lost = [cid for cid, it in items.items() if it.get("boardId") not in boards]
    if lost:
        index += ["", f"Cartes sans tableau connu ({len(lost)}) : " + ", ".join("`#" + c[:6] + "`" for c in lost)]
    io.open(os.path.join(out, "index.md"), "w", encoding="utf-8", newline="\n").write("\n".join(index) + "\n")
    print(f"{len(boards)} tableaux, {len(items)} cartes -> {out}")


if __name__ == "__main__":
    main()
