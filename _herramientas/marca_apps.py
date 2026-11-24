"""Capa de marca común para las herramientas de Finanzas con Lucas.
Se corre después de gen.py. Es idempotente: se puede correr varias veces.
  python3 marca_apps.py            -> aplica encabezado, pie, Bianca pregunta, metadatos para compartir
"""
import re, sys, html
sys.path.insert(0, '/home/claude/marca2'); sys.path.insert(0, '/home/claude/apps')
from piezas import sello_bianca
REPO = '/home/claude/finanzas-con-lucas'
URL = 'https://lucasbergia.github.io/Finanzas-con-Lucas/'
WA = 'https://wa.me/5493624689882?text=' + 'Hola%20Lucas%2C%20estuve%20usando%20las%20herramientas%20de%20Finanzas%20con%20Lucas%20y%20quiero%20que%20me%20brindes%20asesoramiento.'
IG = 'https://www.instagram.com/lucasbergia.fin/'
MARK = lambda s: f'<svg viewBox="0 0 100 100" width="{s}" height="{s}" aria-hidden="true"><path d="M20 10 V80 H90" fill="none" stroke="#FFFFFF" stroke-width="17" stroke-linecap="square"/><path d="M44 58 L60 42 L70 50 L90 24" fill="none" stroke="#6FA0FF" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/><circle cx="90" cy="24" r="8" fill="#6FA0FF"/></svg>'
IG_SVG = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="6" stroke="white" stroke-width="2"/><circle cx="12" cy="12" r="4.2" stroke="white" stroke-width="2"/><circle cx="17.3" cy="6.7" r="1.1" fill="white"/></svg>'

APPS = {
 '': dict(titulo='Herramientas y calculadoras', og='Calculadoras para tomar mejores decisiones de plata',
          desc='Calculadoras gratuitas de Finanzas con Lucas: cuotas o contado, pago mínimo de la tarjeta, meta de ahorro y préstamo a cuota fija o UVA.'),
 'cuotas-vs-contado': dict(titulo='Efectivo vs. Cuotas', og='¿Cuotas o contado?', icono='cuotas',
          desc='Calculá si te conviene pagar en cuotas o de contado, con lo que rinde tu plata y la inflación.',
          faq=[('¿Por qué pagar en cuotas puede salir más barato?', 'Porque mientras vas pagando, la plata que no usaste sigue rindiendo, y con inflación las últimas cuotas pesan menos que la primera. Si las cuotas no tienen recargo o el recargo es menor a lo que rinde tu plata, suelen convenir.'),
               ('¿Qué tasa tengo que poner?', 'La que te paga hoy el lugar donde dejarías la plata: tu billetera virtual, un fondo money market o un plazo fijo. La ves en la misma app, como TNA.'),
               ('¿Y si me hacen descuento por pagar de contado?', 'Cargá como precio de contado el precio con el descuento ya aplicado. Así la calculadora ve el recargo real de las cuotas y la comparación es justa.')]),
 'pago-minimo-tarjeta': dict(titulo='Pago mínimo de la tarjeta', og='¿Qué pasa si pago el mínimo?', icono='tarjeta',
          desc='Calculá cuánto terminás pagando y en cuántos meses si pagás sólo el mínimo de la tarjeta.',
          faq=[('Si pago el mínimo, ¿me cobran intereses?', 'Sí. El saldo que queda sin pagar genera intereses de financiación, y sobre esos intereses se cobra IVA. Por eso la deuda baja mucho más lento de lo que parece.'),
               ('¿Dónde veo la tasa de mi tarjeta?', 'En el resumen. Figura como TNA de financiación y como TEM (tasa mensual); el resumen también informa el CFT, que suma impuestos y cargos.'),
               ('¿Conviene pasar la deuda a un préstamo personal?', 'Puede convenir si el CFT del préstamo es menor al de la tarjeta. Compará siempre CFT contra CFT, no tasa contra tasa.')]),
 'meta-de-ahorro': dict(titulo='Meta de ahorro', og='¿Cuánto tengo que ahorrar por mes?', icono='meta',
          desc='Calculá cuánto tenés que ahorrar por mes para llegar a un objetivo, con y sin rendimiento.',
          faq=[('¿Por qué la meta sube con la inflación?', 'Si lo que querés comprar tiene precio en pesos, ese precio sube con el tiempo. Ajustar la meta evita llegar al monto y descubrir que ya no alcanza.'),
               ('¿Qué rendimiento pongo?', 'Uno prudente: lo que paga hoy una cuenta remunerada o un fondo money market. Las tasas cambian, así que conviene revisar el plan cada pocos meses.'),
               ('¿Qué hago si un mes no llego a ahorrar?', 'Volvé a cargar lo que tenés ahorrado hoy y los meses que te quedan. La calculadora te dice el nuevo monto por mes.')]),
 'prestamo-fijo-vs-uva': dict(titulo='Préstamo: cuota fija o UVA', og='¿Préstamo a cuota fija o UVA?', icono='prestamo',
          desc='Compará un préstamo a cuota fija con uno UVA usando el CFT del banco y la inflación de INDEC.',
          faq=[('¿Qué es la UVA?', 'Es una unidad que publica el Banco Central y que sube todos los días siguiendo la inflación. En un préstamo UVA la deuda se mide en UVA, así que la cuota en pesos sube a medida que sube la inflación.'),
               ('¿Qué es el CFT y por qué lo pido?', 'Es el Costo Financiero Total: suma a la tasa el IVA, los seguros y las comisiones. El banco tiene que informarlo antes de que firmes y es el único número que sirve para comparar préstamos.'),
               ('¿Cuál es el riesgo del UVA?', 'Que la cuota suba más rápido que tu ingreso. Si tu sueldo no acompaña a la inflación, la cuota UVA puede pasar a pesar más en tu presupuesto aunque el préstamo sea más barato.')]),
}

