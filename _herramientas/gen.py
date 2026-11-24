import re, os, sys
sys.path.insert(0, '/home/claude/apps')
from contacto import CSS_C, bloque as contacto_bloque
REPO = '/home/claude/finanzas-con-lucas'
MARK = '<svg viewBox="0 0 100 100" width="26" height="26" role="img" aria-label="Finanzas con Lucas"><path d="M20 10 V80 H90" fill="none" stroke="#FFFFFF" stroke-width="17" stroke-linecap="square"/><path d="M44 58 L60 42 L70 50 L90 24" fill="none" stroke="#6FA0FF" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/><circle cx="90" cy="24" r="8" fill="#6FA0FF"/></svg>'
hub = open(REPO + '/index.html', encoding='utf-8').read()
FAV = re.search(r'<link rel="icon"[^>]+>', hub).group(0)
IG = re.search(r'<a class="ig-pill".*?</a>', hub, re.S).group(0)
CSS = '''
:root{--bg:#F3F6FF;--surface:#FFFFFF;--surface-2:#E8EEFF;--border:#D3DCF7;--text:#070B2E;--muted:#4B5680;--primary:#1730F5;--accent:#1730F5;--soft:#E1E8FF;--ok:#12804A;--ok-soft:#E1F5EA;--bad:#B23A3A;--bad-soft:#FAE7E7;--shadow:rgba(7,11,46,.10);--ig-grad:linear-gradient(135deg,#4f5bd5,#962fbf,#d62976,#fa7e1e,#feda75)}
@media (prefers-color-scheme:dark){:root{--bg:#03040A;--surface:#0A0F33;--surface-2:#101746;--border:#23307A;--text:#FFFFFF;--muted:#A9B6DA;--accent:#6FA0FF;--soft:#111B55;--ok:#3ED28D;--ok-soft:#0F3A2C;--bad:#F17272;--bad-soft:#3B1717;--shadow:rgba(0,0,0,.55)}
 body{background-image:radial-gradient(60% 55% at 78% 20%,rgba(23,48,245,.55),rgba(23,48,245,0) 70%),radial-gradient(55% 60% at 12% 90%,rgba(18,36,200,.45),rgba(18,36,200,0) 70%);background-size:160% 160%;background-attachment:fixed;animation:fclmov 18s ease-in-out infinite alternate}}
@keyframes fclmov{0%{background-position:0% 0%}100%{background-position:100% 60%}}
@media (prefers-reduced-motion:reduce){body{animation:none!important}}
*{box-sizing:border-box}
body{margin:0;min-height:100vh;background-color:var(--bg);color:var(--text);font-family:'Manrope',ui-sans-serif,system-ui,sans-serif;-webkit-font-smoothing:antialiased}
h1,h2,h3{font-family:'Bricolage Grotesque',ui-sans-serif,system-ui,sans-serif;margin:0;text-wrap:balance}
a{color:inherit}
header.top{border-bottom:1px solid var(--border);background:var(--surface)}
.top-inner{max-width:1120px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:16px 20px;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:12px;text-decoration:none}
.brand-mark{width:40px;height:40px;border-radius:11px;background:#1730F5;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.brand h1{font-size:18px;font-weight:800}.brand p{margin:2px 0 0;font-size:12.5px;color:var(--muted)}
.ig-pill{display:inline-flex;align-items:center;gap:8px;padding:8px 16px 8px 8px;border-radius:999px;background:var(--surface-2);border:1px solid var(--border);text-decoration:none;font-size:13px;font-weight:600}
.ig-pill .ig-icon{width:26px;height:26px;border-radius:8px;background:var(--ig-grad);display:flex;align-items:center;justify-content:center}.ig-pill .ig-icon svg{width:14px;height:14px}
.ig-pill .ig-label{display:flex;flex-direction:column;line-height:1.2}.ig-pill .ig-label small{font-weight:500;color:var(--muted);font-size:11px}
main{max-width:1120px;margin:0 auto;padding:28px 20px 56px}
.volver{display:inline-block;font-size:13px;font-weight:700;color:var(--accent);text-decoration:none;padding:10px 0;min-height:44px}
.eyebrow{font-size:11.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin-bottom:8px}
main>h2{font-size:30px;font-weight:800;letter-spacing:-.02em;margin-bottom:8px}
.lead{font-size:15px;color:var(--muted);max-width:68ch;line-height:1.6;margin:0 0 24px}
.layout{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);gap:20px;align-items:start}
@media (max-width:860px){.layout{grid-template-columns:1fr}}
.card{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:22px;box-shadow:0 1px 2px var(--shadow)}
.card h3{font-size:16px;font-weight:800;margin-bottom:14px}
label.f{display:block;font-size:13px;font-weight:700;margin:14px 0 6px}
label.f small{display:block;font-weight:500;color:var(--muted);font-size:12px;margin-top:2px}
input[type=text]{width:100%;min-height:46px;padding:10px 14px;border-radius:11px;border:1px solid var(--border);background:var(--surface-2);color:var(--text);font:600 16px 'Manrope',sans-serif;font-variant-numeric:tabular-nums}
input[aria-invalid=true]{border-color:var(--bad)}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.err{margin-top:12px;padding:10px 12px;border-radius:10px;background:var(--bad-soft);color:var(--bad);font-size:13px;font-weight:600}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:16px}
.kpi{background:var(--surface-2);border:1px solid var(--border);border-radius:12px;padding:14px}
.kpi span{display:block;font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.kpi b{display:block;font:800 24px 'Bricolage Grotesque',sans-serif;margin-top:4px;font-variant-numeric:tabular-nums}
.kpi small{display:block;font-size:12px;color:var(--muted);margin-top:3px;line-height:1.4}
.kpi.ok b{color:var(--ok)}.kpi.bad b{color:var(--bad)}
.verd{padding:14px 16px;border-radius:12px;background:var(--soft);font-size:14.5px;line-height:1.55;margin-bottom:16px}
.verd b{font-weight:800}
.scroll{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:13px;font-variant-numeric:tabular-nums}
th{font-size:11px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);text-align:right;padding:8px 6px;border-bottom:1px solid var(--border)}
td{text-align:right;padding:8px 6px;border-bottom:1px solid var(--border)}th:first-child,td:first-child{text-align:left}
.nota{font-size:12px;color:var(--muted);line-height:1.55;margin-top:14px}
footer{border-top:1px solid var(--border);padding:20px;text-align:center;font-size:12px;color:var(--muted)}
'''
JS = '''
const $ = id => document.getElementById(id);
const nf = (v, d) => isFinite(v) ? Number(v).toLocaleString('es-AR', { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 }) : '—';
const plata = v => isFinite(v) ? (v < 0 ? '−$' : '$') + nf(Math.abs(v)) : '—';
const pc = (v, d) => isFinite(v) ? nf(v * 100, d == null ? 1 : d) + '%' : '—';
/* Acepta 1.000.000 · 1000000 · 21,5 · 21.5 */
function num(str) { let s = String(str == null ? '' : str).trim().replace(/[\\s$%]/g, ''); if (!s) return NaN;
  const c = s.lastIndexOf(','), p = s.lastIndexOf('.');
  if (c >= 0 && p >= 0) s = c > p ? s.replace(/\\./g, '').replace(',', '.') : s.replace(/,/g, '');
  else if (c >= 0) s = (s.match(/,/g).length > 1) ? s.replace(/,/g, '') : s.replace(',', '.');
  else if (p >= 0 && /^-?\\d{1,3}(\\.\\d{3})+$/.test(s)) s = s.replace(/\\./g, '');
  return /^-?\\d*\\.?\\d+$/.test(s) ? parseFloat(s) : NaN; }
function errores(lista) { const e = $('err'); e.hidden = !lista.length; e.textContent = lista.join(' '); }
function marcar(id, mal) { mal ? $(id).setAttribute('aria-invalid', 'true') : $(id).removeAttribute('aria-invalid'); }
'''
def pagina(carpeta, titulo, sub, desc, lead, form, salida, js, tipo='inv'):
    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<title>{titulo} · Finanzas con Lucas</title>
{FAV}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}{CSS_C}</style>
</head>
<body>
<header class="top"><div class="top-inner">
  <a class="brand" href="../"><div class="brand-mark">{MARK}</div><div><h1>{titulo}</h1><p>{sub}</p></div></a>
  {IG}
