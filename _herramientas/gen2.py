"""Segunda tanda de calculadoras de Finanzas con Lucas. Usa pagina() y campo() de gen.py."""
import re
_src = open('/home/claude/apps/gen.py', encoding='utf-8').read().split('# ───────── 1')[0]
exec(_src)

CSS2 = '''<style>.layout>div{min-width:0}input[type=date],select{width:100%;min-height:46px;padding:10px 14px;border-radius:11px;border:1px solid var(--border);background:var(--surface-2);color:var(--text);font:600 16px 'Manrope',sans-serif;color-scheme:light dark}
.seg3{display:flex;gap:6px;flex-wrap:wrap;margin-top:6px}.seg3 button{min-height:44px;padding:8px 14px;border-radius:10px;border:1px solid var(--border);background:var(--surface-2);color:var(--text);font:700 13px Manrope,sans-serif;cursor:pointer}
.seg3 button[aria-pressed=true]{background:#1730F5;border-color:#1730F5;color:#fff}.kpi b{font-size:22px}.fuente{margin-top:10px;font-size:12px;color:var(--muted);line-height:1.5}
td.g,th.g{text-align:left}tr.top td{font-weight:800}.cargando{color:var(--muted);font-size:14px}</style>'''

def fecha(id, etiqueta, ayuda=''):
    return f'<label class="f" for="{id}">{etiqueta}{"<small>" + ayuda + "</small>" if ayuda else ""}</label><input id="{id}" type="date">'
def seg(id, etiqueta, opciones, ayuda=''):
    bs = ''.join(f'<button type="button" data-v="{v}" aria-pressed="{"true" if i == 0 else "false"}">{t}</button>' for i, (v, t) in enumerate(opciones))
    return f'<label class="f">{etiqueta}{"<small>" + ayuda + "</small>" if ayuda else ""}</label><div class="seg3" role="group" aria-label="{etiqueta}" id="{id}">{bs}</div>'

DATOS = r'''
const API = 'https://api.argentinadatos.com/v1/';
/* Trae JSON con copia local para no pedir de más; si falla usa la última copia guardada */
async function traer(url, horas) {
  const k = 'fcl:' + url; let guardado = null;
  try { guardado = JSON.parse(localStorage.getItem(k) || 'null'); } catch (e) {}
  if (guardado && Date.now() - guardado.t < horas * 3600e3) return guardado.d;
  try { const r = await fetch(url); if (!r.ok) throw new Error(r.status); const d = await r.json(); try { localStorage.setItem(k, JSON.stringify({ t: Date.now(), d })); } catch (e) {} return d; }
  catch (e) { if (guardado) return guardado.d; throw e; }
}
const dia = s => { const [a, m, d] = s.split('-').map(Number); return Date.UTC(a, m - 1, d); };
const iso = t => new Date(t).toISOString().slice(0, 10);
const hoyIso = () => { const d = new Date(); return iso(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate())); };
const MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'];
const fLarga = s => { const [a, m, d] = s.split('-').map(Number); return d + ' de ' + MESES[m - 1] + ' de ' + a; };
const fCorta2 = s => s.slice(8) + '/' + s.slice(5, 7) + '/' + s.slice(0, 4);
const mesTxt = s => MESES[+s.slice(5, 7) - 1] + ' de ' + s.slice(0, 4);
/* Valor de una serie diaria en una fecha (el último dato igual o anterior) */
function valorEn(serie, f, campo) { const t = dia(f); let lo = 0, hi = serie.length - 1, r = -1;
  while (lo <= hi) { const m = (lo + hi) >> 1; if (dia(serie[m].fecha) <= t) { r = m; lo = m + 1; } else hi = m - 1; }
  return r < 0 ? null : { v: serie[r][campo || 'venta'], fecha: serie[r].fecha }; }
/* Inflación acumulada entre dos fechas con el IPC mensual de INDEC (prorrateado por días dentro de cada mes) */
function inflEntre(ipc, f0, f1) {
  const m = new Map(ipc.map(x => [x.fecha.slice(0, 7), x.valor / 100])), ult = ipc[ipc.length - 1].fecha.slice(0, 7);
  let t = dia(f0), fin = dia(f1), f = 1, completo = true;
  while (t < fin) { const d = new Date(t), a = d.getUTCFullYear(), mm = d.getUTCMonth(), ini = Date.UTC(a, mm, 1), sig = Date.UTC(a, mm + 1, 1);
    const hasta = Math.min(sig, fin), k = iso(ini).slice(0, 7), pi = m.get(k);
    if (pi == null) { completo = false; break; }
    f *= Math.pow(1 + pi, (hasta - t) / (sig - ini)); t = hasta; }
  return { f, ult, completo };
}
function segValor(id) { return document.querySelector('#' + id + ' [aria-pressed=true]').dataset.v; }
function segs(fn) { document.querySelectorAll('.seg3').forEach(g => g.addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; g.querySelectorAll('button').forEach(x => x.setAttribute('aria-pressed', x === b)); fn(); })); }
function escuchar(fn) { document.querySelectorAll('input,select').forEach(i => i.addEventListener('input', fn)); segs(fn); }
'''
TABLA = '<div class="scroll"><table><thead><tr>{}</tr></thead><tbody id="t"></tbody></table></div>'

