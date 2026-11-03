#!/usr/bin/env python3
"""Generates every SVG used by README.md (no external services needed).

Run from the repo root:  python src/build.py
Output goes to ./assets. All motion is CSS and respects prefers-reduced-motion.
"""
import glob
import os
import textwrap
from xml.sax.saxutils import escape as esc

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets")
os.makedirs(OUT, exist_ok=True)
for _f in glob.glob(os.path.join(OUT, "*.svg")):
    os.remove(_f)

# ---------------------------------------------------------------- palette
BG0 = "#090D14"
BG1 = "#0E1520"
BG2 = "#131C2A"
LINE = "#1F2B3D"
LINE2 = "#2A3A52"
TEXT = "#E8EEF8"
SOFT = "#C5D0E0"
MUTED = "#95A3B8"
DIM = "#5F6D82"
TEAL = "#2DD4BF"
VIOLET = "#8B9CFF"
AMBER = "#F5B84B"

SANS = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "'SF Mono','JetBrains Mono',Consolas,Menlo,'Courier New',monospace"

COMMON_CSS = """
.blink{animation:blink 2s ease-in-out infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.25}}
.dash{stroke-dasharray:4 8;animation:dash 1.4s linear infinite}
@keyframes dash{to{stroke-dashoffset:-12}}
.tw{opacity:.1;animation:tw 5s ease-in-out infinite}
@keyframes tw{0%,100%{opacity:.08}50%{opacity:.55}}
.nudge{animation:nudge 2.4s ease-in-out infinite}
@keyframes nudge{0%,100%{transform:translateX(0)}50%{transform:translateX(4px)}}
.fb{transform-box:fill-box;transform-origin:center}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
"""


def est(text, size, mono=False):
    """Rough rendered width of a string (SVG can't measure text)."""
    return len(text) * size * (0.6 if mono else 0.56)


