"""App Mis finanzas: gastos del mes, tarjetas, inversiones y mapa de cuadrados. Datos en el dispositivo (modo local)."""
import os
_src = open('/home/claude/apps/gen.py', encoding='utf-8').read().split('# ───────── 1')[0]
exec(_src)

CSS3 = r'''
.tabs{display:flex;gap:6px;flex-wrap:wrap;margin:0 0 18px;border-bottom:1px solid var(--border);padding-bottom:10px}
.tabs button{min-height:44px;padding:9px 16px;border-radius:11px;border:1px solid transparent;background:transparent;color:var(--muted);font:800 14px Manrope,sans-serif;cursor:pointer}
.tabs button[aria-selected=true]{background:#1730F5;color:#fff}
.tabs button:not([aria-selected=true]):hover{background:var(--surface-2);color:var(--text)}
.panel[hidden]{display:none}
.local{display:flex;gap:12px;align-items:center;flex-wrap:wrap;justify-content:space-between;padding:12px 16px;border-radius:12px;background:var(--soft);font-size:13.5px;line-height:1.5;margin-bottom:18px}
.local div{flex:1;min-width:240px}.acciones{display:flex;gap:8px;flex-wrap:wrap}
.btn{min-height:44px;padding:9px 16px;border-radius:11px;border:1px solid var(--border);background:var(--surface);color:var(--text);font:700 13.5px Manrope,sans-serif;cursor:pointer;text-decoration:none;display:inline-flex;align-items:center}
.btn.pri{background:#1730F5;border-color:#1730F5;color:#fff}.btn:hover{border-color:var(--accent)}
.grid2{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:20px;align-items:start}
@media (max-width:860px){.grid2{grid-template-columns:minmax(0,1fr)}}
.scroll{position:relative}.grid2>.card{margin-top:0}
.card+.card,.card+.grid2,.grid2+.card,.kpis+.card{margin-top:20px}
details.alta{border:1px solid var(--border);border-radius:12px;padding:0 14px;margin-bottom:16px;background:var(--surface-2)}
details.alta summary{cursor:pointer;min-height:48px;display:flex;align-items:center;font:800 14px Manrope,sans-serif;color:var(--accent)}
.fila{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:0 12px}
select,input[type=date],input[type=month]{width:100%;min-height:46px;padding:10px 12px;border-radius:11px;border:1px solid var(--border);background:var(--surface);color:var(--text);font:600 15px Manrope,sans-serif;color-scheme:light dark}
details.alta input[type=text]{background:var(--surface)}
.form-pie{display:flex;gap:10px;align-items:center;margin:14px 0 16px;flex-wrap:wrap}
.ok-msg{font-size:13px;font-weight:700;color:var(--ok)}
.barras{display:flex;flex-direction:column;gap:8px}
.barra{display:grid;grid-template-columns:120px 1fr 96px;gap:10px;align-items:center;font-size:13px}
.barra .pista{height:12px;border-radius:6px;background:var(--surface-2);overflow:hidden}.barra .pista i{display:block;height:100%;background:#1730F5;border-radius:0 6px 6px 0}
.barra b{text-align:right;font-variant-numeric:tabular-nums}
@media (max-width:480px){.barra{grid-template-columns:90px 1fr 84px}}
td .x{min-width:36px;min-height:36px;border:0;background:transparent;color:var(--muted);cursor:pointer;font-size:18px;border-radius:8px}td .x:hover{background:var(--bad-soft);color:var(--bad)}
td.g,th.g{text-align:left}td.pos{color:var(--ok);font-weight:700}td.neg{color:var(--bad);font-weight:700}
td input.manual{width:110px;min-height:36px;padding:6px 8px;font-size:13px;text-align:right}
.vacio{padding:18px;border:1px dashed var(--border);border-radius:12px;color:var(--muted);font-size:14px;line-height:1.55}
.filtros{display:flex;gap:10px;flex-wrap:wrap;align-items:end;margin-bottom:14px}.filtros label{font-size:12px;font-weight:700;color:var(--muted)}.filtros select{min-width:150px}
.mapa-wrap{position:relative}
.mapa{position:relative;width:100%;height:440px;border-radius:12px;overflow:hidden;background:var(--surface-2)}
@media (max-width:600px){.mapa{height:380px}}
.mapa .grupo{position:absolute;border:2px solid var(--surface);box-sizing:border-box}
.mapa .grupo>span{position:absolute;left:6px;top:3px;font:800 11px Manrope,sans-serif;color:var(--muted);white-space:nowrap;overflow:hidden;max-width:calc(100% - 12px)}
.mapa button.t{position:absolute;box-sizing:border-box;border:2px solid var(--surface);color:#fff;font-family:Manrope,sans-serif;padding:4px;display:flex;flex-direction:column;align-items:center;justify-content:center;overflow:hidden;cursor:pointer;text-align:center;line-height:1.15}
.mapa button.t b{font:800 15px 'Bricolage Grotesque',sans-serif}.mapa button.t small{font-size:12px;font-weight:700;opacity:.95}
.mapa button.t:focus-visible{outline:3px solid #fff;outline-offset:-3px}
.tip{position:absolute;z-index:5;pointer-events:none;min-width:200px;max-width:260px;padding:10px 12px;border-radius:10px;background:var(--surface);border:1px solid var(--border);box-shadow:0 8px 24px var(--shadow);font-size:12.5px;line-height:1.5;color:var(--text)}
.tip b{font-size:14px}.tip[hidden]{display:none}
.escala{display:flex;align-items:center;gap:8px;margin-top:10px;font-size:12px;color:var(--muted)}.escala i{display:block;width:180px;height:10px;border-radius:5px;background:linear-gradient(90deg,#B8362F,#4A5066,#157A45)}
.seg3{display:flex;gap:6px;flex-wrap:wrap}.seg3 button{min-height:40px;padding:7px 12px;border-radius:10px;border:1px solid var(--border);background:var(--surface-2);color:var(--text);font:700 12.5px Manrope,sans-serif;cursor:pointer}.seg3 button[aria-pressed=true]{background:#1730F5;border-color:#1730F5;color:#fff}
.kpi.ok small,.kpi.bad small{color:var(--muted)}
'''

def campo2(id, etiqueta, valor='', ayuda='', modo='decimal', ph=''):
    return f'<div><label class="f" for="{id}">{etiqueta}{"<small>" + ayuda + "</small>" if ayuda else ""}</label><input id="{id}" type="text" inputmode="{modo}" autocomplete="off" value="{valor}" placeholder="{ph}"></div>'
def sel(id, etiqueta, ops, ayuda=''):
    o = ''.join(f'<option value="{v}">{t}</option>' for v, t in ops)
    return f'<div><label class="f" for="{id}">{etiqueta}{"<small>" + ayuda + "</small>" if ayuda else ""}</label><select id="{id}">{o}</select></div>'
def fch(id, etiqueta, tipo='date'):
    return f'<div><label class="f" for="{id}">{etiqueta}</label><input id="{id}" type="{tipo}"></div>'

CLASES = [('cedear', 'CEDEAR'), ('accion', 'Acción argentina'), ('bono', 'Bono'), ('on', 'Obligación negociable'), ('letra', 'Letra'), ('cripto', 'Cripto'), ('fci', 'Fondo común (FCI)'), ('otro', 'Otro')]

