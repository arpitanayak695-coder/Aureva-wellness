#!/usr/bin/env python3
"""Generates every illustration used by the Aureva Wellness site.

This script produced the files already sitting in ./images — you do not need to
run it. Keep it if you want to recolour the palette, change a pose or add a new
illustration in the same style; it only depends on the standard library.

All artwork is original vector work built from primitive shapes in the
reference palette (blush pink / rose / warm cream). Re-run to regenerate:
    python3 gen_assets.py
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- palettes
PAL = {
    "rose":    dict(skin="#F7CDBC", skin2="#EFB7A4", hair="#F0709C", hair2="#D64B7E",
                    cloth="#FB8FB4", cloth2="#E85F94", bg1="#FFEAF1", bg2="#FFD5E3"),
    "amber":   dict(skin="#F3C6AE", skin2="#E3AE93", hair="#E4735C", hair2="#C4543F",
                    cloth="#F79A8E", cloth2="#E0705F", bg1="#FFF0E8", bg2="#FFDCCE"),
    "mauve":   dict(skin="#F2CBC4", skin2="#E0B1A9", hair="#B96E9B", hair2="#94517C",
                    cloth="#D98FC0", cloth2="#B96AA2", bg1="#FBECF6", bg2="#F3D8EC"),
    "sand":    dict(skin="#E8BB9E", skin2="#D5A385", hair="#8A5A4E", hair2="#6B4238",
                    cloth="#F6A8A0", cloth2="#DE7F78", bg1="#FFF1EC", bg2="#FADCD4"),
}

def head(x, y, r, p, tuft=True):
    """Head + hair mass, seen three-quarters/front, eyes closed."""
    s = f'''
  <path d="M{x-r-3},{y+2} q-4,-{r*1.35} {r+3},-{r*1.5} q{r+3},{r*0.15} {r+3},{r*1.5}
           q-{r*0.35},-{r*0.55} -{r+3},-{r*0.55} q-{r*0.62},0 -{r+3},{r*0.55} z"
        fill="{p['hair2']}"/>
  <ellipse cx="{x}" cy="{y}" rx="{r*0.86}" ry="{r}" fill="{p['skin']}"/>
  <path d="M{x-r*0.9},{y-r*0.1} q0,-{r*1.25} {r*0.9},-{r*1.25}
           q{r*0.9},0 {r*0.9},{r*1.25} q-{r*0.2},-{r*0.5} -{r*0.9},-{r*0.5}
           q-{r*0.7},0 -{r*0.9},{r*0.5} z" fill="{p['hair']}"/>
  <path d="M{x-r*0.34},{y+r*0.08} q{r*0.18},{r*0.16} {r*0.36},0" stroke="{p['skin2']}"
        stroke-width="{max(1.2, r*0.09)}" fill="none" stroke-linecap="round"/>
  <path d="M{x+r*0.14},{y+r*0.08} q{r*0.18},{r*0.16} {r*0.36},0" stroke="{p['skin2']}"
        stroke-width="{max(1.2, r*0.09)}" fill="none" stroke-linecap="round"/>
  <path d="M{x-r*0.16},{y+r*0.45} q{r*0.17},{r*0.16} {r*0.34},0" stroke="{p['skin2']}"
        stroke-width="{max(1.1, r*0.08)}" fill="none" stroke-linecap="round"/>'''
    if tuft:
        s += f'''
  <path d="M{x-r*0.95},{y-r*0.15} q-{r*0.5},{r*1.5} {r*0.12},{r*2.1}
           q{r*0.2},-{r*1.1} {r*0.35},-{r*1.6} z" fill="{p['hair']}"/>
  <path d="M{x+r*0.95},{y-r*0.15} q{r*0.5},{r*1.5} -{r*0.12},{r*2.1}
           q-{r*0.2},-{r*1.1} -{r*0.35},-{r*1.6} z" fill="{p['hair']}"/>'''
    return s


def seated(cx, base, s, pal, aura=False):
    """Lotus / sukhasana seated figure. s = scale (1 => ~200px tall)."""
    p = PAL[pal]
    S = lambda v: v * s
    g = [f'<g transform="translate({cx},{base}) scale({s})">']
    g.append(f'<ellipse cx="0" cy="6" rx="104" ry="15" fill="rgba(216,90,140,.13)"/>')
    if aura:
        g.append('<circle cx="0" cy="-118" r="132" fill="none" stroke="rgba(240,112,156,.20)" stroke-width="2"/>')
        g.append('<circle cx="0" cy="-118" r="158" fill="none" stroke="rgba(240,112,156,.12)" stroke-width="2"/>')
    # crossed legs
    g.append(f'<path d="M-92,0 Q0,-44 92,0 Q0,26 -92,0 z" fill="{p["cloth2"]}"/>')
    g.append(f'<path d="M-74,-4 Q0,-36 74,-4 Q0,14 -74,-4 z" fill="{p["cloth"]}"/>')
    g.append(f'<ellipse cx="-14" cy="-6" rx="24" ry="13" fill="{p["skin"]}" transform="rotate(-12 -14 -6)"/>')
    g.append(f'<ellipse cx="16" cy="-9" rx="22" ry="12" fill="{p["skin2"]}" transform="rotate(10 16 -9)"/>')
    # torso
    g.append(f'<path d="M-40,-14 Q-46,-84 -33,-112 Q0,-126 33,-112 Q46,-84 40,-14 Q0,-2 -40,-14 z" fill="{p["cloth"]}"/>')
    g.append(f'<path d="M-33,-112 Q0,-126 33,-112 Q30,-96 0,-92 Q-30,-96 -33,-112 z" fill="{p["cloth2"]}" opacity=".55"/>')
    # arms resting on knees
    for sx in (-1, 1):
        g.append(f'<path d="M{sx*34},-104 Q{sx*82},-72 {sx*70},-16" stroke="{p["skin"]}" '
                 f'stroke-width="19" fill="none" stroke-linecap="round"/>')
        g.append(f'<circle cx="{sx*70}" cy="-14" r="11" fill="{p["skin2"]}"/>')
    g.append(f'<rect x="-9" y="-128" width="18" height="16" rx="8" fill="{p["skin2"]}"/>')
    g.append(head(0, -152, 30, p))
    g.append('</g>')
    return "\n".join(g)


def standing(cx, base, s, pal, arms="up"):
    """Tree pose (vrikshasana) — one foot to inner thigh, arms overhead."""
    p = PAL[pal]
    g = [f'<g transform="translate({cx},{base}) scale({s})">']
    g.append('<ellipse cx="0" cy="4" rx="46" ry="10" fill="rgba(216,90,140,.13)"/>')
    g.append(f'<path d="M-11,-96 L-11,-6 Q-11,2 -2,2 L10,2 Q14,2 12,-4 L2,-96 z" fill="{p["skin"]}"/>')
    g.append(f'<path d="M-8,-104 Q-58,-88 -46,-58 Q-30,-74 -4,-70 z" fill="{p["skin2"]}"/>')
    g.append(f'<path d="M-26,-122 Q0,-132 26,-122 L22,-86 Q0,-78 -22,-86 z" fill="{p["cloth2"]}"/>')
    g.append(f'<path d="M-24,-196 Q0,-206 24,-196 Q30,-160 26,-120 Q0,-110 -26,-120 Q-30,-160 -24,-196 z" fill="{p["cloth"]}"/>')
    if arms == "up":
        g.append(f'<path d="M-20,-190 Q-34,-232 -5,-252" stroke="{p["skin"]}" stroke-width="12" fill="none" stroke-linecap="round"/>')
        g.append(f'<path d="M20,-190 Q34,-232 5,-252" stroke="{p["skin"]}" stroke-width="12" fill="none" stroke-linecap="round"/>')
        g.append(f'<circle cx="0" cy="-256" r="9" fill="{p["skin2"]}"/>')
        hy = -226
    else:
        g.append(f'<path d="M-20,-188 Q-48,-160 -34,-128" stroke="{p["skin"]}" stroke-width="12" fill="none" stroke-linecap="round"/>')
        g.append(f'<path d="M20,-188 Q48,-160 34,-128" stroke="{p["skin"]}" stroke-width="12" fill="none" stroke-linecap="round"/>')
        hy = -226
    g.append(f'<rect x="-6" y="-212" width="12" height="14" rx="6" fill="{p["skin2"]}"/>')
    g.append(head(0, hy, 21, p))
    g.append('</g>')
    return "\n".join(g)


def child_pose(cx, base, s, pal):
    """Balasana — resting forward fold."""
    p = PAL[pal]
    g = [f'<g transform="translate({cx},{base}) scale({s})">']
    g.append('<ellipse cx="0" cy="6" rx="110" ry="14" fill="rgba(216,90,140,.13)"/>')
    g.append(f'<path d="M-96,0 Q-90,-26 -58,-30 L54,-30 Q92,-26 96,0 z" fill="{p["cloth2"]}"/>')
    g.append(f'<path d="M-52,-26 Q-34,-96 34,-84 Q86,-74 92,-6 Q30,-16 -52,-26 z" fill="{p["cloth"]}"/>')
    g.append(f'<path d="M-46,-30 Q-96,-26 -104,-6" stroke="{p["skin"]}" stroke-width="16" fill="none" stroke-linecap="round"/>')
    g.append(f'<path d="M-40,-48 Q-92,-44 -104,-18" stroke="{p["skin2"]}" stroke-width="15" fill="none" stroke-linecap="round"/>')
    g.append(head(-46, -44, 24, p))
    g.append('</g>')
    return "\n".join(g)


def forward_fold(cx, base, s, pal):
    """Paschimottanasana — seated forward stretch."""
    p = PAL[pal]
    g = [f'<g transform="translate({cx},{base}) scale({s})">']
    g.append('<ellipse cx="0" cy="6" rx="112" ry="14" fill="rgba(216,90,140,.13)"/>')
    g.append(f'<path d="M-70,0 L74,0 Q98,0 98,-14 Q98,-26 72,-24 L-64,-22 Q-84,-20 -84,-10 Q-84,0 -70,0 z" fill="{p["skin"]}"/>')
    g.append(f'<path d="M-84,-16 Q-76,-72 -34,-72 Q26,-70 58,-34 Q20,-26 -60,-18 z" fill="{p["cloth"]}"/>')
    g.append(f'<path d="M-56,-60 Q6,-56 62,-28" stroke="{p["skin"]}" stroke-width="14" fill="none" stroke-linecap="round"/>')
    g.append(head(20, -52, 23, p))
    g.append('</g>')
    return "\n".join(g)


def bg(w, h, c1, c2, idp, rays=True, floor=True):
    """Soft gradient backdrop with sun arc and horizon."""
    s = f'''<defs>
  <linearGradient id="bgg{idp}" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/>
  </linearGradient>
  <radialGradient id="sun{idp}" cx=".5" cy=".5" r=".5">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity=".95"/>
    <stop offset="1" stop-color="#FFC9DC" stop-opacity="0"/>
  </radialGradient>
</defs>
<rect width="{w}" height="{h}" fill="url(#bgg{idp})"/>
<circle cx="{w*0.5}" cy="{h*0.42}" r="{h*0.42}" fill="url(#sun{idp})"/>'''
    if rays:
        s += f'<circle cx="{w*0.5}" cy="{h*0.44}" r="{h*0.3}" fill="none" stroke="#FFFFFF" stroke-opacity=".5" stroke-width="2"/>'
        s += f'<circle cx="{w*0.5}" cy="{h*0.44}" r="{h*0.38}" fill="none" stroke="#FFFFFF" stroke-opacity=".3" stroke-width="2"/>'
    if floor:
        s += (f'<path d="M0,{h*0.78} Q{w*0.5},{h*0.70} {w},{h*0.78} L{w},{h} L0,{h} z" '
              f'fill="#FFFFFF" fill-opacity=".55"/>')
    return s


def svg(name, w, h, body, title):
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
           f'width="{w}" height="{h}" role="img" aria-label="{title}">\n'
           f'<title>{title}</title>\n{body}\n</svg>\n')
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(doc)
    return name


def leaf(x, y, s, rot, op=".5"):
    return (f'<path d="M{x},{y} q{18*s},-{26*s} {40*s},-{4*s} q-{20*s},{24*s} -{40*s},{4*s} z" '
            f'fill="#F48CB4" fill-opacity="{op}" transform="rotate({rot} {x} {y})"/>')


# ------------------------------------------------------------------ assets
# 1. hero
b = bg(1200, 820, "#FFF4F8", "#FFD9E6", "hero")
b += '<path d="M0,640 Q300,560 620,632 Q900,690 1200,620 L1200,820 L0,820 z" fill="#FFFFFF" fill-opacity=".6"/>'
b += leaf(120, 300, 1.5, -18) + leaf(1000, 250, 1.6, 22) + leaf(190, 620, 1.1, 14, ".35") + leaf(980, 600, 1.2, -20, ".35")
b += seated(600, 700, 1.75, "rose", aura=True)
svg("hero-yoga.svg", 1200, 820, b, "Illustration of a woman meditating in lotus pose at sunrise")

# 2. about — group class
b = bg(900, 700, "#FFF6F9", "#FFDCE8", "about", rays=False)
b += '<rect x="0" y="540" width="900" height="160" fill="#FFFFFF" fill-opacity=".65"/>'
b += leaf(80, 170, 1.2, -12, ".35") + leaf(760, 150, 1.2, 18, ".35")
for i, (x, pal) in enumerate([(210, "mauve"), (450, "rose"), (690, "amber")]):
    b += f'<rect x="{x-92}" y="536" width="184" height="16" rx="8" fill="#F9A8C6" fill-opacity=".55"/>'
    b += standing(x, 540, 1.28, pal)
svg("about-yoga.svg", 900, 700, b, "Three people practising tree pose together in a bright studio")

# 3. programme cards
programs = [
    ("program-beginner.svg", "rose",  "Beginner yoga class illustration", "seated"),
    ("program-meditation.svg", "mauve", "Guided meditation illustration", "aura"),
    ("program-stress-relief.svg", "amber", "Restorative child's pose illustration", "child"),
    ("program-flexibility.svg", "sand", "Seated forward fold stretch illustration", "fold"),
    ("program-mindfulness.svg", "mauve", "Mindful breathing illustration", "aura"),
    ("program-personal.svg", "rose", "One-to-one personal yoga session illustration", "pair"),
]
for name, pal, alt, kind in programs:
    b = bg(760, 560, PAL[pal]["bg1"], PAL[pal]["bg2"], name.replace(".", ""), rays=(kind == "aura"))
    b += leaf(70, 120, 1.0, -16, ".3") + leaf(640, 110, 1.0, 20, ".3")
    if kind == "seated":
        b += seated(380, 470, 1.35, pal)
    elif kind == "aura":
        b += seated(380, 470, 1.25, pal, aura=True)
    elif kind == "child":
        b += child_pose(380, 470, 1.4, pal)
    elif kind == "fold":
        b += forward_fold(380, 460, 1.35, pal)
    else:
        b += standing(250, 470, 1.15, "mauve", arms="mid") + seated(520, 470, 1.0, pal)
    svg(name, 760, 560, b, alt)

# 4. practice / consistency — studio window
b = bg(820, 720, "#FFF2F7", "#FFDCE9", "studio", rays=False, floor=False)
b += '''<path d="M250,90 q160,-70 320,0 L570,470 L250,470 z" fill="#FFFFFF" fill-opacity=".8"/>
<path d="M410,52 L410,470" stroke="#FBC6D9" stroke-width="6"/>
<path d="M250,250 L570,250" stroke="#FBC6D9" stroke-width="6"/>
<path d="M250,90 q160,-70 320,0 L570,470 L250,470 z" fill="none" stroke="#F69CBE" stroke-width="8"/>
<rect x="0" y="470" width="820" height="250" fill="#FFFFFF" fill-opacity=".6"/>'''
b += leaf(110, 380, 1.4, -14, ".4") + leaf(700, 360, 1.4, 16, ".4")
b += f'<rect x="150" y="620" width="230" height="18" rx="9" fill="#F9A8C6" fill-opacity=".6"/>'
b += f'<rect x="440" y="620" width="230" height="18" rx="9" fill="#F9A8C6" fill-opacity=".6"/>'
b += seated(265, 622, 1.15, "mauve") + seated(555, 622, 1.15, "rose")
svg("practice-studio.svg", 820, 720, b, "Two people meditating side by side in a sunlit studio")

# 5. small strip images
for i, (name, pal, kind, alt) in enumerate([
        ("strip-morning.svg", "rose", "stand", "Morning tree pose practice"),
        ("strip-breathe.svg", "mauve", "seat", "Breathing practice in easy pose"),
        ("strip-evening.svg", "amber", "fold", "Evening stretch practice")]):
    b = bg(420, 560, PAL[pal]["bg1"], PAL[pal]["bg2"], name.replace(".", ""), rays=False)
    if kind == "stand":
        b += standing(210, 470, 1.35, pal)
    elif kind == "seat":
        b += seated(210, 470, 1.1, pal)
    else:
        b += forward_fold(210, 460, 1.1, pal)
    svg(name, 420, 560, b, alt)

# 6. instructor portraits
def portrait(name, pal, alt, style):
    p = PAL[pal]
    ip = name.replace(".", "")
    b = f'''<defs><linearGradient id="p{ip}" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{p['bg1']}"/><stop offset="1" stop-color="{p['bg2']}"/></linearGradient>
    <clipPath id="c{ip}"><circle cx="300" cy="300" r="300"/></clipPath></defs>
  <g clip-path="url(#c{ip})">
  <rect width="600" height="600" fill="url(#p{ip})"/>
  <circle cx="300" cy="286" r="210" fill="#FFFFFF" fill-opacity=".45"/>
  <path d="M110,600 q40,-170 190,-170 q150,0 190,170 z" fill="{p['cloth']}"/>
  <path d="M232,430 q68,44 136,0 l0,-70 l-136,0 z" fill="{p['skin2']}"/>'''
    if style == "long":
        b += f'<path d="M126,430 q-10,-290 174,-290 q184,0 174,290 q-40,-150 -174,-150 q-134,0 -174,150 z" fill="{p["hair2"]}"/>'
    elif style == "bun":
        b += f'<circle cx="300" cy="112" r="56" fill="{p["hair2"]}"/>'
    else:
        b += f'<path d="M150,330 q0,-210 150,-210 q150,0 150,210 q-30,-120 -150,-120 q-120,0 -150,120 z" fill="{p["hair2"]}"/>'
    b += f'''
  <ellipse cx="300" cy="300" rx="132" ry="152" fill="{p['skin']}"/>
  <path d="M164,290 q0,-186 136,-186 q136,0 136,186 q-28,-84 -136,-84 q-108,0 -136,84 z" fill="{p['hair']}"/>
  <path d="M244,300 q26,26 52,0" stroke="{p['skin2']}" stroke-width="9" fill="none" stroke-linecap="round"/>
  <path d="M304,300 q26,26 52,0" stroke="{p['skin2']}" stroke-width="9" fill="none" stroke-linecap="round"/>
  <path d="M280,368 q22,20 44,0" stroke="{p['skin2']}" stroke-width="8" fill="none" stroke-linecap="round"/>
  <ellipse cx="216" cy="338" rx="20" ry="13" fill="{p['cloth']}" opacity=".45"/>
  <ellipse cx="384" cy="338" rx="20" ry="13" fill="{p['cloth']}" opacity=".45"/>
  </g>'''
    svg(name, 600, 600, b, alt)

portrait("instructor-1.svg", "rose", "Portrait illustration of Sophia Bennett, senior yoga guide", "long")
portrait("instructor-2.svg", "amber", "Portrait illustration of Arun Mehra, breathwork guide", "short")
portrait("instructor-3.svg", "mauve", "Portrait illustration of Leah Okafor, meditation guide", "bun")
portrait("member-1.svg", "sand", "Portrait illustration of a smiling member", "short")
portrait("member-2.svg", "mauve", "Portrait illustration of a member after class", "bun")
portrait("member-3.svg", "rose", "Portrait illustration of a long-time member", "long")

# 7. testimonial feature
b = bg(760, 900, "#FFF3F8", "#FFD9E7", "story", rays=False, floor=False)
b += '<rect x="0" y="640" width="760" height="260" fill="#FFFFFF" fill-opacity=".55"/>'
b += leaf(80, 200, 1.3, -18, ".35") + leaf(600, 180, 1.3, 20, ".35")
b += seated(380, 760, 1.5, "amber")
svg("story-feature.svg", 760, 900, b, "A member seated in quiet reflection after class")

# 8. footer figure
b = f'<rect width="600" height="760" fill="none"/>' + leaf(60, 200, 1.2, -16, ".3")
b += standing(300, 700, 2.2, "rose")
svg("footer-yoga.svg", 600, 760, b, "Illustration of a yoga practitioner in tree pose")

# 9. contact page visual
b = bg(760, 900, "#FFF4F9", "#FFDCEA", "contact", rays=True, floor=False)
b += '<rect x="0" y="660" width="760" height="240" fill="#FFFFFF" fill-opacity=".55"/>'
b += leaf(90, 230, 1.3, -16, ".35") + leaf(600, 210, 1.3, 18, ".35")
b += seated(380, 780, 1.55, "mauve", aura=True)
svg("contact-yoga.svg", 760, 900, b, "Illustration of a guide welcoming new students")

# 10. favicon / logo mark
b = '''<defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1">
 <stop offset="0" stop-color="#FB8FB4"/><stop offset="1" stop-color="#E0356F"/></linearGradient></defs>
<rect width="64" height="64" rx="18" fill="url(#lg)"/>
<path d="M32,16 q14,10 14,22 q0,12 -14,12 q-14,0 -14,-12 q0,-12 14,-22 z" fill="#FFFFFF" fill-opacity=".92"/>
<path d="M32,50 q-9,-6 -9,-12" stroke="#FFD9E6" stroke-width="3" fill="none" stroke-linecap="round"/>'''
svg("logo-mark.svg", 64, 64, b, "Aureva Wellness logo")

print("\n".join(sorted(os.listdir(OUT))))
