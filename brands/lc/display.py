import textwrap
from PIL import ImageFont
from core.engine import draw_justified_text

def render(draw, row, fonts, colors, precio_val, path_fonts):
    # --- DESEMPAQUETADO DE FUENTES ---
    # El orden definido en __init__.py es: 
    # f_f, f_m, f_p, f_pv, f_ps, f_s_ind, f_l, f_s_fly
    f_f, f_m, f_p, f_pv, f_ps, f_s_ind, f_l, f_s_fly = fonts
    
    txt_c = colors['txt']
    
    # --- POSICIONAMIENTO DE TEXTOS ---
    cx, ny = 255, 245 
    
    # Marca
    draw.text((cx, 195), row['Marca'], font=f_m, fill=txt_c, anchor="mt")

    # Nombre del producto (Máximo 2 filas)
    lineas_nombre = textwrap.wrap(row['Nombre del producto'], width=22)[:2]
    for l in lineas_nombre:
        draw.text((cx, ny), l, font=f_p, fill=txt_c, anchor="mt")
        ny += 27 

    # Precio desc (Centrado dinámico con coma)
    # Medimos el ancho total incluyendo la coma para que el centrado sea perfecto
    tw = draw.textlength("S/", font=f_ps) + draw.textlength(precio_val, font=f_pv) + 15
    px = cx - tw//2
    
    draw.text((px, ny + 55), "S/ ", font=f_ps, fill=txt_c, anchor="lm")
    draw.text((px + draw.textlength("S/ ", font=f_ps) + 15, ny + 55), precio_val, font=f_pv, fill=txt_c, anchor="lm")
    
    # SKU
    draw.text((cx, ny + 100), str(row['SKU']), font=f_s_ind, fill=txt_c, anchor="mt")

    # --- CONFIGURACIÓN DE LEGALES ---
    # Cargamos la negrita para el título de legales
    f_l_bold = ImageFont.truetype(f"{path_fonts}/HurmeGeometricSans1 Bold.otf", 9)
    tit_legal = "CONDICIONES GENERALES: "
    ancho_negrita = draw.textlength(tit_legal, font=f_l_bold)
    
    # Dibujamos el título
    draw.text((40, 485), tit_legal, font=f_l_bold, fill=txt_c)
    
    # Llamamos a la función de motor central para el cuerpo justificado
    # Usamos prefix_width para que el texto empiece después del título
    draw_justified_text(
        draw, 
        str(row['Legales']), 
        f_l, 
        y_start=485, 
        x_start=40, 
        x_end=960, 
        fill=txt_c, 
        line_spacing=2, 
        prefix_width=ancho_negrita
    )