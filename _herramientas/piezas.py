NEG, NOCHE, AZ, CEL, HIELO = '#03040A', '#070B2E', '#1730F5', '#6FA0FF', '#DCE6FF'
AR = "font-family: 'Bricolage Grotesque', sans-serif"; IN = "font-family: 'Manrope', sans-serif"; MO = "font-family: 'Manrope', sans-serif; font-weight: 800"
def bianca(s, fondo=True, cuerpo=False):
    """Bianca: caniche micro toy blanca, hembra, cola corta tipo pompón. Dibujo original."""
    st = 'stroke="#B9C8EE" stroke-width="2.2"'
    bg = f'<circle cx="100" cy="100" r="100" fill="{AZ}"></circle>' if fondo else ''
    if not cuerpo:
        return f'''<svg width="{s}" height="{s}" viewBox="0 0 200 200" role="img" aria-label="Bianca, caniche blanca">{bg}
<g {st} fill="#FFFFFF" stroke-linejoin="round">
<ellipse cx="52" cy="112" rx="24" ry="38"></ellipse><ellipse cx="148" cy="112" rx="24" ry="38"></ellipse>
<circle cx="100" cy="112" r="50"></circle>
<circle cx="72" cy="66" r="22"></circle><circle cx="128" cy="66" r="22"></circle><circle cx="100" cy="54" r="27"></circle><circle cx="86" cy="76" r="18"></circle><circle cx="114" cy="76" r="18"></circle>
<ellipse cx="100" cy="132" rx="27" ry="21"></ellipse></g>
<circle cx="100" cy="70" r="24" fill="#FFFFFF"></circle>
<circle cx="80" cy="106" r="7" fill="#0B1030"></circle><circle cx="120" cy="106" r="7" fill="#0B1030"></circle><circle cx="82.5" cy="103.5" r="2.2" fill="#FFFFFF"></circle><circle cx="122.5" cy="103.5" r="2.2" fill="#FFFFFF"></circle>
<path d="M90 122 Q100 116 110 122 Q108 132 100 133 Q92 132 90 122 Z" fill="#0B1030"></path>
<path d="M100 133 V140 M100 140 Q93 147 86 142 M100 140 Q107 147 114 142" fill="none" stroke="#0B1030" stroke-width="2.6" stroke-linecap="round"></path>
<path d="M64 160 Q100 178 136 160" fill="none" stroke="{CEL}" stroke-width="9" stroke-linecap="round"></path><circle cx="100" cy="172" r="7" fill="{HIELO}" stroke="{CEL}" stroke-width="2"></circle></svg>'''
    return f'''<svg width="{s}" height="{s}" viewBox="0 0 200 200" role="img" aria-label="Bianca sentada">{bg}
<g {st} fill="#FFFFFF" stroke-linejoin="round">
<circle cx="150" cy="150" r="13"></circle>
<ellipse cx="108" cy="140" rx="42" ry="36"></ellipse>
<circle cx="84" cy="120" r="26"></circle>
<rect x="66" y="140" width="20" height="40" rx="10"></rect><rect x="92" y="144" width="20" height="36" rx="10"></rect>
<ellipse cx="76" cy="182" rx="15" ry="9"></ellipse><ellipse cx="102" cy="182" rx="15" ry="9"></ellipse><ellipse cx="132" cy="178" rx="20" ry="11"></ellipse>
<ellipse cx="50" cy="78" rx="14" ry="26"></ellipse><ellipse cx="116" cy="78" rx="14" ry="26"></ellipse>
<circle cx="83" cy="78" r="33"></circle>
<circle cx="66" cy="46" r="15"></circle><circle cx="100" cy="46" r="15"></circle><circle cx="83" cy="38" r="19"></circle>
<ellipse cx="83" cy="92" rx="18" ry="14"></ellipse></g>
<circle cx="83" cy="50" r="17" fill="#FFFFFF"></circle>
<circle cx="70" cy="74" r="5" fill="#0B1030"></circle><circle cx="96" cy="74" r="5" fill="#0B1030"></circle>
<path d="M77 85 Q83 81 89 85 Q88 92 83 92.500 Q78 92 77 85 Z" fill="#0B1030"></path>
<path d="M83 93 V97 M83 97 Q78 102 74 98 M83 97 Q88 102 92 98" fill="none" stroke="#0B1030" stroke-width="2" stroke-linecap="round"></path>
<path d="M60 108 Q83 120 106 108" fill="none" stroke="{CEL}" stroke-width="7" stroke-linecap="round"></path></svg>'''
def marco(s, inner, bg=AZ, r=0.24):
    return f'<div style="width: {s}px; height: {s}px; border-radius: {s*r}px; background: {bg}; display: flex; align-items: center; justify-content: center; flex-shrink: 0">{inner}</div>'