</div></header>
<main>
  <a class="volver" href="../">← Todas las herramientas</a>
  <div class="eyebrow">Calculadora</div>
  <h2>{titulo}</h2>
  <p class="lead">{lead}</p>
  <div class="layout">
    <div class="card"><h3>Tus datos</h3>{form}<div id="err" class="err" role="alert" hidden></div></div>
    <div class="card"><h3>Resultado</h3>{salida}</div>
  </div>
  {contacto_bloque(titulo, tipo)}
</main>
<footer>Finanzas con Lucas · @LucasBergia.Fin · Herramienta educativa: no es una recomendación de inversión ni reemplaza el asesoramiento profesional.</footer>
<script>{JS}{js}</script>
</body>
</html>
'''
    os.makedirs(f'{REPO}/{carpeta}', exist_ok=True); open(f'{REPO}/{carpeta}/index.html', 'w', encoding='utf-8').write(html)
def campo(id, etiqueta, valor, ayuda='', modo='decimal'):
    return f'<label class="f" for="{id}">{etiqueta}{"<small>" + ayuda + "</small>" if ayuda else ""}</label><input id="{id}" type="text" inputmode="{modo}" autocomplete="off" value="{valor}">'

# ───────── 1 · Pago mínimo de la tarjeta ─────────
pagina('pago-minimo-tarjeta', 'Pago mínimo de la tarjeta', 'Cuánto cuesta financiar el saldo', 'Calculá cuánto terminás pagando y en cuántos meses si pagás sólo el mínimo de la tarjeta.',
 'Pagar el mínimo evita la mora, pero el resto del saldo sigue generando intereses. Esta calculadora muestra cuánto terminás pagando y cuánto tardás, y lo compara con pagar una cuota fija.',
 campo('saldo', 'Saldo del resumen', '500.000') + campo('tna', 'Tasa de financiación (TNA %)', '85', 'Figura en el resumen como tasa nominal anual de financiación') + campo('min', 'Pago mínimo (% del saldo)', '10', 'Cada banco lo calcula a su manera; revisá tu resumen') + campo('piso', 'Pago mínimo en pesos', '10.000', 'Lo menos que se paga por mes mientras quede saldo') + campo('fijo', 'Si en cambio pagás un monto fijo por mes', '80.000') + campo('iva', 'IVA sobre los intereses (%)', '21'),
 '<div class="kpis" id="k"></div><div class="verd" id="v"></div><div class="scroll"><table><thead><tr><th>Mes</th><th>Interés + IVA</th><th>Pago</th><th>Saldo</th></tr></thead><tbody id="t"></tbody></table></div><div class="nota">Supuestos: no hacés compras nuevas, el interés mensual es la TNA dividida 12 y el IVA se aplica sobre el interés. El cálculo real del banco puede incluir otros cargos (seguro, sellos, mantenimiento).</div>',
 r'''