ICONOS = {  # trazos simples, blanco sobre el cuadrado azul de la marca
 'cuotas': '<rect x="3" y="6" width="18" height="13" rx="2.5"/><path d="M3 10.5h18M7 15h4"/>',
 'tarjeta': '<rect x="2.5" y="5" width="15" height="11" rx="2"/><path d="M2.5 9h15"/><circle cx="18.5" cy="17.5" r="3.5" fill="#1730F5"/><path d="M17 19l3-3"/>',
 'meta': '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1" fill="#FFFFFF"/>',
 'prestamo': '<path d="M3.5 11L12 4l8.5 7"/><path d="M6 9.5V20h12V9.5"/><path d="M10 20v-5h4v5"/>',
}
APPS.update({
 'mis-finanzas': dict(titulo='Mis finanzas', og='Tus gastos, tus tarjetas y tus inversiones', icono='finanzas', card='Gastos del mes, cuotas de la tarjeta e inversiones con resultado en pesos y en dólares, y el mapa de tu cartera.',
   desc='Ordená tus gastos del mes, las cuotas de la tarjeta y tus inversiones, con el resultado en pesos y en dólares y un mapa de tu cartera.',
   faq=[('¿Dónde se guardan mis datos?', 'Sólo en el navegador que estás usando: no se envían a ningún servidor y nadie más los ve. Si borrás los datos de navegación o cambiás de dispositivo se pierden, por eso conviene descargar una copia de vez en cuando.'),
        ('¿Cómo calcula si gano en dólares?', 'Pasa cada compra y cada venta a dólares con el dólar MEP de ese día, y compara con lo que vale tu tenencia hoy al MEP actual. Así ves si le ganaste al dólar, no sólo a los pesos.'),
        ('¿La app me dice qué comprar o vender?', 'No. Ordena lo que hiciste y mide cómo te fue. Las decisiones son tuyas; si querés que lo veamos juntos, escribime.')]),
 'rendimiento-real': dict(titulo='Rendimiento contra inflación y dólar', og='¿Le ganaste a la inflación y al dólar?', icono='balanza', card='Si tu inversión le ganó a la inflación de INDEC y al dólar MEP, con datos que se actualizan solos.',
   desc='Calculá si tu inversión le ganó a la inflación de INDEC y al dólar MEP, con datos oficiales actualizados.',
   faq=[('¿Por qué medirlo contra la inflación?', 'Porque ganar 30% cuando los precios subieron 35% es perder poder de compra. Lo que importa es cuántas cosas podés comprar con tu plata al final.'),
        ('¿Por qué el dólar MEP?', 'Es el dólar que se compra en el mercado con bonos, sin tope de monto, y el que usan la mayoría de los inversores para medirse en dólares.'),
        ('¿Qué pongo en lo que tengo hoy?', 'El valor total actual, con intereses, dividendos y cupones cobrados. Si en el medio agregaste o sacaste plata, el resultado se distorsiona: en ese caso conviene medir cada aporte por separado.')]),
 'pesos-a-dolares-historico': dict(titulo='Pesos de antes, en dólares', og='¿Cuánto era en dólares?', icono='dolar', card='Cuántos dólares eran un monto en pesos de cualquier fecha y cuánto representa hoy.',
   desc='Convertí un monto en pesos de cualquier fecha a dólares MEP y oficial, y llevalo a pesos de hoy.',
   faq=[('¿Por qué da distinto por dólar y por inflación?', 'Porque el dólar y los precios no suben al mismo ritmo. Hay períodos en que el dólar sube más que la inflación y otros en que pasa lo contrario.'),
        ('¿Cuál uso para comparar un sueldo?', 'Por inflación, si querés saber si hoy alcanza para lo mismo que antes. Por dólar, si pensás en ahorro o en cosas que se pagan en dólares.'),
        ('¿Qué pasa si la fecha es un feriado?', 'Se usa la última cotización anterior a esa fecha, que es la que valía ese día.')]),
 'aguinaldo': dict(titulo='Aguinaldo', og='¿Cuánto cobrás de aguinaldo?', icono='aguinaldo', card='Tu medio aguinaldo bruto y en mano, completo o proporcional a los días trabajados.',
   desc='Calculá tu aguinaldo (SAC) bruto y neto, completo o proporcional a los días trabajados en el semestre.',
   faq=[('¿Qué cuenta como mejor sueldo?', 'El sueldo bruto mensual más alto del semestre, con horas extra, comisiones y premios. Por lo general las sumas no remunerativas no se incluyen, salvo que el convenio diga otra cosa.'),
        ('¿Cuándo me lo tienen que pagar?', 'La primera cuota hasta el 30 de junio y la segunda hasta el 18 de diciembre. El empleador tiene hasta 4 días hábiles más para pagar.'),
        ('¿Y si dejo el trabajo antes de fin de semestre?', 'Cobrás el aguinaldo proporcional a los días trabajados en la liquidación final.')]),
 'actualizacion-alquiler': dict(titulo='Actualización del alquiler', og='¿Cuánto sube tu alquiler?', icono='llave', card='Los ajustes de tu alquiler por ICL o IPC y el monto estimado del próximo.',
   desc='Calculá el ajuste de tu alquiler por ICL del BCRA o por IPC de INDEC, con los índices oficiales actualizados.',
   faq=[('¿ICL o IPC?', 'El que diga tu contrato. Desde fines de 2023 inquilino y propietario acuerdan libremente el índice y cada cuánto se ajusta.'),
        ('¿Qué es el ICL?', 'El Índice para Contratos de Locación que publica el Banco Central todos los días. Combina en partes iguales la inflación y la evolución de los salarios.'),
        ('¿Por qué el próximo ajuste es estimado?', 'Porque el índice del día del ajuste todavía no se publicó. La calculadora usa el último dato disponible y el número final se conoce ese día.')]),
 'donde-dejar-la-plata': dict(titulo='Dónde dejar la plata', og='¿Dónde dejo la plata? Armá tu diagnóstico', icono='alcancia', card='Contá tu plazo y tu objetivo, mirá lo que paga hoy el mercado y pedí tu propuesta personalizada.',
   desc='Contá cuánto tenés, para cuándo lo necesitás y qué buscás: te mostramos lo que paga hoy el mercado y armamos tu propuesta personalizada.',
   faq=[('¿Por qué no me dicen directamente qué fondo elegir?', 'Porque la mejor opción depende de tu plazo, de cuánto riesgo aceptás, de los impuestos y de los costos de cada plataforma. La tasa más alta de hoy no siempre es la que más te conviene: eso se define mirando tu caso.'),
        ('¿Qué pasa cuando pido la propuesta?', 'Se abre WhatsApp con tus respuestas ya escritas. Lo mandás, Lucas lo revisa y te responde con alternativas concretas para tu monto y tu plazo.'),
        ('¿Qué es un fondo money market?', 'Un fondo que invierte en colocaciones muy cortas, como cuentas remuneradas, plazos fijos y cauciones. Se puede rescatar en el día y es el que usan muchas billeteras virtuales para que tu saldo rinda.')]),
 'monotributo': dict(titulo='Monotributo', og='¿Qué categoría de monotributo te toca?', icono='recibo', card='Tu categoría y cuota mensual con la tabla vigente de ARCA, y cuánto margen te queda.',
   desc='Calculá tu categoría de monotributo y la cuota mensual con la tabla de ARCA vigente desde agosto de 2026.',
   faq=[('¿Qué facturación tengo que mirar?', 'La suma de lo que facturaste en los últimos 12 meses. ARCA la muestra en el Monitor de Facturación, dentro del servicio Monotributo.'),
        ('¿Cuándo me tengo que recategorizar?', 'Dos veces por año, en enero y en julio, con lo facturado en los 12 meses anteriores. Si seguís en la misma categoría no hace falta hacer nada.'),
        ('¿Qué pasa si me paso de la categoría K?', 'Quedás excluido del monotributo y tenés que pasar al régimen general (IVA y Ganancias). Conviene anticiparlo con tu contador.')]),
})
ICONOS.update({
 'finanzas': '<rect x="3" y="3" width="8" height="10" rx="1.5"/><rect x="13" y="3" width="8" height="6" rx="1.5"/><rect x="13" y="11" width="8" height="10" rx="1.5"/><rect x="3" y="15" width="8" height="6" rx="1.5"/>',
 'balanza': '<path d="M12 4v16M7 20h10M5 8h14"/><path d="M5 8l-2.5 6a3 3 0 0 0 5 0L5 8zM19 8l-2.5 6a3 3 0 0 0 5 0L19 8z"/>',
 'dolar': '<path d="M12 3v18"/><path d="M16.5 7.5c-.8-1.3-2.4-2-4.5-2-2.6 0-4.3 1.3-4.3 3.1 0 4.4 8.8 2.3 8.8 6.6 0 1.9-1.8 3.3-4.5 3.3-2.2 0-3.9-.8-4.7-2.2"/>',
 'aguinaldo': '<rect x="3" y="8" width="18" height="13" rx="2"/><path d="M12 8v13M3 12h18"/><path d="M12 8c-2-3.5-6-3.5-6-1s4 1 6 1c2 0 6 1.5 6-1s-4-2.5-6 1z"/>',
 'llave': '<circle cx="8" cy="15" r="4.5"/><path d="M11.2 11.8L20 3M17 6l2.5 2.5M14.5 8.5l2 2"/>',
 'alcancia': '<path d="M5 11a7 6 0 0 1 13-2h2v4h-1.5a7 6 0 0 1-2.5 3V19h-3v-1.6a8 8 0 0 1-3 0V19H7v-2.8A6 6 0 0 1 5 11z"/><path d="M10 6.5h4"/>',
 'recibo': '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6M9 16h3"/>',
})
ORDEN = ['mis-finanzas', 'cuotas-vs-contado', 'rendimiento-real', 'donde-dejar-la-plata', 'prestamo-fijo-vs-uva', 'pago-minimo-tarjeta', 'meta-de-ahorro', 'pesos-a-dolares-historico', 'actualizacion-alquiler', 'aguinaldo', 'monotributo']