# ───────── Rendimiento contra inflación y dólar ─────────
pagina('rendimiento-real', 'Rendimiento contra inflación y dólar', '¿Le ganaste a la inflación y al dólar?', 'Calculá si tu inversión le ganó a la inflación de INDEC y al dólar MEP, con datos oficiales actualizados.',
 'Cargá cuánto pusiste, cuánto tenés hoy y las fechas. La calculadora trae sola la inflación de INDEC y el dólar MEP de cada día, y te muestra el resultado en pesos y en dólares.',
 CSS2 + campo('ini', 'Cuánto pusiste', '1.000.000', 'En pesos') + fecha('f0', 'Cuándo lo pusiste') + campo('fin', 'Cuánto tenés hoy (o cuánto sacaste)', '1.300.000', 'En pesos, con todo lo que ganaste') + fecha('f1', 'Fecha del valor final'),
 '<div class="kpis" id="k"></div><div class="verd" id="v"><span class="cargando">Buscando la inflación de INDEC y el dólar MEP…</span></div><div class="nota" id="nota"></div>',
 DATOS + r'''
let IPC, MEP, OFI;
function calc() {
  if (!IPC) return;
  const ini = num($('ini').value), fin = num($('fin').value), f0 = $('f0').value, f1 = $('f1').value, e = [];
  marcar('ini', !(ini > 0)); marcar('fin', !(fin >= 0)); marcar('f0', !f0 || f0 < '2018-10-29'); marcar('f1', !f1 || f1 <= f0);
  if (!(ini > 0)) e.push('Ingresá cuánto pusiste.'); if (!(fin >= 0)) e.push('Ingresá cuánto tenés hoy.');
  if (!f0 || f0 < '2018-10-29') e.push('La fecha inicial tiene que ser desde el 29/10/2018 (desde ahí hay datos del dólar MEP).');
  if (!f1 || f1 <= f0) e.push('La fecha final tiene que ser posterior a la inicial.');
  errores(e); if (e.length) { $('k').innerHTML = ''; $('v').textContent = 'Completá los datos para ver el resultado.'; return; }
  const r = fin / ini - 1, inf = inflEntre(IPC, f0, f1), real = (1 + r) / inf.f - 1;
  const m0 = valorEn(MEP, f0), m1 = valorEn(MEP, f1), o0 = valorEn(OFI, f0), o1 = valorEn(OFI, f1);
  const u0 = ini / m0.v, u1 = fin / m1.v, rU = u1 / u0 - 1;
  $('k').innerHTML = `<div class="kpi ${r >= 0 ? 'ok' : 'bad'}"><span>En pesos</span><b>${pc(r)}</b><small>de ${plata(ini)} a ${plata(fin)}</small></div>
   <div class="kpi ${real >= 0 ? 'ok' : 'bad'}"><span>Contra la inflación</span><b>${real >= 0 ? '+' : ''}${pc(real)}</b><small>inflación del período: ${pc(inf.f - 1)}</small></div>
   <div class="kpi ${rU >= 0 ? 'ok' : 'bad'}"><span>En dólares MEP</span><b>${rU >= 0 ? '+' : ''}${pc(rU)}</b><small>de US$ ${nf(u0)} a US$ ${nf(u1)}</small></div>`;
  const ok = real >= 0 && rU >= 0, nada = real < 0 && rU < 0;
  $('v').innerHTML = (ok ? '<b>Le ganaste a la inflación y al dólar.</b> ' : nada ? '<b>Perdiste contra la inflación y contra el dólar.</b> ' : real >= 0 ? '<b>Le ganaste a la inflación, pero no al dólar.</b> ' : '<b>Le ganaste al dólar, pero no a la inflación.</b> ') +
    `Para empatarle a la inflación tendrías que tener <b>${plata(ini * inf.f)}</b>, y para empatarle al dólar MEP, <b>${plata(u0 * m1.v)}</b>. Tenés ${plata(fin)}.` +
    (inf.completo ? '' : ` La inflación se cuenta hasta ${mesTxt(inf.ult + '-01')}, el último dato publicado por INDEC.`);
  const msg = `Hola Lucas, usé la calculadora de rendimiento contra inflación y dólar. Entre el ${fCorta2(f0)} y el ${fCorta2(f1)} mi inversión rindió ${pc(r)} en pesos: ${real >= 0 ? 'le ganó' : 'perdió'} a la inflación y ${rU >= 0 ? 'le ganó' : 'perdió'} al dólar MEP. Quiero que me asesores para mejorar el resultado.`;
  document.querySelectorAll('a.fc-wa').forEach(a => a.href = 'https://wa.me/5493624689882?text=' + encodeURIComponent(msg));
  $('nota').innerHTML = `Dólar MEP: ${plata(m0.v)} el ${fLarga(m0.fecha)} y ${plata(m1.v)} el ${fLarga(m1.fecha)}. Con el dólar oficial (Banco Nación, venta) el resultado en dólares sería ${pc(fin / o1.v / (ini / o0.v) - 1)}.<br>Fuentes: INDEC (IPC mensual) y cotizaciones diarias del dólar, vía ArgentinaDatos. La inflación dentro de cada mes se reparte por días.`;
}
const hoy = hoyIso(), d = new Date(dia(hoy)); d.setUTCFullYear(d.getUTCFullYear() - 1); $('f0').value = iso(d.getTime()); $('f1').value = hoy;
escuchar(calc);
Promise.all([traer(API + 'finanzas/indices/inflacion', 12), traer(API + 'cotizaciones/dolares/bolsa', 4), traer(API + 'cotizaciones/dolares/oficial', 4)])
  .then(([a, b, c]) => { IPC = a; MEP = b; OFI = c; const u = MEP[MEP.length - 1].fecha; if ($('f1').value > u) $('f1').value = u; calc(); })
  .catch(() => { $('v').textContent = 'No pudimos traer los datos de INDEC y del dólar. Revisá la conexión y recargá la página.'; });
''')

