"""Shared helpers for Brendan Brain tools. Stdlib only (no PyYAML: frontmatter here is a
deliberately small YAML subset — scalars, [inline, lists], and simple nested maps one level
deep for `repos:`/question entries)."""
import os, re, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
    return datetime.date.today().isoformat()


def slugify(s, maxlen=40):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    if len(s) <= maxlen:
        return s
    cut = s[:maxlen]
    return cut[:cut.rfind("-")] if "-" in cut else cut  # never end mid-word


def die(msg, code=1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)