function simular(saldo, tna, minPct, piso, iva, fijo) {
  const i = tna / 12, filas = []; let s = saldo, pagado = 0, cargos = 0, m = 0;
  while (s > 0.5 && m < 600) { m++;
    const cargo = s * i * (1 + iva), deuda = s + cargo;
    let pago = fijo != null ? fijo : Math.max(deuda * minPct, piso); pago = Math.min(pago, deuda);
    if (pago <= cargo && deuda > pago) { return { nunca: true, mes: m, filas, pagado, cargos }; }
    s = deuda - pago; pagado += pago; cargos += cargo; filas.push({ m, cargo, pago, saldo: s });
  }
  return { meses: m, pagado, cargos, filas, tope: s > 0.5 };
}
function calc() {
  const saldo = num($('saldo').value), tna = num($('tna').value) / 100, mn = num($('min').value) / 100, piso = num($('piso').value), fijo = num($('fijo').value), iva = num($('iva').value) / 100, e = [];
  marcar('saldo', !(saldo > 0)); marcar('tna', !(tna >= 0 && tna <= 10)); marcar('min', !(mn > 0 && mn <= 1)); marcar('piso', !(piso >= 0)); marcar('fijo', !(fijo > 0)); marcar('iva', !(iva >= 0 && iva <= 1));
  if (!(saldo > 0)) e.push('Ingresá el saldo del resumen.'); if (!(tna >= 0 && tna <= 10)) e.push('La tasa va en porcentaje anual, por ejemplo 85.'); if (!(mn > 0 && mn <= 1)) e.push('El pago mínimo va entre 1 y 100%.'); if (!(piso >= 0)) e.push('Revisá el pago mínimo en pesos.'); if (!(fijo > 0)) e.push('Ingresá el monto fijo.'); if (!(iva >= 0 && iva <= 1)) e.push('El IVA va entre 0 y 100%.');
  errores(e); if (e.length) { $('k').innerHTML = ''; $('v').textContent = 'Completá los datos para ver el resultado.'; $('t').innerHTML = ''; return; }
  const a = simular(saldo, tna, mn, piso, iva, null), b = simular(saldo, tna, mn, piso, iva, fijo);
  const txt = r => r.nunca ? 'No se cancela' : r.tope ? 'Más de 50 años' : r.meses + (r.meses === 1 ? ' mes' : ' meses');
  $('k').innerHTML = `<div class="kpi bad"><span>Pagando el mínimo</span><b>${txt(a)}</b><small>Total pagado: ${a.nunca ? '—' : plata(a.pagado)}</small></div>
    <div class="kpi bad"><span>Intereses e IVA con el mínimo</span><b>${a.nunca ? '—' : plata(a.cargos)}</b><small>${a.nunca ? '' : pc(a.cargos / saldo, 0) + ' del saldo original'}</small></div>
    <div class="kpi ok"><span>Pagando ${plata(fijo)} fijos</span><b>${txt(b)}</b><small>Total pagado: ${b.nunca ? '—' : plata(b.pagado)}</small></div>`;
  $('v').innerHTML = a.nunca ? 'Con estos datos el pago mínimo no alcanza a cubrir los intereses: la deuda crece todos los meses.' : b.nunca ? `El monto fijo de ${plata(fijo)} no alcanza a cubrir los intereses del primer mes (${plata(saldo * tna / 12 * (1 + iva))}). Tiene que ser mayor.` :
    `Pagando sólo el mínimo terminás pagando <b>${plata(a.pagado)}</b> por una deuda de ${plata(saldo)}. Con ${plata(fijo)} fijos por mes pagás <b>${plata(b.pagado)}</b>: ${a.pagado > b.pagado ? 'ahorrás <b>' + plata(a.pagado - b.pagado) + '</b>' : 'pagás ' + plata(b.pagado - a.pagado) + ' más'} y terminás ${a.meses > b.meses ? (a.meses - b.meses) + ' meses antes' : 'en un plazo similar'}.`;
  const f = a.filas; const ver = f.length > 14 ? f.slice(0, 12).concat([null], f.slice(-1)) : f;
  $('t').innerHTML = ver.map(r => r ? `<tr><td>${r.m}</td><td>${plata(r.cargo)}</td><td>${plata(r.pago)}</td><td>${plata(r.saldo)}</td></tr>` : '<tr><td colspan="4" style="text-align:center">…</td></tr>').join('');
}
document.querySelectorAll('input').forEach(i => i.addEventListener('input', calc)); calc();
''', 'gas')

# ───────── 2 · Meta de ahorro ─────────
pagina('meta-de-ahorro', 'Meta de ahorro', 'Cuánto apartar por mes', 'Calculá cuánto tenés que ahorrar por mes para llegar a un objetivo, con y sin rendimiento.',
 'Poné cuánto necesitás y para cuándo. La calculadora te dice cuánto apartar por mes si la plata queda quieta y cuánto si la vas invirtiendo a una tasa.',
 campo('obj', 'Cuánto necesitás juntar', '3.000.000', 'En pesos de hoy') + campo('mes', 'En cuántos meses', '12', '', 'numeric') + campo('ini', 'Cuánto tenés ahorrado hoy', '0') + campo('tna', 'Rendimiento de tus ahorros (TNA %)', '25', 'Arranca con lo que pagan hoy los fondos money market (el valor del medio). Poné 0 si no la invertís') + campo('inf', 'Inflación mensual esperada (%)', '0', 'Opcional: si lo que querés comprar sube de precio, la meta sube con la inflación'),
 '<div class="kpis" id="k"></div><div class="verd" id="v"></div><div class="scroll"><table><thead><tr><th>Mes</th><th>Aporte</th><th>Rendimiento</th><th>Acumulado</th></tr></thead><tbody id="t"></tbody></table></div><div class="nota">Supuestos: aportás a fin de cada mes y el rendimiento mensual es la TNA dividida 12, constante. Las tasas reales cambian: conviene revisar el plan cada tanto.</div>',
 r'''