def icono(k, s=24): return f'<svg viewBox="0 0 24 24" width="{s}" height="{s}" fill="none" stroke="#FFFFFF" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONOS[k]}</svg>'

CSS = '''<style id="fcl-marca">
.fclh{position:sticky;top:0;z-index:20;background:rgba(7,11,46,.94);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-bottom:1px solid #23307A;color:#FFFFFF}
.fclh-in{max-width:1120px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:14px;padding:12px 20px}
.fclh-brand{display:flex;align-items:center;gap:11px;text-decoration:none;color:#FFFFFF}
.fclh-mark{width:38px;height:38px;border-radius:10px;background:#1730F5;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.fclh-word{font:800 17px/1.05 'Bricolage Grotesque',ui-sans-serif,system-ui,sans-serif;letter-spacing:-.02em}
.fclh-word span{color:#6FA0FF;font-weight:500}
.fclh-word small{display:block;font:700 10.5px/1.3 'Manrope',sans-serif;letter-spacing:.12em;text-transform:uppercase;color:#A9B6DA;margin-top:3px}
.fclh nav{display:flex;align-items:center;gap:6px}
.fclh nav a{display:inline-flex;align-items:center;gap:7px;min-height:40px;padding:8px 12px;border-radius:10px;font:700 13px 'Manrope',sans-serif;color:#DCE6FF;text-decoration:none}
.fclh nav a:hover{background:#101746;color:#FFFFFF}
.fclh nav a[aria-current=page]{color:#FFFFFF;background:#101746}
.fclh nav a.ig-pill{background:#101746;border:1px solid #23307A;padding:5px 12px 5px 5px}
.fclh nav a.ig-pill .ig-icon{width:28px;height:28px;border-radius:8px;background:linear-gradient(135deg,#4f5bd5,#962fbf,#d62976,#fa7e1e,#feda75);display:flex;align-items:center;justify-content:center}
.fclh nav a.ig-pill .ig-icon svg{width:15px;height:15px}
.fclh .ig-label{display:flex;flex-direction:column;line-height:1.15}.fclh .ig-label small{font-weight:500;font-size:10.5px;color:#A9B6DA}
@media (max-width:560px){.fclh-word small,.fclh .ig-label,.fclh nav a.fclh-todas{display:none}.fclh nav a.ig-pill{padding:5px}}
.fcl-hero{margin:6px 0 22px}
.fcl-hero .volver{display:inline-flex;align-items:center;min-height:44px;font:700 13px 'Manrope',sans-serif;color:var(--accent,#1730F5);text-decoration:none}
.fcl-hero .eyebrow{font:800 11.5px 'Manrope',sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--accent,#1730F5);margin-bottom:8px}
.fcl-hero h1{font:800 30px/1.15 'Bricolage Grotesque',ui-sans-serif,system-ui,sans-serif;letter-spacing:-.02em;margin:0 0 8px}
.fcl-hero p{font-size:15px;color:var(--muted,var(--text-muted,#4B5680));max-width:68ch;line-height:1.6;margin:0}
.fclb{margin-top:24px;background:var(--surface,#FFFFFF);border:1px solid var(--border,#D3DCF7);border-radius:16px;padding:22px;display:grid;grid-template-columns:auto 1fr;gap:6px 22px;align-items:start}
.fclb-head{display:flex;flex-direction:column;align-items:center;gap:8px;grid-row:span 2}
.fclb-tit{font:800 15px/1 'Bricolage Grotesque',sans-serif;text-align:center}.fclb-tit span{display:block;color:var(--accent,#1730F5);font-size:15px;margin-top:2px}
.fclb h2{font:800 20px/1.2 'Bricolage Grotesque',sans-serif;margin:4px 0 4px}
.fclb p.fclb-sub{margin:0 0 6px;font-size:13.5px;color:var(--muted,var(--text-muted,#4B5680))}
.fclb details{border-top:1px solid var(--border,#D3DCF7)}
.fclb summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:12px;min-height:48px;padding:10px 0;font:700 15px 'Manrope',sans-serif}
.fclb summary::-webkit-details-marker{display:none}
.fclb summary::after{content:'+';font:800 20px 'Bricolage Grotesque',sans-serif;color:var(--accent,#1730F5)}
.fclb details[open] summary::after{content:'−'}
.fclb details p{margin:0 0 14px;font-size:14.5px;line-height:1.6;color:var(--text,#070B2E)}
@media (max-width:620px){.fclb{grid-template-columns:1fr}.fclb-head{flex-direction:row;grid-row:auto}.fclb-tit{text-align:left}}
.fclf{text-align:left;padding:0;font-size:inherit;background:#070B2E;color:#DCE6FF;border-top:1px solid #23307A;margin-top:40px}
.fclf-in{max-width:1120px;margin:0 auto;padding:28px 20px 34px;display:grid;grid-template-columns:1fr auto;gap:18px 30px;align-items:center}
.fclf-brand{display:flex;align-items:center;gap:12px}
.fclf-brand b{display:block;font:800 18px 'Bricolage Grotesque',sans-serif;color:#FFFFFF;letter-spacing:-.02em}
.fclf-brand span{font-size:12.5px;color:#A9B6DA}
.fclf nav{display:flex;gap:4px;flex-wrap:wrap}
.fclf nav a{min-height:44px;display:inline-flex;align-items:center;padding:8px 12px;border-radius:10px;color:#DCE6FF;font:700 13px 'Manrope',sans-serif;text-decoration:none}
.fclf nav a:hover{background:#101746;color:#FFFFFF}
.fclf-legal{grid-column:1/-1;margin:0;padding-top:16px;border-top:1px solid #1B2566;font-size:12px;line-height:1.6;color:#A9B6DA}
@media (max-width:700px){.fclf-in{grid-template-columns:1fr}}
.fclh a:focus-visible,.fclf a:focus-visible{outline:2px solid #6FA0FF;outline-offset:2px}
</style>'''