# ───────── Conversor histórico a dólares ─────────
pagina('pesos-a-dolares-historico', 'Pesos de antes, en dólares', 'Cuánto era en dólares y cuánto es hoy', 'Convertí un monto en pesos de cualquier fecha a dólares MEP y oficial, y llevalo a pesos de hoy.',
 'Poné un monto y una fecha: un sueldo, el precio de un auto, lo que pagaste por algo. Te decimos cuántos dólares eran ese día y cuánto representa hoy, por dólar y por inflación.',
 CSS2 + campo('monto', 'Monto en pesos', '500.000') + fecha('f0', 'Fecha', 'Desde el 29/10/2018 para el dólar MEP'),
 '<div class="kpis" id="k"></div><div class="verd" id="v"><span class="cargando">Buscando el dólar y la inflación…</span></div><div class="nota" id="nota"></div>',
 DATOS + r'''
let IPC, MEP, OFI;
function calc() {
  if (!IPC) return;
  const monto = num($('monto').value), f0 = $('f0').value, e = [], hoy = MEP[MEP.length - 1].fecha;
  marcar('monto', !(monto > 0)); marcar('f0', !f0 || f0 < '2018-10-29' || f0 >= hoy);
  if (!(monto > 0)) e.push('Ingresá el monto.'); if (!f0 || f0 < '2018-10-29' || f0 >= hoy) e.push('Elegí una fecha entre el 29/10/2018 y ayer.');
  errores(e); if (e.length) { $('k').innerHTML = ''; $('v').textContent = 'Completá los datos para ver el resultado.'; return; }
  const m0 = valorEn(MEP, f0), m1 = valorEn(MEP, hoy), o0 = valorEn(OFI, f0), o1 = valorEn(OFI, hoy), inf = inflEntre(IPC, f0, hoy);
  const usd = monto / m0.v, porDolar = usd * m1.v, porInf = monto * inf.f;
  $('k').innerHTML = `<div class="kpi"><span>En dólares MEP</span><b>US$ ${nf(usd)}</b><small>a ${plata(m0.v)} el ${fLarga(m0.fecha)}</small></div>
   <div class="kpi"><span>En dólares oficiales</span><b>US$ ${nf(monto / o0.v)}</b><small>a ${plata(o0.v)}, venta Banco Nación</small></div>
   <div class="kpi"><span>Hoy, por dólar MEP</span><b>${plata(porDolar)}</b><small>los mismos dólares a ${plata(m1.v)}</small></div>
   <div class="kpi"><span>Hoy, por inflación</span><b>${plata(porInf)}</b><small>inflación acumulada ${pc(inf.f - 1)}</small></div>`;
  $('v').innerHTML = `<b>${plata(monto)}</b> del ${fLarga(f0)} eran <b>US$ ${nf(usd)}</b> al dólar MEP. Para comprar esos mismos dólares hoy necesitás <b>${plata(porDolar)}</b>; ajustado por inflación, ese monto equivale a <b>${plata(porInf)}</b>. ` +
    (porDolar > porInf ? 'El dólar subió más que los precios: medido en dólares, hoy las cosas en pesos están más baratas que entonces.' : 'Los precios subieron más que el dólar: medido en dólares, hoy las cosas en pesos están más caras que entonces.') +
    (inf.completo ? '' : ` La inflación se cuenta hasta ${mesTxt(inf.ult + '-01')}, último dato de INDEC.`);
  $('nota').textContent = 'Fuentes: cotizaciones diarias del dólar MEP y oficial, e IPC de INDEC, vía ArgentinaDatos. Si la fecha cae en un feriado o fin de semana se usa la última cotización anterior.';
}
const d = new Date(); $('f0').value = iso(Date.UTC(d.getFullYear() - 2, d.getMonth(), 1));
escuchar(calc);
Promise.all([traer(API + 'finanzas/indices/inflacion', 12), traer(API + 'cotizaciones/dolares/bolsa', 4), traer(API + 'cotizaciones/dolares/oficial', 4)])
  .then(([a, b, c]) => { IPC = a; MEP = b; OFI = c; calc(); })
  .catch(() => { $('v').textContent = 'No pudimos traer los datos del dólar y de INDEC. Revisá la conexión y recargá la página.'; });
''')

