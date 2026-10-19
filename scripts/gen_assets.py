#!/usr/bin/env python3
"""Generates the animated SVG assets used by README.md.

Run from the repo root:  python3 scripts/gen_assets.py
Everything is plain SVG + CSS keyframes, so GitHub renders the animations
inside <img> tags without any JavaScript.
"""
from pathlib import Path
import random
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

CYAN = "#00c9ff"
MAGENTA = "#ff2e88"
BG0 = "#05070d"
BG1 = "#0a1628"
MONO = "'JetBrains Mono','Fira Code','SFMono-Regular',Consolas,Menlo,monospace"

REDUCED = """
@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; }
  .reveal { clip-path: none !important; opacity: 1 !important; }
}"""


def write(name, svg):
    (OUT / name).write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", name)


# --------------------------------------------------------------------------- hero
def hero():
    W, H = 1000, 340
    rnd = random.Random(7)

    particles = []
    for i in range(34):
        x = rnd.randint(10, W - 10)
        r = rnd.choice([0.8, 1.1, 1.4, 1.8])
        dur = rnd.uniform(6, 14)
        delay = -rnd.uniform(0, dur)
        col = CYAN if rnd.random() > 0.25 else MAGENTA
        particles.append(
            f'<circle cx="{x}" cy="{H + 10}" r="{r}" fill="{col}" class="p" '
            f'style="animation-duration:{dur:.1f}s;animation-delay:{delay:.1f}s"/>'
        )

    # perspective floor: vanishing point at (500, 205)
    vx, vy = 500, 258
    verticals = "".join(
        f'<line x1="{vx}" y1="{vy}" x2="{vx + k * 95}" y2="{H}"/>' for k in range(-14, 15)
    )
    horizontals = "".join(
        f'<line x1="0" y1="{vy + d}" x2="{W}" y2="{vy + d}"/>'
        for d in [4, 10, 18, 29, 43, 61, 84, 113]
    )

    sub = "> computer science & engineering // ai & systems architecture"
    n = len(sub)
    char_w = 10.8  # ~0.6em at 18px monospace
    sub_w = n * char_w
    sub_x = (W - sub_w) / 2

    roles = [
        "AI / ML · COMPUTER VISION",
        "COMPILERS · EMBEDDED · LOW-LEVEL",
        "FULL-STACK · CLOUD-NATIVE",
        "ALGORITHMS · OPTIMIZATION",
    ]
    role_cycle = 12  # seconds for whole loop
    role_nodes = "".join(
        f'<text x="{W/2}" y="250" class="role" style="animation-delay:{(i * role_cycle / len(roles)) - (role_cycle if i else 0)}s">{escape(r)}</text>'
        for i, r in enumerate(roles)
    )

    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="JYNXX — Computer Science &amp; Engineering, AI &amp; Systems Architecture">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{BG0}"/><stop offset="1" stop-color="{BG1}"/>
  </linearGradient>
  <radialGradient id="glow" cx="50%" cy="58%" r="55%">
    <stop offset="0" stop-color="{CYAN}" stop-opacity=".28"/>
    <stop offset=".55" stop-color="{CYAN}" stop-opacity=".05"/>
    <stop offset="1" stop-color="{CYAN}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="floorFade" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/>
    <stop offset=".5" stop-color="#fff" stop-opacity=".6"/>
    <stop offset="1" stop-color="#fff" stop-opacity="1"/>
  </linearGradient>
  <mask id="floorMask"><rect x="0" y="{vy}" width="{W}" height="{H - vy}" fill="url(#floorFade)"/></mask>
  <linearGradient id="titleGrad" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#ffffff"/>
    <stop offset=".5" stop-color="#bff1ff"/>
    <stop offset="1" stop-color="#ffffff"/>
  </linearGradient>
  <linearGradient id="sheen" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/>
    <stop offset=".5" stop-color="#fff" stop-opacity=".85"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="titleClip"><text x="{W/2}" y="178" class="title">JYNXX</text></clipPath>
  <clipPath id="sliceA"><rect x="0" y="118" width="{W}" height="14" class="sliceA"/></clipPath>
  <clipPath id="sliceB"><rect x="0" y="150" width="{W}" height="10" class="sliceB"/></clipPath>
    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="#000" opacity=".22"/>
  </pattern>
