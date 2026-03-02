import textwrap
from PIL import ImageFont
from core.engine import draw_justified_text

def render(draw, row, fonts, colors, precio_val, path_fonts):
    # --- DESEMPAQUETADO DE FUENTES ---
    # El orden definido en __init__.py es: 
    # f_f, f_m, f_p, f_pv, f_ps, f_s_ind, f_l, f_s_fly
    f_f, f_m, f_p, f_pv, f_ps, f_s_ind, f_l, f_s_fly = fonts
    
    txt_c = colors['txt']
    
    # --- POSICIONAMIENTO DE TEXTOS (MARCA Y PRODUCTO) ---
    # Story usa x=150 y y=1482 para textos [cite: 124, 125]
    cx_textos = 150 
    anchor_y_textos = 1482 

    # Marca
    draw.text((cx_textos, anchor_y_textos), row['Marca'], font=f_m, fill=txt_c, anchor="lt")
    
    # Nombre del producto (2 filas máximo)
    ny = anchor_y_textos + 65 
    for l in textwrap.wrap(row['Nombre del producto'], width=22)[:2]:
        draw.text((cx_textos, ny), l, font=f_p, fill=txt_c, anchor="lt")
        ny += 40 

    # --- POSICIONAMIENTO DE PRECIO (DERECHA) ---
    # Story usa el eje x=810 y y=1540 para el bloque de precio [cite: 126, 127]
    anchor_y_precio = 1540 
    espacio_entre_simbolo = 20
    
    # Medimos el ancho total incluyendo la coma para un centrado perfecto
    tw = draw.textlength("S/", font=f_ps) + draw.textlength(precio_val, font=f_pv) + espacio_entre_simbolo
    
    # Eje x=810 para centrar el bloque de precio
    px_bloque_completo = 810 - tw//2
    
    # Dibujo de S/ y Precio (anchor "ls" para nivelar el ras) [cite: 128]
    draw.text((px_bloque_completo, anchor_y_precio), "S/", font=f_ps, fill=txt_c, anchor="ls")
    
    # Posición X del número con el nuevo espacio reducido
    px_numero = px_bloque_completo + draw.textlength("S/", font=f_ps) + espacio_entre_simbolo
    draw.text((px_numero, anchor_y_precio), precio_val, font=f_pv, fill=txt_c, anchor="ls")

    # --- SKU ---
    # Centrado en el eje 810, bajando relativo al precio [cite: 129]
    draw.text((810, anchor_y_precio + 40), str(row['SKU']), font=f_s_ind, fill=txt_c, anchor="mt") 

    # --- CONFIGURACIÓN DE LEGALES ---
    # Cargamos la negrita para Story (tamaño 14) [cite: 129]
    f_l_bold = ImageFont.truetype(f"{path_fonts}/HurmeGeometricSans1 Bold.otf", 14)
    tit_legal = "CONDICIONES GENERALES: "
    ancho_negrita = draw.textlength(tit_legal, font=f_l_bold)
    
    # Dibujo del título en y=1802 [cite: 130, 131]
    draw.text((65, 1802), tit_legal, font=f_l_bold, fill=txt_c)

    # Llamamos a la función de motor central para el cuerpo justificado
    draw_justified_text(
        draw, 
        str(row['Legales']), 
        f_l, 
        y_start=1802, 
        x_start=65, 
        x_end=1015, 
        fill=txt_c, 
        line_spacing=2, 
        prefix_width=ancho_negrita
    )