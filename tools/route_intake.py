#!/usr/bin/env python3
"""Deterministic first-pass router for system/INTAKE_POLICY.md. It SUGGESTS; the session's
model judgment decides (and must tell Brendan the decision in one plain sentence).
Usage: route_intake.py --request "verbatim ask" [--explain]
Prints one machine-readable line:
  MODE=<1..6> NAME=<mode-name> ANSWER_NOW=<y|n> TASK=<none|task|watch> CAPTURE=<y|n|ask> EXPAND=<y|n> FLAGS=<suggested new_task.py flags or ->
plus, with --explain, the sentence to say to Brendan."""
import argparse, re, sys

MODES = {1: "immediate", 2: "immediate_plus_memory", 3: "immediate_plus_overnight",
         4: "same_day_task", 5: "background_research", 6: "watch"}

# Override phrases (checked first; any hit wins, later rules refine). Patterns are
# lowercase substrings/regex over Brendan's words — examples, deliberately generous.
OVERRIDES = [
    (r"\b(do ?n[o']?t save|don't remember|no need to (remember|save)|off the record)\b", ("capture", "n")),
    (r"\b(remember this|save this|add (this )?to (the )?brain)\b", ("capture", "y")),
    (r"\b(answer (this |me )?now|just answer|just the answer|quick answer only)\b", ("mode", 1)),
    (r"\bjust a one[- ]?off\b|\bone[- ]?off question\b|\bone time question\b", ("mode", 1)),
    (r"\b(research (it|this) overnight|overnight (pass|research|expansion)|more (depth|detail) tomorrow|quick answer (and|then) research)\b", ("mode", 3)),
    (r"\b(tomorrow'?s paper|in the (morning )?paper|newspaper article|morning article)\b", ("publish", "newspaper")),
    (r"\b(make (this|it) a watch|keep watching|keep an eye on|track this|alert me when)\b", ("mode", 6)),
    (r"\b(before (dinner|tonight|this evening)|by (tonight|end of day|eod)|this afternoon|today\b)", ("mode", 4)),
    (r"\b(deep (report|dive)|thorough|until it'?s strong|exhaustive)\b", ("depth", "deep")),
]

TIME_SENSITIVE = r"\b(price|listing|in stock|inventory|score|deadline|sale|open(s|ing)? (at|until)|tickets?)\b"
PREFERENCE_SIGNAL = r"\b(i (love|hate|prefer|always|never|can'?t stand)|my favorite)\b"


def route(text):
    t = " " + text.lower().strip() + " "
    d = {"mode": None, "capture": None, "publish": None, "depth": None}
    for pat, (key, val) in OVERRIDES:
        if re.search(pat, t):
            if d[key] is None:
                d[key] = val
    mode = d["mode"]
    if mode is None:
        if re.search(r"\?\s*$", text) and len(text) < 200 and not re.search(r"\b(research|compare|find|look into)\b", t):
            mode = 1                     # short direct question → answer now
        elif re.search(r"\b(research|compare|evaluate|find (me|the) (best|strongest)|look into)\b", t):
            mode = 5
        else:
            mode = 1                     # unknown → answer now, capture undecided
    capture = d["capture"] or ("y" if mode == 2 else ("n" if mode == 1 else "ask"))
    if d["capture"] == "y" and mode == 1:
        mode = 2
    answer_now = "y" if mode in (1, 2, 3) else "n"
    task = "watch" if mode == 6 else ("task" if mode in (3, 4, 5) else "none")
    expand = "y" if mode == 3 else "n"
    flags = []
    if task != "none":
        if mode == 3:
            flags += ["--depth deep", "--effort 2_pass"]
        if mode == 4:
            flags += ["--urgency high", "--deadline TODAY"]
        if mode == 6:
            flags += ["--recurrence watch"]
        if d["depth"] == "deep" and "--depth deep" not in flags:
            flags += ["--depth deep"]
        flags += [f"--publish {d['publish'] or 'file_only'}"]
    hints = []
    if re.search(TIME_SENSITIVE, t):
        hints.append("time_sensitive: verify near use / consider watch")
    if re.search(PREFERENCE_SIGNAL, t):
        hints.append("preference_signal: log evidence in PROPOSED_RULES.md")
    return mode, answer_now, task, capture, expand, flags, hints


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--request", required=True)
    ap.add_argument("--explain", action="store_true")
    a = ap.parse_args()
    mode, answer_now, task, capture, expand, flags, hints = route(a.request)
    print(f"MODE={mode} NAME={MODES[mode]} ANSWER_NOW={answer_now} TASK={task} "
          f"CAPTURE={capture} EXPAND={expand} FLAGS={' '.join(flags) if flags else '-'}")
    for h in hints:
        print(f"HINT {h}")
    if a.explain:
        say = {1: "I'll answer now and won't save anything.",
               2: "I'll answer now and remember the durable part.",
               3: "Quick answer now; queuing a deep overnight pass.",
               4: "Treating this as a same-day task with a deadline today.",
               5: "Queued as background research; it'll surface when done.",
               6: "Setting up a recurring watch; say 'stop watching' to end it."}[mode]
        print(f"SAY {say} (Override anytime: 'answer now', 'research overnight', "
              f"'make it a watch', 'don't save this'.)")


if __name__ == "__main__":
    main()
