"""Datos vivos compartidos: tasas de referencia de hoy (plazo fijo y money market) e inflación de INDEC.
Se insertan en las páginas para que los valores por defecto se actualicen solos en cada visita."""
import re

TASAS_JS = r'''
/* Tasas de referencia de hoy: mediana de plazos fijos (tasa para clientes) y de fondos money market con más de $1.000 millones */
async function fclTasasHoy() {
  const B = 'https://api.argentinadatos.com/v1/finanzas/', get = async (u) => { const k = 'fcl:' + u; let g = null; try { g = JSON.parse(localStorage.getItem(k) || 'null'); } catch (e) {}
    if (g && Date.now() - g.t < 6 * 3600e3) return g.d; try { const r = await fetch(u); if (!r.ok) throw 0; const d = await r.json(); try { localStorage.setItem(k, JSON.stringify({ t: Date.now(), d })); } catch (e) {} return d; } catch (e) { if (g) return g.d; throw e; } };
  const [pf, u, p] = await Promise.all([get(B + 'tasas/plazoFijo'), get(B + 'fci/mercadoDinero/ultimo'), get(B + 'fci/mercadoDinero/penultimo')]);
  const med = a => { const s = a.slice().sort((x, y) => x - y); return s.length ? s[Math.floor(s.length / 2)] : NaN; };
  const dia = s => Date.UTC(+s.slice(0, 4), +s.slice(5, 7) - 1, +s.slice(8, 10)), prev = new Map(p.map(x => [x.fondo, x])), mm = []; let fecha = null;
  u.forEach(x => { const y = prev.get(x.fondo); if (!y || !x.vcp || !y.vcp || !(x.patrimonio >= 1e9)) return; const d = (dia(x.fecha) - dia(y.fecha)) / 864e5; if (d < 1 || d > 7) return; const t = (x.vcp / y.vcp - 1) * 365 / d; if (t > 0 && t < 2) { mm.push(t); fecha = x.fecha; } });
  const pfs = pf.map(x => x.tnaClientes).filter(t => t > 0);
  return { pf: med(pfs), pfMax: Math.max(...pfs), mm: med(mm), mmMax: Math.max(...mm), nPf: pfs.length, nMm: mm.length, fecha };
}
async function fclInflacionHoy() {
  const u = 'https://api.argentinadatos.com/v1/finanzas/indices/inflacion', r = await fetch(u); const d = await r.json(); const ult = d.slice(-12);
  return { mensual: ult[11].valor / 100, anual: ult.reduce((a, x) => a * (1 + x.valor / 100), 1) - 1, fecha: ult[11].fecha };
}
'''

def cuotas(ruta):
    """Cuotas vs contado: inflación de INDEC y tasas de hoy como valores iniciales."""
    s = open(ruta, encoding='utf-8').read()
    s = re.sub(r'\n?/\*fcl-vivo\*/.*?/\*/fcl-vivo\*/', '', s, flags=re.S)
    s = s.replace('<p class="hint">Dato de referencia:', '<p class="hint" id="hintInf">Dato de referencia:', 1)
    vivo = TASAS_JS + r'''
  var tocado = { tna: false, inflacion: false }; els.tna.addEventListener('input', function () { tocado.tna = true; }); els.inflacion.addEventListener('input', function () { tocado.inflacion = true; });
  var MESES_V = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'];
  fclInflacionHoy().then(function (x) { var m = MESES_V[+x.fecha.slice(5, 7) - 1] + ' ' + x.fecha.slice(0, 4);
    document.getElementById('hintInf').innerHTML = 'Último dato de INDEC (' + m + '): <strong class="num">' + pct(x.mensual * 100, 1) + '</strong> mensual (' + pct(x.anual * 100, 1) + ' en los últimos 12 meses). Se actualiza solo; podés cambiarlo por tu propia proyección.';
    if (!tocado.inflacion) { els.inflacion.value = (Math.round(x.mensual * 1000) / 10).toFixed(1); render(); } }).catch(function () {});
  fclTasasHoy().then(function (t) { var r = function (v) { return Math.round(v * 100); };
    if (isFinite(t.mm)) { DEFAULT_TNA.fci = r(t.mm); CHIPS.fci = [r(t.mm) - 6, r(t.mm) - 3, r(t.mm), r(t.mmMax)].filter(function (v, i, a) { return v > 0 && a.indexOf(v) === i; }); }
    if (isFinite(t.pf)) { DEFAULT_TNA.pf = r(t.pf); CHIPS.pf = [r(t.pf) - 3, r(t.pf), r(t.pfMax)].filter(function (v, i, a) { return v > 0 && a.indexOf(v) === i; }); }
    if (!tocado.tna) els.tna.value = DEFAULT_TNA[state.instrumento]; renderChips(); render(); }).catch(function () {});
'''
    s = s.replace('  renderChips();\n  render();\n})();', '/*fcl-vivo*/' + vivo + '/*/fcl-vivo*/\n  renderChips();\n  render();\n})();', 1)
    open(ruta, 'w', encoding='utf-8').write(s)

if __name__ == '__main__':
    cuotas('/home/claude/finanzas-con-lucas/cuotas-vs-contado/index.html'); print('ok')