def wrap(w, h, body, title, desc="", css=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">
<title id="t">{esc(title)}</title>
<desc id="d">{esc(desc or title)}</desc>
<defs>
  <linearGradient id="acc" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{TEAL}"/><stop offset="1" stop-color="{VIOLET}"/>
  </linearGradient>
  <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{LINE2}"/><stop offset="1" stop-color="{LINE2}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="shg" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{TEAL}" stop-opacity="0"/>
    <stop offset="0.5" stop-color="{TEAL}" stop-opacity="0.9"/>
    <stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
  </linearGradient>
</defs>
<style>
text{{font-family:{SANS};}}
.m{{font-family:{MONO};}}
{COMMON_CSS}
{css}
</style>
{body}
</svg>
"""


def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", name)


def kf(name, pts):
    """pts: list of (percent, css-declarations)."""
    inner = "".join(f"{p}%{{{d}}}" for p, d in pts)
    return f"@keyframes {name}{{{inner}}}\n"


def flow(items, maxw, size=12.5, gap=8):
    rows, x = [[]], 0
    for c in items:
        w = est(c, size) + 22
        if x + w > maxw and rows[-1]:
            rows.append([])
            x = 0
        rows[-1].append((x, w, c))
        x += w + gap
    return rows


def chips_svg(rows, ox, oy, size=12.5, ch=26, gap=8):
    out = []
    for r, items in enumerate(rows):
        yy = oy + r * (ch + gap)
        for x, w, c in items:
            out.append(f'<rect x="{ox+x:.0f}" y="{yy}" width="{w:.0f}" height="{ch}" rx="13" fill="{BG2}" stroke="{LINE2}"/>')
            out.append(f'<text x="{ox+x+w/2:.0f}" y="{yy+17}" font-size="{size}" text-anchor="middle" fill="{SOFT}">{esc(c)}</text>')
    return "\n".join(out)


def rows_height(rows, ch=26, gap=8):
    return len(rows) * ch + (len(rows) - 1) * gap


def shimmer(W, H, rx, delay):
    """A soft highlight that slowly travels along the top edge of a card."""
    cid = "cc"
    svg = (
        f'<defs><clipPath id="{cid}"><rect width="{W}" height="{H}" rx="{rx}"/></clipPath></defs>'
        f'<g clip-path="url(#{cid})">'
        f'<rect x="0" y="0" width="{W}" height="2" fill="url(#acc)" opacity="0.22"/>'
        f'<rect class="sh" x="-140" y="0" width="140" height="2" fill="url(#shg)" style="animation-delay:{delay:.1f}s"/></g>'
    )
    css = f".sh{{animation:sh 7s linear infinite}}\n@keyframes sh{{from{{transform:translateX(0)}}to{{transform:translateX({W+140}px)}}}}\n"
    return svg, css


# ================================================================= HERO
def hero():
    W, H = 1000, 460
    cx, cy = 740, 246
    hub_w, hub_h = 150, 52
    ag_w, ag_h = 132, 48
    agents = [
        ("RETRIEVER", "RAG · vectors", 610, 150),
        ("TOOL USE", "MCP · functions", 870, 150),
        ("VISION", "CNN · real-time", 610, 342),
        ("EVALUATOR", "metrics · evals", 870, 342),
    ]

    css = [
        ".hubring{opacity:.4;animation:breathe 4s ease-in-out infinite}",
        "@keyframes breathe{0%,100%{opacity:.35}50%{opacity:.95}}",
        ".glow{opacity:.14;animation:glow 4s ease-in-out infinite}",
        "@keyframes glow{0%,100%{opacity:.10}50%{opacity:.24}}",
        ".pk{opacity:0}",
        ".ar{opacity:.3}",
    ]
    for i, (_, _, x, y) in enumerate(agents):
        dx, dy = x - cx, y - cy
        s = 25 * i
        pts = []
        if s > 0:
            pts += [(0, "transform:translate(0,0);opacity:0"), (s, "transform:translate(0,0);opacity:0")]
        else:
            pts += [(0, "transform:translate(0,0);opacity:0")]
        pts += [
            (s + 1, "transform:translate(0,0);opacity:1"),
            (s + 8, f"transform:translate({dx}px,{dy}px);opacity:1"),
            (s + 12, f"transform:translate({dx}px,{dy}px);opacity:1"),
            (s + 19, "transform:translate(0,0);opacity:1"),
            (s + 21, "transform:translate(0,0);opacity:0"),
            (100, "transform:translate(0,0);opacity:0"),
        ]
        css.append(kf(f"pk{i}", pts))
        css.append(f".pk{i}{{animation:pk{i} 8s linear infinite}}")
        rp = [(0, "opacity:.3")] if s == 0 else [(0, "opacity:.3"), (s + 6, "opacity:.3")]
        rp += [(s + 8, "opacity:1"), (s + 13, "opacity:1"), (s + 22, "opacity:.3"), (100, "opacity:.3")]
        css.append(kf(f"ar{i}", rp))
        css.append(f".ar{i}{{animation:ar{i} 8s ease-in-out infinite}}")

    b = []
    b.append(f"""
<defs>
  <clipPath id="clip"><rect width="{W}" height="{H}" rx="20"/></clipPath>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M40 0H0V40" fill="none" stroke="#111A28" stroke-width="1"/>
  </pattern>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{BG0}"/><stop offset="1" stop-color="#0C1320"/>
  </linearGradient>
  <radialGradient id="g1" cx="0.85" cy="0.1" r="0.6">
    <stop offset="0" stop-color="{TEAL}" stop-opacity="0.18"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="hg" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{TEAL}"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="g2" cx="0.05" cy="1" r="0.55">
    <stop offset="0" stop-color="{VIOLET}" stop-opacity="0.16"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
  </radialGradient>
</defs>
<g clip-path="url(#clip)">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" fill="url(#grid)"/>
  <rect width="{W}" height="{H}" fill="url(#g1)"/>
  <rect width="{W}" height="{H}" fill="url(#g2)"/>
</g>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="20" fill="none" stroke="{LINE}"/>
""")

    for i, (px, py) in enumerate([(120, 36), (300, 96), (470, 40), (60, 392), (260, 436), (430, 330), (500, 436), (985, 28), (968, 440)]):
        b.append(f'<circle class="tw" cx="{px}" cy="{py}" r="1.6" fill="{TEAL}" style="animation-delay:-{(i*0.9)%5:.1f}s"/>')

    # left column
    b.append(f'<circle class="blink" cx="46" cy="68" r="4" fill="{TEAL}"/>')
    b.append(
        f'<text class="m" x="62" y="73" font-size="12" font-weight="700" letter-spacing="1.8" fill="{TEAL}">AI ENGINEER'
        f'<tspan dx="10" fill="{DIM}" font-weight="400">/</tspan><tspan dx="10" fill="{MUTED}" font-weight="400">FORWARD DEPLOYED</tspan>'
        f'<tspan dx="10" fill="{DIM}" font-weight="400">/</tspan><tspan dx="10" fill="{MUTED}" font-weight="400">FULL-STACK</tspan></text>'
    )
    b.append(f'<text x="40" y="148" font-size="64" font-weight="800" letter-spacing="-1.5" fill="{TEXT}">Gouri Pawar</text>')
    b.append(f'<rect x="42" y="168" width="72" height="4" rx="2" fill="url(#acc)"/>')
    for i, line in enumerate(["I take GenAI and LLM systems", "from problem to production:", "RAG, agents and the full stack."]):
        b.append(f'<text x="40" y="{214+i*30}" font-size="22" fill="{MUTED}">{esc(line)}</text>')
    b.append(f'<rect x="40" y="318" width="420" height="1.5" fill="url(#fade)"/>')
    b.append(f'<text class="m" x="40" y="352" font-size="12.5" letter-spacing="1.5" fill="{TEAL}">RAG · AGENTS · ORCHESTRATION</text>')
    b.append(f'<text class="m" x="40" y="376" font-size="12.5" letter-spacing="1.5" fill="{MUTED}">DEEP LEARNING · RESEARCH · FULL-STACK</text>')
    b.append(f'<text class="m" x="40" y="424" font-size="12" letter-spacing="1" fill="{DIM}">PYTHON · FASTAPI · LANGGRAPH · PGVECTOR · REACT</text>')

    # right panel: orchestration graph
    b.append(f'<rect x="520.5" y="44.5" width="439" height="371" rx="16" fill="{BG1}" fill-opacity="0.7" stroke="{LINE}"/>')
    b.append(f'<text class="m" x="544" y="76" font-size="12" letter-spacing="2" fill="{DIM}">// ORCHESTRATION</text>')
    b.append(f'<circle class="blink" cx="920" cy="72" r="3.5" fill="{TEAL}"/>')
    b.append(f'<text class="m" x="908" y="76" font-size="12" letter-spacing="2" text-anchor="end" fill="{DIM}">LIVE</text>')
    b.append(f'<circle class="glow" cx="{cx}" cy="{cy}" r="120" fill="url(#hg)"/>')

    for _, _, x, y in agents:
        b.append(f'<line class="dash" x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="{LINE2}" stroke-width="2"/>')
    for i in range(4):
        b.append(
            f'<g class="pk pk{i}"><circle cx="{cx}" cy="{cy}" r="10" fill="{TEAL}" opacity="0.2"/>'
            f'<circle cx="{cx}" cy="{cy}" r="4" fill="{TEAL}"/></g>'
        )

    b.append(f'<rect x="{cx-hub_w/2}" y="{cy-hub_h/2}" width="{hub_w}" height="{hub_h}" rx="12" fill="{BG1}" stroke="{LINE2}"/>')
    b.append(f'<rect class="hubring" x="{cx-hub_w/2}" y="{cy-hub_h/2}" width="{hub_w}" height="{hub_h}" rx="12" fill="none" stroke="url(#acc)" stroke-width="1.8"/>')
    b.append(f'<text class="m" x="{cx}" y="{cy-3}" font-size="12.5" font-weight="700" letter-spacing="1.5" text-anchor="middle" fill="{TEXT}">ORCHESTRATOR</text>')
    b.append(f'<text x="{cx}" y="{cy+15}" font-size="12" text-anchor="middle" fill="{MUTED}">plan · route · verify</text>')

    for i, (name, sub, x, y) in enumerate(agents):
        b.append(f'<rect x="{x-ag_w/2}" y="{y-ag_h/2}" width="{ag_w}" height="{ag_h}" rx="11" fill="{BG1}" stroke="{LINE2}"/>')
        b.append(f'<rect class="ar ar{i}" x="{x-ag_w/2}" y="{y-ag_h/2}" width="{ag_w}" height="{ag_h}" rx="11" fill="none" stroke="url(#acc)" stroke-width="1.8"/>')
        b.append(f'<text class="m" x="{x}" y="{y-3}" font-size="12.5" font-weight="700" letter-spacing="1.5" text-anchor="middle" fill="{TEXT}">{name}</text>')
        b.append(f'<text x="{x}" y="{y+14}" font-size="11.5" text-anchor="middle" fill="{MUTED}">{esc(sub)}</text>')

    b.append(f'<text class="m" x="{cx}" y="396" font-size="12" letter-spacing="1" text-anchor="middle" fill="{DIM}">shared state · typed tool calls · eval loop</text>')

    save(
        "hero.svg",
        wrap(
            W, H, "\n".join(b),
            "Gouri Pawar — AI Engineer",
            "Gouri Pawar. AI Engineer, Forward Deployed and Full-Stack. I take GenAI and LLM systems from problem to production: RAG, agents and the full stack. "
            "Animated diagram of an orchestrator coordinating retriever, tool-use, vision and evaluator agents.",
            "\n".join(css),
        ),
    )


# ================================================================= SECTION BARS
def section(n, title, tag):
    W, H = 1000, 56
    tx = 62
    lx = tx + est(title, 20) * 1.08 + 22
    rx_ = W - 22 - est(tag, 12, True) - 22
    lw = max(60, rx_ - lx)
    seg = 70
    css = f".scan{{animation:scan 5s ease-in-out infinite alternate}}\n@keyframes scan{{from{{transform:translateX(0)}}to{{transform:translateX({lw-seg:.0f}px)}}}}\n"
    b = [
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="{BG1}" stroke="{LINE}"/>',
        f'<text class="m" x="24" y="34" font-size="14" font-weight="700" fill="{AMBER}">{n}</text>',
        f'<rect x="50" y="20" width="1.5" height="16" fill="{LINE2}"/>',
        f'<text x="{tx}" y="36" font-size="20" font-weight="700" fill="{TEXT}">{esc(title)}</text>',
        f'<rect x="{lx:.0f}" y="28" width="{lw:.0f}" height="1.5" rx="0.75" fill="{LINE2}"/>',
        f'<rect class="scan" x="{lx:.0f}" y="27.5" width="{seg}" height="2.5" rx="1.25" fill="url(#acc)"/>',
        f'<text class="m" x="{W-22}" y="33" font-size="12" text-anchor="end" fill="{DIM}">{esc(tag)}</text>',
    ]
    save(f"section-{n}.svg", wrap(W, H, "\n".join(b), f"{n} — {title}", css=css))


# ================================================================= OVERVIEW (designed, not plain text)
def overview():
    W = 1000
    summary = (
        "AI Engineer with 3+ years taking GenAI and LLM solutions from problem to production: scoping the need, "
        "prototyping quickly and deploying RAG systems, FastAPI/Flask AI services and React interfaces that real "
        "users depend on. Strong across the full stack, comfortable in ambiguous problem spaces, and experienced in "
        "turning complex AI systems into clear learning content for users."
    )
    lines = textwrap.wrap(summary, 100)
    pad = 32
    y_par = 78
    lh = 25
    y_pills = y_par + (len(lines) - 1) * lh + 26
    y_tiles = y_pills + 30 + 26
    tile_h = 120
    H = y_tiles + tile_h + 26

    tiles = [
        ("3+", "years shipping GenAI, LLM and full-stack systems"),
        ("~60%", "less manual query resolution with the LOF Chatbot, a production RAG system"),
        ("3", "universities in the international AI research team I led"),
        ("8.92", "CGPA, B.E. Computer Science, University of Mumbai"),
    ]
    sh, shcss = shimmer(W, H, 18, -2.0)
    b = [
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="{BG1}" stroke="{LINE}"/>',
        sh,
        f'<circle class="blink" cx="{pad+4}" cy="40" r="3.5" fill="{TEAL}"/>',
        f'<text class="m" x="{pad+16}" y="44" font-size="12" letter-spacing="2" fill="{TEAL}">// PROFILE</text>',
        f'<text class="m" x="{W-pad}" y="44" font-size="12" letter-spacing="1.5" text-anchor="end" fill="{DIM}">MUMBAI, INDIA</text>',
    ]
    for i, line in enumerate(lines):
        b.append(f'<text x="{pad}" y="{y_par+i*lh}" font-size="16" fill="{SOFT}">{esc(line)}</text>')

    # open-to pills
    b.append(f'<text class="m" x="{pad}" y="{y_pills+20}" font-size="12" letter-spacing="2" fill="{DIM}">OPEN TO</text>')
    px = pad + 82
    for role in ["AI Engineer", "Forward Deployed Engineer", "Full-Stack Engineer"]:
        w = est(role, 13.5) + 40
        b.append(f'<rect x="{px:.0f}" y="{y_pills}" width="{w:.0f}" height="30" rx="15" fill="{BG2}" stroke="{LINE2}"/>')
        b.append(f'<circle cx="{px+16:.0f}" cy="{y_pills+15}" r="3" fill="url(#acc)"/>')
        b.append(f'<text x="{px+27:.0f}" y="{y_pills+20}" font-size="13.5" font-weight="600" fill="{TEXT}">{esc(role)}</text>')
        px += w + 10

    tw = (W - 2 * pad - 3 * 18) / 4
    for i, (val, label) in enumerate(tiles):
        x = pad + i * (tw + 18)
        b.append(f'<rect x="{x+0.5:.1f}" y="{y_tiles+0.5}" width="{tw-1:.1f}" height="{tile_h-1}" rx="14" fill="{BG2}" stroke="{LINE}"/>')
        b.append(f'<text x="{x+18:.0f}" y="{y_tiles+46}" font-size="32" font-weight="800" fill="{TEAL}">{esc(val)}</text>')
        for j, line in enumerate(textwrap.wrap(label, 28)):
            b.append(f'<text x="{x+18:.0f}" y="{y_tiles+69+j*17}" font-size="12.5" fill="{MUTED}">{esc(line)}</text>')

    alt = ("Profile. " + summary + " Open to: AI Engineer, Forward Deployed Engineer, Full-Stack Engineer. "
           "3+ years shipping GenAI, LLM and full-stack systems; about 60% less manual query resolution with the LOF Chatbot; "
           "led a 3-university international research team; 8.92 CGPA, B.E. Computer Science, University of Mumbai.")
    save("overview.svg", wrap(W, H, "\n".join(b), "Profile overview", alt, shcss))


# ================================================================= CAPABILITY GLYPHS (48x48, animated)
STROKE = f'fill="none" stroke="{TEAL}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"'


def g_rag():
    svg = (
        f'<g {STROKE}><rect x="12" y="7" width="24" height="34" rx="4"/></g>'
        f'<g stroke="{SOFT}" stroke-width="1.8" stroke-linecap="round" opacity="0.45"><line x1="17" y1="17" x2="31" y2="17"/><line x1="17" y1="24" x2="31" y2="24"/><line x1="17" y1="31" x2="26" y2="31"/></g>'
        f'<rect class="beam" x="9" y="10" width="30" height="2.6" rx="1.3" fill="url(#acc)"/>'
    )
    css = ".beam{animation:scan2 3.2s ease-in-out infinite alternate}\n@keyframes scan2{from{transform:translateY(0)}to{transform:translateY(26px)}}\n"
    return svg, css


def g_agent():
    svg = (
        f'<g class="spin fb"><rect width="48" height="48" fill="none"/>'
        f'<g {STROKE}><path d="M24 9 A15 15 0 1 1 9 24"/><path d="M5 29 L9 24 L13 29"/></g></g>'
        f'<circle class="blink" cx="24" cy="24" r="3.6" fill="{TEAL}"/>'
    )
    css = ".spin{animation:spin 9s linear infinite}\n@keyframes spin{to{transform:rotate(360deg)}}\n"
    return svg, css


def g_orch():
    svg = (
        f'<g stroke="{TEAL}" stroke-width="1.6" opacity="0.55"><line x1="24" y1="24" x2="24" y2="8"/><line x1="24" y1="24" x2="10" y2="35"/><line x1="24" y1="24" x2="38" y2="35"/></g>'
        f'<circle class="rip fb" cx="24" cy="24" r="19" fill="none" stroke="{TEAL}" stroke-width="1.4"/>'
        f'<circle class="sat" cx="24" cy="8" r="3.6" fill="{TEAL}"/>'
        f'<circle class="sat" style="animation-delay:.9s" cx="10" cy="35" r="3.6" fill="{TEAL}"/>'
        f'<circle class="sat" style="animation-delay:1.8s" cx="38" cy="35" r="3.6" fill="{TEAL}"/>'
        f'<circle cx="24" cy="24" r="5.5" fill="{TEAL}"/>'
    )
    css = (
        ".rip{opacity:0;animation:rip 3s ease-out infinite}\n"
        "@keyframes rip{0%{transform:scale(.3);opacity:.8}100%{transform:scale(1);opacity:0}}\n"
        ".sat{animation:sat 2.7s ease-in-out infinite}\n"
        "@keyframes sat{0%,100%{opacity:.4}50%{opacity:1}}\n"
    )
    return svg, css


def g_dl():
    xs = [8, 24, 40]
    layers = [[12, 24, 36], [12, 24, 36], [18, 30]]
    lines, nodes = [], []
    for li in range(2):
        for ya in layers[li]:
            for yb in layers[li + 1]:
                lines.append(f'<line x1="{xs[li]}" y1="{ya}" x2="{xs[li+1]}" y2="{yb}"/>')
    for li, ys in enumerate(layers):
        for y in ys:
            nodes.append(f'<circle class="dn" style="animation-delay:{li*0.7:.1f}s" cx="{xs[li]}" cy="{y}" r="3.2" fill="{TEAL}"/>')
    svg = f'<g stroke="{TEAL}" stroke-width="1" opacity="0.28">{"".join(lines)}</g>' + "".join(nodes)
    css = ".dn{animation:dn 2.4s ease-in-out infinite}\n@keyframes dn{0%,100%{opacity:.3}40%{opacity:1}}\n"
    return svg, css


def g_research():
    svg = (
        f'<path d="M9 7 V39 H42" fill="none" stroke="{SOFT}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" opacity="0.4"/>'
        f'<path class="draw" pathLength="1" d="M12 34 C18 34 18 23 24 26 S33 13 40 11" {STROKE}/>'
        f'<circle class="end" cx="40" cy="11" r="3.4" fill="{TEAL}"/>'
    )
    css = (
        ".draw{stroke-dasharray:1 1;animation:draw 5.5s ease-in-out infinite}\n"
        "@keyframes draw{0%{stroke-dashoffset:1;opacity:1}55%{stroke-dashoffset:0;opacity:1}88%{stroke-dashoffset:0;opacity:1}100%{stroke-dashoffset:0;opacity:0}}\n"
        ".end{opacity:0;animation:end 5.5s ease-in-out infinite}\n"
        "@keyframes end{0%,52%{opacity:0}60%{opacity:1}88%{opacity:1}100%{opacity:0}}\n"
    )
    return svg, css


def g_full():
    svg = (
        f'<g {STROKE}><rect x="5" y="8" width="38" height="32" rx="5"/><line x1="5" y1="16" x2="43" y2="16"/>'
        f'<path d="M15 24 L10.5 28 L15 32"/><path d="M33 24 L37.5 28 L33 32"/></g>'
        f'<circle cx="10" cy="12" r="1.3" fill="{TEAL}"/><circle cx="14" cy="12" r="1.3" fill="{TEAL}" opacity=".6"/><circle cx="18" cy="12" r="1.3" fill="{TEAL}" opacity=".3"/>'
        f'<rect class="blink" x="22.8" y="23" width="2.4" height="10" rx="1" fill="{TEAL}"/>'
    )
    return svg, ""


# ================================================================= FOCUS-AREA CARDS
def cap(n, tag, title, desc, chips, glyph):
    W, H = 322, 242
    gsvg, gcss = glyph()
    sh, shcss = shimmer(W, H, 16, -(n * 1.4))
    b = [
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="{BG1}" stroke="{LINE}"/>',
        sh,
        f'<rect x="18.5" y="20.5" width="59" height="59" rx="15" fill="{BG2}" stroke="{LINE2}"/>',
        f'<g transform="translate(24,26)">{gsvg}</g>',
        f'<text class="m" x="{W-20}" y="38" font-size="12" letter-spacing="2" text-anchor="end" fill="{DIM}">0{n}</text>',
        f'<text class="m" x="{W-20}" y="58" font-size="11" letter-spacing="1.5" text-anchor="end" fill="{TEAL}">{esc(tag)}</text>',
        f'<text x="20" y="112" font-size="19" font-weight="700" fill="{TEXT}">{esc(title)}</text>',
    ]
    dl = textwrap.wrap(desc, 36)
    assert len(dl) <= 3, (title, dl)
    for i, line in enumerate(dl):
        b.append(f'<text x="20" y="{136+i*18}" font-size="13.5" fill="{MUTED}">{esc(line)}</text>')
    rows = flow(chips, W - 40)
    assert len(rows) == 1, (title, rows)
    b.append(chips_svg(rows, 20, H - 20 - 26))
    save(f"cap-{n}.svg", wrap(W, H, "\n".join(b), f"{title} — {desc}", css=gcss + shcss))


def capabilities():
    cap(1, "RETRIEVAL", "RAG Systems",
        "Production RAG with chunking, embeddings and vector search; cut manual queries by ~60%.",
        ["pgvector", "ChromaDB", "Embeddings"], g_rag)
    cap(2, "AUTONOMY", "Agentic AI",
        "Tool calling, structured outputs and multi-step workflows built with LangChain and LangGraph.",
        ["LangChain", "Tool calling"], g_agent)
    cap(3, "COORDINATION", "Agent Orchestration",
        "Agent workflow orchestration with LangGraph and MCP: explicit state, routing and tool access.",
        ["LangGraph", "MCP", "Workflows"], g_orch)
    cap(4, "MODELS", "Deep Learning",
        "CNN/RNN and computer vision: sign-language recognition on live video for deaf users.",
        ["CNN/RNN", "Computer vision"], g_dl)
    cap(5, "DISCOVERY", "Research",
        "Led a 3-university team on AI traffic control; models beat rule-based baselines.",
        ["Fuzzy logic", "PTV Vissim"], g_research)
    cap(6, "PRODUCTS", "Full-Stack",
        "React, Node.js and FastAPI products with REST APIs, WebSockets and high-availability MySQL.",
        ["React", "FastAPI", "Node.js"], g_full)


# ================================================================= EXPERIENCE TIMELINE
def experience():
    W = 1000
    jobs = [
        dict(co="PedTech Global", role="Software Engineer · CDLC.CLUB, an AI and robotics learning product",
             when="AUG 2026 – SEP 2026", where="Dubai, UAE",
             pts=["Built and shipped core features on the CDLC.CLUB platform team for PedTech Global's AI and robotics learning product.",
                  "Turned founder-built AI products into structured, project-based learning paths, making complex AI/ML systems understandable to end users."],
             tech=[]),
        dict(co="Lab of Future", role="Software Engineer & Researcher",
             when="MAY 2024 – JUL 2026", where="Jaipur & Dubai",
             pts=["Built and shipped LOF Chatbot, a production RAG system covering document ingestion and chunking, embeddings, vector search retrieval and LLM prompt design, served via FastAPI and cutting manual query resolution by ~60%.",
                  "Owned AI services end to end: Python microservices (FastAPI/Flask) and REST APIs for LLM, model and retrieval serving, supporting concurrent users through WebSocket event streaming.",
                  "Engineered Lab of Future Studio, a multi-module simulation platform (coding, drone, robotics, space), and LOF Community App, a real-time WebSocket platform for live discussions and user channels."],
             tech=["Python", "RAG", "LLMs", "Embeddings", "Vector search", "FastAPI", "Flask", "MongoDB", "WebSockets", "React"]),
        dict(co="TinkerXLabs", role="Full Stack Developer",
             when="SEP 2023 – APR 2024", where="Mumbai, India",
             pts=["Delivered a Point of Sale system end to end: inventory, billing, Razorpay webhook payments and a sales analytics dashboard.",
                  "Implemented a MySQL InnoDB Cluster for high availability, achieving zero downtime for billing operations."],
             tech=["Python", "Java", "MySQL", "Razorpay webhooks", "Data analytics"]),
        dict(co="ONE STOP", role="Machine Learning Intern",
             when="JUN 2021 – AUG 2021", where="Mumbai, India",
             pts=["Delivered 3 supervised ML models (disease prediction, spam filtering, malware classification) with scikit-learn, each achieving 90%+ accuracy.",
                  "Served the models through a Django + PostgreSQL REST API backend for real-time inference."],
             tech=["Python", "Scikit-learn", "Pandas", "Django", "PostgreSQL"]),
    ]
    x0 = 60
    cw = W - x0
    gap = 16
    y = 0
    blocks, nodes_y = [], []
    for j in jobs:
        lines = [textwrap.wrap(p, 112) for p in j["pts"]]
        h = 86 + sum(len(l) * 20 + 6 for l in lines)
        rows = flow(j["tech"], cw - 48) if j["tech"] else []
        if rows:
            h += 8 + rows_height(rows)
        h += 20 if rows else 12
        blocks.append((y, h, lines, rows))
        nodes_y.append(y + 34)
        y += h + gap
    H = y - gap

    dist = nodes_y[-1] - nodes_y[0]
    css = (
        ".tl{opacity:0;animation:tl 7s linear infinite}\n"
        f"@keyframes tl{{0%{{transform:translateY(0);opacity:0}}8%{{opacity:1}}92%{{opacity:1}}100%{{transform:translateY({dist}px);opacity:0}}}}\n"
        ".np{animation:np 3s ease-out infinite;transform-box:fill-box;transform-origin:center}\n"
        "@keyframes np{0%{transform:scale(1);opacity:.8}100%{transform:scale(2.6);opacity:0}}\n"
    )
    b = [f'<rect x="23.25" y="{nodes_y[0]}" width="1.5" height="{dist}" fill="{LINE2}"/>']
    b.append(f'<g class="tl"><circle cx="24" cy="{nodes_y[0]}" r="7" fill="{TEAL}" opacity="0.25"/><circle cx="24" cy="{nodes_y[0]}" r="3" fill="{TEAL}"/></g>')
    for i, (j, (by, bh, lines, rows)) in enumerate(zip(jobs, blocks)):
        ny = nodes_y[i]
        b.append(f'<line x1="32" y1="{ny}" x2="{x0}" y2="{ny}" stroke="{LINE2}" stroke-width="1.5"/>')
        if i == 0:
            b.append(f'<circle class="np" cx="24" cy="{ny}" r="6" fill="none" stroke="{TEAL}" stroke-width="1.5"/>')
        b.append(f'<circle cx="24" cy="{ny}" r="7" fill="{BG1}" stroke="{TEAL}" stroke-width="2"/>')
        b.append(f'<circle cx="24" cy="{ny}" r="2.5" fill="{TEAL}"/>')
        b.append(f'<rect x="{x0+0.5}" y="{by+0.5}" width="{cw-1}" height="{bh-1}" rx="16" fill="{BG1}" stroke="{LINE}"/>')
        b.append(f'<text x="{x0+24}" y="{by+36}" font-size="20" font-weight="700" fill="{TEXT}">{esc(j["co"])}</text>')
        b.append(f'<text x="{x0+24}" y="{by+58}" font-size="13.5" fill="{TEAL}">{esc(j["role"])}</text>')
        b.append(f'<text class="m" x="{W-24}" y="{by+34}" font-size="12" letter-spacing="1.5" text-anchor="end" fill="{SOFT}">{j["when"]}</text>')
        b.append(f'<text x="{W-24}" y="{by+54}" font-size="12.5" text-anchor="end" fill="{DIM}">{esc(j["where"])}</text>')
        yy = by + 90
        for pl in lines:
            b.append(f'<circle cx="{x0+28}" cy="{yy-4}" r="2.6" fill="{TEAL}" opacity="0.8"/>')
            for k, line in enumerate(pl):
                b.append(f'<text x="{x0+42}" y="{yy+k*20}" font-size="13.5" fill="{MUTED}">{esc(line)}</text>')
            yy += len(pl) * 20 + 6
        if rows:
            b.append(chips_svg(rows, x0 + 24, yy + 4))
    alt = "Experience. " + " ".join(f"{j['co']}, {j['role']}, {j['when'].title()}, {j['where']}. " + " ".join(j["pts"]) for j in jobs)
    save("experience.svg", wrap(W, H, "\n".join(b), "Experience", alt, css))


# ================================================================= PROJECT CARDS
def pglyph(kind):
    s = f'stroke="{TEAL}" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    if kind == "rag":
        svg = (
            f'<g transform="translate(422,24)" {s}><line class="dash" x1="4" y1="22" x2="22" y2="4"/><line class="dash" x1="4" y1="22" x2="22" y2="40"/>'
            f'<line class="dash" x1="22" y1="4" x2="40" y2="22"/><line class="dash" x1="22" y1="40" x2="40" y2="22"/>'
            f'<circle cx="4" cy="22" r="4" fill="{BG1}"/><circle cx="22" cy="4" r="4" fill="{BG1}"/>'
            f'<circle cx="22" cy="40" r="4" fill="{BG1}"/><circle class="blink" cx="40" cy="22" r="4.5" fill="{TEAL}"/></g>'
        )
        return svg, ""
    if kind == "video":
        svg = (
            f'<g transform="translate(420,28)" {s}><rect x="0" y="0" width="46" height="32" rx="7"/>'
            f'<path d="M19 9 L33 16 L19 23 Z" fill="{TEAL}"/></g>'
            f'<circle class="blink" cx="458" cy="38" r="3" fill="{TEAL}"/>'
        )
        return svg, ""
    if kind == "traffic":
        svg = (
            f'<g transform="translate(422,24)" {s}><path d="M4 22 H40"/><path d="M22 4 V40"/>'
            f'<circle cx="22" cy="22" r="7" fill="{BG1}"/><circle cx="22" cy="22" r="2" fill="{TEAL}"/>'
            f'<circle class="rip2 fb" cx="22" cy="22" r="20" stroke-width="1.4"/></g>'
        )
        css = (
            ".rip2{opacity:0;animation:rip2 3s ease-out infinite}\n"
            "@keyframes rip2{0%{transform:scale(.3);opacity:.8}100%{transform:scale(1);opacity:0}}\n"
        )
        return svg, css
    svg = (
        f'<g transform="translate(424,26)" {s}><rect class="bar fb" style="animation-delay:0s" x="0" y="22" width="9" height="16" rx="2"/>'
        f'<rect class="bar fb" style="animation-delay:.4s" x="15" y="12" width="9" height="26" rx="2"/>'
        f'<rect class="bar fb" style="animation-delay:.8s" x="30" y="0" width="9" height="38" rx="2" fill="{TEAL}"/></g>'
    )
    css = (
        ".bar{transform-origin:bottom;animation:bar 3.6s ease-in-out infinite}\n"
        "@keyframes bar{0%,100%{transform:scaleY(1)}50%{transform:scaleY(.72)}}\n"
    )
    return svg, css


def pcard(idx, fname, tag, title, desc, chips, kind):
    W, H = 490, 226
    gsvg, gcss = pglyph(kind)
    sh, shcss = shimmer(W, H, 16, -(idx * 1.7))
    b = [
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="{BG1}" stroke="{LINE}"/>',
        sh,
        gsvg,
        f'<text class="m" x="24" y="42" font-size="12" letter-spacing="2" fill="{TEAL}">{esc(tag)}</text>',
        f'<text x="24" y="82" font-size="26" font-weight="700" fill="{TEXT}">{esc(title)}</text>',
    ]
    dl = textwrap.wrap(desc, 54)
    assert len(dl) <= 3, (title, dl)
    for i, line in enumerate(dl):
        b.append(f'<text x="24" y="{112+i*21}" font-size="14" fill="{MUTED}">{esc(line)}</text>')
    rows = flow(chips, W - 48)
    assert len(rows) == 1, (title, rows)
    b.append(chips_svg(rows, 24, H - 22 - 26))
    save(fname, wrap(W, H, "\n".join(b), f"{title} — {desc}", css=gcss + shcss))


def projects():
    pcard(1, "work-1.svg", "01 · RAG / GENAI", "LOF Chatbot",
          "Production RAG system: ingestion, chunking, embeddings, vector search and prompt design. Cut manual query resolution by ~60%.",
          ["FastAPI", "Embeddings", "Vector search", "LLMs"], "rag")
    pcard(2, "work-2.svg", "02 · DEEP LEARNING / REAL-TIME", "WeConnect",
          "Video calls for deaf users: a Python computer-vision service recognizes sign language on live frames, with Node.js WebRTC signaling.",
          ["WebRTC", "React", "Node.js", "MongoDB"], "video")
    pcard(3, "work-3.svg", "03 · APPLIED RESEARCH", "V2X Traffic Control",
          "Led a 3-university team on real-time AI traffic control for unconventional intersections; models beat rule-based baselines.",
          ["Fuzzy logic", "ML/DL", "PTV Vissim", "Flask"], "traffic")
    pcard(4, "work-4.svg", "04 · FULL-STACK", "Point of Sale",
          "End-to-end POS: inventory, billing, Razorpay webhooks and analytics, on high-availability MySQL with zero billing downtime.",
          ["Python", "Java", "MySQL", "Razorpay"], "pos")


# ================================================================= TOOLKIT
def toolkit():
    W = 1000
    gx, gy, pad = 17, 17, 18
    ch, cgap = 26, 8
    rows_def = [
        ([("GENAI & AGENTS", ["LLM integration", "OpenAI APIs", "Hugging Face", "Prompt engineering", "Context engineering",
                              "Structured outputs", "Function calling", "LangChain", "LangGraph", "MCP"]),
          ("RAG & RETRIEVAL", ["RAG pipelines", "Embeddings", "Semantic search", "Document chunking", "Vector search", "pgvector", "ChromaDB"]),
          ("ML & DEEP LEARNING", ["CNN/RNN", "Deep learning", "Computer vision", "Scikit-learn", "Pandas", "Fuzzy logic", "Feature engineering"])], None),
        ([("BACKEND & APIS", ["FastAPI", "Flask", "Django", "Node.js", "Express", "REST APIs", "Microservices", "Pydantic", "Async", "WebSockets"]),
          ("DATA & MESSAGING", ["PostgreSQL", "MySQL", "MongoDB", "Redis", "RabbitMQ", "Firebase", "Caching"]),
          ("FRONTEND", ["React.js", "Redux", "HTML5", "CSS3", "Tailwind CSS", "Responsive UI"])], None),
        ([("DEVOPS & EDGE", ["Git", "GitHub", "Docker", "Kubernetes", "CI/CD", "Cloud deployment", "Linux", "Raspberry Pi", "Arduino", "MQTT", "LoRaWAN"]),
          ("LANGUAGES", ["Python (primary)", "SQL", "JavaScript (ES6+)", "Java"])], [0.68, 0.32]),
    ]

    css = ".gd{animation:gd 4.2s ease-in-out infinite}\n@keyframes gd{0%,100%{opacity:.45}50%{opacity:1}}\n"
    b = []
    y = 0
    k = 0
    alt_parts = []
    for groups, fr in rows_def:
        n = len(groups)
        total = W - (n - 1) * gx
        widths = [total / n] * n if fr is None else [total * f for f in fr]
        laid = []
        for (title, items), bw in zip(groups, widths):
            rows = flow(items, bw - 2 * pad)
            laid.append((title, items, rows, bw))
        rh = max(56 + rows_height(r) + pad for _, _, r, _ in laid)
        x = 0
        for title, items, rows, bw in laid:
            b.append(f'<rect x="{x+0.5:.1f}" y="{y+0.5}" width="{bw-1:.1f}" height="{rh-1}" rx="16" fill="{BG1}" stroke="{LINE}"/>')
            b.append(f'<circle class="gd" style="animation-delay:-{k*0.7:.1f}s" cx="{x+pad+4:.1f}" cy="{y+30}" r="4" fill="url(#acc)"/>')
            b.append(f'<text class="m" x="{x+pad+16:.1f}" y="{y+34}" font-size="12" font-weight="700" letter-spacing="2" fill="{TEXT}">{esc(title)}</text>')
            b.append(chips_svg(rows, x + pad, y + 56))
            alt_parts.append(f"{title.title()}: {', '.join(items)}.")
            x += bw + gx
            k += 1
        y += rh + gy
    H = y - gy
    save("stack.svg", wrap(W, H, "\n".join(b), "Technical toolkit", "Toolkit. " + " ".join(alt_parts), css))


# ================================================================= APPROACH (delivery loop)
def approach():
    W, H = 1000, 190
    steps = [
        ("Scope the real problem", "Understand the user and what “good” looks like before writing code."),
        ("Prototype quickly", "Working RAG or agent demos early, so feedback is real."),
        ("Deploy for real users", "FastAPI/Flask services, WebSockets and React UIs people rely on."),
        ("Measure and iterate", "Track outcomes, like the ~60% cut in manual queries."),
    ]
    tw, gap = 220, 40
    css = (
        ".rg{opacity:.35;animation:rg 8s ease-in-out infinite}\n"
        "@keyframes rg{0%{opacity:.35}4%{opacity:1}22%{opacity:1}27%{opacity:.35}100%{opacity:.35}}\n"
    )
    b = []
    for i, (t, d) in enumerate(steps):
        x = i * (tw + gap)
        b.append(f'<rect x="{x+0.5}" y="0.5" width="{tw-1}" height="{H-1}" rx="16" fill="{BG1}" stroke="{LINE}"/>')
        b.append(f'<circle cx="{x+36}" cy="38" r="15" fill="none" stroke="{LINE2}" stroke-width="1.8"/>')
        b.append(f'<circle class="rg" style="animation-delay:{i*2}s" cx="{x+36}" cy="38" r="15" fill="none" stroke="url(#acc)" stroke-width="1.8"/>')
        b.append(f'<text class="m" x="{x+36}" y="43" font-size="13" font-weight="700" text-anchor="middle" fill="{TEAL}">0{i+1}</text>')
        tl = textwrap.wrap(t, 19)
        for j, line in enumerate(tl):
            b.append(f'<text x="{x+20}" y="{80+j*20}" font-size="16.5" font-weight="700" fill="{TEXT}">{esc(line)}</text>')
        for j, line in enumerate(textwrap.wrap(d, 29)):
            b.append(f'<text x="{x+20}" y="{80+len(tl)*20+8+j*17}" font-size="12.5" fill="{MUTED}">{esc(line)}</text>')
        if i < 3:
            mx = x + tw + gap / 2
            b.append(f'<g class="nudge" style="animation-delay:{i*0.4}s"><path d="M{mx-6} {H/2-8} L{mx+4} {H/2} L{mx-6} {H/2+8}" fill="none" stroke="{DIM}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></g>')
    save("approach.svg", wrap(W, H, "\n".join(b), "How I deliver",
         "Scope the real problem, prototype quickly, deploy for real users, measure and iterate.", css))


# ================================================================= EDUCATION & LEADERSHIP
def education():
    W, H = 1000, 146
    items = [
        ("EDUCATION", "B.E. Computer Science Engineering", "University of Mumbai · 2023 · CGPA 8.92/10"),
        ("TEAM LEAD", "International V2X Research Project", "Symbiosis Institute of Technology, University of Belgrade and University of Kragujevac"),
        ("CO-LEAD", "Google Developer Student Club", "GDSC"),
    ]
    bw, gx = 322, 17
    css = ".ed{animation:blink 3s ease-in-out infinite}"
    b = []
    for i, (tag, title, sub) in enumerate(items):
        x = i * (bw + gx)
        b.append(f'<rect x="{x+0.5}" y="0.5" width="{bw-1}" height="{H-1}" rx="16" fill="{BG1}" stroke="{LINE}"/>')
        b.append(f'<circle class="ed" style="animation-delay:-{i*0.9}s" cx="{x+24}" cy="30" r="3.5" fill="url(#acc)"/>')
        b.append(f'<text class="m" x="{x+38}" y="34" font-size="12" font-weight="700" letter-spacing="2" fill="{TEAL}">{tag}</text>')
        b.append(f'<text x="{x+20}" y="64" font-size="16" font-weight="700" fill="{TEXT}">{esc(title)}</text>')
        for j, line in enumerate(textwrap.wrap(sub, 44)):
            b.append(f'<text x="{x+20}" y="{86+j*17}" font-size="12.5" fill="{MUTED}">{esc(line)}</text>')
    save("education.svg", wrap(W, H, "\n".join(b), "Education and leadership",
         "B.E. Computer Science Engineering, University of Mumbai, 2023, CGPA 8.92/10. Team Lead of the International V2X Research Project "
         "(Symbiosis Institute of Technology, University of Belgrade, University of Kragujevac). Co-Lead of the Google Developer Student Club (GDSC).", css))


# ================================================================= CONNECT + FOOTER
def button(fname, glyph_txt, label, handle):
    W, H = 240, 60
    b = [
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="{BG1}" stroke="{LINE2}"/>',
        f'<rect x="10" y="10" width="40" height="40" rx="11" fill="{BG2}" stroke="{LINE}"/>',
        f'<text class="m" x="30" y="35" font-size="14" font-weight="700" text-anchor="middle" fill="{TEAL}">{esc(glyph_txt)}</text>',
        f'<text class="m" x="64" y="26" font-size="11" letter-spacing="2" fill="{DIM}">{esc(label)}</text>',
        f'<text x="64" y="44" font-size="13.5" font-weight="600" fill="{TEXT}">{esc(handle)}</text>',
    ]
    save(fname, wrap(W, H, "\n".join(b), f"{label} — {handle}"))


def buttons():
    button("btn-linkedin.svg", "in", "LINKEDIN", "gouripawar")
    button("btn-email.svg", "@", "EMAIL", "gourivpawar@gmail.com")
    button("btn-github.svg", "</>", "GITHUB", "GouriVPawar")


def footer():
    W, H = 1000, 68
    b = [
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="{BG1}" stroke="{LINE}"/>',
        f'<circle class="blink" cx="{W/2-140}" cy="29" r="3.5" fill="{TEAL}"/>',
        f'<text x="{W/2}" y="34" font-size="16" text-anchor="middle" fill="{SOFT}">Stay curious. Ship thoughtfully.</text>',
        f'<circle class="blink" cx="{W/2+140}" cy="29" r="3.5" fill="{VIOLET}"/>',
        f'<text class="m" x="{W/2}" y="54" font-size="11" letter-spacing="3" text-anchor="middle" fill="{DIM}">GOURI PAWAR</text>',
    ]
    save("footer.svg", wrap(W, H, "\n".join(b), "Stay curious. Ship thoughtfully. Gouri Pawar."))


if __name__ == "__main__":
    hero()
    for n, t, tag in [
        ("01", "Overview", "// who I am"),
        ("02", "Focus Areas", "// six disciplines, one system"),
        ("03", "Experience", "// where I have shipped"),
        ("04", "Selected Work", "// things I have built"),
        ("05", "Toolkit", "// what I build with"),
        ("06", "Approach", "// how I deliver"),
        ("07", "Education & Leadership", "// background"),
        ("08", "Connect", "// say hello"),
    ]:
        section(n, t, tag)
    overview()
    capabilities()
    experience()
    projects()
    toolkit()
    approach()
    education()
    buttons()
    footer()
