import textwrap
from PIL import ImageFont
from core.engine import draw_justified_text

def render(draw, row, fonts, colors, precio_val, path_fonts):
    # --- DESEMPAQUETADO DE FUENTES ---
    # El orden definido en __init__.py es: 
    # f_f, f_m, f_p, f_pv, f_ps, f_s_ind, f_l, f_s_fly
    f_f, f_m, f_p, f_pv, f_ps, f_s_ind, f_l, f_s_fly = fonts
    
    txt_c = colors['txt']
    y_base, y_p = 850, 865

    # --- POSICIONAMIENTO DE PRECIO Y SKU (DERECHA) ---
    # Medimos el ancho total incluyendo la coma para un centrado perfecto
    tw_p = draw.textlength("S/", font=f_ps) + draw.textlength(precio_val, font=f_pv) + 15
    px_inicio_bloque = 820 - tw_p // 2 
    
    # Dibujo de S/ y Monto
    draw.text((px_inicio_bloque, y_p), "S/", font=f_ps, fill=txt_c, anchor="ls")
    draw.text((px_inicio_bloque + draw.textlength("S/", font=f_ps) + 15, y_p), precio_val, font=f_pv, fill=txt_c, anchor="ls")
    
    # SKU centrado bajo el bloque de precio
    draw.text((820, y_p + 30), str(row['SKU']), font=f_s_ind, fill=txt_c, anchor="mt") 

    # --- POSICIONAMIENTO DE TEXTOS (IZQUIERDA) ---
    # Marca
    draw.text((200, y_base), row['Marca'], font=f_m, fill=txt_c, anchor="ls")
    
    # Nombre del producto (2 líneas máximo)
    ny = y_base + 10 
    for l in textwrap.wrap(row['Nombre del producto'], width=25)[:2]:
        draw.text((200, ny), l, font=f_p, fill=txt_c, anchor="lt")
        ny += 30

    # --- CONFIGURACIÓN DE LEGALES ---
    # Cargamos la negrita para el título de legales (tamaño 13 según tu tabla)
    f_l_bold = ImageFont.truetype(f"{path_fonts}/HurmeGeometricSans1 Bold.otf", 13)
    tit_legal = "CONDICIONES GENERALES: "
    ancho_negrita = draw.textlength(tit_legal, font=f_l_bold)
    
    # Dibujo del título
    draw.text((50, 990), tit_legal, font=f_l_bold, fill=txt_c)
    
    # Llamamos a la función de motor central para el cuerpo justificado
    draw_justified_text(
        draw, 
        str(row['Legales']), 
        f_l, 
        y_start=990, 
        x_start=50, 
        x_end=1030, 
        fill=txt_c, 
        line_spacing=2, 
        prefix_width=ancho_negrita
    )