#!/usr/bin/env python3
"""Build a practice-exam page from question data and the page template, and audit the batch.

Usage:
  python3 build_exam.py exam.json [section1.json section2.json ...] --out exam.html
  python3 build_exam.py exam.json [section files ...] --audit-only

exam.json holds the page-level content and, optionally, the sections. Sections can also be
passed as separate files (one section per file, in the order given), which is the easy way
to draft a long exam in batches. The input format is documented in references/exam-page.md.

The script never touches the template's styling or script. It fills the content slots,
computes the coverage map from the questions' source tags, and prints an audit of answer
letters, option lengths, Bloom mix and coverage. Errors block the build; warnings do not.
"""
import argparse
import html
import json
import os
import re
import sys
from collections import Counter

LETTERS = "ABCDE"
BLOOM = ["Remember", "Understand", "Apply", "Analyze", "Integrate"]
ALLOWED_TAGS = {"sub", "sup", "i", "b", "em", "strong", "br"}
HEDGES = re.compile(r"\b(can|may|might|sometimes|usually|often|typically|in some cases)\b", re.I)
ABSOLUTES = re.compile(r"\b(always|never|only|all|none|every|cannot)\b", re.I)
CLAUSE = re.compile(r"\b(because|by|which|so that|since)\b", re.I)


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def words(s):
    return len(strip_tags(s).split())


def check_fragment(s, where, errors):
    """Text fields are HTML fragments. Allow light inline markup only."""
    for m in re.finditer(r"<\s*(/?)\s*([A-Za-z][A-Za-z0-9]*)", s):
        if m.group(2).lower() not in ALLOWED_TAGS:
            errors.append(f"{where}: tag <{m.group(2)}> is not allowed here "
                          f"(write a literal '<' as &lt;; allowed tags: {', '.join(sorted(ALLOWED_TAGS))})")
    if re.search(r"&(?![A-Za-z]+;|#\d+;|#x[0-9A-Fa-f]+;)", s):
        errors.append(f"{where}: bare '&' (write &amp;)")


def table_html(t, where, errors):
    if not t:
        return ""
    heads, rows = t.get("headers") or [], t.get("rows") or []
    if not heads or not rows:
        errors.append(f"{where}: table needs headers and rows")
        return ""
    for r in rows:
        if len(r) != len(heads):
            errors.append(f"{where}: table row has {len(r)} cells, header has {len(heads)}")
    for cell in [t.get("caption", "")] + list(heads) + [c for r in rows for c in r]:
        check_fragment(str(cell), where + " table", errors)
    cap = f"<caption>{t['caption']}</caption>" if t.get("caption") else ""
    head = "".join(f"<th>{h}</th>" for h in heads)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tblwrap"><table class="dt">{cap}<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def figure_html(f, where, errors):
    if not f:
        return ""
    svg = (f.get("svg") or "").strip()
    if not svg.startswith("<svg") or not svg.endswith("</svg>"):
        errors.append(f"{where}: figure.svg must be one complete <svg>…</svg> element")
    if "viewBox" not in svg:
        errors.append(f"{where}: figure svg needs a viewBox so it scales on a phone")
    if re.search(r"<\s*(script|image|foreignObject|iframe)|\son\w+\s*=\s*[\"']|\shref\s*=", svg, re.I):
        errors.append(f"{where}: figure svg must be self-contained drawing only (no script, image, links)")
    cap = f.get("caption", "")
    check_fragment(cap, where + " figure caption", errors)
    return f'<figure class="fig">{svg}' + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"


def ranges(nums):
    out, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        out.append(str(nums[i]) if i == j else f"{nums[i]}–{nums[j]}")
        i = j + 1
    return ", ".join(out)


def load(paths):
    meta, sections = {}, []
    for p in paths:
        d = json.load(open(p, encoding="utf8"))
        if isinstance(d, list):                      # a list of sections
            sections.extend(d)
        elif "questions" in d:                       # one section
            sections.append(d)
        else:                                        # the page-level file
            meta = d
            sections.extend(d.get("sections") or [])
    return meta, sections