BODY = f'''
<div class="local" id="aviso"><div><b>Tus datos quedan guardados sólo en este navegador.</b> Nadie más los ve. Descargá una copia de vez en cuando; cuando esté lista la cuenta con usuario y contraseña, vas a poder pasarlos a la nube.</div>
<div class="acciones"><button class="btn" id="bExp" type="button">Descargar copia</button><label class="btn" for="fImp">Cargar copia</label><input id="fImp" type="file" accept="application/json" hidden><button class="btn" id="bEj" type="button">Ver con un ejemplo</button></div></div>
<div class="tabs" role="tablist" aria-label="Secciones">
 <button role="tab" id="tab-res" aria-controls="p-res" aria-selected="true">Resumen</button>
 <button role="tab" id="tab-gas" aria-controls="p-gas" aria-selected="false" tabindex="-1">Gastos del mes</button>
 <button role="tab" id="tab-tar" aria-controls="p-tar" aria-selected="false" tabindex="-1">Tarjetas</button>
 <button role="tab" id="tab-inv" aria-controls="p-inv" aria-selected="false" tabindex="-1">Inversiones</button>
</div>

<section class="panel" id="p-res" role="tabpanel" aria-labelledby="tab-res">
 <div class="filtros"><div><label for="mesRes">Mes</label><input id="mesRes" type="month"></div></div>
 <div class="kpis" id="kRes"></div>
 <div class="card"><h3>Tu cartera</h3><div class="kpis" id="kCar"></div><div id="mapaRes"></div></div>
 <div class="card"><h3>En qué se fue la plata este mes</h3><div id="catRes"></div></div>
</section>

<section class="panel" id="p-gas" role="tabpanel" aria-labelledby="tab-gas" hidden>
 <div class="filtros"><div><label for="mesGas">Mes</label><input id="mesGas" type="month"></div></div>
 <div class="kpis" id="kGas"></div>
 <div class="grid2">
  <div class="card"><h3>Cargar un movimiento</h3>
   <div class="fila">{sel('mTipo', 'Tipo', [('gasto', 'Gasto'), ('ingreso', 'Ingreso')])}{fch('mFecha', 'Fecha')}</div>
   <div class="fila">{sel('mCat', 'Categoría', [])}{campo2('mMonto', 'Monto', '', '', 'decimal', '0')}</div>
   {campo2('mDet', 'Detalle', '', 'Opcional', 'text', 'Por ejemplo: luz, supermercado')}
   <div class="form-pie"><button class="btn pri" id="bMov" type="button">Agregar movimiento</button><span class="ok-msg" id="okMov" aria-live="polite"></span></div>
   <div class="err" id="errMov" role="alert" hidden></div>
   <p class="nota">Las compras con tarjeta se cargan en la pestaña Tarjetas: sus cuotas aparecen solas en el mes en que las pagás.</p>
  </div>
  <div class="card"><h3>Por categoría</h3><div id="catGas"></div></div>
 </div>
 <div class="card"><h3>Movimientos del mes</h3><div class="scroll"><table><thead><tr><th class="g">Fecha</th><th class="g">Categoría</th><th class="g">Detalle</th><th>Monto</th><th><span class="sr">Borrar</span></th></tr></thead><tbody id="tMov"></tbody></table></div></div>
</section>

<section class="panel" id="p-tar" role="tabpanel" aria-labelledby="tab-tar" hidden>
 <div class="grid2">
  <div class="card"><h3>Tus tarjetas</h3>
   <details class="alta" id="altaTar"><summary>Agregar una tarjeta</summary>
    {campo2('tNom', 'Nombre', '', '', 'text', 'Visa Galicia')}
    <div class="fila">{campo2('tCie', 'Día de cierre', '25', 'Figura en el resumen', 'numeric')}{campo2('tVen', 'Día de vencimiento', '5', 'Del mes siguiente al cierre', 'numeric')}</div>
    <div class="form-pie"><button class="btn pri" id="bTar" type="button">Agregar tarjeta</button></div><div class="err" id="errTar" role="alert" hidden></div>
   </details>
   <div id="listaTar"></div>
  </div>
  <div class="card"><h3>Cargar una compra con tarjeta</h3>
   <div class="fila">{sel('cTar', 'Tarjeta', [])}{fch('cFecha', 'Fecha de compra')}</div>
   <div class="fila">{campo2('cMonto', 'Monto total', '', '', 'decimal', '0')}{campo2('cCuo', 'Cuotas', '1', '', 'numeric')}</div>
   <div class="fila">{sel('cCat', 'Categoría', [])}{campo2('cDet', 'Detalle', '', '', 'text', 'Heladera, pasajes…')}</div>
   <div class="form-pie"><button class="btn pri" id="bCon" type="button">Agregar compra</button><span class="ok-msg" id="okCon" aria-live="polite"></span></div>
   <div class="err" id="errCon" role="alert" hidden></div>
  </div>
 </div>
 <div class="card"><h3>Lo que vas a pagar de tarjeta</h3><div class="scroll"><table><thead id="hProy"></thead><tbody id="tProy"></tbody></table></div><p class="nota">Cada cuota se asigna al resumen según el día de cierre de la tarjeta y se paga en el vencimiento siguiente. No incluye intereses, impuestos ni cargos del resumen.</p></div>
 <div class="card"><h3>Compras con cuotas pendientes</h3><div class="scroll"><table><thead><tr><th class="g">Compra</th><th class="g">Tarjeta</th><th>Cuota</th><th>Valor cuota</th><th>Falta pagar</th><th><span class="sr">Borrar</span></th></tr></thead><tbody id="tCon"></tbody></table></div></div>
</section>

<section class="panel" id="p-inv" role="tabpanel" aria-labelledby="tab-inv" hidden>
 <div class="filtros">
  <div><label for="fBro">Broker o plataforma</label><select id="fBro"></select></div>
  <div><label for="fCar">Cartera</label><select id="fCar"></select></div>
  <div><button class="btn" id="bPre" type="button">Actualizar precios</button></div>
 </div>
 <div class="kpis" id="kInv"></div>
 <div class="card"><h3>Mapa de tu cartera</h3><div id="mapaInv"></div></div>
 <div class="card"><h3>Cargar una compra o venta</h3>
  <div class="fila">{sel('oTipo', 'Operación', [('compra', 'Compra'), ('venta', 'Venta')])}{fch('oFecha', 'Fecha')}{sel('oCla', 'Tipo de activo', CLASES)}</div>
  <div class="fila">{campo2('oEsp', 'Especie', '', 'Ticker o nombre', 'text', 'AAPL, GGAL, AL30, BTC')}{campo2('oCan', 'Cantidad', '', '', 'decimal', '0')}{campo2('oPre', 'Precio por unidad', '', '<span id="oPreAy">En la moneda que elijas</span>', 'decimal', '0')}</div>
  <div class="fila">{sel('oMon', 'Moneda del precio', [('ARS', 'Pesos'), ('USD', 'Dólares')])}{campo2('oCom', 'Comisión y gastos', '0', 'En la misma moneda', 'decimal')}{campo2('oBro', 'Broker o plataforma', '', '', 'text', 'PPI, IOL, Binance…')}{campo2('oCar', 'Cartera', '', 'Para agrupar: largo plazo, jubilación…', 'text', 'General')}</div>
  <div class="form-pie"><button class="btn pri" id="bOp" type="button">Agregar operación</button><span class="ok-msg" id="okOp" aria-live="polite"></span></div>
  <div class="err" id="errOp" role="alert" hidden></div>
 </div>
 <div class="card"><h3>Tenencias</h3><div class="scroll"><table><thead><tr><th class="g">Especie</th><th>Cantidad</th><th>Precio promedio</th><th>Precio hoy</th><th>Valor hoy</th><th>Resultado en $</th><th>Resultado en US$</th><th>Peso</th></tr></thead><tbody id="tTen"></tbody></table></div><p class="nota" id="notaTen"></p></div>
 <div class="card"><h3>Ventas y resultado realizado</h3><div class="scroll"><table><thead><tr><th class="g">Fecha</th><th class="g">Especie</th><th>Cantidad</th><th>Precio de venta</th><th>Resultado en $</th><th>Resultado en US$</th></tr></thead><tbody id="tVen"></tbody></table></div></div>
 <div class="card"><h3>Todas las operaciones</h3><div class="scroll"><table><thead><tr><th class="g">Fecha</th><th class="g">Operación</th><th class="g">Especie</th><th>Cantidad</th><th>Precio</th><th class="g">Broker</th><th class="g">Cartera</th><th><span class="sr">Borrar</span></th></tr></thead><tbody id="tOps"></tbody></table></div></div>
</section>
'''