# ───────── Aguinaldo ─────────
pagina('aguinaldo', 'Aguinaldo', 'Cuánto cobrás de medio aguinaldo', 'Calculá tu aguinaldo (SAC) bruto y neto, completo o proporcional a los días trabajados en el semestre.',
 'El aguinaldo es la mitad del mejor sueldo bruto mensual del semestre. Si empezaste a trabajar durante el semestre, se cobra en proporción a los días trabajados.',
 CSS2 + campo('mejor', 'Mejor sueldo bruto mensual del semestre', '1.200.000', 'El más alto de enero a junio o de julio a diciembre, con horas extra y comisiones') +
 seg('sem', '¿Qué aguinaldo querés calcular?', [('1', 'Primer semestre (junio)'), ('2', 'Segundo semestre (diciembre)')]) +
 fecha('ing', 'Fecha de ingreso', 'Sólo si empezaste a trabajar durante ese semestre. Si no, dejalo vacío') + campo('apo', 'Descuentos de ley (%)', '17', 'Jubilación 11%, PAMI 3% y obra social 3%'),
 '<div class="kpis" id="k"></div><div class="verd" id="v"></div><div class="nota">El aguinaldo se paga en dos cuotas: la primera hasta el 30 de junio y la segunda hasta el 18 de diciembre (con hasta 4 días hábiles de margen). No incluye el impuesto a las Ganancias, que sólo se descuenta en sueldos altos. Si trabajás en relación de dependencia, tu recibo es el dato final.</div>',
 DATOS + r'''
function calc() {
  const mejor = num($('mejor').value), apo = num($('apo').value) / 100, s = segValor('sem'), ing = $('ing').value, e = [];
  const a = new Date().getFullYear(), ini = s === '1' ? Date.UTC(a, 0, 1) : Date.UTC(a, 6, 1), fin = s === '1' ? Date.UTC(a, 5, 30) : Date.UTC(a, 11, 31);
  const tot = Math.round((fin - ini) / 864e5) + 1; let dias = tot;
  if (ing) { const t = dia(ing); if (t > fin) e.push('La fecha de ingreso es posterior al semestre.'); else if (t > ini) dias = Math.round((fin - t) / 864e5) + 1; }
  marcar('mejor', !(mejor > 0)); marcar('apo', !(apo >= 0 && apo < 1));
  if (!(mejor > 0)) e.push('Ingresá el mejor sueldo bruto.'); if (!(apo >= 0 && apo < 1)) e.push('Los descuentos van entre 0 y 99%.');
  errores(e); if (e.length) { $('k').innerHTML = ''; $('v').textContent = 'Completá los datos para ver el resultado.'; return; }
  const bruto = mejor / 2 * dias / tot, neto = bruto * (1 - apo);
  $('k').innerHTML = `<div class="kpi ok"><span>Aguinaldo neto</span><b>${plata(neto)}</b><small>lo que cobrás, aproximado</small></div>
   <div class="kpi"><span>Aguinaldo bruto</span><b>${plata(bruto)}</b><small>${dias === tot ? 'semestre completo' : dias + ' de ' + tot + ' días del semestre'}</small></div>
   <div class="kpi"><span>Descuentos</span><b>${plata(bruto - neto)}</b><small>${pc(apo, 0)} del bruto</small></div>`;
  $('v').innerHTML = `Con un mejor sueldo de ${plata(mejor)}, el aguinaldo de ${s === '1' ? 'junio' : 'diciembre'} es de <b>${plata(bruto)}</b> bruto y <b>${plata(neto)}</b> en mano.` + (dias < tot ? ` Es proporcional porque trabajaste ${dias} de los ${tot} días del semestre.` : '');
}
if (new Date().getMonth() >= 6) document.querySelectorAll('#sem button').forEach(b => b.setAttribute('aria-pressed', b.dataset.v === '2'));
escuchar(calc); calc();
''', 'gas')

