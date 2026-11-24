import segno, io, urllib.parse, re
NUM = '5493624689882'
MSG = {'inv': 'Hola Lucas, estuve usando la aplicación {app} y quiero que me brindes asesoramiento sobre inversiones.',
       'gas': 'Hola Lucas, estuve usando la aplicación {app} y quiero que me ayudes a ordenar mis gastos y mis presupuestos.',
       'gen': 'Hola Lucas, estuve usando las herramientas de Finanzas con Lucas y quiero que me brindes asesoramiento.'}
TXT = {'inv': 'Escribime por WhatsApp y vemos cómo ordenar tus inversiones.', 'gas': 'Escribime por WhatsApp y vemos cómo ordenar tus gastos y tu presupuesto.', 'gen': 'Escribime por WhatsApp y lo vemos con tus números.'}
CSS_C = '''
.fcl-contacto{margin-top:24px;display:flex;gap:22px;align-items:center;flex-wrap:wrap;background:#070B2E;border:1px solid #23307A;border-radius:16px;padding:22px;color:#FFFFFF}
.fcl-contacto .fc-t{flex:1;min-width:230px}
.fcl-contacto h3{font-family:'Bricolage Grotesque',ui-sans-serif,system-ui,sans-serif;font-size:21px;font-weight:800;margin:0 0 6px;color:#FFFFFF}
.fcl-contacto p{margin:0 0 14px;font-size:14.5px;line-height:1.5;color:#DCE6FF}
.fcl-contacto a.fc-wa{display:inline-flex;align-items:center;gap:8px;min-height:46px;padding:12px 18px;border-radius:11px;background:#0E7A41;color:#FFFFFF;font-weight:800;font-size:15px;text-decoration:none}
.fcl-contacto a.fc-wa:hover{background:#0B6636}
.fcl-contacto .fc-qr{background:#FFFFFF;border-radius:12px;padding:8px;line-height:0;text-align:center}
.fcl-contacto .fc-qr svg{width:124px;height:124px;display:block}
.fcl-contacto .fc-qr span{display:block;font-size:10.5px;font-weight:700;color:#070B2E;line-height:1.3;margin-top:5px}
@media (max-width:600px){.fcl-contacto .fc-qr{display:none}}
'''
def enlace(app, tipo): return 'https://wa.me/' + NUM + '?text=' + urllib.parse.quote(MSG[tipo].format(app=app))
def bloque(app, tipo):
    url = enlace(app, tipo); b = io.BytesIO(); segno.make(url, error='m').save(b, kind='svg', xmldecl=False, svgns=True, border=1, dark='#070B2E', omitsize=True)
    svg = b.getvalue().decode().replace('<svg ', '<svg role="img" aria-label="Código QR para escribir por WhatsApp" ', 1)
    return f'''<section class="fcl-contacto" aria-label="Contacto">
  <div class="fc-t"><h3>¿Querés que lo miremos juntos?</h3><p>{TXT[tipo]}</p>
  <a class="fc-wa" href="{url}" target="_blank" rel="noopener noreferrer"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.5 8.5 0 0 1-12.6 7.4L3 20l1.2-5.1A8.5 8.5 0 1 1 21 11.5Z"/></svg>Hablar con Lucas</a></div>
  <div class="fc-qr">{svg}<span>Escaneá con el celular</span></div>
</section>'''
def quitar(s): return re.sub(r'\n?<section class="fcl-contacto".*?</section>', '', s, flags=re.S)
