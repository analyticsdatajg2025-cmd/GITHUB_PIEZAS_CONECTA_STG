import textwrap
from io import BytesIO
import requests
from PIL import Image, ImageFont
from core.engine import draw_justified_text, formatear_precio

def render(draw, img, data_input, fonts, border_c, txt_c, path_fonts, row):
    # --- AJUSTE CRÍTICO: Desempaquetado exacto según el orden del __init__.py ---
    # El orden es: f_f, f_m, f_p, f_pv, f_ps, f_s_ind, f_l, f_s_fly
    f_f, f_m, f_p, f_pv, f_ps, f_s_ind, f_l, f_s_fly = fonts
    
    azul_oscuro = (10, 6, 60)
    amarillo_lc = (254, 215, 0)

    # 1. Fecha (Usa f_f cargada en el __init__)
    f_txt = str(row['Fecha_disponibilidad_flyer']).upper()
    wf = draw.textlength(f_txt, font=f_f)
    draw.rounded_rectangle([64, 235, 64+wf+35, 285], radius=10, outline=amarillo_lc, width=3)
    draw.text((64+(wf+35)//2, 260), f_txt, font=f_f, fill=amarillo_lc, anchor="mm")

    # 2. Configuración de Cuadrícula Dinámica
    num_prod = len(data_input)
    box_w, box_h = (456, 456) if num_prod <= 6 else (456, 375)
    img_size = 338 if num_prod <= 6 else 250
    gap_y = 30 if num_prod <= 6 else 15

    for i, (idx, p) in enumerate(data_input.iterrows()):
        if i >= 8: break
        xp = 64 + (i % 2) * (box_w + 40)
        yp = 340 + (i // 2) * (box_h + gap_y)
        
        # Caja de producto
        draw.rounded_rectangle([xp, yp, xp+box_w, yp+box_h], radius=15, fill=(255,255,255), outline=border_c, width=2)
        
        # Imagen del producto
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            pi_res = requests.get(p['Foto del producto calado'], headers=headers, timeout=10)
            pi = Image.open(BytesIO(pi_res.content)).convert("RGBA")
            pi.thumbnail((img_size, img_size), Image.Resampling.LANCZOS)
            img.paste(pi, (int(xp + (box_w - pi.width) // 2), int(yp + 20)), pi)
        except: pass

        # Formateo de precio con la función del core/engine.py
        p_val = formatear_precio(p['Precio desc'])
        cl, cr = xp + 114, xp + 342
        
        # Marca (Usamos tamaño 18 fijo para Flyer)
        f_marca_fly = ImageFont.truetype(f"{path_fonts}/HurmeGeometricSans1 Bold.otf", 18)
        draw.text((cl, yp + box_h - 86), p['Marca'], font=f_marca_fly, fill=azul_oscuro, anchor="mm")
        
        # Nombre del producto (2 líneas máximo)
        y_nombre = yp + box_h - 61
        for ln in textwrap.wrap(str(p['Nombre del producto']), width=18)[:2]:
            draw.text((cl, y_nombre), ln, font=f_p, fill=azul_oscuro, anchor="mm")
            y_nombre += 20
        
        # Precio centrado dinámicamente con la coma
        y_precio = yp + box_h - 57
        # Medimos el ancho total incluyendo la coma para que el centrado sea perfecto
        tw_p = draw.textlength("S/", font=f_ps) + draw.textlength(p_val, font=f_pv) + 8
        px_inicio_precio = cr - tw_p // 2
        
        draw.text((px_inicio_precio, y_precio), "S/", font=f_ps, fill=azul_oscuro, anchor="lm")
        draw.text((px_inicio_precio + draw.textlength("S/", font=f_ps) + 8, y_precio), p_val, font=f_pv, fill=azul_oscuro, anchor="lm")
        
        # SKU (Usa f_s_fly definido en el __init__)
        draw.text((cr, yp + box_h - 22), str(p['SKU']), font=f_s_fly, fill=azul_oscuro, anchor="mm")

    # 3. Legales con justificado profesional
    y_legales = 1815
    f_l_bold = ImageFont.truetype(f"{path_fonts}/HurmeGeometricSans1 Bold.otf", 16)
    tit_legal = "CONDICIONES GENERALES: "
    ancho_negrita = draw.textlength(tit_legal, font=f_l_bold)
    
    draw.text((64, y_legales), tit_legal, font=f_l_bold, fill=txt_c)
    
    # Llamamos a la función del motor central core/engine.py
    draw_justified_text(
        draw, 
        str(row['Legales']), 
        f_l, 
        y_start=y_legales, 
        x_start=64, 
        x_end=1016, 
        fill=txt_c, 
        line_spacing=2, 
        prefix_width=ancho_negrita
    )