# ───────── Alquiler ─────────
pagina('actualizacion-alquiler', 'Actualización del alquiler', 'Cuánto vas a pagar en el próximo ajuste', 'Calculá el ajuste de tu alquiler por ICL del BCRA o por IPC de INDEC, con los índices oficiales actualizados.',
 'Cargá el alquiler con el que arrancó el contrato, la fecha de inicio, cada cuánto ajusta y con qué índice. La calculadora trae los índices oficiales y arma todos los ajustes hasta hoy y el próximo.',
 CSS2 + campo('monto', 'Alquiler inicial del contrato', '450.000') + fecha('f0', 'Fecha de inicio del contrato') +
 seg('cada', '¿Cada cuánto ajusta?', [('3', 'Cada 3 meses'), ('4', 'Cada 4 meses'), ('6', 'Cada 6 meses'), ('12', 'Cada 12 meses')]) +
 seg('ind', '¿Con qué índice?', [('icl', 'ICL (BCRA)'), ('ipc', 'IPC (INDEC)')], 'Está escrito en tu contrato'),
 '<div class="kpis" id="k"></div><div class="verd" id="v"><span class="cargando">Buscando los índices…</span></div>' + TABLA.format('<th class="g">Desde</th><th>Ajuste</th><th>Alquiler</th>') + '<div class="nota" id="nota"></div>',
 DATOS + r'''
let IPC = null, ICL = null, iclDesde = null, pidiendo = false;
const sumarMeses = (s, n) => { const [a, m, d] = s.split('-').map(Number); const t = new Date(Date.UTC(a, m - 1 + n, 1)); const ult = new Date(Date.UTC(t.getUTCFullYear(), t.getUTCMonth() + 1, 0)).getUTCDate(); return iso(Date.UTC(t.getUTCFullYear(), t.getUTCMonth(), Math.min(d, ult))); };
function factorIPC(desde, hasta) { /* meses completos desde el mes de inicio hasta el mes anterior al ajuste */
  const m = new Map(IPC.map(x => [x.fecha.slice(0, 7), x.valor / 100])); let f = 1, k = desde.slice(0, 7), fin = hasta.slice(0, 7), faltan = 0;
  while (k < fin) { const pi = m.get(k); if (pi == null) faltan++; else f *= 1 + pi; k = sumarMeses(k + '-01', 1).slice(0, 7); }
  return { f, faltan };
}
async function cargarICL(f0) {
  if (iclDesde && iclDesde <= f0) return; if (pidiendo) return; pidiendo = true;
  const desde = iso(dia(f0) - 10 * 864e5), u = 'https://api.bcra.gob.ar/estadisticas/v4.0/monetarias/40?desde=' + desde + '&hasta=' + hoyIso() + '&limit=3000';
  try { const j = await traer(u, 12); ICL = j.results[0].detalle.map(x => ({ fecha: x.fecha, venta: x.valor })).sort((a, b) => a.fecha < b.fecha ? -1 : 1); iclDesde = f0; }
  catch (e) { $('v').textContent = 'No pudimos traer el ICL del Banco Central. Probá con IPC o recargá la página.'; }
  pidiendo = false; calc();
}
function calc() {
  const monto = num($('monto').value), f0 = $('f0').value, cada = +segValor('cada'), ind = segValor('ind'), hoy = hoyIso(), e = [];
  marcar('monto', !(monto > 0)); const minF = sumarMeses(hoy, -96); marcar('f0', !f0 || f0 > hoy || f0 < minF);
  if (!(monto > 0)) e.push('Ingresá el alquiler inicial.'); if (!f0 || f0 > hoy || f0 < minF) e.push('La fecha de inicio tiene que ser de los últimos 8 años y no futura.');
  errores(e); if (e.length) { $('k').innerHTML = ''; $('t').innerHTML = ''; $('v').textContent = 'Completá los datos para ver el resultado.'; return; }
  if (ind === 'icl' && !(ICL && iclDesde <= f0)) { cargarICL(f0); $('v').innerHTML = '<span class="cargando">Buscando el ICL del Banco Central…</span>'; return; }
  if (ind === 'ipc' && !IPC) return;
  const filas = [{ desde: f0, f: 1, alq: monto }]; let k = 1, prox = null, aviso = '';
  while (true) { const fa = sumarMeses(f0, cada * k); if (fa > hoy) { prox = fa; break; }
    let f; if (ind === 'icl') { const a = valorEn(ICL, filas[k - 1].desde), b = valorEn(ICL, fa); f = b.v / a.v; }
    else { const r = factorIPC(filas[k - 1].desde, fa); f = r.f; if (r.faltan) aviso = 'Algún mes del ajuste todavía no tiene dato de INDEC: ese tramo se completa cuando se publique.'; }
    filas.push({ desde: fa, f, alq: filas[k - 1].alq * f }); k++; if (k > 200) break; }
  let est; const ult = filas[filas.length - 1];
  if (ind === 'icl') { const a = valorEn(ICL, ult.desde), b = ICL[ICL.length - 1]; est = { f: b.venta / a.v, hasta: b.fecha }; }
  else { const r = factorIPC(ult.desde, prox); est = { f: r.f, hasta: IPC[IPC.length - 1].fecha.slice(0, 7), faltan: r.faltan }; }
  $('k').innerHTML = `<div class="kpi"><span>Alquiler actual</span><b>${plata(ult.alq)}</b><small>desde el ${fLarga(ult.desde)}</small></div>
   <div class="kpi"><span>Próximo ajuste</span><b>${prox.slice(8)}/${prox.slice(5,7)}/${prox.slice(0,4)}</b><small>faltan ${Math.round((dia(prox) - dia(hoy)) / 864e5)} días</small></div>
   <div class="kpi"><span>Estimado del próximo</span><b>${plata(ult.alq * est.f)}</b><small>+${pc(est.f - 1)} con datos ${ind === 'icl' ? 'al ' + fLarga(est.hasta) : 'hasta ' + mesTxt(est.hasta + '-01')}</small></div>`;
  $('v').innerHTML = `Hoy pagás <b>${plata(ult.alq)}</b>. El ${fLarga(prox)} ajusta por ${ind === 'icl' ? 'ICL' : 'IPC'}: con los datos publicados hasta ahora, el nuevo alquiler sería de unos <b>${plata(ult.alq * est.f)}</b>. El número final se conoce ${ind === 'icl' ? 'con el ICL del día del ajuste' : 'cuando INDEC publique los meses que faltan'}.` + (aviso ? ' ' + aviso : '');
  $('t').innerHTML = filas.map((r, i) => `<tr${i === filas.length - 1 ? ' class="top"' : ''}><td class="g">${fLarga(r.desde)}</td><td>${i ? '+' + pc(r.f - 1) : 'inicio'}</td><td>${plata(r.alq)}</td></tr>`).join('');
  $('nota').innerHTML = ind === 'icl' ? 'ICL: Índice para Contratos de Locación del Banco Central (variable 40). Cada ajuste usa el ICL del día de inicio del período y el del día del ajuste.' : 'IPC: inflación mensual de INDEC. Cada ajuste multiplica la inflación de los meses del período, desde el mes de inicio hasta el mes anterior al ajuste. Algunos contratos usan otra convención: seguí lo que diga el tuyo.';
}
const d = new Date(); $('f0').value = iso(Date.UTC(d.getFullYear() - 1, d.getMonth() - 2, 1));
escuchar(calc);
traer(API + 'finanzas/indices/inflacion', 12).then(a => { IPC = a; calc(); }).catch(() => {}); calc();
''', 'gas')

