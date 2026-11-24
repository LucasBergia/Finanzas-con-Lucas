import sys, asyncio
sys.path.insert(0,'/home/claude/marca2'); sys.path.insert(0,'/home/claude/apps')
from piezas import HELMET, GRANO
from marca_apps import APPS, MARK, icono, REPO
from playwright.async_api import async_playwright
def pag(c, a):
    ic = icono(a['icono'], 54) if a.get('icono') else MARK(60)
    sub = 'Calculadora gratuita' if c else 'Calculadoras gratuitas'
    return f'''<!DOCTYPE html><html><head><meta charset="utf-8">{HELMET}<style>body{{width:1200px;height:630px;overflow:hidden}}
.fcl-bg{{animation:none!important}}</style></head><body><div class="fcl-bg" style="position:relative;width:1200px;height:630px;overflow:hidden">{GRANO}
<div style="position:relative;height:100%;box-sizing:border-box;padding:64px 72px;display:flex;flex-direction:column;justify-content:space-between;color:#fff">
<div style="display:flex;align-items:center;gap:18px"><div style="width:68px;height:68px;border-radius:17px;background:#1730F5;display:flex;align-items:center;justify-content:center">{MARK(44)}</div>
<div style="font:800 34px/1 'Bricolage Grotesque';letter-spacing:-.02em">Finanzas <span style="font-weight:500;color:#6FA0FF">con</span> Lucas</div></div>
<div><div style="display:flex;align-items:center;gap:16px;margin-bottom:22px"><div style="width:84px;height:84px;border-radius:20px;background:rgba(23,48,245,.9);border:2px solid rgba(111,160,255,.6);display:flex;align-items:center;justify-content:center">{ic}</div>
<div style="font:800 17px 'Manrope';letter-spacing:.16em;text-transform:uppercase;color:#6FA0FF">{sub}</div></div>
<div style="font:800 76px/1.02 'Bricolage Grotesque';letter-spacing:-.035em;max-width:1000px">{a['og']}</div></div>
<div style="display:flex;justify-content:space-between;align-items:center;font:700 20px 'Manrope';color:#DCE6FF"><span>Hacé la cuenta con tus números</span><span style="color:#6FA0FF">@LucasBergia.Fin</span></div>
</div></div></body></html>'''
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width':1200,'height':630})
        for c, a in APPS.items():
            await pg.set_content(pag(c, a)); await pg.wait_for_timeout(1200)
            out = f'{REPO}/{c + "/" if c else ""}og.png'; await pg.screenshot(path=out); print(out)
        await b.close()
asyncio.run(main())