JS3 = r'''
const API = 'https://api.argentinadatos.com/v1/', D912 = 'https://data912.com/live/';
const CLASE = { cedear: 'CEDEARs', accion: 'Acciones', bono: 'Bonos', on: 'Obligaciones negociables', letra: 'Letras', cripto: 'Cripto', fci: 'Fondos', otro: 'Otros' };
const PANEL = { cedear: 'arg_cedears', accion: 'arg_stocks', bono: 'arg_bonds', on: 'arg_corp', letra: 'arg_notes' };
const CADA100 = { bono: 1, on: 1, letra: 1 };
const CAT_G = ['Vivienda y alquiler', 'Servicios', 'Supermercado', 'Transporte', 'Salud', 'Educación', 'Salidas y comida', 'Ropa', 'Suscripciones', 'Impuestos', 'Deudas y préstamos', 'Otros'];
const CAT_I = ['Sueldo', 'Honorarios', 'Alquileres cobrados', 'Otros ingresos'];
const CLAVE = 'fcl-mis-finanzas-v1';
const uid = () => Math.random().toString(36).slice(2, 10) + Date.now().toString(36).slice(-4);
const hoyIso = () => { const d = new Date(); return new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate())).toISOString().slice(0, 10); };
const mesDe = s => s.slice(0, 7);
const sumMes = (ym, n) => { const [a, m] = ym.split('-').map(Number); const d = new Date(Date.UTC(a, m - 1 + n, 1)); return d.toISOString().slice(0, 7); };
const MES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'];
const mesCorto = ym => MES[+ym.slice(5) - 1] + ' ' + ym.slice(2, 4);
const fCorta = s => s.slice(8) + '/' + s.slice(5, 7) + '/' + s.slice(2, 4);
const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
const usd = v => isFinite(v) ? (v < 0 ? '−US$ ' : 'US$ ') + nf(Math.abs(v)) : '—';
const sig = v => isFinite(v) ? (v > 0 ? '+' : v < 0 ? '−' : '') + pc(Math.abs(v)) : '—';
const cls = v => v > 0.00001 ? 'pos' : v < -0.00001 ? 'neg' : '';

/* ── Datos guardados ── */
let S = { movs: [], tarjetas: [], consumos: [], ops: [], manual: {} };
function cargar() { try { const d = JSON.parse(localStorage.getItem(CLAVE) || 'null'); if (d) S = Object.assign(S, d); } catch (e) {} }
function guardar() { try { localStorage.setItem(CLAVE, JSON.stringify(S)); } catch (e) { $('aviso').querySelector('div').innerHTML = '<b>No se pudo guardar en este navegador.</b> Descargá una copia para no perder lo que cargaste.'; } }

/* ── Mercado ── */
let MEP = null, PRECIOS = {}, CRIPTO = {}, precioHora = null;
async function traer(url, minutos) {
  const k = 'fcl:' + url; let g = null; try { g = JSON.parse(localStorage.getItem(k) || 'null'); } catch (e) {}
  if (g && Date.now() - g.t < minutos * 60e3) return g.d;
  try { const r = await fetch(url); if (!r.ok) throw new Error(r.status); const d = await r.json(); try { localStorage.setItem(k, JSON.stringify({ t: Date.now(), d })); } catch (e) {} return d; }
  catch (e) { if (g) return g.d; throw e; }
}
function mepEn(f) { if (!MEP) return null; const t = f; let lo = 0, hi = MEP.length - 1, r = -1; while (lo <= hi) { const m = (lo + hi) >> 1; if (MEP[m].fecha <= t) { r = m; lo = m + 1; } else hi = m - 1; } return r < 0 ? MEP[0].venta : MEP[r].venta; }
const mepHoy = () => MEP ? MEP[MEP.length - 1].venta : null;
async function actualizarPrecios(forzar) {
  const clases = new Set(S.ops.map(o => o.clase)); const min = forzar ? 0 : 10;
  try { MEP = await traer(API + 'cotizaciones/dolares/bolsa', forzar ? 0 : 240); } catch (e) {}
  await Promise.all(Object.entries(PANEL).filter(([c]) => clases.has(c)).map(async ([c, p]) => { try { const l = await traer(D912 + p, min); PRECIOS[c] = new Map(l.map(x => [x.symbol, x])); } catch (e) {} }));
  const cr = [...new Set(S.ops.filter(o => o.clase === 'cripto').map(o => o.especie))].filter(x => !/^(USDT|USD)$/.test(x));
  if (cr.length) { try { const l = await traer('https://api.binance.com/api/v3/ticker/24hr?symbols=' + encodeURIComponent(JSON.stringify(cr.map(x => x + 'USDT'))), min); CRIPTO = Object.fromEntries(l.map(x => [x.symbol.replace(/USDT$/, ''), { usd: +x.lastPrice, pct: +x.priceChangePercent }])); } catch (e) {} }
  precioHora = new Date(); todo();
}
/* Precio actual en pesos por unidad (ya dividido por 100 en bonos, ON y letras) y variación del día */
function precioActual(clase, esp) {
  const f = CADA100[clase] ? 0.01 : 1, m = S.manual[esp];
  if (clase === 'cripto') { if (/^(USDT|USD)$/.test(esp)) return { ars: mepHoy(), pct: 0, src: 'auto' }; const c = CRIPTO[esp]; if (c && mepHoy()) return { ars: c.usd * mepHoy(), pct: c.pct / 100, src: 'auto' }; }
  else if (PRECIOS[clase] && PRECIOS[clase].get(esp)) { const x = PRECIOS[clase].get(esp); const p = x.c || x.px_bid; if (p) return { ars: p * f, pct: (x.pct_change || 0) / 100, src: 'auto' }; }
  if (m && m.p > 0) return { ars: m.p * f, pct: null, src: 'manual' };
  return null;
}

/* ── Cálculo de la cartera ── */
function posiciones(filtro) {
  const ops = S.ops.filter(o => (!filtro.bro || o.broker === filtro.bro) && (!filtro.car || o.cartera === filtro.car)).slice().sort((a, b) => a.fecha < b.fecha ? -1 : a.fecha > b.fecha ? 1 : (a.tipo === 'compra' ? -1 : 1));
  const P = new Map(), ventas = [], avisos = [];
  ops.forEach(o => {
    const k = o.clase + '|' + o.especie, f = CADA100[o.clase] ? 0.01 : 1, mep = o.mep || mepEn(o.fecha);
    if (!P.has(k)) P.set(k, { clase: o.clase, especie: o.especie, q: 0, cARS: 0, cUSD: 0, rARS: 0, rUSD: 0 });
    const p = P.get(k); if (!mep) return;
    const brutoARS = o.moneda === 'USD' ? o.cantidad * o.precio * f * mep : o.cantidad * o.precio * f;
    const comARS = o.moneda === 'USD' ? (o.comision || 0) * mep : (o.comision || 0);
    if (o.tipo === 'compra') { p.q += o.cantidad; p.cARS += brutoARS + comARS; p.cUSD += (brutoARS + comARS) / mep; }
    else { if (o.cantidad > p.q + 1e-9) { avisos.push(`La venta de ${o.cantidad} ${o.especie} del ${fCorta(o.fecha)} supera lo que tenías (${nf(p.q, 4)}).`); return; }
      const parte = o.cantidad / p.q, cA = p.cARS * parte, cU = p.cUSD * parte, nA = brutoARS - comARS, nU = nA / mep;
      ventas.push({ fecha: o.fecha, especie: o.especie, q: o.cantidad, precio: o.precio, moneda: o.moneda, rARS: nA - cA, rUSD: nU - cU, pARS: (nA - cA) / cA, pUSD: (nU - cU) / cU });
      p.rARS += nA - cA; p.rUSD += nU - cU; p.cARS -= cA; p.cUSD -= cU; p.q -= o.cantidad; }
  });
  const m1 = mepHoy(), lista = [];
  P.forEach(p => { if (p.q <= 1e-9) return; const pa = precioActual(p.clase, p.especie);
    p.precio = pa; p.vARS = pa ? pa.ars * p.q : null; p.vUSD = pa && m1 ? p.vARS / m1 : null;
    p.gARS = p.vARS != null ? p.vARS - p.cARS : null; p.gUSD = p.vUSD != null ? p.vUSD - p.cUSD : null;
    p.pARS = p.gARS != null ? p.gARS / p.cARS : null; p.pUSD = p.gUSD != null ? p.gUSD / p.cUSD : null; lista.push(p); });
  const tot = lista.reduce((s, p) => s + (p.vARS || 0), 0); lista.forEach(p => p.peso = p.vARS ? p.vARS / tot : 0);
  lista.sort((a, b) => (b.vARS || 0) - (a.vARS || 0));
  return { lista, ventas: ventas.reverse(), avisos, tot, P };
}

/* ── Mapa de cuadrados (treemap) ── */
function squarify(nodes, x, y, w, h) {
  const tot = nodes.reduce((s, n) => s + n.v, 0), res = []; if (!tot || w <= 0 || h <= 0) return res;
  const it = nodes.map(n => ({ n, a: n.v / tot * w * h })); let row = [], i = 0;
  const peor = (r, l) => { const s = r.reduce((a, b) => a + b.a, 0); let mx = 0, mn = Infinity; r.forEach(q => { mx = Math.max(mx, q.a); mn = Math.min(mn, q.a); }); return Math.max(l * l * mx / (s * s), s * s / (l * l * mn)); };
  const poner = r => { const s = r.reduce((a, b) => a + b.a, 0);
    if (w >= h) { const cw = s / h; let cy = y; r.forEach(q => { const ch = q.a / cw; res.push({ n: q.n, x, y: cy, w: cw, h: ch }); cy += ch; }); x += cw; w -= cw; }
    else { const ch = s / w; let cx = x; r.forEach(q => { const cw = q.a / ch; res.push({ n: q.n, x: cx, y, w: cw, h: ch }); cx += cw; }); y += ch; h -= ch; } };
  while (i < it.length) { const l = Math.min(w, h); if (!row.length || peor(row.concat([it[i]]), l) <= peor(row, l)) { row.push(it[i]); i++; } else { poner(row); row = []; } }
  if (row.length) poner(row); return res;
}
/* Color divergente: rojo para pérdida, gris en cero, verde para ganancia (tope en ±30%, o ±5% para el día) */
function colorDe(p, tope) { if (p == null || !isFinite(p)) return '#5B6178';
  const t = Math.min(Math.abs(p) / tope, 1), a = [74, 80, 102], b = p >= 0 ? [21, 122, 69] : [184, 54, 47];
  return 'rgb(' + a.map((v, i) => Math.round(v + (b[i] - v) * Math.pow(t, 0.75))).join(',') + ')'; }
let modoMapa = { color: 'total', mon: 'ARS' };
function mapa(cont, lista, chico) {
  const conPrecio = lista.filter(p => p.vARS > 0);
  if (!conPrecio.length) { cont.innerHTML = '<div class="vacio">Cuando cargues compras de activos con precio, acá vas a ver cada uno como un cuadrado: el tamaño es cuánto pesa en tu cartera y el color si vas ganando (verde) o perdiendo (rojo).</div>'; return; }
  const ctrl = chico ? '' : `<div class="filtros" style="margin-bottom:10px"><div><label>Color según</label><div class="seg3" data-m="color"><button type="button" data-v="total" aria-pressed="${modoMapa.color === 'total'}">Resultado total</button><button type="button" data-v="dia" aria-pressed="${modoMapa.color === 'dia'}">Variación de hoy</button></div></div>
    <div><label>Resultado medido en</label><div class="seg3" data-m="mon"><button type="button" data-v="ARS" aria-pressed="${modoMapa.mon === 'ARS'}">Pesos</button><button type="button" data-v="USD" aria-pressed="${modoMapa.mon === 'USD'}">Dólares</button></div></div></div>`;
  cont.innerHTML = ctrl + '<div class="mapa-wrap"><div class="mapa" role="group" aria-label="Mapa de la cartera"></div><div class="tip" hidden></div></div>' +
    `<div class="escala"><span>${modoMapa.color === 'dia' ? '−5%' : '−30%'}</span><i></i><span>${modoMapa.color === 'dia' ? '+5%' : '+30% o más'}</span><span style="margin-left:auto">Tamaño: peso en la cartera</span></div>`;
  const el = cont.querySelector('.mapa'), tip = cont.querySelector('.tip'), W = el.clientWidth, H = el.clientHeight;
  const grupos = {}; conPrecio.forEach(p => { (grupos[p.clase] = grupos[p.clase] || []).push(p); });
  const gs = Object.entries(grupos).map(([c, l]) => ({ c, l, v: l.reduce((s, p) => s + p.vARS, 0) })).sort((a, b) => b.v - a.v);
  let html = '';
  squarify(gs, 0, 0, W, H).forEach(g => {
    const cab = g.h > 60 && g.w > 70 ? 18 : 0;
    html += `<div class="grupo" style="left:${g.x}px;top:${g.y}px;width:${g.w}px;height:${g.h}px">${cab ? '<span>' + CLASE[g.n.c] + ' · ' + pc(g.n.v / conPrecio.reduce((s, p) => s + p.vARS, 0), 0) + '</span>' : ''}</div>`;
    squarify(g.n.l.map(p => ({ p, v: p.vARS })), g.x, g.y + cab, g.w, g.h - cab).forEach(r => {
      const p = r.n.p, val = modoMapa.color === 'dia' ? (p.precio && p.precio.pct) : (modoMapa.mon === 'USD' ? p.pUSD : p.pARS), tope = modoMapa.color === 'dia' ? 0.05 : 0.3;
      const lab = r.w > 46 && r.h > 28, lab2 = r.h > 48 && r.w > 56;
      html += `<button type="button" class="t" data-k="${esc(p.clase + '|' + p.especie)}" style="left:${r.x}px;top:${r.y}px;width:${r.w}px;height:${r.h}px;background:${colorDe(val, tope)}" aria-label="${esc(p.especie)}: ${pc(p.peso)} de la cartera, ${val == null ? 'sin dato' : sig(val)}">${lab ? '<b>' + esc(p.especie) + '</b>' : ''}${lab2 ? '<small>' + (val == null ? 's/d' : sig(val)) + '</small>' : ''}</button>`;
    });
  });
  el.innerHTML = html;
  const mostrar = (b, ev) => { const p = conPrecio.find(x => x.clase + '|' + x.especie === b.dataset.k); if (!p) return;
    tip.innerHTML = `<b>${esc(p.especie)}</b> · ${CLASE[p.clase]}<br>Peso en la cartera: ${pc(p.peso)}<br>Valor hoy: ${plata(p.vARS)} (${usd(p.vUSD)})<br>Resultado en pesos: ${plata(p.gARS)} (${sig(p.pARS)})<br>Resultado en dólares: ${usd(p.gUSD)} (${sig(p.pUSD)})` + (p.precio && p.precio.pct != null ? `<br>Hoy: ${sig(p.precio.pct)}` : '');
    tip.hidden = false; const bx = b.getBoundingClientRect(), wr = el.getBoundingClientRect();
    let lx = bx.left - wr.left + bx.width / 2 - 120, ly = bx.top - wr.top + bx.height + 6; lx = Math.max(4, Math.min(lx, W - 264)); if (ly + 140 > H) ly = Math.max(4, bx.top - wr.top - 146); tip.style.left = lx + 'px'; tip.style.top = ly + 'px'; };
  el.querySelectorAll('button.t').forEach(b => { b.addEventListener('mouseenter', e => mostrar(b, e)); b.addEventListener('focus', e => mostrar(b, e)); b.addEventListener('click', e => mostrar(b, e)); b.addEventListener('mouseleave', () => tip.hidden = true); b.addEventListener('blur', () => tip.hidden = true); });
  cont.querySelectorAll('.seg3[data-m]').forEach(g => g.addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; modoMapa[g.dataset.m] = b.dataset.v; todo(); }));
}

/* ── Tarjetas: en qué mes se paga cada cuota ── */
function mesPago(c, k) { const t = S.tarjetas.find(x => x.id === c.tarjeta) || { cierre: 25 }; const d = +c.fecha.slice(8); const cierre = d <= t.cierre ? mesDe(c.fecha) : sumMes(mesDe(c.fecha), 1); return sumMes(cierre, k + 1); }
function cuotasDelMes(ym) { const out = []; S.consumos.forEach(c => { for (let k = 0; k < c.cuotas; k++) if (mesPago(c, k) === ym) out.push({ c, k, monto: c.monto / c.cuotas }); }); return out; }

/* ── Gastos del mes ── */
function resumenMes(ym) {
  const movs = S.movs.filter(m => mesDe(m.fecha) === ym), cuo = cuotasDelMes(ym);
  const ing = movs.filter(m => m.tipo === 'ingreso').reduce((s, m) => s + m.monto, 0), gasE = movs.filter(m => m.tipo === 'gasto').reduce((s, m) => s + m.monto, 0), gasT = cuo.reduce((s, x) => s + x.monto, 0);
  const cats = {}; movs.filter(m => m.tipo === 'gasto').forEach(m => cats[m.cat] = (cats[m.cat] || 0) + m.monto); cuo.forEach(x => cats[x.c.cat] = (cats[x.c.cat] || 0) + x.monto);
  return { movs, cuo, ing, gas: gasE + gasT, gasT, cats };
}
function barras(cats) { const l = Object.entries(cats).sort((a, b) => b[1] - a[1]), mx = l.length ? l[0][1] : 0, t = l.reduce((s, x) => s + x[1], 0);
  return l.length ? '<div class="barras">' + l.map(([c, v]) => `<div class="barra"><span>${esc(c)}</span><div class="pista"><i style="width:${v / mx * 100}%"></i></div><b>${plata(v)}</b></div>`).join('') + `</div><p class="nota">Total: ${plata(t)}. Incluye las cuotas de tarjeta que vencen este mes.</p>` : '<div class="vacio">Todavía no hay gastos cargados en este mes.</div>'; }
function kpisMes(r) { return `<div class="kpi"><span>Ingresos</span><b>${plata(r.ing)}</b><small>${r.movs.filter(m => m.tipo === 'ingreso').length} movimientos</small></div>
  <div class="kpi"><span>Gastos</span><b>${plata(r.gas)}</b><small>${plata(r.gasT)} son de tarjeta</small></div>
  <div class="kpi ${r.ing - r.gas >= 0 ? 'ok' : 'bad'}"><span>Te queda</span><b>${plata(r.ing - r.gas)}</b><small>${r.ing ? pc((r.ing - r.gas) / r.ing, 0) + ' de lo que entró' : 'cargá tus ingresos'}</small></div>`; }

/* ── Pintar todo ── */
function filtro() { return { bro: $('fBro').value, car: $('fCar').value }; }
function opciones(id, vals, todos) { const el = $(id), v = el.value; el.innerHTML = (todos ? `<option value="">${todos}</option>` : '') + vals.map(x => `<option value="${esc(x)}">${esc(x)}</option>`).join(''); if ([...el.options].some(o => o.value === v)) el.value = v; }
function todo() {
  opciones('fBro', [...new Set(S.ops.map(o => o.broker).filter(Boolean))].sort(), 'Todos'); opciones('fCar', [...new Set(S.ops.map(o => o.cartera).filter(Boolean))].sort(), 'Todas');
  opciones('cTar', S.tarjetas.map(t => t.nombre)); [...$('cTar').options].forEach((o, i) => o.value = S.tarjetas[i].id);
  const ym = $('mesRes').value, rm = resumenMes(ym); $('kRes').innerHTML = kpisMes(rm); $('catRes').innerHTML = barras(rm.cats);
  const yg = $('mesGas').value, rg = resumenMes(yg); $('kGas').innerHTML = kpisMes(rg); $('catGas').innerHTML = barras(rg.cats);
  const filas = rg.movs.map(m => ({ f: m.fecha, cat: m.cat, det: m.det, monto: m.tipo === 'ingreso' ? m.monto : -m.monto, id: m.id })).concat(rg.cuo.map(x => ({ f: null, cat: x.c.cat, det: `${x.c.det || 'Compra'} · cuota ${x.k + 1} de ${x.c.cuotas} (${(S.tarjetas.find(t => t.id === x.c.tarjeta) || {}).nombre || 'tarjeta'})`, monto: -x.monto })));
  $('tMov').innerHTML = filas.length ? filas.sort((a, b) => (b.f || '') < (a.f || '') ? -1 : 1).map(r => `<tr><td class="g">${r.f ? fCorta(r.f) : 'Tarjeta'}</td><td class="g">${esc(r.cat)}</td><td class="g">${esc(r.det)}</td><td class="${cls(r.monto)}">${plata(r.monto)}</td><td>${r.id ? `<button class="x" data-borrar="movs" data-id="${r.id}" aria-label="Borrar movimiento">×</button>` : ''}</td></tr>`).join('') : '<tr><td colspan="5" class="g">Sin movimientos en este mes.</td></tr>';
  // tarjetas
  $('listaTar').innerHTML = S.tarjetas.length ? '<table><tbody>' + S.tarjetas.map(t => `<tr><td class="g"><b>${esc(t.nombre)}</b></td><td class="g">cierra el ${t.cierre}, vence el ${t.vence}</td><td><button class="x" data-borrar="tarjetas" data-id="${t.id}" aria-label="Borrar tarjeta ${esc(t.nombre)}">×</button></td></tr>`).join('') + '</tbody></table>' : '<div class="vacio">Agregá tus tarjetas con el día de cierre y de vencimiento del resumen.</div>';
  if (!S.tarjetas.length) $('altaTar').open = true;
  const m0 = mesDe(hoyIso()), meses = [0, 1, 2, 3, 4, 5].map(k => sumMes(m0, k));
  $('hProy').innerHTML = '<tr><th class="g">Tarjeta</th>' + meses.map(m => `<th>${mesCorto(m)}</th>`).join('') + '</tr>';
  const fila = id => meses.map(m => cuotasDelMes(m).filter(x => !id || x.c.tarjeta === id).reduce((s, x) => s + x.monto, 0));
  $('tProy').innerHTML = S.tarjetas.length ? S.tarjetas.map(t => `<tr><td class="g">${esc(t.nombre)}</td>${fila(t.id).map(v => `<td>${v ? plata(v) : '—'}</td>`).join('')}</tr>`).join('') + `<tr class="top"><td class="g"><b>Total</b></td>${fila(null).map(v => `<td><b>${v ? plata(v) : '—'}</b></td>`).join('')}</tr>` : '<tr><td class="g">Sin tarjetas cargadas.</td></tr>';
  const pend = S.consumos.map(c => { let pag = 0; for (let k = 0; k < c.cuotas; k++) if (mesPago(c, k) < m0) pag++; return { c, pag }; }).filter(x => x.pag < x.c.cuotas);
  $('tCon').innerHTML = pend.length ? pend.map(({ c, pag }) => `<tr><td class="g">${esc(c.det || 'Compra')} <small style="color:var(--muted)">${fCorta(c.fecha)}</small></td><td class="g">${esc((S.tarjetas.find(t => t.id === c.tarjeta) || {}).nombre || '—')}</td><td>${pag + 1} de ${c.cuotas}</td><td>${plata(c.monto / c.cuotas)}</td><td>${plata(c.monto / c.cuotas * (c.cuotas - pag))}</td><td><button class="x" data-borrar="consumos" data-id="${c.id}" aria-label="Borrar compra">×</button></td></tr>`).join('') : '<tr><td colspan="6" class="g">No hay cuotas pendientes.</td></tr>';
  // inversiones
  const R = posiciones(filtro()), m1 = mepHoy();
  const cA = R.lista.reduce((s, p) => s + p.cARS, 0), cU = R.lista.reduce((s, p) => s + p.cUSD, 0), conP = R.lista.filter(p => p.vARS != null);
  const vA = conP.reduce((s, p) => s + p.vARS, 0), vU = conP.reduce((s, p) => s + (p.vUSD || 0), 0), gA = conP.reduce((s, p) => s + p.gARS, 0), gU = conP.reduce((s, p) => s + (p.gUSD || 0), 0);
  const cAp = conP.reduce((s, p) => s + p.cARS, 0), cUp = conP.reduce((s, p) => s + p.cUSD, 0), rA = R.ventas.reduce((s, v) => s + v.rARS, 0), rU = R.ventas.reduce((s, v) => s + v.rUSD, 0);
  const kc = `<div class="kpi"><span>Valor de la cartera</span><b>${plata(vA)}</b><small>${usd(vU)} al MEP de ${m1 ? plata(m1) : '—'}</small></div>
   <div class="kpi ${gA >= 0 ? 'ok' : 'bad'}"><span>Resultado en pesos</span><b>${plata(gA)}</b><small>${sig(cAp ? gA / cAp : NaN)} sobre lo invertido</small></div>
   <div class="kpi ${gU >= 0 ? 'ok' : 'bad'}"><span>Resultado en dólares</span><b>${usd(gU)}</b><small>${sig(cUp ? gU / cUp : NaN)} sobre lo invertido</small></div>
   <div class="kpi"><span>Ya realizado (ventas)</span><b>${plata(rA)}</b><small>${usd(rU)}</small></div>`;
  $('kInv').innerHTML = kc; $('kCar').innerHTML = kc;
  mapa($('mapaInv'), R.lista, false); mapa($('mapaRes'), posiciones({}).lista, true);
  $('tTen').innerHTML = R.lista.length ? R.lista.map(p => { const mon = p.clase === 'cripto' ? 'USD' : 'ARS', ppc = p.cARS / p.q / (CADA100[p.clase] ? 0.01 : 1);
    const hoyP = p.precio ? p.precio.ars / (CADA100[p.clase] ? 0.01 : 1) : null;
    return `<tr><td class="g"><b>${esc(p.especie)}</b><br><small style="color:var(--muted)">${CLASE[p.clase]}</small></td><td>${nf(p.q, p.q % 1 ? 4 : 0)}</td><td>${plata(ppc)}</td>
     <td>${p.precio && p.precio.src === 'auto' ? plata(hoyP) : `<input class="manual" data-manual="${esc(p.especie)}" inputmode="decimal" aria-label="Precio de hoy de ${esc(p.especie)} en pesos" placeholder="precio $" value="${S.manual[p.especie] ? nf(S.manual[p.especie].p, 2) : ''}">`}</td>
     <td>${p.vARS != null ? plata(p.vARS) : '—'}</td><td class="${cls(p.gARS)}">${p.gARS != null ? plata(p.gARS) + '<br><small>' + sig(p.pARS) + '</small>' : '—'}</td><td class="${cls(p.gUSD)}">${p.gUSD != null ? usd(p.gUSD) + '<br><small>' + sig(p.pUSD) + '</small>' : '—'}</td><td>${p.vARS ? pc(p.peso) : '—'}</td></tr>`; }).join('') : '<tr><td colspan="8" class="g">Todavía no cargaste operaciones.</td></tr>';
  $('notaTen').innerHTML = (R.avisos.length ? '<b style="color:var(--bad)">' + R.avisos.map(esc).join(' ') + '</b><br>' : '') + 'Precios de acciones, CEDEARs, bonos, ON y letras: último operado en BYMA vía data912 (bonos, ON y letras se cotizan cada 100 nominales). Cripto: Binance en dólares, pasado a pesos al MEP. Fondos y otros activos: cargá el precio a mano en la columna Precio hoy. El resultado en dólares usa el dólar MEP del día de cada compra y venta.' + (precioHora ? ` Precios actualizados a las ${precioHora.toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit' })}.` : '');
  $('tVen').innerHTML = R.ventas.length ? R.ventas.map(v => `<tr><td class="g">${fCorta(v.fecha)}</td><td class="g">${esc(v.especie)}</td><td>${nf(v.q, v.q % 1 ? 4 : 0)}</td><td>${v.moneda === 'USD' ? usd(v.precio) : plata(v.precio)}</td><td class="${cls(v.rARS)}">${plata(v.rARS)}<br><small>${sig(v.pARS)}</small></td><td class="${cls(v.rUSD)}">${usd(v.rUSD)}<br><small>${sig(v.pUSD)}</small></td></tr>`).join('') : '<tr><td colspan="6" class="g">Sin ventas todavía.</td></tr>';
  const ops = S.ops.filter(o => (!filtro().bro || o.broker === filtro().bro) && (!filtro().car || o.cartera === filtro().car)).slice().sort((a, b) => a.fecha < b.fecha ? 1 : -1);
  $('tOps').innerHTML = ops.length ? ops.map(o => `<tr><td class="g">${fCorta(o.fecha)}</td><td class="g">${o.tipo === 'compra' ? 'Compra' : 'Venta'}</td><td class="g">${esc(o.especie)}</td><td>${nf(o.cantidad, o.cantidad % 1 ? 4 : 0)}</td><td>${o.moneda === 'USD' ? usd(o.precio) : plata(o.precio)}</td><td class="g">${esc(o.broker || '—')}</td><td class="g">${esc(o.cartera || '—')}</td><td><button class="x" data-borrar="ops" data-id="${o.id}" aria-label="Borrar operación">×</button></td></tr>`).join('') : '<tr><td colspan="8" class="g">Sin operaciones.</td></tr>';
}

/* ── Formularios ── */
function err(id, l) { const e = $(id); e.hidden = !l.length; e.textContent = l.join(' '); }
function aviso(id, t) { $(id).textContent = t; setTimeout(() => { $(id).textContent = ''; }, 2500); }
function catOpts() { opciones('mCat', $('mTipo').value === 'ingreso' ? CAT_I : CAT_G); }
$('mTipo').addEventListener('change', catOpts);
$('bMov').addEventListener('click', () => { const monto = num($('mMonto').value), f = $('mFecha').value, e = [];
  if (!(monto > 0)) e.push('Ingresá el monto.'); if (!f) e.push('Elegí la fecha.'); marcar('mMonto', !(monto > 0)); err('errMov', e); if (e.length) return;
  S.movs.push({ id: uid(), tipo: $('mTipo').value, fecha: f, cat: $('mCat').value, det: $('mDet').value.trim(), monto }); guardar();
  $('mMonto').value = ''; $('mDet').value = ''; $('mesGas').value = mesDe(f); todo(); aviso('okMov', 'Movimiento agregado'); });
$('bTar').addEventListener('click', () => { const n = $('tNom').value.trim(), c = num($('tCie').value), v = num($('tVen').value), e = [];
  if (!n) e.push('Poné un nombre.'); if (!(Number.isInteger(c) && c >= 1 && c <= 31)) e.push('El día de cierre va de 1 a 31.'); if (!(Number.isInteger(v) && v >= 1 && v <= 31)) e.push('El día de vencimiento va de 1 a 31.');
  err('errTar', e); if (e.length) return; S.tarjetas.push({ id: uid(), nombre: n, cierre: c, vence: v }); guardar(); $('tNom').value = ''; $('altaTar').open = false; todo(); });
$('bCon').addEventListener('click', () => { const monto = num($('cMonto').value), n = num($('cCuo').value), f = $('cFecha').value, e = [];
  if (!S.tarjetas.length) e.push('Primero agregá una tarjeta.'); if (!(monto > 0)) e.push('Ingresá el monto total.'); if (!(Number.isInteger(n) && n >= 1 && n <= 60)) e.push('Las cuotas van de 1 a 60.'); if (!f) e.push('Elegí la fecha.');
  err('errCon', e); if (e.length) return; S.consumos.push({ id: uid(), tarjeta: $('cTar').value, fecha: f, monto, cuotas: n, cat: $('cCat').value, det: $('cDet').value.trim() }); guardar();
  $('cMonto').value = ''; $('cDet').value = ''; $('cCuo').value = '1'; todo(); aviso('okCon', 'Compra agregada'); });
$('oCla').addEventListener('change', () => { const c = $('oCla').value; $('oPreAy').textContent = CADA100[c] ? 'Precio cada 100 nominales, como figura en el broker' : c === 'cripto' ? 'Por unidad; en cripto suele ser en dólares' : 'Por unidad, en la moneda que elijas'; if (c === 'cripto') $('oMon').value = 'USD'; });
$('bOp').addEventListener('click', async () => { const esp = $('oEsp').value.trim().toUpperCase(), q = num($('oCan').value), p = num($('oPre').value), com = num($('oCom').value) || 0, f = $('oFecha').value, e = [];
  if (!esp) e.push('Poné la especie.'); if (!(q > 0)) e.push('Ingresá la cantidad.'); if (!(p > 0)) e.push('Ingresá el precio.'); if (!f) e.push('Elegí la fecha.'); if (f > hoyIso()) e.push('La fecha no puede ser futura.');
  ['oEsp', 'oCan', 'oPre'].forEach((id, i) => marcar(id, [!esp, !(q > 0), !(p > 0)][i])); err('errOp', e); if (e.length) return;
  S.ops.push({ id: uid(), tipo: $('oTipo').value, fecha: f, clase: $('oCla').value, especie: esp, cantidad: q, precio: p, moneda: $('oMon').value, comision: com, broker: $('oBro').value.trim(), cartera: $('oCar').value.trim() || 'General' });
  guardar(); $('oEsp').value = ''; $('oCan').value = ''; $('oPre').value = ''; $('oCom').value = '0'; aviso('okOp', 'Operación agregada'); await actualizarPrecios(false); });
document.addEventListener('click', e => { const b = e.target.closest('[data-borrar]'); if (!b) return; const l = b.dataset.borrar; S[l] = S[l].filter(x => x.id !== b.dataset.id); if (l === 'tarjetas') S.consumos = S.consumos.filter(c => c.tarjeta !== b.dataset.id); guardar(); todo(); });
document.addEventListener('change', e => { const i = e.target.closest('[data-manual]'); if (!i) return; const v = num(i.value); if (v > 0) S.manual[i.dataset.manual] = { p: v, fecha: hoyIso() }; else delete S.manual[i.dataset.manual]; guardar(); todo(); });
['mesRes', 'mesGas', 'fBro', 'fCar'].forEach(id => $(id).addEventListener('change', todo));
$('bPre').addEventListener('click', () => actualizarPrecios(true));
let rz; window.addEventListener('resize', () => { clearTimeout(rz); rz = setTimeout(todo, 200); });

/* Pestañas */
const tabs = [...document.querySelectorAll('[role=tab]')];
function abrir(t) { tabs.forEach(x => { const on = x === t; x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1; $(x.getAttribute('aria-controls')).hidden = !on; }); todo(); }
tabs.forEach((t, i) => { t.addEventListener('click', () => abrir(t)); t.addEventListener('keydown', e => { if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { const n = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length]; n.focus(); abrir(n); } }); });

/* Copia de seguridad */
$('bExp').addEventListener('click', () => { const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([JSON.stringify(S, null, 1)], { type: 'application/json' })); a.download = 'mis-finanzas-' + hoyIso() + '.json'; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 1000); });
$('fImp').addEventListener('change', async e => { const f = e.target.files[0]; if (!f) return; try { const d = JSON.parse(await f.text()); if (!d || !Array.isArray(d.ops) || !Array.isArray(d.movs)) throw 0; S = Object.assign({ movs: [], tarjetas: [], consumos: [], ops: [], manual: {} }, d); guardar(); await actualizarPrecios(false); } catch (x) { $('aviso').querySelector('div').innerHTML = '<b>Ese archivo no es una copia de Mis finanzas.</b> Elegí el archivo .json que descargaste desde acá.'; } e.target.value = ''; });
$('bEj').addEventListener('click', async () => { if ((S.ops.length || S.movs.length) && !window.confirm('El ejemplo reemplaza lo que cargaste en este navegador. Si querés conservarlo, primero descargá una copia. ¿Seguimos?')) return;
  const m = mesDe(hoyIso()), d = n => m + '-' + String(n).padStart(2, '0'), ant = k => sumMes(m, -k) + '-10';
  const tv = uid(), tm = uid();
  S = { manual: { 'FIMA PREMIUM': { p: 92.5, fecha: hoyIso() } }, tarjetas: [{ id: tv, nombre: 'Visa', cierre: 25, vence: 5 }, { id: tm, nombre: 'Mastercard', cierre: 20, vence: 2 }],
    movs: [{ id: uid(), tipo: 'ingreso', fecha: d(1), cat: 'Sueldo', det: 'Sueldo', monto: 2400000 }, { id: uid(), tipo: 'gasto', fecha: d(2), cat: 'Vivienda y alquiler', det: 'Alquiler', monto: 650000 }, { id: uid(), tipo: 'gasto', fecha: d(4), cat: 'Supermercado', det: 'Súper', monto: 320000 }, { id: uid(), tipo: 'gasto', fecha: d(8), cat: 'Servicios', det: 'Luz, gas e internet', monto: 145000 }, { id: uid(), tipo: 'gasto', fecha: d(12), cat: 'Transporte', det: 'Nafta', monto: 110000 }],
    consumos: [{ id: uid(), tarjeta: tv, fecha: ant(2), monto: 1200000, cuotas: 6, cat: 'Otros', det: 'Heladera' }, { id: uid(), tarjeta: tm, fecha: ant(1), monto: 180000, cuotas: 3, cat: 'Ropa', det: 'Zapatillas' }, { id: uid(), tarjeta: tv, fecha: ant(1), monto: 95000, cuotas: 1, cat: 'Salidas y comida', det: 'Cena' }],
    ops: [{ id: uid(), tipo: 'compra', fecha: ant(10), clase: 'cedear', especie: 'SPY', cantidad: 40, precio: 38000, moneda: 'ARS', comision: 0, broker: 'PPI', cartera: 'Largo plazo' },
      { id: uid(), tipo: 'compra', fecha: ant(8), clase: 'cedear', especie: 'AAPL', cantidad: 60, precio: 21000, moneda: 'ARS', comision: 0, broker: 'PPI', cartera: 'Largo plazo' },
      { id: uid(), tipo: 'compra', fecha: ant(6), clase: 'cedear', especie: 'MELI', cantidad: 25, precio: 24000, moneda: 'ARS', comision: 0, broker: 'PPI', cartera: 'Largo plazo' },
      { id: uid(), tipo: 'compra', fecha: ant(7), clase: 'accion', especie: 'GGAL', cantidad: 300, precio: 6200, moneda: 'ARS', comision: 0, broker: 'IOL', cartera: 'Largo plazo' },
      { id: uid(), tipo: 'compra', fecha: ant(5), clase: 'accion', especie: 'YPFD', cantidad: 40, precio: 41000, moneda: 'ARS', comision: 0, broker: 'IOL', cartera: 'Largo plazo' },
      { id: uid(), tipo: 'venta', fecha: ant(1), clase: 'accion', especie: 'GGAL', cantidad: 100, precio: 7400, moneda: 'ARS', comision: 0, broker: 'IOL', cartera: 'Largo plazo' },
      { id: uid(), tipo: 'compra', fecha: ant(9), clase: 'bono', especie: 'AL30', cantidad: 2000, precio: 62, moneda: 'USD', comision: 0, broker: 'PPI', cartera: 'Renta fija' },
      { id: uid(), tipo: 'compra', fecha: ant(4), clase: 'cripto', especie: 'BTC', cantidad: 0.02, precio: 98000, moneda: 'USD', comision: 0, broker: 'Binance', cartera: 'Cripto' },
      { id: uid(), tipo: 'compra', fecha: ant(3), clase: 'fci', especie: 'FIMA PREMIUM', cantidad: 5000, precio: 85, moneda: 'ARS', comision: 0, broker: 'Galicia', cartera: 'Corto plazo' }] };
  guardar(); await actualizarPrecios(false); });

/* Inicio */
cargar(); const H = hoyIso(); $('mesRes').value = $('mesGas').value = mesDe(H); ['mFecha', 'cFecha', 'oFecha'].forEach(id => $(id).value = H); catOpts(); opciones('cCat', CAT_G);
todo(); actualizarPrecios(false);
'''

html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="Ordená tus gastos del mes, las cuotas de la tarjeta y tus inversiones, con el resultado en pesos y en dólares y un mapa de tu cartera.">
<title>Mis finanzas · Finanzas con Lucas</title>
{FAV}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}{CSS_C}{CSS3}.sr{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}}</style>
</head>
<body>
<header class="top"></header>
<main>
  <a class="volver" href="../">← Todas las herramientas</a>
  <div class="eyebrow">Aplicación</div>
  <h2>Mis finanzas</h2>
  <p class="lead">Tus gastos del mes, las cuotas de la tarjeta y tus inversiones en un solo lugar. Cargá tus compras y ventas y vas a ver si estás ganando o perdiendo, en pesos y en dólares.</p>
  {BODY}
  {contacto_bloque('Mis finanzas', 'inv')}
</main>
<footer></footer>
<script>{JS}{JS3}</script>
</body>
</html>
'''
os.makedirs(f'{REPO}/mis-finanzas', exist_ok=True)
open(f'{REPO}/mis-finanzas/index.html', 'w', encoding='utf-8').write(html)
print('ok')
