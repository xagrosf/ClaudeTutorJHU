#!/usr/bin/env python3
"""Draw exam figures (traces, plots, I-V curves, time courses) as inline SVG in the page's house style.

    import sys; sys.path.insert(0, "<skill>/scripts")
    from svgfig import line_plot
    svg = line_plot(
        title="Red-cell sugar entry vs external concentration",
        xlabel="External sugar (mM)", ylabel="Initial rate of entry (arbitrary units)",
        xlim=(0, 20), ylim=(0, 100), xticks=[0, 5, 10, 15, 20], yticks=[0, 25, 50, 75, 100],
        series=[{"label": "D-glucose", "points": [(0, 0), (2, 40), (5, 66), (20, 90)]},
                {"label": "L-glucose", "points": [(0, 0), (20, 8)]}],
        vlines=[{"x": 2, "label": "ATP added"}],          # dashed vertical markers
        hlines=[{"y": 0}],                                # e.g. a zero-current line
        marks=[{"x": 5, "y": 66, "text": "X"}],           # letters the stem or options refer to
    )

Put the returned string in a question's figure.svg. Series are told apart by dash pattern as
well as colour, so the figure still reads in greyscale. Plot only values the course materials
show or state; a figure is data, and invented data is an outside fact.

For diagrams that are not x-y plots, write the SVG by hand with the same conventions:
viewBox 560 wide, white background, the INK/MUTED/GRID colours and FONT below, 11-13 px text.
"""
from html import escape

W = 560
LEFT, RIGHT, TOP, BOTTOM = 68, 538, 36, 272
INK, MUTED, GRID = "#14202A", "#5D6C77", "#E3E8EB"
COLORS = ["#0F5F6B", "#9C4A32", "#5B4B9A", "#14202A"]
DASHES = ["", "7 4", "2 3", "10 3 2 3"]
FONT = "system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif"


def _text(x, y, s, size=11, anchor="middle", fill=MUTED, weight=400, extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{fill}" '
            f'font-weight="{weight}" {extra}font-family="{FONT}">{escape(str(s))}</text>')


def _fmt(v):
    return str(int(v)) if float(v).is_integer() else f"{v:g}"


def line_plot(title, xlabel, ylabel, xlim, ylim, xticks, yticks, series,
              vlines=(), hlines=(), marks=(), legend=True):
    sx = lambda x: LEFT + (x - xlim[0]) / (xlim[1] - xlim[0]) * (RIGHT - LEFT)
    sy = lambda y: BOTTOM - (y - ylim[0]) / (ylim[1] - ylim[0]) * (BOTTOM - TOP)
    show_legend = legend and any(s.get("label") for s in series)
    height = 350 if show_legend else 330
    o = [f'<svg viewBox="0 0 {W} {height}" width="{W}" role="img" aria-label="{escape(title)}" '
         f'style="max-width:100%;height:auto;background:#fff">']
    o.append(_text((LEFT + RIGHT) / 2, 16, title, 13, fill=INK, weight=600))
    for x in xticks:
        o.append(f'<line x1="{sx(x):.1f}" y1="{TOP}" x2="{sx(x):.1f}" y2="{BOTTOM}" stroke="{GRID}"/>')
        o.append(_text(sx(x), BOTTOM + 17, _fmt(x)))
    for y in yticks:
        o.append(f'<line x1="{LEFT}" y1="{sy(y):.1f}" x2="{RIGHT}" y2="{sy(y):.1f}" stroke="{GRID}"/>')
        o.append(_text(LEFT - 7, sy(y) + 4, _fmt(y), anchor="end"))
    o.append(f'<line x1="{LEFT}" y1="{BOTTOM}" x2="{RIGHT}" y2="{BOTTOM}" stroke="{INK}"/>')
    o.append(f'<line x1="{LEFT}" y1="{TOP}" x2="{LEFT}" y2="{BOTTOM}" stroke="{INK}"/>')
    for h in hlines:
        o.append(f'<line x1="{LEFT}" y1="{sy(h["y"]):.1f}" x2="{RIGHT}" y2="{sy(h["y"]):.1f}" stroke="{MUTED}" stroke-dasharray="5 4"/>')
        if h.get("label"):
            o.append(_text(RIGHT - 4, sy(h["y"]) - 5, h["label"], 10.5, anchor="end"))
    for v in vlines:
        o.append(f'<line x1="{sx(v["x"]):.1f}" y1="{TOP}" x2="{sx(v["x"]):.1f}" y2="{BOTTOM}" stroke="{MUTED}" stroke-dasharray="5 4"/>')
        if v.get("label"):
            o.append(_text(sx(v["x"]) + 4, TOP + 12, v["label"], 10.5, anchor="start"))
    for i, s in enumerate(series):
        color = s.get("color") or COLORS[i % len(COLORS)]
        dash = s.get("dash", DASHES[i % len(DASHES)])
        d = " ".join(("M" if j == 0 else "L") + f"{sx(x):.1f},{sy(y):.1f}" for j, (x, y) in enumerate(s["points"]))
        o.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.4" stroke-dasharray="{dash}" stroke-linejoin="round"/>')
    for m in marks:
        o.append(_text(sx(m["x"]) + m.get("dx", 0), sy(m["y"]) + m.get("dy", -8), m["text"], 12, fill=INK, weight=600))
    o.append(_text((LEFT + RIGHT) / 2, 322 if show_legend else 316, xlabel, 12, fill=INK))
    o.append(_text(16, (TOP + BOTTOM) / 2, ylabel, 12, fill=INK, extra=f'transform="rotate(-90 16.0 {(TOP + BOTTOM) / 2:.1f})" '))
    if show_legend:
        x = LEFT
        for i, s in enumerate(series):
            if not s.get("label"):
                continue
            color = s.get("color") or COLORS[i % len(COLORS)]
            dash = s.get("dash", DASHES[i % len(DASHES)])
            o.append(f'<line x1="{x:.1f}" y1="336.0" x2="{x + 22:.1f}" y2="336.0" stroke="{color}" stroke-width="2.4" stroke-dasharray="{dash}"/>')
            o.append(_text(x + 28, 340, s["label"], 11, anchor="start", fill=INK))
            x += 28 + 6.6 * len(str(s["label"])) + 18
    o.append("</svg>")
    return "".join(o)


if __name__ == "__main__":
    print(line_plot("Demo", "x", "y", (0, 10), (0, 100), [0, 5, 10], [0, 50, 100],
                    [{"label": "A", "points": [(0, 0), (10, 100)]}, {"label": "B", "points": [(0, 100), (10, 0)]}]))