def logoA(s, bg=AZ, fg='#FFFFFF', ac=CEL):   # F con punto
    return marco(s, f'<div style="{AR}; font-weight: 900; font-size: {s*0.74}px; line-height: 1; color: {fg}; letter-spacing: -0.04em">F<span style="color: {ac}">.</span></div>', bg)
def logoB(s, bg=AZ, fg='#FFFFFF', ac=CEL):   # FL
    return marco(s, f'<div style="{AR}; font-weight: 900; font-size: {s*0.6}px; line-height: 1; color: {fg}; letter-spacing: -0.06em">F<span style="color: {ac}">L</span></div>', bg)
def logoC(s, bg=AZ, fg='#FFFFFF', ac=CEL):   # F geométrica de barras
    return marco(s, f'<svg width="{s*0.62}" height="{s*0.62}" viewBox="0 0 100 100" role="img" aria-label="Letra F"><rect x="20" y="12" width="20" height="76" fill="{fg}"></rect><rect x="20" y="12" width="62" height="20" fill="{fg}"></rect><rect x="20" y="44" width="42" height="18" fill="{fg}"></rect><rect x="68" y="44" width="14" height="18" fill="{ac}"></rect></svg>', bg)
def palabra(size, fg='#FFFFFF', ac=CEL):
    return f'<div style="{AR}; font-weight: 800; font-size: {size}px; line-height: 0.98; letter-spacing: -0.03em; color: {fg}">Finanzas<br><span style="font-weight: 500; color: {ac}">con</span> Lucas</div>'
def bloque(icon, size, fg='#FFFFFF', ac=CEL):
    return f'<div style="display: flex; align-items: center; gap: {size*0.55}px">{icon}{palabra(size, fg, ac)}</div>'
def pie(icon, size, fg='#FFFFFF', ac=CEL):
    return f'<div style="display: flex; align-items: center; gap: {size*0.6}px">{icon}<div style="display: flex; flex-direction: column; gap: 2px"><div style="{AR}; font-weight: 800; font-size: {size}px; letter-spacing: -0.02em; line-height: 1.05; color: {fg}">Finanzas con Lucas</div><div style="{MO}; font-weight: 500; font-size: {size*0.5}px; letter-spacing: 0.06em; color: {ac}">@LUCASBERGIA.FIN</div></div></div>'
GRANO = '<svg aria-hidden="true" width="100%" height="100%" style="position: absolute; inset: 0; opacity: 0.38; mix-blend-mode: overlay; pointer-events: none"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"></feTurbulence><feColorMatrix type="saturate" values="0"></feColorMatrix></filter><rect width="100%" height="100%" filter="url(#g)"></rect></svg>'
def fondo(w, h, inner, extra=''):
    return f'<div class="fcl-bg" style="position: relative; width: {w}; height: {h}; overflow: hidden; box-sizing: border-box; {extra}">{GRANO}<div style="position: relative; width: 100%; height: 100%; box-sizing: border-box">{inner}</div></div>'