# ───────── Dónde dejar la plata (diagnóstico que termina en consulta) ─────────
CSS_DD = '''<style>.prop{margin-top:16px;padding:18px;border-radius:14px;background:#070B2E;border:1px solid #23307A;color:#fff}
.prop h4{font:800 19px/1.2 'Bricolage Grotesque',sans-serif;margin:0 0 6px;color:#fff}.prop p{margin:0 0 12px;font-size:14px;line-height:1.55;color:#DCE6FF}
.prop a{display:inline-flex;align-items:center;gap:8px;min-height:48px;padding:12px 18px;border-radius:11px;background:#0E7A41;color:#fff;font:800 15px Manrope,sans-serif;text-decoration:none}.prop a:hover{background:#0B6636}
.fam{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 4px}.fam span{padding:7px 12px;border-radius:999px;background:var(--surface-2);border:1px solid var(--border);font-size:13px;font-weight:700}
.ref{font-size:13.5px;line-height:1.6;margin-top:12px}.ref b{font-weight:800}</style>'''
pagina('donde-dejar-la-plata', 'Dónde dejar la plata', 'Armá tu diagnóstico y pedí tu propuesta', 'Contá cuánto tenés, para cuándo lo necesitás y qué buscás: te mostramos lo que paga hoy el mercado y armamos tu propuesta personalizada.',
 'Respondé cuatro preguntas. Te mostramos cuánto paga hoy el mercado en promedio, cuánto perdés si la plata queda quieta y qué alternativas se suelen analizar en tu caso. La propuesta concreta, con instrumentos y montos, la armamos juntos.',
 CSS2 + CSS_DD + campo('monto', '¿Cuánto querés invertir?', '1.000.000', 'En pesos. Si tenés dólares, poné el equivalente') +
 seg('plazo', '¿Para cuándo podés necesitar la plata?', [('ya', 'En cualquier momento'), ('corto', 'En 1 a 6 meses'), ('largo', 'En más de 6 meses')]) +
 seg('obj', '¿Qué buscás?', [('inf', 'Que no pierda contra la inflación'), ('usd', 'Protegerme en dólares'), ('renta', 'Cobrar una renta'), ('crec', 'Hacerla crecer a largo plazo')]) +
 seg('riesgo', 'Si en un mes tu inversión baja 10%, ¿qué hacés?', [('bajo', 'Vendo: no quiero perder'), ('medio', 'Espero a que se recupere'), ('alto', 'Aprovecho y compro más')]),
 '<div class="kpis" id="k"></div><div class="verd" id="v"><span class="cargando">Buscando las tasas de hoy…</span></div><h3 style="margin-top:4px">Lo que solemos analizar en un caso como el tuyo</h3><div class="fam" id="fam"></div><p class="nota" style="margin-top:6px">Son familias de instrumentos, no recomendaciones. Cuál conviene, en qué proporción y con qué plataforma depende de tus números, de los impuestos y de los costos: eso lo vemos en la consulta.</p><div class="prop"><h4>Pedí tu propuesta personalizada</h4><p id="propTxt">Te escribo con una propuesta concreta para tu monto y tu plazo. Tus respuestas ya van en el mensaje.</p><a id="waProp" href="#" target="_blank" rel="noopener noreferrer"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.5 8.5 0 0 1-12.6 7.4L3 20l1.2-5.1A8.5 8.5 0 1 1 21 11.5Z"/></svg>Quiero mi propuesta</a></div><div class="nota" id="nota"></div>',
 DATOS + __import__('vivo').TASAS_JS + r'''
let T = null, REM = null;
const TXT = { plazo: { ya: 'la puedo necesitar en cualquier momento', corto: 'la necesito en 1 a 6 meses', largo: 'no la necesito por más de 6 meses' },
  obj: { inf: 'que no pierda contra la inflación', usd: 'protegerme en dólares', renta: 'cobrar una renta', crec: 'hacerla crecer a largo plazo' },
  riesgo: { bajo: 'si baja 10% vendo', medio: 'si baja 10% espero', alto: 'si baja 10% compro más' } };
function familias(pl, ob, ri) {
  const f = new Set();
  if (pl === 'ya') ['Fondos money market', 'Cuentas remuneradas', 'Caución colocadora'].forEach(x => f.add(x));
  if (pl === 'corto') ['Plazo fijo', 'Letras del Tesoro (LECAP)', 'Fondos T+1', 'Caución colocadora'].forEach(x => f.add(x));
  if (pl === 'largo') { if (ob === 'inf') ['Bonos que ajustan por inflación (CER)', 'Fondos de renta fija'].forEach(x => f.add(x));
    if (ob === 'usd') ['Obligaciones negociables en dólares', 'Bonos en dólares', 'Dólar MEP'].forEach(x => f.add(x));
    if (ob === 'renta') ['Obligaciones negociables con cupón', 'Bonos con renta', 'Plazo fijo'].forEach(x => f.add(x));
    if (ob === 'crec') (ri === 'bajo' ? ['Fondos de renta fija', 'Bonos CER'] : ['CEDEARs', 'Acciones argentinas', 'Fondos de renta variable']).forEach(x => f.add(x)); }
  else { if (ob === 'usd') ['Dólar MEP', 'Fondos en dólares'].forEach(x => f.add(x)); if (ob === 'inf' && pl === 'corto') f.add('Bonos CER cortos'); }
  return [...f];
}
function calc() {
  const monto = num($('monto').value), pl = segValor('plazo'), ob = segValor('obj'), ri = segValor('riesgo'), e = [];
  marcar('monto', !(monto > 0)); if (!(monto > 0)) e.push('Ingresá el monto.'); errores(e);
  $('fam').innerHTML = familias(pl, ob, ri).map(x => '<span>' + x + '</span>').join('');
  const msg = `Hola Lucas, usé "Dónde dejar la plata". Tengo ${monto > 0 ? plata(monto) : 'un monto'} para invertir, ${TXT.plazo[pl]}, busco ${TXT.obj[ob]} y ${TXT.riesgo[ri]}. ¿Me armás una propuesta?`;
  const url = 'https://wa.me/5493624689882?text=' + encodeURIComponent(msg); $('waProp').href = url; document.querySelectorAll('a.fc-wa').forEach(a => a.href = url);
  if (e.length || !T) { $('k').innerHTML = ''; if (e.length) $('v').textContent = 'Completá el monto para ver tu diagnóstico.'; return; }
  const inf = REM ? REM / 100 : null, gPf = monto * T.pf, gMm = monto * T.mm;
  $('k').innerHTML = `<div class="kpi"><span>Plazo fijo, promedio</span><b>${pc(T.pf)}</b><small>tasa anual, valor del medio entre ${T.nPf} bancos</small></div>
   <div class="kpi"><span>Money market, promedio</span><b>${pc(T.mm)}</b><small>tasa anual, valor del medio entre ${T.nMm} fondos</small></div>
   <div class="kpi ${inf != null ? 'bad' : ''}"><span>Inflación esperada</span><b>${inf != null ? pc(inf) : '—'}</b><small>próximos 12 meses, según el Banco Central</small></div>`;
  $('v').innerHTML = (inf != null ? `Si tus ${plata(monto)} quedan quietos, en un año pierden <b>${plata(monto * inf / (1 + inf))}</b> de poder de compra. ` : '') +
    `A las tasas promedio de hoy, un plazo fijo te daría unos <b>${plata(gPf)}</b> en un año y un fondo money market unos <b>${plata(gMm)}</b>` +
    (inf != null ? `: ${T.pf > inf || T.mm > inf ? 'por encima de la inflación esperada.' : 'por debajo de la inflación esperada.'} ` : '. ') +
    'Con una cartera armada para tu caso se puede buscar más rendimiento o más protección, según lo que priorices.';
  $('nota').innerHTML = `Referencias de hoy: tasas para clientes que informan los bancos al Banco Central y variación diaria de los fondos money market con más de $1.000 millones (al ${fLarga(T.fecha)}), vía ArgentinaDatos; inflación esperada: mediana del Relevamiento de Expectativas de Mercado (REM) del Banco Central. Se actualizan solas. Los rendimientos pasados no garantizan los futuros.`;
}
escuchar(calc); calc();
Promise.all([fclTasasHoy(), traer('https://api.bcra.gob.ar/estadisticas/v4.0/monetarias/29?desde=' + iso(Date.now() - 200 * 864e5) + '&limit=20', 12).catch(() => null)]).then(([t, r]) => {
  T = t; if (r) { const d = r.results[0].detalle.slice().sort((a, b) => a.fecha < b.fecha ? 1 : -1)[0]; if (d && d.valor > 0) REM = d.valor; } calc();
}).catch(() => { $('v').textContent = 'No pudimos traer las tasas de hoy. Igual podés pedir tu propuesta con el botón de abajo.'; });
''')