def convert(meta, sections):
    """Validate and convert to the template's compact data. Returns (exam, flat, errors, warnings)."""
    errors, warnings, exam, flat = [], [], [], []
    order = meta.get("source_order") or []
    n = 0
    if not sections:
        errors.append("no sections")
    for sec in sections:
        qs = []
        if not sec.get("title") or not sec.get("questions"):
            errors.append(f"section {sec.get('title')!r}: needs a title and at least one question")
        for q in sec.get("questions") or []:
            n += 1
            w = f"Q{n}"
            for k in ("stem", "explanation", "concept"):
                if not (q.get(k) or "").strip():
                    errors.append(f"{w}: missing {k}")
                check_fragment(q.get(k) or "", f"{w} {k}", errors)
            opts = q.get("options") or []
            if not 2 <= len(opts) <= 5:
                errors.append(f"{w}: has {len(opts)} options; the page supports 2 to 5")
            correct = [i for i, o in enumerate(opts) if o.get("correct")]
            if len(correct) != 1:
                errors.append(f"{w}: exactly one option must be marked correct (found {len(correct)})")
            o_out = []
            for i, o in enumerate(opts):
                check_fragment(o.get("text") or "", f"{w} option {LETTERS[i] if i < 5 else i}", errors)
                check_fragment(o.get("why") or "", f"{w} why {LETTERS[i] if i < 5 else i}", errors)
                if not (o.get("text") or "").strip():
                    errors.append(f"{w}: empty option text")
                if not o.get("correct") and not (o.get("why") or "").strip():
                    errors.append(f"{w}: distractor {LETTERS[i] if i < 5 else i} has no 'why' line")
                o_out.append([o.get("text", ""), 1 if o.get("correct") else 0, "" if o.get("correct") else o.get("why", "")])
            if q.get("bloom") not in BLOOM:
                errors.append(f"{w}: bloom must be one of {BLOOM}, got {q.get('bloom')!r}")
            src = q.get("source")
            src = [src] if isinstance(src, str) else list(src or [])
            if not src:
                errors.append(f"{w}: missing source")
            for s in src:
                if " / " in s:
                    errors.append(f"{w}: source name {s!r} must not contain ' / ' (the page uses it as the separator)")
                if order and s not in order:
                    errors.append(f"{w}: source {s!r} is not in source_order")
            if q.get("bloom") == "Integrate" and len(src) < 2:
                warnings.append(f"{w}: tagged Integrate but lists one source")
            stem = q.get("stem", "") + table_html(q.get("table"), w, errors)
            item = {"p": stem, "f": figure_html(q.get("figure"), w, errors), "o": o_out,
                    "e": q.get("explanation", ""), "c": q.get("concept", ""), "b": q.get("bloom", ""),
                    "t": " / ".join(src), "q": 1 if q.get("quantitative") else 0,
                    "d": 1 if (q.get("data") or q.get("figure") or q.get("table")) else 0}
            qs.append(item)
            flat.append({"n": n, "src": src, "opts": o_out, "correct": correct[0] if len(correct) == 1 else None,
                         "bloom": q.get("bloom"), "q": item["q"], "d": item["d"], "concept": q.get("concept", "")})
        exam.append({"title": sec.get("title", ""), "qs": qs})
    for k in ("course", "title", "scope_label", "intro_html", "scope_html"):
        if not (meta.get(k) or "").strip():
            errors.append(f"exam.json: missing {k}")
    return exam, flat, errors, warnings


def audit(meta, flat, warnings):
    out = []
    total = len(flat)
    pct = lambda a, b: f"{(100 * a / b):.0f}%" if b else "n/a"
    out.append(f"Questions: {total}")
    letters = Counter(LETTERS[f["correct"]] for f in flat if f["correct"] is not None)
    out.append("Answer letters: " + ", ".join(f"{l} {letters.get(l, 0)}" for l in LETTERS))
    runs, run = [], 1
    for a, b in zip(flat, flat[1:]):
        run = run + 1 if a["correct"] == b["correct"] else 1
        if run == 3:
            runs.append(f"Q{b['n'] - 2}–Q{b['n']}")
    out.append("Same letter three or more times in a row: " + (", ".join(runs) or "none"))

    five = [f for f in flat if len(f["opts"]) == 5 and f["correct"] is not None]
    longest = shortest = 0
    spread, only = [], []
    for f in flat:
        if f["correct"] is None:
            continue
        L = [words(o[0]) for o in f["opts"]]
        c = f["correct"]
        if len(f["opts"]) == 5:
            longest += L[c] == max(L) and L.count(max(L)) == 1
            shortest += L[c] == min(L)
        if max(L) - min(L) > max(3, round(0.2 * max(L))):
            spread.append(f"Q{f['n']} ({min(L)}–{max(L)} words)")
        texts = [strip_tags(o[0]) for o in f["opts"]]
        for label, rx in (("number", re.compile(r"\d")), ("because/by/which clause", CLAUSE), ("hedge", HEDGES)):
            hits = [bool(rx.search(t)) for t in texts]
            if hits[c] and sum(hits) == 1 and len(texts) > 2:
                only.append(f"Q{f['n']} ({label})")
    out.append(f"Correct answer is the single longest option (5-option items): {longest} of {len(five)} = {pct(longest, len(five))} (target 20% or less)")
    out.append(f"Correct answer is shortest or tied-shortest (5-option items): {shortest} of {len(five)} = {pct(shortest, len(five))} (target 20% or more)")
    out.append("Option lengths outside the 20% / 3-word band: " + (", ".join(spread) or "none"))
    out.append("Correct option is the only one with a give-away feature: " + (", ".join(only) or "none"))
    ca = sum(bool(ABSOLUTES.search(strip_tags(f["opts"][f["correct"]][0]))) for f in flat if f["correct"] is not None)
    da = sum(bool(ABSOLUTES.search(strip_tags(o[0]))) for f in flat for i, o in enumerate(f["opts"]) if i != f["correct"])
    ch = sum(bool(HEDGES.search(strip_tags(f["opts"][f["correct"]][0]))) for f in flat if f["correct"] is not None)
    dh = sum(bool(HEDGES.search(strip_tags(o[0]))) for f in flat for i, o in enumerate(f["opts"]) if i != f["correct"])
    nd = sum(len(f["opts"]) - 1 for f in flat)
    out.append(f"Absolutes: in {ca}/{total} correct answers, {da}/{nd} distractors. Hedges: in {ch}/{total} correct answers, {dh}/{nd} distractors.")

    bl = Counter(f["bloom"] for f in flat)
    out.append("Bloom: " + ", ".join(f"{b} {bl.get(b, 0)} ({pct(bl.get(b, 0), total)})" for b in BLOOM))
    nq, ndq = sum(f["q"] for f in flat), sum(f["d"] for f in flat)
    out.append(f"Quantitative: {nq} ({pct(nq, total)}). Data/figure: {ndq} ({pct(ndq, total)}).")
    per = Counter(s for f in flat for s in f["src"])
    order = meta.get("source_order") or list(dict.fromkeys(s for f in flat for s in f["src"]))
    out.append("Questions per source: " + "; ".join(f"{s} {per.get(s, 0)}" for s in order))
    empty = [s for s in order if not per.get(s)]
    if empty:
        warnings.append("sources with no question: " + ", ".join(empty))
    dup = [c for c, k in Counter(f["concept"].strip().lower() for f in flat).items() if k > 1 and c]
    if dup:
        warnings.append("concept line used more than once (possible duplicate question): " + "; ".join(dup))
    return out