function cuota(meta, n, ini, i) { const fv = ini * Math.pow(1 + i, n); return i > 0 ? (meta - fv) * i / (Math.pow(1 + i, n) - 1) : (meta - ini) / n; }
function calc() {
  const obj = num($('obj').value), n = num($('mes').value), ini = num($('ini').value), tna = num($('tna').value) / 100, inf = num($('inf').value) / 100, e = [];
  marcar('obj', !(obj > 0)); marcar('mes', !(Number.isInteger(n) && n >= 1 && n <= 600)); marcar('ini', !(ini >= 0)); marcar('tna', !(tna >= 0 && tna <= 10)); marcar('inf', !(inf >= 0 && inf <= 0.5));
  if (!(obj > 0)) e.push('Ingresá cuánto necesitás juntar.'); if (!(Number.isInteger(n) && n >= 1 && n <= 600)) e.push('Los meses van en números enteros, de 1 a 600.'); if (!(ini >= 0)) e.push('Revisá lo que tenés ahorrado.'); if (!(tna >= 0 && tna <= 10)) e.push('La tasa va en porcentaje anual, por ejemplo 25.'); if (!(inf >= 0 && inf <= 0.5)) e.push('La inflación mensual va entre 0 y 50%.');
  errores(e); if (e.length) { $('k').innerHTML = ''; $('v').textContent = 'Completá los datos para ver el resultado.'; $('t').innerHTML = ''; return; }
  const meta = obj * Math.pow(1 + inf, n), i = tna / 12, sin = cuota(meta, n, ini, 0), con = cuota(meta, n, ini, i);
  if (con <= 0) { $('k').innerHTML = ''; $('v').innerHTML = `Con lo que ya tenés ahorrado y ese rendimiento llegás a la meta sin aportar más: en ${n} meses tendrías <b>${plata(ini * Math.pow(1 + i, n))}</b>.`; $('t').innerHTML = ''; return; }
  $('k').innerHTML = `<div class="kpi ok"><span>Invirtiendo los ahorros</span><b>${plata(con)}</b><small>por mes, a ${pc(tna, 1)} anual</small></div>
    <div class="kpi"><span>Sin invertir</span><b>${plata(Math.max(sin, 0))}</b><small>por mes, con la plata quieta</small></div>
    <div class="kpi"><span>Meta al final</span><b>${plata(meta)}</b><small>${inf > 0 ? 'ajustada por inflación de ' + pc(inf, 1) + ' mensual' : 'sin ajuste por inflación'}</small></div>`;
  $('v').innerHTML = `Para juntar <b>${plata(meta)}</b> en ${n} meses tenés que apartar <b>${plata(con)}</b> por mes. El rendimiento aporta <b>${plata(meta - ini - con * n)}</b>: son ${plata(Math.max(sin, 0) - con)} menos por mes que guardando la plata sin invertir.`;
  let ac = ini, f = []; for (let m = 1; m <= n; m++) { const r = ac * i; ac += r + con; f.push([m, con, r, ac]); }
  const ver = f.length > 14 ? f.slice(0, 12).concat([null], f.slice(-1)) : f;
  $('t').innerHTML = ver.map(r => r ? `<tr><td>${r[0]}</td><td>${plata(r[1])}</td><td>${plata(r[2])}</td><td>${plata(r[3])}</td></tr>` : '<tr><td colspan="4" style="text-align:center">…</td></tr>').join('');
}
document.querySelectorAll('input').forEach(i => i.addEventListener('input', calc)); calc();
/* Rendimiento inicial: la mediana de los fondos money market de hoy (se actualiza sola) */
let tnaTocada = false; $('tna').addEventListener('input', () => tnaTocada = true);
''' + __import__('vivo').TASAS_JS + r'''
fclTasasHoy().then(t => { if (!tnaTocada && isFinite(t.mm)) { $('tna').value = String(Math.round(t.mm * 100)); calc(); } }).catch(() => {});
''')

# ───────── 3 · Préstamo: cuota fija o UVA ─────────
CSS_P = '<style>.layout>div{min-width:0}.kpis{grid-template-columns:repeat(auto-fit,minmax(190px,1fr))}.kpi b{font-size:21px;white-space:nowrap}.seg3{display:flex;gap:6px;flex-wrap:wrap;margin-top:6px}.seg3 button{min-height:44px;padding:8px 14px;border-radius:10px;border:1px solid var(--border);background:var(--surface-2);color:var(--text);font:700 13px Manrope,sans-serif;cursor:pointer;text-align:left}.seg3 button small{display:block;font-weight:500;font-size:11.5px;color:var(--muted)}.seg3 button[aria-pressed=true]{background:#1730F5;border-color:#1730F5;color:#fff}.seg3 button[aria-pressed=true] small{color:#DCE6FF}.sub{font:800 12px Manrope,sans-serif;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);margin:22px 0 0;padding-top:16px;border-top:1px solid var(--border)}.dos{display:grid;grid-template-columns:1fr 1fr;gap:0 12px}@media (max-width:420px){.dos{grid-template-columns:1fr}}.pedi{margin-top:12px;padding:12px 14px;border-radius:12px;background:var(--soft);font-size:13.5px;line-height:1.5}.pedi b{font-weight:800}.aviso{margin-bottom:16px;padding:12px 14px;border-radius:12px;background:var(--bad-soft);color:var(--bad);font-size:13.5px;font-weight:600;line-height:1.5}.dato{margin-top:10px;font-size:13.5px;line-height:1.55;color:var(--text)}.dato b{font-weight:800}.dato small{display:block;color:var(--muted);font-size:12px;margin-top:4px}.tit{font:800 20px "Bricolage Grotesque",sans-serif;line-height:1.2;margin-bottom:6px}.tit.ok{color:var(--ok)}details.mes{margin-top:16px}details.mes summary{cursor:pointer;font-weight:700;font-size:13.5px;color:var(--accent);min-height:44px;display:flex;align-items:center}td.g,th.g{text-align:left}</style>'
pagina('prestamo-fijo-vs-uva', 'Préstamo: cuota fija o UVA', 'Cuál te conviene con la inflación esperada', 'Compará un préstamo a cuota fija con uno UVA usando el CFT del banco y la inflación de INDEC.',
 'Cargá el monto, el plazo y el costo que te informó el banco. La inflación no hay que adivinarla: la calculadora toma el último dato de INDEC y lo que espera el mercado, y te dice cuál de los dos préstamos te conviene.',
 CSS_P + '<div class="sub" style="margin-top:0;padding-top:0;border-top:0">¿Para qué es el préstamo?</div><div class="seg3" role="group" aria-label="Tipo de préstamo"><button type="button" data-tipo="auto" aria-pressed="true">Auto</button><button type="button" data-tipo="moto" aria-pressed="false">Moto</button><button type="button" data-tipo="casa" aria-pressed="false">Vivienda</button><button type="button" data-tipo="personal" aria-pressed="false">Personal</button></div><div class="dato" id="tipoNota"></div>' + campo('monto', 'Monto del préstamo', '15.000.000') + campo('n', 'Plazo en meses', '48', '', 'numeric') +
 '<div class="sub">El costo que te informó el banco</div><div class="seg3" role="group" aria-label="Qué dato tenés"><button type="button" data-modo="cft" aria-pressed="true">Tengo el CFT<small>es el dato correcto para comparar</small></button><button type="button" data-modo="tna" aria-pressed="false">Sólo tengo la tasa (TNA)<small>el resultado va a ser aproximado</small></button></div>' +
 '<div class="dos"><div>' + campo('tf', '<span id="lTf">CFT del préstamo a cuota fija (%)</span>', '43') + '</div><div>' + campo('tu', '<span id="lTu">CFT del préstamo UVA (%)</span>', '13', 'Sin contar el ajuste por UVA') + '</div></div>' +
 '<div class="pedi"><b>Pedile siempre el CFT al banco.</b> El Costo Financiero Total (CFT o CFTEA) suma a la tasa el IVA, los seguros y las comisiones. El banco tiene que informártelo antes de firmar, y es el número que sirve para comparar un préstamo con otro. La TNA sola siempre muestra un costo menor al real. </div>' +
 '<div class="sub">Inflación</div><div class="dato" id="infDato">Buscando el último dato de INDEC…</div>',
 '<div class="aviso" id="aviso" hidden></div><div class="verd" id="v"></div><div class="kpis" id="k"></div><h3 style="margin-top:6px">¿Y si la inflación es otra?</h3><div class="scroll"><table><thead><tr><th class="g">Si la inflación…</th><th>Por mes</th><th class="g">Te conviene</th><th>Fija, sobre inflación</th><th>UVA, sobre inflación</th><th>UVA pasa a la fija</th></tr></thead><tbody id="esc"></tbody></table></div><details class="mes"><summary>Ver las cuotas mes a mes</summary><div class="scroll"><table><thead><tr><th>Mes</th><th>Inflación</th><th>Cuota fija</th><th>Cuota UVA</th><th>Diferencia</th></tr></thead><tbody id="t"></tbody></table></div></details><div class="nota" id="nota"></div>',
 r"""
/* Datos de referencia. La inflación mensual se actualiza sola desde la serie de INDEC; estos valores quedan de respaldo.
   La expectativa del mercado (REM) se trae de la API del Banco Central (variable 29); estos valores quedan de respaldo. */
const RESPALDO = { hasta: '2026-10-31', serie: [2.5, 2.8, 2.9, 2.9, 3.4, 2.6, 2.1, 1.9, 2.1, 1.7, 1.9, 2.2] };
let REM = { anual12: 21.8, relevamiento: 'octubre de 2026', enVivo: false };
const MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'];
let INDEC = { mensual: RESPALDO.serie[11] / 100, anual: RESPALDO.serie.reduce((a, v) => a * (1 + v / 100), 1) - 1, mes: 'octubre de 2026', enVivo: false };
const aMensual = anual => Math.pow(1 + anual, 1 / 12) - 1;
const frances = (p, i, n) => i > 0 ? p * i / (1 - Math.pow(1 + i, -n)) : p / n;
/* Pagos en la unidad del préstamo (pesos o UVA). ivaInt sólo se usa cuando falta el CFT. */
function pagos(p, i, n, ivaInt) { const c = frances(p, i, n), out = []; let s = p; for (let m = 1; m <= n; m++) { const int = s * i; out.push(c + int * ivaInt); s -= (c - int); } return out; }
function comparar(p, n, iF, iU, ivaInt, inflMensual) {
  const pf = pagos(p, iF, n, ivaInt), pu = pagos(p, iU, n, ivaInt), filas = []; let idx = 1, hoyF = 0, hoyU = 0, totF = 0, totU = 0, cruce = null;
  for (let m = 0; m < n; m++) { idx *= 1 + inflMensual; const u = pu[m] * idx; hoyF += pf[m] / idx; hoyU += pu[m]; totF += pf[m]; totU += u; if (cruce == null && u > pf[m]) cruce = m + 1; filas.push({ m: m + 1, f: pf[m], u }); }
  /* Se decide por el costo anual por encima de la inflación (lo que de verdad cuesta el préstamo), no por la suma de cuotas */
  const cF = Math.pow(1 + tir(p, pf), 12) - 1, cU = Math.pow(1 + tir(p, pu), 12) - 1, inflAnual = Math.pow(1 + inflMensual, 12) - 1, realF = (1 + cF) / (1 + inflAnual) - 1;
  return { filas, hoyF, hoyU, totF, totU, cruce, cF, cU, realF, conviene: cU < realF ? 'UVA' : 'Cuota fija', dif: Math.abs(hoyF - hoyU), coincide: (cU < realF) === (hoyU < hoyF) };
}
/* Tasa mensual que iguala el monto recibido con las cuotas (bisección) */
function tir(recibido, flujos) { const vp = r => flujos.reduce((s, f, k) => s + f / Math.pow(1 + r, k + 1), 0) - recibido;
  let a = 0, b = 5; if (vp(a) < 0) return 0; for (let k = 0; k < 80; k++) { const m = (a + b) / 2; vp(m) > 0 ? a = m : b = m; } return (a + b) / 2; }
/* Inflación mensual a partir de la cual deja de convenir el UVA (bisección) */
function inflacionDeCorte(p, n, iF, iU, ivaInt) { const r = comparar(p, n, iF, iU, ivaInt, 0), x = (1 + r.cF) / (1 + r.cU) - 1; return x <= 0 ? 0 : x > 20 ? null : aMensual(x); }
let MODO = 'cft';
/* Ejemplos por tipo de préstamo, armados con tasas publicadas en noviembre de 2026. Son un punto de partida: se reemplazan por los del banco. */
const TIPOS = {
  auto: { monto: '15.000.000', n: '48', tf: '43', tu: '13', nota: 'Para autos hay las dos opciones y cambian mucho según el banco y la marca. El ejemplo usa las tasas que publica un banco (fija 29,9% y UVA 9,9% de TNA), llevadas a costo total sumando el IVA. Hay líneas UVA desde 0% hasta 25% y fijas desde 0% hasta 47%.' },
  moto: { monto: '3.000.000', n: '36', tf: '61', tu: '20', nota: 'Para motos casi todo lo que se ofrece es a cuota fija. El costo de la fija es el de una línea de banco público (CFT 60,72%). El del UVA es un valor de ejemplo, porque casi no hay líneas: si te ofrecen una, cargá su CFT.' },
  casa: { monto: '80.000.000', n: '240', tf: '60', tu: '10', nota: 'Para vivienda hoy casi todos los créditos son UVA (CFT cerca de 10%). No vas a encontrar uno a cuota fija en pesos a 20 años: el valor de la fija es un ejemplo, para ver cuánto tendría que costar para competir.' },
  personal: { monto: '5.000.000', n: '36', tf: '78', tu: '10', nota: 'Los préstamos personales son casi todos a cuota fija (el ejemplo usa un CFT de 78%, de una línea para quienes cobran el sueldo en el banco). Personales UVA casi no se ofrecen: el valor del UVA es un ejemplo.' }
};
function ponerTipo(t) { const x = TIPOS[t]; ['monto', 'n', 'tf', 'tu'].forEach(k => $(k).value = x[k]); $('tipoNota').innerHTML = x.nota + '<small>Los números cargados son un ejemplo. Reemplazalos por los que te informe tu banco.</small>';
  document.querySelectorAll('[data-tipo]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.tipo === t)));
  if (MODO !== 'cft') document.querySelector('[data-modo=cft]').click(); else calc(); }
document.querySelectorAll('[data-tipo]').forEach(b => b.addEventListener('click', () => ponerTipo(b.dataset.tipo)));
function pintarInflacion() {
  $('infDato').innerHTML = `Último dato de INDEC (${INDEC.mes}): <b>${pc(INDEC.mensual, 1)}</b> en el mes y <b>${pc(INDEC.anual, 1)}</b> en los últimos 12 meses.<br>Lo que espera el mercado para los próximos 12 meses: <b>${pc(REM.anual12 / 100, 1)}</b>, que equivale a ${pc(aMensual(REM.anual12 / 100), 1)} por mes.<small>${INDEC.enVivo ? 'Dato de INDEC actualizado automáticamente.' : 'No se pudo actualizar el dato de INDEC: se usa el último guardado.'} La expectativa sale del Relevamiento de Expectativas de Mercado del Banco Central (REM) de ${REM.relevamiento}${REM.enVivo ? ', y se actualiza sola cada mes' : ' (último dato guardado)'}. INDEC mide la inflación pasada; no publica proyecciones.</small>`;
}
function calc() {
  const p = num($('monto').value), n = num($('n').value), tf = num($('tf').value) / 100, tu = num($('tu').value) / 100, e = [], cft = MODO === 'cft';
  const v = [['monto', p > 0, 'Ingresá el monto del préstamo.'], ['n', Number.isInteger(n) && n >= 1 && n <= 480, 'El plazo va en meses enteros, de 1 a 480.'], ['tf', tf > 0 && tf <= 20, 'Cargá ' + (cft ? 'el CFT' : 'la tasa') + ' del préstamo a cuota fija, en porcentaje anual.'], ['tu', tu >= 0 && tu <= 5, 'Cargá ' + (cft ? 'el CFT' : 'la tasa') + ' del préstamo UVA, en porcentaje anual.']];
  v.forEach(x => { marcar(x[0], !x[1]); if (!x[1]) e.push(x[2]); });
  errores(e); $('aviso').hidden = cft || e.length > 0;
  if (e.length) { $('k').innerHTML = ''; $('v').textContent = 'Completá los datos para ver el resultado.'; $('t').innerHTML = ''; $('esc').innerHTML = ''; return; }
  /* Con CFT: tasa mensual equivalente al costo anual informado. Con TNA: TNA / 12 más 21% de IVA sobre el interés. */
  const iF = cft ? aMensual(tf) : tf / 12, iU = cft ? aMensual(tu) : tu / 12, iva = cft ? 0 : 0.21;
  if (!cft) $('aviso').textContent = 'Resultado aproximado: con la TNA sólo se puede sumar el IVA sobre los intereses (21%). Faltan seguros y comisiones, que cambian según el banco. Pedí el CFT de los dos préstamos y cargalo para tener la cuenta correcta.';
  const esp = aMensual(REM.anual12 / 100), r = comparar(p, n, iF, iU, iva, esp), f = r.filas;
  const esc = [['es la que espera el mercado', esp], ['sigue como el último mes', INDEC.mensual], ['sigue como el último año', aMensual(INDEC.anual)], ['sube al doble de la esperada', esp * 2], ['llega a 100% anual', aMensual(1)]].map(x => ({ t: x[0], i: x[1], r: comparar(p, n, iF, iU, iva, x[1]) }));
  const corte = inflacionDeCorte(p, n, iF, iU, iva);
  const uva = r.conviene === 'UVA';
  $('v').innerHTML = `<div class="tit ok">Te conviene ${uva ? 'el préstamo UVA' : 'el préstamo a cuota fija'}</div>Con la inflación que espera el mercado (${pc(REM.anual12 / 100, 1)} anual), la cuota fija te cuesta <b>${pc(r.realF, 0)}</b> por año por encima de la inflación y el UVA <b>${pc(r.cU, 0)}</b>. ${uva ? 'El UVA es más barato.' : 'La cuota fija es más barata.'}${r.coincide ? ' Sumando todas las cuotas en pesos de hoy, ' + (uva ? 'con el UVA' : 'con la cuota fija') + ' pagás <b>' + plata(r.dif) + '</b> menos.' : ''}
    ${r.cruce ? ' La cuota UVA arranca más baja, pero desde el mes <b>' + r.cruce + '</b> pasa a ser más alta que la fija.' : ' La cuota UVA queda por debajo de la fija durante todo el plazo.'}
    <br><br>${corte == null ? 'Con estos costos el UVA conviene aunque la inflación sea muy alta.' : corte === 0 ? 'Con estos costos la cuota fija conviene aunque no haya inflación.' : 'El punto de quiebre: la cuota fija pasa a convenir si la inflación promedia más de <b>' + pc(corte, 1) + ' por mes</b> (' + pc(Math.pow(1 + corte, 12) - 1, 0) + ' anual) durante todo el préstamo. El último dato fue ' + pc(INDEC.mensual, 1) + '.'}
    <br><br>Dicho de otra forma: con este UVA y la inflación esperada, la cuota fija recién conviene si su ${cft ? 'CFT' : 'costo anual'} es menor a <b>${pc((1 + r.cU) * (1 + REM.anual12 / 100) - 1, 0)}</b>. El que cargaste ${cft ? 'es' : 'equivale a'} ${pc(r.cF, 0)}.
    <br><br>Tené en cuenta el riesgo del UVA: la cuota sube todos los meses con la inflación. Sirve si tu ingreso también se actualiza.`;
  $('k').innerHTML = `<div class="kpi"><span>Cuota fija</span><b>${plata(f[0].f)}</b><small>${iva ? 'la primera; baja un poco porque baja el IVA' : 'igual los ' + n + ' meses'}</small></div>
    <div class="kpi"><span>Primera cuota UVA</span><b>${plata(f[0].u)}</b><small>${pc(1 - f[0].u / f[0].f, 0)} más baja que la fija</small></div>
    <div class="kpi"><span>Última cuota UVA</span><b>${plata(f[n - 1].u)}</b><small>estimada con la inflación esperada</small></div>
    <div class="kpi"><span>Total en pesos de hoy</span><b>${plata(uva ? r.hoyU : r.hoyF)}</b><small>con ${uva ? 'el UVA' : 'la cuota fija'} · con ${uva ? 'la fija' : 'el UVA'}: ${plata(uva ? r.hoyF : r.hoyU)}</small></div>`;
  $('esc').innerHTML = esc.map(x => `<tr><td class="g">${x.t}</td><td>${pc(x.i, 1)}</td><td class="g"><b>${x.r.conviene}</b></td><td>${pc(x.r.realF, 0)}</td><td>${pc(x.r.cU, 0)}</td><td>${x.r.cruce ? 'mes ' + x.r.cruce : 'nunca'}</td></tr>`).join('');
  const ver = f.length > 14 ? f.slice(0, 12).concat([null], f.slice(-1)) : f;
  $('t').innerHTML = ver.map(x => x ? `<tr><td>${x.m}</td><td>${pc(esp, 1)}</td><td>${plata(x.f)}</td><td>${plata(x.u)}</td><td>${plata(x.u - x.f)}</td></tr>` : '<tr><td colspan="5" style="text-align:center">…</td></tr>').join('');
  $('nota').textContent = 'Cómo se calcula: cuotas por sistema francés. ' + (cft ? 'La tasa de cada mes es la equivalente al CFT anual que cargaste, así la cuota ya incluye IVA, seguros y comisiones.' : 'La tasa mensual es la TNA dividida 12, más 21% de IVA sobre el interés.') + ' La cuota UVA se ajusta todos los meses por la inflación. Para decidir se compara cuánto cuesta cada préstamo por año por encima de la inflación: en la cuota fija es el costo anual menos la inflación; en el UVA es su costo anual tal cual. "En pesos de hoy" descuenta cada cuota por esa misma inflación. La inflación futura no se conoce: por eso la tabla muestra qué pasa en otros casos.';
}
document.querySelectorAll('[data-modo]').forEach(b => b.addEventListener('click', () => { MODO = b.dataset.modo; document.querySelectorAll('[data-modo]').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
  $('lTf').textContent = MODO === 'cft' ? 'CFT del préstamo a cuota fija (%)' : 'Tasa del préstamo a cuota fija (TNA %)'; $('lTu').textContent = MODO === 'cft' ? 'CFT del préstamo UVA (%)' : 'Tasa del préstamo UVA (TNA %)'; calc(); }));
document.querySelectorAll('input').forEach(i => i.addEventListener('input', calc));
pintarInflacion(); ponerTipo('auto');
/* Serie mensual de inflación de INDEC (vía argentinadatos.com). Si falla, queda el dato guardado. */
(async () => { try { const c = new AbortController(); setTimeout(() => c.abort(), 9000);
  const d = await (await fetch('https://api.argentinadatos.com/v1/finanzas/indices/inflacion', { signal: c.signal })).json();
  const ult = d.slice(-12); if (ult.length < 12 || ult.some(x => !(typeof x.valor === 'number' && x.valor > -5 && x.valor < 60))) return;
  const f = ult[11].fecha.split('-'); if (ult[11].fecha < RESPALDO.hasta) return;
  INDEC = { mensual: ult[11].valor / 100, anual: ult.reduce((a, x) => a * (1 + x.valor / 100), 1) - 1, mes: MESES[+f[1] - 1] + ' de ' + f[0], enVivo: true }; pintarInflacion(); calc();
} catch (e) {} })();
/* Expectativa de inflación a 12 meses (mediana del REM), API del Banco Central */
(async () => { try { const c = new AbortController(); setTimeout(() => c.abort(), 9000); const desde = new Date(Date.now() - 200 * 864e5).toISOString().slice(0, 10);
  const j = await (await fetch('https://api.bcra.gob.ar/estadisticas/v4.0/monetarias/29?desde=' + desde + '&limit=20', { signal: c.signal })).json();
  const d = j.results[0].detalle.slice().sort((a, b) => a.fecha < b.fecha ? 1 : -1)[0]; if (!(d && d.valor > 0 && d.valor < 500)) return;
  const f = d.fecha.split('-'); REM = { anual12: d.valor, relevamiento: MESES[+f[1] - 1] + ' de ' + f[0], enVivo: true }; pintarInflacion(); calc();
} catch (e) {} })();
""", 'gas')

# ───────── Página de herramientas ─────────
def tarjeta(href, t, d): return f'''      <a class="tool-card" href="./{href}/">
        <div class="tool-icon">{MARK.replace('width="26" height="26"', 'width="24" height="24"')}</div>
        <div class="tool-info">
          <h3>{t}</h3>
          <p>{d}</p>
        </div>
        <div class="tool-arrow">→</div>
      </a>
'''
if 'pago-minimo-tarjeta' not in hub:
    a = hub.index('      <div class="tool-card soon">'); b = hub.index('</div>', hub.index('Acá va a aparecer')) ; b = hub.index('</div>', b + 6) + 6
    nuevas = tarjeta('pago-minimo-tarjeta', 'Pago mínimo de la tarjeta', 'Cuánto terminás pagando y en cuántos meses si pagás sólo el mínimo.') + tarjeta('meta-de-ahorro', 'Meta de ahorro', 'Cuánto apartar por mes para llegar a un objetivo, con y sin rendimiento.') + tarjeta('prestamo-fijo-vs-uva', 'Préstamo: cuota fija o UVA', 'Cómo queda cada cuota mes a mes según la inflación que supongas.')
    hub = hub[:a] + nuevas + hub[b:].lstrip('\n')
    open(REPO + '/index.html', 'w', encoding='utf-8').write(hub)
print('ok')

# Capa de marca común (encabezado, pie, Bianca pregunta, imágenes para compartir)
import marca_apps
for _c, _a in marca_apps.APPS.items(): marca_apps.aplicar(_c, _a)
