#!/usr/bin/env python3
"""Generate the `man yaniv` header SVGs (dark + light) into assets/.

Edit LINES below, then run: python3 scripts/build_header.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

THEMES = {
    "dark": dict(bg="#0d1117", bar="#161b22", border="#30363d", fg="#e6edf3",
                 dim="#8b949e", head="#f0883e", accent="#58a6ff", prompt="#3fb950"),
    "light": dict(bg="#ffffff", bar="#f6f8fa", border="#d0d7de", fg="#1f2328",
                  dim="#59636e", head="#bc4c00", accent="#0969da", prompt="#1a7f37"),
}

# Each line is a list of (text, css-class) segments. None = blank line.
LINES = [
    [("$ ", "p"), ("man yaniv", "b")],
    "MANHEADER",
    None,
    [("NAME", "h")],
    [("    yaniv", "b"), (" — ships AI products on the edge, teaches C to humans", "")],
    None,
    [("SYNOPSIS", "h")],
    [("    yaniv ", "b"), ("[", "d"), ("--day", "a"), (" taboola", ""), ("] [", "d"),
     ("--evening", "a"), (" hac", ""), ("] [", "d"), ("--night", "a"), (" ship", ""), ("]", "d")],
    None,
    [("DESCRIPTION", "h")],
    [("    Software Engineer at ", ""), ("Taboola", "b"), (", Tel Aviv.", "")],
    [("    CS Instructor at ", ""), ("Hadassah Academic College", "b"), (" — C & Operating Systems.", "")],
    [("    Builds on ", ""), ("Cloudflare Workers · D1 · R2", "a"), (", wired to ", ""),
     ("Claude + MCP", "a"), (".", "")],
    None,
    [("SEE ALSO", "h")],
    [("    suitedcv", "a"), ("(1)  ", "d"), ("pashutcode", "a"), ("(1)  ", "d"),
     ("dalpak", "a"), ("(1)  ", "d"), ("poetools", "a"), ("(1)", "d")],
    None,
    "CURSOR",
]

W, PAD, BAR, LH, FS = 820, 28, 36, 22, 15
FONT = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"


def build(t: dict) -> str:
    h = BAR + PAD + LH * len(LINES) + PAD - LH // 2
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" '
        f'role="img" aria-label="man yaniv — Software Engineer at Taboola, CS Instructor at HAC">',
        "<style>",
        f"text{{font-family:{FONT};font-size:{FS}px;fill:{t['fg']};white-space:pre}}",
        f".b{{font-weight:700}} .h{{font-weight:700;fill:{t['head']}}} .d{{fill:{t['dim']}}}",
        f".a{{fill:{t['accent']}}} .p{{fill:{t['prompt']};font-weight:700}}",
        ".l{animation:in .35s ease-out backwards}",
        "@keyframes in{from{opacity:0}}",
        ".c{animation:blink 1.1s steps(1) infinite}",
        "@keyframes blink{50%{opacity:0}}",
        "@media (prefers-reduced-motion:reduce){.l,.c{animation:none}}",
        "</style>",
        f'<rect x=".5" y=".5" width="{W-1}" height="{h-1}" rx="10" fill="{t["bg"]}" stroke="{t["border"]}"/>',
        f'<path d="M10.5 .5h{W-21}a10 10 0 0 1 10 10v{BAR-10}h-{W-1}v-{BAR-10}a10 10 0 0 1 10-10z" fill="{t["bar"]}"/>',
        f'<line x1=".5" y1="{BAR}" x2="{W-.5}" y2="{BAR}" stroke="{t["border"]}"/>',
    ]
    for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        out.append(f'<circle cx="{22 + i*20}" cy="{BAR/2}" r="6" fill="{c}"/>')
    out.append(f'<text x="{W/2}" y="{BAR/2 + 5}" text-anchor="middle" class="d" style="font-size:13px">yaniv@hac: ~</text>')

    y = BAR + PAD + 4
    for i, line in enumerate(LINES):
        delay = f'style="animation-delay:{0.15 + i*0.07:.2f}s"'
        if line == "MANHEADER":
            out.append(f'<g class="l" {delay}>'
                       f'<text x="{PAD}" y="{y}" class="b">YANIV(1)</text>'
                       f'<text x="{W/2}" y="{y}" text-anchor="middle" class="d">Field Manual</text>'
                       f'<text x="{W-PAD}" y="{y}" text-anchor="end" class="b">YANIV(1)</text></g>')
        elif line == "CURSOR":
            out.append(f'<g class="l" {delay}><text x="{PAD}" y="{y}"><tspan class="p">$ </tspan>'
                       f'<tspan class="c" style="fill:{t["fg"]}">█</tspan></text></g>')
        elif line:
            spans = "".join(f'<tspan class="{cls}">{escape(txt)}</tspan>' if cls else f"<tspan>{escape(txt)}</tspan>"
                            for txt, cls in line)
            out.append(f'<g class="l" {delay}><text x="{PAD}" y="{y}">{spans}</text></g>')
        y += LH
    out.append("</svg>")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    assets = Path(__file__).resolve().parent.parent / "assets"
    assets.mkdir(exist_ok=True)
    for name, theme in THEMES.items():
        (assets / f"header-{name}.svg").write_text(build(theme), encoding="utf-8")
        print(f"wrote assets/header-{name}.svg")