def coverage_html(meta, flat):
    order = meta.get("source_order") or list(dict.fromkeys(s for f in flat for s in f["src"]))
    noun = meta.get("source_noun", "lecture")
    rows = ""
    for s in order:
        nums = [f["n"] for f in flat if s in f["src"]]
        if nums:
            rows += (f'<div class="brow"><span class="nm">{html.escape(s)}</span>'
                     f'<span class="sc">{len(nums)}</span><span class="covq">{ranges(nums)}</span></div>')
    return ('<details class="navwrap covwrap"><summary>Coverage map — ' + html.escape(noun) +
            ' → question numbers (integrating questions are listed under every ' + html.escape(noun) +
            ' they draw on)</summary><div class="cov">' + rows + '</div></details>')


def build(meta, exam, flat, template):
    t = open(template, encoding="utf8").read()
    total = len(flat)
    kicker = (f"{html.escape(meta['course']).upper()} &middot; {total} QUESTIONS &middot; "
              f"<b>{html.escape(meta['scope_label']).upper()}</b>")
    data = json.dumps(exam, ensure_ascii=False).replace("</", "<\\/").replace("<!--", "<\\!--")
    slots = {
        "<!--__PAGE_TITLE__-->": html.escape(meta.get("page_title") or meta["title"]),
        "<!--__KICKER__-->": kicker,
        "<!--__TITLE__-->": html.escape(meta["title"]),
        "<!--__INTRO__-->": meta["intro_html"],
        "<!--__COVERAGE__-->": coverage_html(meta, flat),
        "<!--__SCOPE__-->": meta["scope_html"],
        "/*__EXAM_DATA__*/[]": data,
    }
    for k, v in slots.items():
        if t.count(k) != 1:
            sys.exit(f"template slot {k} not found exactly once; the template asset has been altered")
        t = t.replace(k, v)
    return t


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", help="exam.json, then any section files in order")
    ap.add_argument("--out", help="path for the built page")
    ap.add_argument("--audit-only", action="store_true", help="validate and print the audit without building")
    ap.add_argument("--template", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "exam-template.html"))
    a = ap.parse_args()

    meta, sections = load(a.inputs)
    exam, flat, errors, warnings = convert(meta, sections)
    if a.audit_only:
        errors = [e for e in errors if not e.startswith("exam.json: missing")]
    for k in ("intro_html", "scope_html"):
        check_fragment(meta.get(k) or "", f"exam.json {k}", errors)
    lines = audit(meta, flat, warnings) if flat else []
    print("AUDIT")
    for l in lines:
        print("  " + l)
    for w in warnings:
        print("WARNING  " + w)
    for e in errors:
        print("ERROR    " + e)
    if errors:
        sys.exit(f"{len(errors)} error(s); nothing built")
    if a.audit_only:
        return
    if not a.out:
        sys.exit("give --out PATH, or --audit-only")
    page = build(meta, exam, flat, a.template)
    open(a.out, "w", encoding="utf8").write(page)
    print(f"Built {a.out}: {len(flat)} questions in {len(exam)} sections, {len(page) // 1024} KB")


if __name__ == "__main__":
    main()
