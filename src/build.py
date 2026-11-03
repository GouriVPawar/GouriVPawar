#!/usr/bin/env python3
"""Generates the SVG assets used by README.md.

Run from the repo root:  python src/build.py
All files are written to ./assets
"""
import os
import textwrap
from xml.sax.saxutils import escape as esc

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(OUT, exist_ok=True)

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


def est(text, size, mono=False):
    """Rough rendered width of a string (SVGs can't measure text)."""
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
</defs>
<style>
text{{font-family:{SANS};}}
.m{{font-family:{MONO};}}
{css}
</style>
{body}
</svg>
"""


def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", name)


# ---------------------------------------------------------------- hero
def hero():
    W, H = 1000, 430
    nodes = [
        ("INGEST", "docs · APIs · files"),
        ("CHUNK", "semantic splitting"),
        ("EMBED", "dense vectors"),
        ("RETRIEVE", "pgvector · Chroma"),
        ("GENERATE", "grounded answers"),
    ]
    xs = [110 + 195 * i for i in range(5)]
    ny, nh, nw = 330, 58, 150
    cy = ny + nh // 2

    css = f"""
.ring{{opacity:.35;animation:pulse 6s ease-in-out infinite}}
@keyframes pulse{{0%{{opacity:.35}}3%{{opacity:1}}12%{{opacity:.35}}100%{{opacity:.35}}}}
.pkt{{opacity:0;animation:travel 6s linear infinite}}
@keyframes travel{{0%{{transform:translateX(0);opacity:0}}3%{{opacity:1}}77%{{opacity:1}}80%{{transform:translateX(780px);opacity:0}}100%{{transform:translateX(780px);opacity:0}}}}
.flow{{stroke-dasharray:4 8;animation:dash 1.2s linear infinite}}
@keyframes dash{{to{{stroke-dashoffset:-12}}}}
.blink{{animation:blink 2s ease-in-out infinite}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:.3}}}}
@media (prefers-reduced-motion:reduce){{.ring,.pkt,.flow,.blink{{animation:none}}}}
"""

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
  <radialGradient id="g1" cx="0.88" cy="0.05" r="0.6">
    <stop offset="0" stop-color="{TEAL}" stop-opacity="0.20"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/>
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

    # eyebrow
    b.append(f'<circle class="blink" cx="46" cy="68" r="4" fill="{TEAL}"/>')
    b.append(
        f'<text class="m" x="62" y="73" font-size="13" font-weight="700" letter-spacing="2.5" fill="{TEAL}">AI ENGINEER'
        f'<tspan dx="14" fill="{DIM}" font-weight="400">/</tspan><tspan dx="14" fill="{MUTED}" font-weight="400">GENAI · RAG · BACKEND</tspan></text>'
    )
    b.append(
        f'<text class="m" x="960" y="73" font-size="12" text-anchor="end" letter-spacing="1.5" fill="{DIM}">PYTHON · FASTAPI · LANGCHAIN · PGVECTOR</text>'
    )

    # name + tagline
    b.append(
        f'<text x="40" y="152" font-size="70" font-weight="800" letter-spacing="-1.5" fill="{TEXT}">Gouri Pawar</text>'
    )
    b.append(f'<rect x="42" y="172" width="72" height="4" rx="2" fill="url(#acc)"/>')
    b.append(
        f'<text x="40" y="222" font-size="24" fill="{MUTED}">I build intelligent systems that hold up in production.</text>'
    )
    b.append(
        f'<text class="m" x="40" y="254" font-size="14" fill="{DIM}">LLM applications · retrieval systems · backend engineering</text>'
    )

    # pipeline
    b.append(
        f'<text class="m" x="40" y="302" font-size="12" letter-spacing="2" fill="{DIM}">// GROUNDED GENERATION, END TO END</text>'
    )
    b.append(
        f'<line x1="{xs[0]}" y1="{cy}" x2="{xs[-1]}" y2="{cy}" stroke="{LINE2}" stroke-width="2" class="flow"/>'
    )
    # travelling packet (drawn before nodes so it only shows in the gaps)
    b.append(
        f'<g class="pkt"><circle cx="{xs[0]}" cy="{cy}" r="11" fill="{TEAL}" opacity="0.22"/>'
        f'<circle cx="{xs[0]}" cy="{cy}" r="4.5" fill="{TEAL}"/></g>'
    )
    for i, (label, sub) in enumerate(nodes):
        x = xs[i]
        delay = (6 + 0.18 - i * 1.2) % 6
        b.append(
            f'<rect x="{x-nw/2}" y="{ny}" width="{nw}" height="{nh}" rx="12" fill="{BG1}" stroke="{LINE2}"/>'
        )
        b.append(
            f'<rect class="ring" style="animation-delay:-{delay:.2f}s" x="{x-nw/2}" y="{ny}" width="{nw}" height="{nh}" rx="12" fill="none" stroke="url(#acc)" stroke-width="1.8"/>'
        )
        b.append(
            f'<text class="m" x="{x}" y="{ny+25}" font-size="13" font-weight="700" letter-spacing="2" text-anchor="middle" fill="{TEXT}">{label}</text>'
        )
        b.append(
            f'<text x="{x}" y="{ny+44}" font-size="12" text-anchor="middle" fill="{MUTED}">{esc(sub)}</text>'
        )
        if i < len(nodes) - 1:
            mx = x + 97.5
            b.append(
                f'<path d="M{mx-4} {cy-6} L{mx+3} {cy} L{mx-4} {cy+6}" fill="none" stroke="{DIM}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
            )

    save(
        "hero.svg",
        wrap(
            W, H, "\n".join(b),
            "Gouri Pawar — AI Engineer",
            "Gouri Pawar. AI Engineer building intelligent systems that hold up in production: GenAI, RAG and backend engineering. Animated pipeline: ingest, chunk, embed, retrieve, generate.",
            css,
        ),
    )


# ---------------------------------------------------------------- metrics strip
def metrics():
    W, H = 1000, 142
    tiles = [
        ("8.92", "CGPA · B.E. Computer Science, University of Mumbai"),
        ("RAG", "Production retrieval systems, from ingestion to grounded answers"),
        ("Intl.", "Led an international research collaboration on AI traffic control"),
        ("Full-stack", "APIs, real-time systems, IoT and edge hardware"),
    ]
    tw, gap = 232, 24
    b = []
    for i, (val, label) in enumerate(tiles):
        x = i * (tw + gap)
        b.append(f'<rect x="{x+0.5}" y="0.5" width="{tw-1}" height="{H-1}" rx="14" fill="{BG1}" stroke="{LINE}"/>')
        b.append(f'<rect x="{x+20}" y="0" width="36" height="3" rx="1.5" fill="url(#acc)"/>')
        b.append(f'<text x="{x+20}" y="54" font-size="34" font-weight="800" fill="{TEAL}">{esc(val)}</text>')
        for j, line in enumerate(textwrap.wrap(label, 31)):
            b.append(f'<text x="{x+20}" y="{80+j*18}" font-size="13" fill="{MUTED}">{esc(line)}</text>')
    save("metrics.svg", wrap(W, H, "\n".join(b), "Highlights",
         "8.92 CGPA at University of Mumbai; production RAG systems; led an international research collaboration; full-stack, real-time and IoT experience."))


# ---------------------------------------------------------------- section headers
def section(n, title, tag):
    W, H = 1000, 56
    tx = 48
    lx = tx + est(title, 22) + 20
    b = [
        f'<text class="m" x="2" y="35" font-size="15" font-weight="700" fill="{AMBER}">{n}</text>',
        f'<text x="{tx}" y="37" font-size="22" font-weight="700" fill="{TEXT}">{esc(title)}</text>',
        f'<rect x="{lx:.0f}" y="28" width="{W - 200 - lx:.0f}" height="1.5" fill="url(#fade)"/>',
        f'<text class="m" x="{W-2}" y="33" font-size="12" text-anchor="end" fill="{DIM}">{esc(tag)}</text>',
    ]
    save(f"section-{n}.svg", wrap(W, H, "\n".join(b), f"{n} — {title}"))


# ---------------------------------------------------------------- project cards
def glyph(kind):
    s = f'stroke="{TEAL}" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    if kind == "rag":
        return (f'<g transform="translate(422,24)" {s}><line x1="4" y1="22" x2="22" y2="4"/><line x1="4" y1="22" x2="22" y2="40"/>'
                f'<line x1="22" y1="4" x2="40" y2="22"/><line x1="22" y1="40" x2="40" y2="22"/>'
                f'<circle cx="4" cy="22" r="4" fill="{BG1}"/><circle cx="22" cy="4" r="4" fill="{BG1}"/>'
                f'<circle cx="22" cy="40" r="4" fill="{BG1}"/><circle cx="40" cy="22" r="4" fill="{TEAL}"/></g>')
    if kind == "video":
        return (f'<g transform="translate(420,28)" {s}><rect x="0" y="0" width="46" height="32" rx="7"/>'
                f'<path d="M19 9 L33 16 L19 23 Z" fill="{TEAL}"/></g>')
    if kind == "traffic":
        return (f'<g transform="translate(422,24)" {s}><path d="M4 22 H40"/><path d="M22 4 V40"/>'
                f'<circle cx="22" cy="22" r="7" fill="{BG1}"/><circle cx="22" cy="22" r="2" fill="{TEAL}"/></g>')
    return (f'<g transform="translate(424,26)" {s}><rect x="0" y="22" width="9" height="16" rx="2"/>'
            f'<rect x="15" y="12" width="9" height="26" rx="2"/><rect x="30" y="0" width="9" height="38" rx="2" fill="{TEAL}"/></g>')


def card(fname, tag, title, desc, chips, kind):
    W, H = 490, 250
    b = [
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="{BG1}" stroke="{LINE}"/>',
        f'<rect x="24" y="0" width="64" height="3" rx="1.5" fill="url(#acc)"/>',
        glyph(kind),
        f'<text class="m" x="24" y="40" font-size="12" letter-spacing="2" fill="{TEAL}">{esc(tag)}</text>',
        f'<text x="24" y="80" font-size="26" font-weight="700" fill="{TEXT}">{esc(title)}</text>',
    ]
    for i, line in enumerate(textwrap.wrap(desc, 52)):
        b.append(f'<text x="24" y="{110+i*21}" font-size="14" fill="{MUTED}">{esc(line)}</text>')

    # chips anchored to the bottom, wrapping
    ch, gap, maxw = 26, 8, W - 48
    rows, x, row = [[]], 0, 0
    for c in chips:
        w = est(c, 12.5) + 22
        if x + w > maxw and rows[row]:
            rows.append([]); row += 1; x = 0
        rows[row].append((x, w, c)); x += w + gap
    y0 = H - 22 - len(rows) * ch - (len(rows) - 1) * gap
    for r, items in enumerate(rows):
        yy = y0 + r * (ch + gap)
        for x, w, c in items:
            b.append(f'<rect x="{24+x:.0f}" y="{yy}" width="{w:.0f}" height="{ch}" rx="13" fill="{BG2}" stroke="{LINE2}"/>')
            b.append(f'<text x="{24+x+w/2:.0f}" y="{yy+17}" font-size="12.5" text-anchor="middle" fill="{SOFT}">{esc(c)}</text>')
    save(fname, wrap(W, H, "\n".join(b), f"{title} — {desc}"))


def cards():
    card("work-1.svg", "01 · GENAI / RAG", "LOF Chatbot",
         "Production RAG and LLM system: ingestion, chunking, embeddings, vector retrieval and grounded responses.",
         ["Ingestion", "Chunking", "Embeddings", "Vector retrieval", "Grounded answers"], "rag")
    card("work-2.svg", "02 · REAL-TIME / VISION", "WeConnect",
         "Real-time video communication platform with built-in sign-language recognition.",
         ["WebSockets", "Video", "Computer vision", "Accessibility"], "video")
    card("work-3.svg", "03 · APPLIED RESEARCH", "V2X Traffic",
         "Led international applied-AI research on intelligent control at unconventional intersections.",
         ["Research lead", "Applied AI", "International", "Traffic control"], "traffic")
    card("work-4.svg", "04 · FULL-STACK", "Point of Sale",
         "Full-stack inventory, billing and analytics platform with Razorpay payment webhooks.",
         ["Inventory", "Billing", "Razorpay webhooks", "Analytics"], "pos")


# ---------------------------------------------------------------- toolkit
def toolkit():
    W = 1000
    groups = [
        ("GENAI & LLMS", ["OpenAI APIs", "LangChain", "LangGraph", "Hugging Face", "Prompt engineering",
                          "Structured outputs", "Function calling", "AI agents", "MCP"]),
        ("MACHINE LEARNING", ["scikit-learn", "Pandas", "CNNs", "RNNs", "Computer vision", "Deep learning", "Fuzzy logic"]),
        ("BACKEND & APIS", ["Python", "FastAPI", "Flask", "Django", "Node.js", "Express", "REST", "Pydantic", "Async", "WebSockets"]),
        ("DATA & RETRIEVAL", ["PostgreSQL", "pgvector", "ChromaDB", "MongoDB", "MySQL", "Redis", "RabbitMQ", "Firebase"]),
        ("FRONTEND", ["React", "Redux", "TypeScript", "JavaScript", "Tailwind CSS"]),
        ("INFRA & EDGE", ["Docker", "Kubernetes", "Linux", "CI/CD", "MQTT", "Raspberry Pi", "Arduino", "LoRaWAN"]),
    ]
    bw, gx, gy, pad = 322, 17, 17, 18
    ch, cgap = 26, 8
    maxw = bw - 2 * pad

    laid = []
    for title, items in groups:
        rows, x, row = [[]], 0, 0
        for c in items:
            w = est(c, 12.5) + 22
            if x + w > maxw and rows[row]:
                rows.append([]); row += 1; x = 0
            rows[row].append((x, w, c)); x += w + cgap
        h = 56 + len(rows) * ch + (len(rows) - 1) * cgap + pad
        laid.append((title, rows, h))

    row_h = [max(laid[0][2], laid[1][2], laid[2][2]), max(laid[3][2], laid[4][2], laid[5][2])]
    H = row_h[0] + gy + row_h[1]
    b = []
    for idx, (title, rows, _) in enumerate(laid):
        r, c = divmod(idx, 3)
        ox = c * (bw + gx)
        oy = 0 if r == 0 else row_h[0] + gy
        bh = row_h[r]
        b.append(f'<rect x="{ox+0.5}" y="{oy+0.5}" width="{bw-1}" height="{bh-1}" rx="16" fill="{BG1}" stroke="{LINE}"/>')
        b.append(f'<circle cx="{ox+pad+4}" cy="{oy+30}" r="4" fill="url(#acc)"/>')
        b.append(f'<text class="m" x="{ox+pad+16}" y="{oy+34}" font-size="12" font-weight="700" letter-spacing="2" fill="{TEXT}">{esc(title)}</text>')
        for ri, items in enumerate(rows):
            yy = oy + 56 + ri * (ch + cgap)
            for x, w, t in items:
                b.append(f'<rect x="{ox+pad+x:.0f}" y="{yy}" width="{w:.0f}" height="{ch}" rx="13" fill="{BG2}" stroke="{LINE2}"/>')
                b.append(f'<text x="{ox+pad+x+w/2:.0f}" y="{yy+17}" font-size="12.5" text-anchor="middle" fill="{SOFT}">{esc(t)}</text>')
    alt = "Technical toolkit. " + " ".join(f"{t.title()}: {', '.join(i)}." for t, g in groups for i in [g])
    save("stack.svg", wrap(W, H, "\n".join(b), "Technical toolkit", alt))


# ---------------------------------------------------------------- approach
def approach():
    W = 1000
    steps = [
        ("Start with the user problem", "Clarify who it is for and what “good” looks like before writing code."),
        ("Build deliberately", "Clean APIs, typed contracts and few moving parts."),
        ("Measure what matters", "Evaluate retrieval and answer quality, not just demos."),
        ("Improve continuously", "Iterate from real usage, logs and feedback."),
    ]
    tw, gap = 220, 40
    ty = 0
    # compute height
    H = 190
    b = []
    for i, (t, d) in enumerate(steps):
        x = i * (tw + gap)
        b.append(f'<rect x="{x+0.5}" y="0.5" width="{tw-1}" height="{H-1}" rx="16" fill="{BG1}" stroke="{LINE}"/>')
        b.append(f'<circle cx="{x+36}" cy="38" r="15" fill="none" stroke="url(#acc)" stroke-width="1.8"/>')
        b.append(f'<text class="m" x="{x+36}" y="43" font-size="13" font-weight="700" text-anchor="middle" fill="{TEAL}">0{i+1}</text>')
        for j, line in enumerate(textwrap.wrap(t, 19)):
            b.append(f'<text x="{x+20}" y="{78+j*20}" font-size="16.5" font-weight="700" fill="{TEXT}">{esc(line)}</text>')
        n_title = len(textwrap.wrap(t, 19))
        for j, line in enumerate(textwrap.wrap(d, 29)):
            b.append(f'<text x="{x+20}" y="{78+n_title*20+8+j*17}" font-size="12.5" fill="{MUTED}">{esc(line)}</text>')
        if i < 3:
            mx = x + tw + gap / 2
            b.append(f'<path d="M{mx-6} {H/2-8} L{mx+4} {H/2} L{mx-6} {H/2+8}" fill="none" stroke="{DIM}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    save("approach.svg", wrap(W, H, "\n".join(b), "How I work",
         "Start with the user problem, build deliberately, measure what matters, improve continuously."))


# ---------------------------------------------------------------- connect buttons
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
    button("btn-leetcode.svg", "{ }", "LEETCODE", "Anonymous_gp")


# ---------------------------------------------------------------- footer
def footer():
    W, H = 1000, 84
    b = [
        f'<rect x="0" y="22" width="{W}" height="1.5" fill="url(#fade)" opacity="0.8"/>',
        f'<text x="{W/2}" y="56" font-size="16" text-anchor="middle" fill="{MUTED}">Stay curious. Ship thoughtfully.</text>',
        f'<text class="m" x="{W/2}" y="76" font-size="11" letter-spacing="3" text-anchor="middle" fill="{DIM}">GOURI PAWAR</text>',
    ]
    save("footer.svg", wrap(W, H, "\n".join(b), "Stay curious. Ship thoughtfully. Gouri Pawar."))


if __name__ == "__main__":
    hero()
    metrics()
    for n, t, tag in [
        ("01", "Overview", "// what I do"),
        ("02", "Selected Work", "// things I have shipped"),
        ("03", "Toolkit", "// what I build with"),
        ("04", "Approach", "// how I work"),
        ("05", "Activity", "// on GitHub"),
        ("06", "Connect", "// say hello"),
    ]:
        section(n, t, tag)
    cards()
    toolkit()
    approach()
    buttons()
    footer()
