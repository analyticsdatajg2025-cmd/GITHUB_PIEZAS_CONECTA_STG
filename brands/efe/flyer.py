import textwrap
from core.engine import draw_justified_text, draw_efe_preciador, draw_dotted_line, formatear_precio

def render(draw, img, data_input, fonts, path_fonts, row, tipo):
    # 1. Renderizado de Fecha
    # Se utiliza la fuente f_f cargada en el orquestador [cite: 23]
    f_txt = str(row['Fecha_disponibilidad_flyer']).upper()
    w_f = draw.textlength(f_txt, font=fonts['f_f'])
    
    # Contenedor naranja para la fecha
    draw.rounded_rectangle([190, 244, 190 + w_f + 40, 284], radius=10, fill="#FFA002")
    draw.text((190 + (w_f + 40)//2, 264), f_txt, font=fonts['f_f'], fill=(255,255,255), anchor="mm")

    # 2. Bucle de procesamiento de productos (Cuadrícula dinámica) [cite: 26-37]
    for i, (idx, p) in enumerate(data_input.iterrows()):
        if i >= 8: break # Límite máximo de 8 productos por flyer
        
        # Coordenadas dinámicas de la cuadrícula
        xp = 65 + (i % 2) * 495
        yp = 350 + (i // 2) * 442 # Coordenada base Flyer EFE
        
        # Formateo automático de precio con coma de miles
        p_precio_fmt = formatear_precio(p['Precio desc'])
        cx_col1, cx_col2 = xp + 125, xp + 345

        # Renderizado de Marca y Nombre del producto
        draw.text((cx_col1, yp + 315), p['Marca'], font=fonts['f_m'], fill=(0,0,0), anchor="mm")
        y_n = yp + 345
        for line in textwrap.wrap(str(p['Nombre del producto']), width=18)[:4]:
            draw.text((cx_col1, y_n), line, font=fonts['f_p'], fill=(0,0,0), anchor="mm")
            y_n += 22

        # Lógica de Precios y SKU según el Tipo de Diseño
        if "EFERTON" in tipo:
            # Diseño con preciador naranja característico
            draw_efe_preciador(draw, cx_col2, yp + 325, "S/", p_precio_fmt, fonts['f_ps'], fonts['f_pv'], scale=0.9, padding_h=10)
            draw.text((cx_col2 + 8, yp + 375), str(p['SKU']), font=fonts['f_s_ind'], fill=(0,0,0), anchor="mm")
        else:
            # Diseño de Precio Irresistible (Texto naranja sin fondo)
            w_s = draw.textlength("S/", font=fonts['f_ps'])
            w_num = draw.textlength(p_precio_fmt, font=fonts['f_pv'])
            x_ini = cx_col2 - ((w_s + 5 + w_num) // 2)
            draw.text((x_ini, yp + 342), "S/", font=fonts['f_ps'], fill="#FFA002", anchor="ls")
            draw.text((x_ini + w_s + 5, yp + 342), p_precio_fmt, font=fonts['f_pv'], fill="#FFA002", anchor="ls")
            draw.text((cx_col2 + 8, yp + 367), str(p['SKU']), font=fonts['f_s_ind'], fill=(0,0,0), anchor="mm")

        # Dibujo de divisores punteados entre productos 
        line_c = "#00ACDE" if "EFERTON" in tipo else "#0A74DA"
        if i % 2 == 0 and (i + 1) < len(data_input): 
            draw_dotted_line(draw, (xp + 475, yp + 20), (xp + 475, yp + 410), line_c)

    # 3. Bloque de Legales (Justificado automático con negrita para EFE)
    draw_justified_text(
        draw, 
        str(row['Legales']), 
        fonts['f_l'], 
        y_start=1835, 
        x_start=70, 
        x_end=1010, 
        fill=(255,255,255), 
        auto_bold=True
    )