#!/usr/bin/env python3
"""Update the live pantry (domains/concierge/kitchen/PANTRY.md) from pasted receipt or
grocery-list text. Manual-first ingestion (no OCR/connector exists — KITCHEN_PROFILE).

Usage:
  receipt_to_pantry.py --paste-file <file> --source "vons 2026-07-11" [--receipt]
  receipt_to_pantry.py --add "2 lb flour" [--expires 2026-12-01] [--source manual]
  receipt_to_pantry.py --remove "flour"
  receipt_to_pantry.py --list

Paste format (one item/line): "[qty] [unit] item [| expires YYYY-MM-DD]"
  e.g. "2 lb chuck roast | expires 2026-07-14", "strawberries", "1 dozen eggs"
--receipt mode additionally strips prices ($4.99), totals/tax/store-noise lines.
Idempotent per --source: re-running the same source replaces that source's rows instead
of duplicating them. Rows are last-write-wins (live_state class, MEMORY_POLICY)."""
import argparse, os, re, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brainlib import ROOT, today

PANTRY = os.path.join(ROOT, "domains", "concierge", "kitchen", "PANTRY.md")
UNITS = {"lb", "lbs", "oz", "g", "kg", "ml", "l", "cup", "cups", "dozen", "count", "ct",
         "pack", "packs", "can", "cans", "jar", "jars", "bunch", "bag", "bags", "box",
         "boxes", "stick", "sticks", "quart", "pint", "gallon", "each"}
NOISE = re.compile(r"^(subtotal|total|tax|change|cash|card|visa|debit|credit|balance|"
                   r"savings|member|thank|welcome)\b", re.I)
# full-line noise: pure date/time/number lines, dividers, store headers ("VONS STORE #2114")
FULLNOISE = re.compile(r"^([\d/:.\-\s]+|[*=\-_]{3,})$|store\s*#|market\s*#", re.I)
DEFAULT_EXPIRY_DAYS = {  # conservative fresh-item guesses; blank = shelf-stable/unknown
    "strawberr": 4, "berr": 4, "lettuce": 5, "spinach": 5, "milk": 7, "cream": 7,
    "chicken": 2, "beef": 3, "fish": 2, "pork": 3, "herb": 5, "cilantro": 5, "lime": 14,
    "lemon": 14, "mushroom": 5, "puff pastry": 3,
}


def parse_line(line, receipt_mode):
    s = line.strip()
    if not s or s.startswith("#") or s.startswith("|"):
        return None
    if receipt_mode:
        if NOISE.match(s) or FULLNOISE.search(s):
            return None
        s = re.sub(r"\$?\d+\.\d{2}\b", "", s).strip(" .@xX*")
        if not s:
            return None
    expires = ""
    if "| expires" in s.lower():
        s, _, exp = s.partition("|")
        m = re.search(r"\d{4}-\d{2}-\d{2}", exp)
        expires = m.group(0) if m else ""
        s = s.strip()
    qty, unit = "1", ""
    m = re.match(r"^(\d+(?:\.\d+)?)\s*[xX]?\s+(.*)$", s)
    if m:
        qty, s = m.group(1), m.group(2)
    parts = s.split(None, 1)
    if len(parts) == 2 and parts[0].lower().rstrip(".") in UNITS:
        unit, s = parts[0].lower().rstrip("."), parts[1]
    item = re.sub(r"\s+", " ", s).strip(" -,.").lower()
    if not item or len(item) < 2:
        return None
    if not expires:
        for key, days in DEFAULT_EXPIRY_DAYS.items():
            if key in item:
                expires = (datetime.date.today() + datetime.timedelta(days=days)).isoformat()
                break
    return item, qty, unit, expires


def load():
    text = open(PANTRY, encoding="utf-8").read()
    rows = []
    in_inv = False
    for line in text.splitlines():
        if line.startswith("## Inventory"):
            in_inv = True
            continue
        if in_inv and line.startswith("## "):
            in_inv = False
        if in_inv and line.startswith("|") and "---" not in line and "| item |" not in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 7 and cells[0]:
                rows.append(cells[:7])
    return text, rows


def save(text, rows):
    rows.sort(key=lambda r: r[0])
    table = ["| item | qty | unit | confidence | expires | source | updated |",
             "|---|---|---|---|---|---|---|"] + \
            ["| " + " | ".join(r) + " |" for r in rows]
    body = "\n".join(table) if rows else "\n".join(table) + \
        "\n\n*(empty until Brendan's first paste — plans must treat pantry as unknown and say so)*"
    new = re.sub(r"(## Inventory\n\n).*?(\n\n## Shopping)",
                 r"\1" + body.replace("\\", "\\\\") + r"\2", text, flags=re.S)
    new = re.sub(r"^updated_at: .*$", f"updated_at: {today()}", new, count=1, flags=re.M)
    open(PANTRY, "w", encoding="utf-8").write(new)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paste-file")
    ap.add_argument("--receipt", action="store_true")
    ap.add_argument("--source", default="manual")
    ap.add_argument("--add")
    ap.add_argument("--expires", default="")
    ap.add_argument("--remove")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    text, rows = load()
    if a.list:
        for r in rows:
            print(" | ".join(r))
        print(f"{len(rows)} items")
        return
    if a.remove:
        keep = [r for r in rows if a.remove.lower() not in r[0]]
        print(f"removed {len(rows) - len(keep)} row(s) matching '{a.remove}'")
        save(text, keep)
        return
    new_items = []
    if a.add:
        p = parse_line(a.add, False)
        if not p:
            sys.exit(f"could not parse: {a.add}")
        item, qty, unit, exp = p
        new_items.append((item, qty, unit, a.expires or exp))
    elif a.paste_file:
        for line in open(a.paste_file, encoding="utf-8"):
            p = parse_line(line, a.receipt)
            if p:
                new_items.append(p)
    else:
        ap.print_help()
        return
    # idempotency: drop this source's previous rows, then re-add
    rows = [r for r in rows if r[5] != a.source]
    existing = {r[0]: r for r in rows}
    for item, qty, unit, exp in new_items:
        conf = "confirmed" if a.source == "manual" else "likely"
        if item in existing:            # same item from another source: last write wins
            rows.remove(existing[item])
        rows.append([item, qty, unit, conf, exp, a.source, today()])
    save(text, rows)
    print(f"pantry updated: +{len(new_items)} item(s) from source '{a.source}' "
          f"({len(rows)} total). Review expiries — defaults are guesses.")


if __name__ == "__main__":
    main()