def header(raiz, actual):
    todas = '' if actual == '' else f'<a class="fclh-todas" href="{raiz}">Todas las herramientas</a>'
    return (f'<header class="fclh"><div class="fclh-in"><a class="fclh-brand" href="{raiz}" aria-label="Finanzas con Lucas, inicio">'
            f'<span class="fclh-mark">{MARK(25)}</span><span class="fclh-word">Finanzas <span>con</span> Lucas<small>Herramientas y calculadoras</small></span></a>'
            f'<nav aria-label="Principal">{todas}<a class="ig-pill" href="{IG}" target="_blank" rel="noopener noreferrer"><span class="ig-icon">{IG_SVG}</span>'
            f'<span class="ig-label">Seguime<small>@LucasBergia.Fin</small></span></a></nav></div></header>')

def footer(raiz):
    return (f'<footer class="fclf"><div class="fclf-in"><div class="fclf-brand"><span class="fclh-mark">{MARK(25)}</span><div><b>Finanzas con Lucas</b><span>Finanzas personales con números reales · @LucasBergia.Fin</span></div></div>'
            f'<nav aria-label="Pie"><a href="{raiz}">Herramientas</a><a href="{IG}" target="_blank" rel="noopener noreferrer">Instagram</a><a href="{WA}" target="_blank" rel="noopener noreferrer">WhatsApp</a></nav>'
            '<p class="fclf-legal">Herramientas educativas y gratuitas. Los resultados dependen de los datos que cargues y no son una recomendación de inversión ni reemplazan el asesoramiento profesional. Las tasas y la inflación cambian: revisá siempre los datos vigentes antes de decidir.</p></div></footer>')