</defs>
<style>
  .title {{ font: 800 118px {MONO}; letter-spacing: 22px; text-anchor: middle; }}
  .sub   {{ font: 500 18px {MONO}; fill: #cfefff; }}
  .role  {{ font: 700 14px {MONO}; letter-spacing: 5px; text-anchor: middle; fill: {CYAN}; opacity: 0;
            animation: role {role_cycle}s linear infinite; }}
  .hud   {{ font: 600 11px {MONO}; letter-spacing: 2px; fill: {CYAN}; opacity: .75; }}
  .grid line {{ stroke: {CYAN}; stroke-width: 1; opacity: .22; }}
  .hlines {{ animation: floor 2.4s linear infinite; }}
  .p {{ animation-name: rise; animation-timing-function: linear; animation-iteration-count: infinite; opacity: 0; }}
  .main {{ animation: flicker 6s infinite; }}
  .gc {{ animation: gC 3.2s steps(1) infinite; }}
  .gm {{ animation: gM 3.2s steps(1) infinite; }}
  .sliceA {{ animation: sA 3.2s steps(1) infinite; }}
  .sliceB {{ animation: sB 3.2s steps(1) infinite; }}
  .sheen {{ animation: sheen 5s ease-in-out infinite; }}
  .type {{ clip-path: inset(0 100% 0 0); animation: type 3.2s steps({n}) .6s forwards; }}
  .cursor {{ animation: cur 3.2s steps({n}) .6s forwards, blink 1s steps(1) infinite; }}
  .scanbar {{ animation: scanbar 4.5s linear infinite; }}
  .dot {{ animation: pulse 1.6s ease-in-out infinite; }}
  .bracket {{ animation: bracket 3s ease-in-out infinite; }}

  @keyframes floor {{ from {{ transform: translateY(0); }} to {{ transform: translateY(14px); }} }}
  @keyframes rise {{ 0% {{ transform: translateY(0); opacity: 0; }} 10% {{ opacity: .9; }}
                     80% {{ opacity: .6; }} 100% {{ transform: translateY(-{H + 40}px); opacity: 0; }} }}
  @keyframes flicker {{ 0%,19%,21%,62%,64%,100% {{ opacity: 1; }} 20%,63% {{ opacity: .55; }} }}
  @keyframes gC {{ 0% {{ transform: translate(-3px,0); }} 8% {{ transform: translate(-9px,2px); }}
                   10% {{ transform: translate(-2px,-1px); }} 52% {{ transform: translate(-12px,0); }}
                   54% {{ transform: translate(-3px,0); }} 100% {{ transform: translate(-3px,0); }} }}
  @keyframes gM {{ 0% {{ transform: translate(3px,0); }} 8% {{ transform: translate(10px,-2px); }}
                   10% {{ transform: translate(2px,1px); }} 52% {{ transform: translate(13px,1px); }}
                   54% {{ transform: translate(3px,0); }} 100% {{ transform: translate(3px,0); }} }}
  @keyframes sA {{ 0%,100% {{ transform: translate(0,0); }} 8% {{ transform: translate(0,0); }} 9% {{ transform: translate(0,24px); }}
                   12% {{ transform: translate(0,0); }} 51% {{ transform: translate(0,40px); }} 55% {{ transform: translate(0,0); }} }}
  @keyframes sB {{ 0%,100% {{ transform: translate(0,0); }} 9% {{ transform: translate(0,-18px); }}
                   12% {{ transform: translate(0,0); }} 52% {{ transform: translate(0,-30px); }} 55% {{ transform: translate(0,0); }} }}
  @keyframes sheen {{ 0% {{ transform: translateX(-420px); }} 55%,100% {{ transform: translateX({W + 60}px); }} }}
  @keyframes type {{ to {{ clip-path: inset(0 0 0 0); }} }}
  @keyframes cur {{ to {{ transform: translateX({sub_w}px); }} }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  @keyframes scanbar {{ from {{ transform: translateY(-60px); }} to {{ transform: translateY({H + 60}px); }} }}
  @keyframes pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: .2; }} }}
  @keyframes bracket {{ 0%,100% {{ opacity: .9; }} 50% {{ opacity: .35; }} }}
  @keyframes role {{ 0% {{ opacity: 0; transform: translateY(6px); }} 3% {{ opacity: 1; transform: translateY(0); }}
                     22% {{ opacity: 1; transform: translateY(0); }} 25%,100% {{ opacity: 0; transform: translateY(-6px); }} }}
  {REDUCED}
