"""Shared helpers for Brendan Brain tools. Stdlib only (no PyYAML: frontmatter here is a
deliberately small YAML subset — scalars, [inline, lists], and simple nested maps one level
deep for `repos:`/question entries)."""
import os, re, sys, datetime
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── Time policy (V2, 2026-07-11): containers run UTC, Brendan lives in Pacific.
# ALL user-facing dates (edition names, task dates, freshness windows, watch dueness)
# are America/Los_Angeles. Machine timestamps that need wall-clock precision should be
# stored as ISO datetimes WITH offset. See system/SCHEDULE_PLAN.md.
PACIFIC = ZoneInfo("America/Los_Angeles")


def now_pt():
    return datetime.datetime.now(tz=PACIFIC)


def editorial_date(dt=None, cutoff_hour=20):
    """Which morning edition a result belongs to: content produced at/after 20:00 PT
    belongs to TOMORROW's paper (a 11pm result is for the morning reader), unless the
    caller explicitly dates it otherwise. Pass an aware datetime to evaluate a specific
    instant."""
    dt = dt or now_pt()
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=PACIFIC)
    dt = dt.astimezone(PACIFIC)
    d = dt.date()
    if dt.hour >= cutoff_hour:
        d += datetime.timedelta(days=1)
    return d.isoformat()

ARTIFACT_TYPES = {"task", "timeline", "knowledge", "report", "prediction", "outcome",
                  "decision", "watch", "question", "annotation", "edition", "operation",
                  "domain_profile", "live_state"}
SENSITIVITIES = {"public", "personal", "private", "health", "financial"}
TASK_STATUSES = {"inbox", "triaged", "active", "waiting_for_brendan",
                 "continuing_with_assumption", "scheduled", "verification",
                 "ready_for_publication", "published", "completed", "failed",
                 "cancelled", "watching"}
# folder → statuses allowed to live there
FOLDER_STATUS = {
    "inbox": {"inbox"},
    "active": {"triaged", "active", "continuing_with_assumption", "verification",
               "ready_for_publication", "published"},
    "waiting_for_brendan": {"waiting_for_brendan"},
    "scheduled": {"scheduled"},
    "watches": {"watching"},
    "completed": {"completed", "published"},
    "failed": {"failed", "cancelled"},
}
SENSITIVE = {"health", "private", "financial"}

# ── Watch eligibility (production bug B, 2026-07-11): the watch runner and the newspaper
# builder MUST share one definition of "a watch that exists for real purposes right now".
# A cancelled synthetic test watch once reached a real edition because each tool had its
# own filter.
WATCH_EXCLUDED_STATUSES = {"cancelled", "completed", "failed", "archived", "expired",
                           "published"}
SYNTHETIC_MARKERS = ("synthetic", "fixture", "test-only")


def is_active_watch(fm, rel=""):
    """True only for a live, real watch: watch-typed, not in a terminal status, not a
    synthetic/fixture artifact, not living under tests/."""
    if fm.get("artifact_type") != "watch" and str(fm.get("status")) != "watching":
        return False
    if str(fm.get("status")) in WATCH_EXCLUDED_STATUSES:
        return False
    hay = f"{fm.get('id', '')} {fm.get('title', '')} {fm.get('dedupe_key', '')}".lower()
    if any(m in hay for m in SYNTHETIC_MARKERS):
        return False
    if rel.startswith("tests" + os.sep) or "fixture" in rel.lower():
        return False
    return True


def watch_is_due(fm, on_date):
    """Dueness for an ELIGIBLE watch. Empty next_run means due ONLY for a never-run watch
    (first run); an empty next_run on a watch that HAS run is malformed, not due
    (production bug B requirement 3)."""
    nr, lr = str(fm.get("next_run", "") or ""), str(fm.get("last_run", "") or "")
    if not nr:
        return not lr
    return nr <= on_date


def parse_frontmatter(text):
    """Return (dict, body). Empty dict if no frontmatter."""
    if not text.startswith("---"):
        return {}, text
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if not m:
        return {}, text
    raw, body = m.group(1), text[m.end():]
    fm, cur_key, cur_map = {}, None, None
    for line in raw.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        s = line.strip()
        if indent >= 2 and cur_key and s.startswith("- "):
            fm.setdefault(cur_key, [])
            if isinstance(fm[cur_key], list):
                fm[cur_key].append(s[2:].strip())
            continue
        if indent >= 2 and cur_map is not None and ":" in s:
            k, v = s.split(":", 1)
            cur_map[k.strip()] = _scalar(v)
            continue
        cur_map = None
        if ":" in s:
            k, v = s.split(":", 1)
            k, v = k.strip(), v.strip()
            cur_key = k
            if v == "":
                fm[k] = {}
                cur_map = fm[k]
            elif v.startswith("[") and v.endswith("]"):
                inner = v[1:-1].strip()
                fm[k] = [x.strip().strip("'\"") for x in inner.split(",")] if inner else []
            else:
                fm[k] = _scalar(v)
    return fm, body


def _scalar(v):
    v = v.strip()
    v = re.sub(r"\s+#.*$", "", v)  # trailing comment
    return v.strip().strip("'\"")


def iter_artifacts():
    """Yield (relpath, frontmatter, body) for every .md with valid-looking frontmatter."""
    skip = {".git", "node_modules", "tests"}
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in skip and not d.startswith(".")]
        for fn in sorted(filenames):
            if not fn.endswith(".md"):
                continue
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, ROOT)
            try:
                text = open(p, encoding="utf-8").read()
            except OSError:
                continue
            fm, body = parse_frontmatter(text)
            if fm.get("id"):
                yield rel, fm, body


def today():
    """PACIFIC calendar date (time policy above) — the user-facing 'today' everywhere."""
    return now_pt().date().isoformat()


def slugify(s, maxlen=40):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    if len(s) <= maxlen:
        return s
    cut = s[:maxlen]
    return cut[:cut.rfind("-")] if "-" in cut else cut  # never end mid-word


def die(msg, code=1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)
