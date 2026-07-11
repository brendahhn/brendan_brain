#!/usr/bin/env python3
"""Cross-repo operation ledger (CROSS_REPOSITORY_POLICY.md).
Usage:
  oplog.py start <slug> --repos repo1,repo2         -> creates op record, prints id
  oplog.py set <op-id> <repo> <state>               -> planned|committed|pushed|verified|failed
  oplog.py status [<op-id>]                         -> show one/all unfinished ops"""
import os, re, subprocess, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brainlib import ROOT, today, slugify, die, now_pt


def _autocommit(path, msg):
    """Op records must persist even when the operation itself fails mid-flight
    (arch review finding #10). Commit is local-only; pushing follows the caller's flow."""
    try:
        subprocess.run(["git", "-C", ROOT, "add", os.path.relpath(path, ROOT)],
                       check=True, capture_output=True)
        subprocess.run(["git", "-C", ROOT, "commit", "-q", "-m", msg, "--only",
                        os.path.relpath(path, ROOT)], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"note: oplog autocommit skipped ({e.stderr.decode().strip()[:80]})",
              file=sys.stderr)

OPS = os.path.join(ROOT, "system", "operations")
STATES = {"planned", "committed", "pushed", "verified", "failed"}


def path_for(opid):
    return os.path.join(OPS, f"{opid}.md")


def start(slug, repos):
    opid = f"op-{today().replace('-', '')}-{slugify(slug)}"
    p = path_for(opid)
    if os.path.exists(p):
        print(opid)  # idempotent
        return
    os.makedirs(OPS, exist_ok=True)
    rl = "\n".join(f"  {r}: planned" for r in repos)
    open(p, "w", encoding="utf-8").write(f"""---
id: {opid}
artifact_type: operation
started_at: {now_pt().isoformat(timespec='seconds')}
repos:
{rl}
---
# Operation {opid}

## Log
- {now_pt().isoformat(timespec='seconds')} created
""")
    _autocommit(p, f"op: start {opid}")
    print(opid)


def set_state(opid, repo, state):
    if state not in STATES:
        die(f"bad state '{state}'")
    p = path_for(opid)
    if not os.path.exists(p):
        die(f"no such op {opid}")
    text = open(p, encoding="utf-8").read()
    new, n = re.subn(rf"^(  {re.escape(repo)}): \w+$", rf"\1: {state}", text, flags=re.M)
    if n == 0:
        die(f"repo '{repo}' not in op {opid}")
    new += f"- {now_pt().isoformat(timespec='seconds')} {repo} -> {state}\n"
    open(p, "w", encoding="utf-8").write(new)
    _autocommit(p, f"op: {opid} {repo}={state}")
    print(f"{opid}: {repo} -> {state}")


def status(opid=None):
    if not os.path.isdir(OPS):
        print("no operations")
        return
    files = [f for f in sorted(os.listdir(OPS)) if f.endswith(".md")]
    if opid:
        files = [f for f in files if f.startswith(opid)]
    unfinished = 0
    for f in files:
        text = open(os.path.join(OPS, f), encoding="utf-8").read()
        states = re.findall(r"^  ([\w.-]+): (\w+)$", text, flags=re.M)
        done = all(s == "verified" for _, s in states)
        flag = "DONE" if done else ("PARTIAL/FAILED" if any(s == "failed" for _, s in states)
                                    else "IN PROGRESS")
        if not done:
            unfinished += 1
        if opid or not done:
            print(f"{f[:-3]}: {flag} " + " ".join(f"{r}={s}" for r, s in states))
    if not opid:
        print(f"{unfinished} unfinished operation(s)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        die(__doc__)
    cmd = sys.argv[1]
    if cmd == "start":
        repos = []
        if "--repos" in sys.argv:
            repos = sys.argv[sys.argv.index("--repos") + 1].split(",")
        start(sys.argv[2], repos or ["brendan_brain"])
    elif cmd == "set":
        set_state(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == "status":
        status(sys.argv[2] if len(sys.argv) > 2 else None)
    else:
        die(f"unknown command {cmd}")