</style>

<rect width="{W}" height="{H}" rx="18" fill="url(#bg)"/>
<rect width="{W}" height="{H}" rx="18" fill="url(#glow)"/>

<g class="grid" mask="url(#floorMask)">
  {verticals}
  <g class="hlines">{horizontals}</g>
</g>
<line x1="0" y1="{vy}" x2="{W}" y2="{vy}" stroke="{CYAN}" stroke-opacity=".55"/>

<g>{''.join(particles)}</g>

<!-- glitch title -->
<g opacity=".85">
  <text x="{W/2}" y="178" class="title gc" fill="{CYAN}" opacity=".75">JYNXX</text>
  <text x="{W/2}" y="178" class="title gm" fill="{MAGENTA}" opacity=".7">JYNXX</text>
</g>
<text x="{W/2}" y="178" class="title main" fill="url(#titleGrad)">JYNXX</text>
<g clip-path="url(#sliceA)"><text x="{W/2}" y="178" class="title gc" fill="#fff">JYNXX</text></g>
<g clip-path="url(#sliceB)"><text x="{W/2}" y="178" class="title gm" fill="#fff">JYNXX</text></g>
<g clip-path="url(#titleClip)"><g transform="skewX(-20)"><rect x="0" y="60" width="160" height="140" fill="url(#sheen)" class="sheen" opacity=".55"/></g></g>

<!-- typed subtitle -->
<text x="{sub_x}" y="214" class="sub type">{escape(sub)}</text>
<rect x="{sub_x}" y="199" width="10" height="19" fill="{CYAN}" class="cursor"/>

{role_nodes}

<!-- HUD -->
<g fill="none" stroke="{CYAN}" stroke-width="2" class="bracket">
  <path d="M24 52 V24 H52"/><path d="M{W-52} 24 H{W-24} V52"/>
  <path d="M24 {H-52} V{H-24} H52"/><path d="M{W-52} {H-24} H{W-24} V{H-52}"/>
</g>
<circle cx="70" cy="38" r="4" fill="#3dff9a" class="dot"/>
<text x="82" y="42" class="hud">SYS.ONLINE</text>
<text x="{W-70}" y="42" class="hud" text-anchor="end">ID://THEJYNXX</text>
<text x="70" y="{H-30}" class="hud">NODE CORE-01 · UPTIME 99.9%</text>
<text x="{W-70}" y="{H-30}" class="hud" text-anchor="end">BUILD 2026.10</text>

