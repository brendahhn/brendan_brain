#!/usr/bin/env python3
"""Create a new domain (DOMAIN_POLICY.md). Usage:
new_domain.py <slug> --title "Title" [--sensitivity personal] [--reason "why it earns a domain"]"""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brainlib import ROOT, today, slugify, die


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--title", required=True)
    ap.add_argument("--sensitivity", default="personal")
    ap.add_argument("--reason", default="")
    a = ap.parse_args()
    slug = slugify(a.slug)
    d = os.path.join(ROOT, "domains", slug)
    if os.path.exists(os.path.join(d, "DOMAIN_PROFILE.md")):
        print(f"EXISTS domains/{slug}/")
        return
    os.makedirs(d, exist_ok=True)
    reason = a.reason or "created on request"
    open(os.path.join(d, "DOMAIN_PROFILE.md"), "w", encoding="utf-8").write(f"""---
id: domain-{slug}
artifact_type: domain_profile
domain: {slug}
status: active
sensitivity: {a.sensitivity}
created_at: {today()}
created_by: brain-domain
---
# Domain: {a.title}

Created {today()}. Reason: {reason}

Subfolders (knowledge/ research/ observations/ predictions/ tasks/) are created when first
needed — no empty scaffolding (DOMAIN_POLICY.md).
""")
    print(f"domains/{slug}/DOMAIN_PROFILE.md")


if __name__ == "__main__":
    main()