# ───────── Monotributo ─────────
pagina('monotributo', 'Monotributo', 'Qué categoría te toca y cuánto pagás', 'Calculá tu categoría de monotributo y la cuota mensual con la tabla de ARCA vigente desde agosto de 2026.',
 'Cargá lo que facturaste en los últimos 12 meses y tu actividad. Te decimos en qué categoría estás, cuánto pagás por mes y cuánto margen te queda antes de pasar a la siguiente.',
 CSS2 + campo('fact', 'Facturación de los últimos 12 meses', '20.000.000', 'La suma de lo que facturaste en el último año') + seg('act', 'Actividad', [('s', 'Servicios'), ('b', 'Venta de bienes')]),
 '<div class="kpis" id="k"></div><div class="verd" id="v"></div>' + TABLA.format('<th class="g">Categoría</th><th>Facturación anual hasta</th><th>Cuota mensual</th>') + '<div class="nota">Tabla de ARCA vigente desde el 1 de agosto de 2026 hasta la próxima actualización (febrero de 2027). La cuota incluye impuesto integrado, aporte jubilatorio y obra social. La categoría también depende de la superficie del local, la energía consumida y el alquiler: si superás alguno de esos topes, corresponde una categoría más alta. Verificá siempre en arca.gob.ar.</div>',
 DATOS + r'''
/* ARCA, valores desde el 1/8/2026: [categoría, tope anual, cuota servicios, cuota bienes] */
const TAB = [['A', 12009410.45, 49527.18, 49527.18], ['B', 17595182.74, 56379.08, 56379.08], ['C', 24670494.31, 66020.12, 64530.58], ['D', 30628651.43, 84612.93, 82564.81], ['E', 36028231.33, 119811.45, 108267.51], ['F', 45151659.41, 150784.21, 129930.65], ['G', 53995798.87, 230312.94, 158815.05], ['H', 81924660.37, 522706.68, 317895.01], ['I', 91699761.90, 963747.86, 474992.78], ['J', 105012519.20, 1167299.76, 580793.69], ['K', 126610838.75, 1614446.04, 702103.24]];
function calc() {
  const fact = num($('fact').value), act = segValor('act'), e = [], c = act === 's' ? 2 : 3;
  marcar('fact', !(fact >= 0)); if (!(fact >= 0)) e.push('Ingresá lo que facturaste en los últimos 12 meses.');
  errores(e); if (e.length) { $('k').innerHTML = ''; $('v').textContent = 'Completá los datos para ver el resultado.'; return; }
  const i = TAB.findIndex(r => fact <= r[1]);
  $('t').innerHTML = TAB.map((r, j) => `<tr${j === i ? ' class="top"' : ''}><td class="g">${r[0]}${j === i ? ' (la tuya)' : ''}</td><td>${plata(r[1])}</td><td>${plata(r[c])}</td></tr>`).join('');
  if (i < 0) { $('k').innerHTML = `<div class="kpi bad"><span>Categoría</span><b>Fuera del régimen</b><small>superás el tope de la K</small></div>`;
    $('v').innerHTML = `Con ${plata(fact)} facturados superás el tope máximo del monotributo (${plata(TAB[10][1])}). Corresponde pasar al régimen general: consultalo con tu contador.`; return; }
  const r = TAB[i], sig = TAB[i + 1];
  $('k').innerHTML = `<div class="kpi"><span>Tu categoría</span><b>${r[0]}</b><small>hasta ${plata(r[1])} al año</small></div>
   <div class="kpi"><span>Cuota mensual</span><b>${plata(r[c])}</b><small>${act === 's' ? 'servicios' : 'venta de bienes'}</small></div>
   <div class="kpi ok"><span>Margen hasta el tope</span><b>${plata(r[1] - fact)}</b><small>unos ${plata((r[1] - fact) / 12)} por mes</small></div>`;
  $('v').innerHTML = `Con ${plata(fact)} facturados en 12 meses te corresponde la <b>categoría ${r[0]}</b> y pagás <b>${plata(r[c])}</b> por mes.` + (sig ? ` Si superás ${plata(r[1])}, pasás a la ${sig[0]} y la cuota sube a ${plata(sig[c])}.` : ' Es la categoría más alta del régimen.');
}
escuchar(calc); calc();
''', 'gas')
print('ok')