<rect width="{W}" height="{H}" fill="url(#scan)" rx="18"/>
<rect x="0" y="0" width="{W}" height="60" fill="{CYAN}" opacity=".05" class="scanbar"/>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{CYAN}" stroke-opacity=".35"/>
</svg>"""
    write("hero.svg", svg)


# ------------------------------------------------------------------ section headers
def header(slug, num, label, hint):
    W, H = 1000, 70
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(label)}">
<style>
  .n {{ font: 700 14px {MONO}; fill: {MAGENTA}; letter-spacing: 2px; }}
  .t {{ font: 800 26px {MONO}; fill: #e8f9ff; letter-spacing: 4px; }}
  .h {{ font: 500 12px {MONO}; fill: #6b8ba3; letter-spacing: 1px; }}
  .line {{ stroke-dasharray: 1000; stroke-dashoffset: 1000; animation: draw 1.6s cubic-bezier(.6,0,.2,1) .2s forwards; }}
  .node {{ animation: node 2.2s ease-in-out infinite; transform-origin: center; transform-box: fill-box; }}
  .run {{ animation: run 3.5s linear 1.8s infinite; opacity: 0; }}
  .reveal {{ clip-path: inset(0 100% 0 0); animation: rev .9s steps(18) forwards; }}
  @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
  @keyframes rev {{ to {{ clip-path: inset(0 0 0 0); }} }}
  @keyframes node {{ 0%,100% {{ transform: scale(1); opacity: 1; }} 50% {{ transform: scale(1.8); opacity: .3; }} }}
  @keyframes run {{ 0% {{ transform: translateX(0); opacity: 0; }} 5% {{ opacity: 1; }} 95% {{ opacity: 1; }} 100% {{ transform: translateX(640px); opacity: 0; }} }}
  {REDUCED}
</style>
<text x="6" y="30" class="n">{num} //</text>
<text x="66" y="31" class="t reveal">{escape(label)}</text>
<text x="{W - 6}" y="30" class="h" text-anchor="end">{escape(hint)}</text>
<line x1="6" y1="52" x2="{W - 6}" y2="52" stroke="{CYAN}" stroke-opacity=".18" stroke-width="1"/>
<line x1="6" y1="52" x2="{W - 6}" y2="52" stroke="url(#g{slug})" stroke-width="2" class="line"/>
<defs><linearGradient id="g{slug}" x1="0" x2="1"><stop offset="0" stop-color="{MAGENTA}"/><stop offset=".25" stop-color="{CYAN}"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient></defs>
<circle cx="6" cy="52" r="4" fill="{MAGENTA}" class="node"/>
<rect x="6" y="50" width="60" height="4" rx="2" fill="{CYAN}" class="run"/>
</svg>"""
    write(f"h-{slug}.svg", svg)


# ------------------------------------------------------------------ about terminal
def terminal():
    W = 1000
    lines = [
        ("cmd", "whoami"),
        ("out", "anurag ghosh  ·  aka jynxx  ·  cs & engineering"),
        ("gap", ""),
        ("cmd", "cat ~/focus.yml"),
        ("kv", ("ai_vision", "neural models, deep learning pipelines, vision architectures")),
        ("kv", ("systems", "low-level programming, embedded (x86 / 8051), compiler design")),
        ("kv", ("software", "high-performance full-stack apps & cloud-native services")),
        ("kv", ("core_cs", "algorithm optimization, operating systems, concurrency")),
        ("kv", ("ethos", "clean architecture, resilient by default")),
        ("gap", ""),
        ("cmd", "git log --oneline -1"),
        ("out2", "a1b2c3d  feat: continuously architecting & shipping open source"),
        ("prompt", ""),
    ]
    top, lh = 74, 26
    y = top
    t = 0.5
    nodes = []
    for kind, val in lines:
        if kind == "gap":
            y += lh // 2
            continue
        if kind == "cmd":
            n = len(val)
            dur = max(0.35, n * 0.045)
            nodes.append(
                f'<g class="ln" style="animation-delay:{t:.2f}s"><text x="36" y="{y}" class="ps">❯</text></g>'
                f'<text x="60" y="{y}" class="cmd tp" style="--n:{n};animation-delay:{t + 0.15:.2f}s;animation-duration:{dur:.2f}s;animation-timing-function:steps({n})">{escape(val)}</text>'
            )
            t += dur + 0.45
        elif kind in ("out", "out2"):
            cls = "out" if kind == "out" else "out2"
            nodes.append(f'<text x="60" y="{y}" class="{cls} ln" style="animation-delay:{t:.2f}s">{escape(val)}</text>')
            t += 0.35
        elif kind == "kv":
            k, v = val
            nodes.append(
                f'<g class="ln" style="animation-delay:{t:.2f}s">'
                f'<text x="60" y="{y}" class="k">{escape(k)}<tspan class="c">:</tspan></text>'
                f'<text x="200" y="{y}" class="v">{escape(v)}</text></g>'
            )
            t += 0.22
        elif kind == "prompt":
            nodes.append(
                f'<g class="ln" style="animation-delay:{t:.2f}s"><text x="36" y="{y}" class="ps">❯</text>'
                f'<rect x="60" y="{y - 15}" width="10" height="19" fill="{CYAN}" class="blink"/></g>'
            )
        y += lh
    H = y + 16

    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="About: AI and computer vision, systems and compilers, full-stack and cloud, core CS">