HELMET = '''<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
body{margin:0}
a{color:#6FA0FF}a:hover{color:#DCE6FF}
.fcl-bg{background-color:#03040A;background-image:radial-gradient(60% 55% at 78% 30%,rgba(23,48,245,.95),rgba(23,48,245,0) 70%),radial-gradient(55% 60% at 18% 85%,rgba(18,36,200,.85),rgba(18,36,200,0) 70%),radial-gradient(40% 40% at 50% 55%,rgba(111,160,255,.22),rgba(111,160,255,0) 70%);background-size:160% 160%;animation:fclmov 18s ease-in-out infinite alternate}
@keyframes fclmov{0%{background-position:0% 0%}100%{background-position:100% 60%}}
@media (prefers-reduced-motion: reduce){.fcl-bg{animation:none}}
</style>'''

def logoD(s, bg=AZ, fg='#FFFFFF', ac=CEL):   # globo de diálogo con f
    return f'<svg width="{s}" height="{s}" viewBox="0 0 120 120" role="img" aria-label="Globo de diálogo con la letra f"><path d="M26 10 H94 A20 20 0 0 1 114 30 V70 A20 20 0 0 1 94 90 H58 L32 112 V90 H26 A20 20 0 0 1 6 70 V30 A20 20 0 0 1 26 10 Z" fill="{bg}"></path><text x="60" y="74" text-anchor="middle" font-family="Bricolage Grotesque, sans-serif" font-weight="800" font-size="72" fill="{fg}">f</text><circle cx="86" cy="68" r="6.500" fill="{ac}"></circle></svg>'
def logoE(s, bg=AZ, fg='#FFFFFF', ac=CEL):   # L que es el eje de un gráfico
    return marco(s, f'<svg width="{s*0.66}" height="{s*0.66}" viewBox="0 0 100 100" role="img" aria-label="Letra L con una línea de gráfico que sube"><path d="M20 10 V80 H90" fill="none" stroke="{fg}" stroke-width="17" stroke-linecap="square" stroke-linejoin="miter"></path><path d="M44 58 L60 42 L70 50 L90 24" fill="none" stroke="{ac}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"></path><circle cx="90" cy="24" r="8" fill="{ac}"></circle></svg>', bg)
def logoG(size, fg='#FFFFFF', ac=CEL, pill=AZ, pfg='#FFFFFF'):   # logotipo en una línea con "con" en pastilla
    return f'<div style="display: inline-flex; align-items: center; gap: {size*0.2}px; {AR}; font-weight: 800; font-size: {size}px; letter-spacing: -0.03em; line-height: 1; color: {fg}">finanzas<span style="font-size: {size*0.5}px; font-weight: 700; letter-spacing: 0; background: {pill}; color: {pfg}; padding: {size*0.14}px {size*0.26}px; border-radius: {size}px">con</span>lucas</div>'

def sello_bianca(s, fondo_c=AZ, globo='#FFFFFF', signo=AZ):
    """Sello de la sección de preguntas: la cara de Bianca con un globo de pregunta."""
    g = s*0.44
    cara = bianca(s) if fondo_c == AZ else bianca(s).replace(f'fill="{AZ}"></circle>', f'fill="{fondo_c}"></circle>', 1)
    return f'<div style="position: relative; width: {s*1.16}px; height: {s*1.08}px; flex-shrink: 0"><div style="position: absolute; left: 0; bottom: 0">{cara}</div><svg style="position: absolute; right: 0; top: 0" width="{g}" height="{g}" viewBox="0 0 100 100" role="img" aria-label="Pregunta"><path d="M22 6 H78 A18 18 0 0 1 96 24 V56 A18 18 0 0 1 78 74 H44 L20 94 V74 A18 18 0 0 1 4 56 V24 A18 18 0 0 1 22 6 Z" fill="{globo}" stroke="{NOCHE}" stroke-width="5"></path><text x="50" y="60" text-anchor="middle" font-family="Bricolage Grotesque, sans-serif" font-weight="800" font-size="56" fill="{signo}">?</text></svg></div>'
def bianca_pregunta(s, fg='#FFFFFF', ac=CEL):
    return f'<div style="display: flex; align-items: center; gap: {s*0.22}px">{sello_bianca(s)}<div style="{AR}; font-weight: 800; font-size: {s*0.42}px; line-height: 0.98; letter-spacing: -0.03em; color: {fg}">Bianca<br><span style="color: {ac}">pregunta</span></div></div>'