def bianca(faq):
    items = ''.join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in faq)
    sello = sello_bianca(64)
    return (f'<section class="fclb" aria-labelledby="fclb-h"><div class="fclb-head">{sello}<div class="fclb-tit">Bianca<span>pregunta</span></div></div>'
            f'<div><h2 id="fclb-h">Las preguntas que todos se hacen</h2><p class="fclb-sub">Bianca pregunta lo que nadie se anima a preguntar. Responde Lucas.</p>{items}</div></section>')

def meta(carpeta, a):
    url = URL + (carpeta + '/' if carpeta else '')
    tit = ('Finanzas con Lucas · ' + a['titulo']) if carpeta else 'Finanzas con Lucas · Herramientas y calculadoras'
    d = html.escape(a['desc'], quote=True)
    return (f'<!--fcl-meta--><meta name="theme-color" content="#070B2E"><link rel="canonical" href="{url}">'
            f'<meta property="og:type" content="website"><meta property="og:site_name" content="Finanzas con Lucas"><meta property="og:locale" content="es_AR">'
            f'<meta property="og:title" content="{html.escape(tit, quote=True)}"><meta property="og:description" content="{d}"><meta property="og:url" content="{url}">'
            f'<meta property="og:image" content="{url}og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
            f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{url}og.png"><!--/fcl-meta-->')

def aplicar(carpeta, a):
    ruta = f'{REPO}/{carpeta + "/" if carpeta else ""}index.html'
    s = open(ruta, encoding='utf-8').read()
    raiz = './' if carpeta == '' else '../'
    # metadatos y estilos
    s = re.sub(r'<!--fcl-meta-->.*?<!--/fcl-meta-->', '', s, flags=re.S)
    s = re.sub(r'<style id="fcl-marca">.*?</style>', '', s, flags=re.S)
    s = re.sub(r'<meta name="description"[^>]*>', f'<meta name="description" content="{html.escape(a["desc"], quote=True)}">', s, count=1)
    if carpeta == 'cuotas-vs-contado':
        s = re.sub(r'<title>.*?</title>', '<title>Efectivo vs. Cuotas · Finanzas con Lucas</title>', s, count=1)
    s = s.replace('</head>', meta(carpeta, a) + CSS + '</head>', 1)
    # encabezado
    s = re.sub(r'<header class="(?:top|fclh)".*?</header>', header(raiz, carpeta), s, count=1, flags=re.S)
    # pie (el viejo footer, la barra azul fija de cuotas y el pie de marca anterior)
    s = re.sub(r'<div class="footer-cta">.*?</div>\s*</div>', '', s, count=1, flags=re.S)
    s = re.sub(r'<footer[^>]*>.*?</footer>', '', s, flags=re.S)
    s = s.replace('</main>', '</main>\n' + footer(raiz), 1)
    # Bianca pregunta, antes del bloque de contacto
    s = re.sub(r'<section class="fclb[^"]*".*?</section>', '', s, flags=re.S)
    if a.get('faq'):
        s = s.replace('<section class="fcl-contacto"', bianca(a['faq']) + '\n<section class="fcl-contacto"', 1)
    # encabezado de página en cuotas (no lo tenía)
    if carpeta == 'cuotas-vs-contado' and 'class="fcl-hero"' not in s:
        s = s.replace('<main class="wrap">', '<main class="wrap"><div class="fcl-hero"><a class="volver" href="../">← Todas las herramientas</a><div class="eyebrow">Calculadora</div><h1>Efectivo vs. Cuotas</h1><p>¿Te conviene pagar en cuotas o de contado? Cargá el precio, las cuotas y dónde dejarías la plata, y hacé la cuenta con tus números.</p></div>', 1)
    # íconos por herramienta en la página de inicio
    if carpeta == '':
        viejas = {c: re.search(r'<a class="tool-card" href="\./' + c + r'/">.*?</a>', s, re.S) for c in ORDEN}
        def tarjeta(c):
            x = APPS[c]; m = viejas.get(c); desc = x.get('card') or (re.search(r'<p>(.*?)</p>', m.group(0), re.S).group(1) if m else x['desc'])
            return (f'<a class="tool-card" href="./{c}/">\n        <div class="tool-icon">{icono(x["icono"])}</div>\n        <div class="tool-info">\n          <h3>{x["titulo"]}</h3>\n          <p>{desc}</p>\n        </div>\n        <div class="tool-arrow">→</div>\n      </a>')
        cards = re.findall(r'<a class="tool-card".*?</a>', s, re.S)
        bloque = '\n      '.join(tarjeta(c) for c in ORDEN)
        ini = s.index(cards[0]); fin = s.index(cards[-1]) + len(cards[-1])
        s = s[:ini] + bloque + s[fin:]
        s = s.replace('Cómo queda cada cuota mes a mes según la inflación que supongas.', 'Cuál te conviene según el CFT del banco y la inflación de INDEC.')
        s = re.sub(r'<section class="fclb-ig".*?</section>', '', s, flags=re.S)
        ig = (f'<section class="fclb fclb-ig" aria-labelledby="fclb-h"><div class="fclb-head">{sello_bianca(64)}<div class="fclb-tit">Bianca<span>pregunta</span></div></div>'
              '<div><h2 id="fclb-h">¿Tenés una pregunta de plata?</h2><p class="fclb-sub" style="margin-bottom:12px">Mandala por mensaje directo en Instagram. Las mejores las responde Lucas en la sección Bianca pregunta.</p>'
              f'<a href="https://ig.me/m/lucasbergia.fin" target="_blank" rel="noopener noreferrer" style="display:inline-flex;align-items:center;min-height:44px;padding:10px 16px;border-radius:11px;background:#1730F5;color:#FFFFFF;font:800 14px Manrope,sans-serif;text-decoration:none">Mandar mi pregunta</a></div></section>')
        s = s.replace('<section class="fcl-contacto"', ig + '\n<section class="fcl-contacto"', 1)
    # en las páginas de gen.py el título pasa a ser el h1 de la página
    s = re.sub(r'(<main>\s*)<a class="volver" href="\.\./">← Todas las herramientas</a>\s*<div class="eyebrow">Calculadora</div>\s*<h2>(.*?)</h2>\s*<p class="lead">(.*?)</p>',
               r'\1<div class="fcl-hero"><a class="volver" href="../">← Todas las herramientas</a><div class="eyebrow">Calculadora</div><h1>\2</h1><p>\3</p></div>', s, count=1, flags=re.S)
    open(ruta, 'w', encoding='utf-8').write(s)
    return ruta

if __name__ == '__main__':
    for c, a in APPS.items(): print(aplicar(c, a))