<defs>
  <linearGradient id="tb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1220"/><stop offset="1" stop-color="#070b14"/></linearGradient>
  <linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="{MAGENTA}"/><stop offset=".5" stop-color="{CYAN}"/><stop offset="1" stop-color="{MAGENTA}"/></linearGradient>
</defs>
<style>
  text {{ font: 500 15px {MONO}; }}
  .ps {{ fill: {MAGENTA}; font-weight: 700; }}
  .cmd {{ fill: #ffffff; font-weight: 600; }}
  .out {{ fill: #9fdcff; }}
  .out2 {{ fill: #3dff9a; }}
  .k {{ fill: {CYAN}; font-weight: 600; }}
  .c {{ fill: #6b8ba3; }}
  .v {{ fill: #c9d6e2; }}
  .bar {{ font: 600 12px {MONO}; fill: #6b8ba3; letter-spacing: 1px; }}
  .ln {{ opacity: 0; animation: fade .25s ease-out forwards; }}
  .tp {{ clip-path: inset(0 100% 0 0); animation-name: type; animation-fill-mode: forwards; }}
  .blink {{ animation: blink 1s steps(1) infinite; }}
  .edge {{ stroke-dasharray: 220 1400; animation: orbit 7s linear infinite; }}
  @keyframes fade {{ from {{ opacity: 0; transform: translateX(-6px); }} to {{ opacity: 1; transform: none; }} }}
  @keyframes type {{ to {{ clip-path: inset(0 0 0 0); }} }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  @keyframes orbit {{ to {{ stroke-dashoffset: -1620; }} }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} .ln {{ opacity: 1; }} .tp {{ clip-path: none; }} }}
</style>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="url(#tb)" stroke="#1b2a3d"/>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="none" stroke="url(#edge)" stroke-width="2" class="edge" pathLength="1620"/>
<path d="M1 44 H{W-1}" stroke="#1b2a3d"/>
<circle cx="28" cy="23" r="6" fill="#ff5f57"/><circle cx="48" cy="23" r="6" fill="#febc2e"/><circle cx="68" cy="23" r="6" fill="#28c840"/>
<text x="{W/2}" y="27" class="bar" text-anchor="middle">jynxx@core: ~ — zsh</text>
{''.join(nodes)}
</svg>"""
    write("about-terminal.svg", svg)


# ------------------------------------------------------------------------- footer
def footer():
    W, H = 1000, 150
    bars = []
    rnd = random.Random(3)
    nb = 64
    bw = W / nb
    for i in range(nb):
        d = rnd.uniform(0.9, 2.2)
        delay = -rnd.uniform(0, d)
        col = CYAN if i % 9 else MAGENTA
        bars.append(
            f'<rect x="{i * bw + 2:.1f}" y="{H - 70}" width="{bw - 4:.1f}" height="70" rx="2" fill="{col}" class="eq" '
            f'style="animation-duration:{d:.2f}s;animation-delay:{delay:.2f}s"/>'
        )
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="End of transmission">
<defs>
  <linearGradient id="fbg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG0}"/></linearGradient>
  <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <mask id="m"><rect width="{W}" height="{H}" fill="url(#fade)" transform="rotate(180 {W/2} {H/2})"/></mask>
</defs>
<style>
  .eq {{ transform-box: fill-box; transform-origin: bottom; animation-name: eq; animation-iteration-count: infinite;
         animation-direction: alternate; animation-timing-function: ease-in-out; opacity: .65; }}
  .t {{ font: 700 15px {MONO}; fill: #e8f9ff; letter-spacing: 6px; text-anchor: middle; }}
  .blink {{ animation: blink 1.2s steps(1) infinite; }}
  @keyframes eq {{ from {{ transform: scaleY(.08); }} to {{ transform: scaleY(1); }} }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  {REDUCED}
</style>
<rect width="{W}" height="{H}" rx="18" fill="url(#fbg)"/>
<clipPath id="fc"><rect width="{W}" height="{H}" rx="18"/></clipPath>
<g mask="url(#m)" clip-path="url(#fc)">{''.join(bars)}</g>
<text x="{W/2}" y="52" class="t">// END OF TRANSMISSION<tspan fill="{CYAN}" class="blink"> _</tspan></text>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{CYAN}" stroke-opacity=".3"/>
</svg>"""
    write("footer.svg", svg)


# ----------------------------------------------------------------------- trophies
def trophies():
    W, H = 1000, 195
    card_w = 152
    card_h = 168
    gap = 12
    start_x = 14
    y = 14

    items = [
        {
            "rank": "SSS",
            "title": "COMMITS",
            "desc": "ACTIVE SHIP",
            "col": "#ffca28",
            "path": """<path d="M-14 20 h28 v3 h-28 z M-5 14 h10 v6 h-10 z" fill="#ffca28"/>
<path d="M-16 -12 h32 c0 16 -8 24 -16 24 s-16 -8 -16 -24 z" fill="none" stroke="#ffca28" stroke-width="2"/>
<path d="M-16 -8 c-6 0 -10 4 -10 10 s4 10 10 10 M16 -8 c6 0 10 4 10 10 s-4 10 -10 10" fill="none" stroke="#ffca28" stroke-width="1.8"/>
<polygon points="0,-7 2,-2 7,-2 3,1 5,6 0,3 -5,6 -3,1 -7,-2 -2,-2" fill="#ffca28"/>"""
        },
        {
            "rank": "SS",
            "title": "POLYGLOT",
            "desc": "7+ STACKS",
            "col": CYAN,
            "path": f"""<rect x="-18" y="-18" width="36" height="36" rx="6" transform="rotate(45)" fill="none" stroke="{CYAN}" stroke-width="2"/>
<path d="M-8 -6 L-15 0 L-8 6 M8 -6 L15 0 L8 6 M-2 8 L2 -8" fill="none" stroke="{CYAN}" stroke-width="2" stroke-linecap="round"/>"""
        },
        {
            "rank": "S",
            "title": "REPOSITORIES",
            "desc": "24+ ARCHIVES",
            "col": MAGENTA,
            "path": f"""<path d="M-18 -6 L0 -14 L18 -6 L0 2 Z" fill="none" stroke="{MAGENTA}" stroke-width="2"/>
<path d="M-18 2 L0 10 L18 2 M-18 9 L0 17 L18 9" fill="none" stroke="{MAGENTA}" stroke-width="2"/>
<circle cx="0" cy="-6" r="2.5" fill="{MAGENTA}"/>"""
        },
        {
            "rank": "SSS",
            "title": "SYSTEMS & AI",
            "desc": "LOW-LEVEL & DL",
            "col": "#ff7b00",
            "path": """<rect x="-15" y="-15" width="30" height="30" rx="4" fill="none" stroke="#ff7b00" stroke-width="2"/>
<rect x="-7" y="-7" width="14" height="14" rx="2" fill="#ff7b00" opacity=".35" stroke="#ff7b00" stroke-width="1.5"/>
<path d="M-9 -19 v4 M0 -19 v4 M9 -19 v4 M-9 15 v4 M0 15 v4 M9 15 v4 M-19 -9 h4 M-19 0 h4 M-19 9 h4 M15 -9 h4 M15 0 h4 M15 9 h4" stroke="#ff7b00" stroke-width="1.8"/>"""
        },
        {
            "rank": "A",
            "title": "PULL SHARK",
            "desc": "PR ARCHITECT",
            "col": CYAN,
            "path": f"""<circle cx="-10" cy="-11" r="3.5" fill="{CYAN}"/><circle cx="-10" cy="11" r="3.5" fill="{CYAN}"/><circle cx="10" cy="0" r="3.5" fill="{CYAN}"/>
<path d="M-10 -7 v14 M-10 -5 c0 6 10 4 10 5" fill="none" stroke="{CYAN}" stroke-width="2" stroke-linecap="round"/>
<path d="M1 -13 c3 6 13 8 13 8 c-3 0 -8 -3 -13 -8" fill="{CYAN}"/>"""
        },
        {
            "rank": "S",
            "title": "TELEMETRY",
            "desc": "31D SIGNAL",
            "col": "#3dff9a",
            "path": """<circle cx="0" cy="0" r="20" fill="none" stroke="#3dff9a" stroke-width="1.5" stroke-dasharray="3 3" opacity=".5"/>
<path d="M-15 0 h7 l4 -11 l5 22 l4 -15 l3 4 h7" fill="none" stroke="#3dff9a" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>"""
        },
    ]

    cards = []
    for i, it in enumerate(items):
        cx = start_x + i * (card_w + gap)
        center_x = cx + card_w / 2
        col = it["col"]
        rank = it["rank"]
        title = it["title"]
        desc = it["desc"]
        path = it["path"]
        glow_id = f"tg{i}"
        card = f"""
  <!-- Card {i}: {title} -->
  <g class="trophy-card" style="animation-delay: {i * 0.15:.2f}s">
    <defs>
      <radialGradient id="{glow_id}" cx="50%" cy="45%" r="50%">
        <stop offset="0" stop-color="{col}" stop-opacity=".22"/>
        <stop offset="1" stop-color="{col}" stop-opacity="0"/>
      </radialGradient>
    </defs>
    <!-- Background -->
    <rect x="{cx}" y="{y}" width="{card_w}" height="{card_h}" rx="12" fill="url(#cardBg)" stroke="#17263c" stroke-width="1"/>
    <!-- Glow aura -->
    <circle cx="{center_x}" cy="{y + 68}" r="45" fill="url(#{glow_id})"/>
    <!-- Rank Pill -->
    <rect x="{cx + card_w - 46}" y="{y + 10}" width="36" height="17" rx="8.5" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".5" stroke-width="1"/>
    <text x="{cx + card_w - 28}" y="{y + 22}" fill="{col}" font-family="{MONO}" font-size="9" font-weight="800" text-anchor="middle">{rank}</text>
    <!-- Star Label -->
    <text x="{cx + 12}" y="{y + 22}" fill="{col}" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="1">★ RANK</text>
    <!-- Emblem -->
    <g transform="translate({center_x}, {y + 68})" class="icon-pulse">
      {path}
    </g>
    <!-- Title -->
    <text x="{center_x}" y="{y + 126}" fill="#f0f6fc" font-family="{MONO}" font-size="11" font-weight="800" letter-spacing="1.5" text-anchor="middle">{title}</text>
    <!-- Subtitle / Stat -->
    <text x="{center_x}" y="{y + 144}" fill="#6b8ba3" font-family="{MONO}" font-size="9" font-weight="600" letter-spacing="0.8" text-anchor="middle">{desc}</text>
    <!-- Bottom accent line -->
    <line x1="{cx + 25}" y1="{y + card_h - 1}" x2="{cx + card_w - 25}" y2="{y + card_h - 1}" stroke="{col}" stroke-width="2" stroke-opacity=".7" stroke-linecap="round"/>
  </g>"""
        cards.append(card)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Cyberpunk Profile Trophies">
<defs>
  <linearGradient id="cardBg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#0a1220"/>
    <stop offset="1" stop-color="#05070e"/>
  </linearGradient>
</defs>
<style>
  .trophy-card {{ transform-origin: center; }}
  .icon-pulse {{ animation: icPulse 3s ease-in-out infinite; transform-origin: center; }}
  @keyframes icPulse {{
    0%, 100% {{ transform: scale(1); }}
    50% {{ transform: scale(1.06); }}
  }}
  {REDUCED}
</style>
{''.join(cards)}
</svg>"""
    write("trophies.svg", svg)


if __name__ == "__main__":
    hero()
    terminal()
    for args in [
        ("about", "01", "ABOUT", "~/whoami"),
        ("stack", "02", "TECH STACK", "tools of the trade"),
        ("stats", "03", "TELEMETRY", "live from github"),
        ("achievements", "04", "ACHIEVEMENTS", "milestones unlocked"),
        ("trophies", "05", "TROPHIES", "achievement.log"),
        ("snake", "06", "CONTRIBUTIONS", "the snake eats my commits"),
        ("connect", "07", "CONNECT", "open a channel"),
    ]:
        header(*args)
    trophies()
    footer()

