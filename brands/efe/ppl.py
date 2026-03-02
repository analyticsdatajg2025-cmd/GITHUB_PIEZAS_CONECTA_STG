import textwrap
from core.engine import draw_justified_text, draw_efe_preciador

def render(draw, row, fonts, precio_val, tipo, path_fonts):
    # Lógica de renderizado para Pieza Principal (Post)
    
    if "EFERTON" in tipo:
        # --- DISEÑO EFERTON (Centrado dinámico) ---
        # Marca alineada a la izquierda en la base del bloque
        draw.text((90, 930), row['Marca'], font=fonts['f_m'], fill=(255,255,255), anchor="ls")
        
        # Nombre del producto centrado (hasta 3 filas)
        ny = 890 if len(textwrap.wrap(str(row['Nombre del producto']), width=25)) > 1 else 900
        for line in textwrap.wrap(str(row['Nombre del producto']), width=25)[:3]:
            draw.text((500, ny), line, font=fonts['f_p'], fill=(255,255,255), anchor="mm")
            ny += 28
            
        # SKU posicionado relativo al final del nombre
        draw.text((500, ny + 5), str(row['SKU']), font=fonts['f_s_ind'], fill=(255,255,255), anchor="mm")
        
        # Preciador naranja fijo a la derecha
        draw_efe_preciador(draw, 840, 910, "S/", precio_val, fonts['f_ps'], fonts['f_pv'], scale=1.0, tracking=-3)
    
    else:
        # --- DISEÑO PRECIO IRRESISTIBLE (Columna izquierda) ---
        lx = 91
        # Marca fija
        draw.text((lx, 639), row['Marca'], font=fonts['f_m'], fill=(255,255,255), anchor="ls")
        
        # Nombre del producto dinámico (hasta 4 filas)
        ny = 675
        for lp in textwrap.wrap(row['Nombre del producto'], width=13)[:4]:
            draw.text((lx, ny), lp, font=fonts['f_p'], fill=(255,255,255), anchor="ls")
            ny += 30
            
        # SKU dinámico
        y_sku = ny + 10
        draw.text((lx, y_sku), str(row['SKU']), font=fonts['f_s_ind'], fill=(255,255,255), anchor="ls")
        
        # LÓGICA DE SEGURIDAD PARA EL PRECIO:
        # El precio baja si el nombre del producto empuja el SKU hacia abajo
        py = max(830, y_sku + 80)
        
        w_s = draw.textlength("S/", font=fonts['f_ps'])
        draw.text((lx, py), "S/", font=fonts['f_ps'], fill=(255,255,255), anchor="ls")
        draw.text((lx + w_s + 10, py), precio_val, font=fonts['f_pv'], fill=(255,255,255), anchor="ls")

    # Legales con justificado y auto_bold para Poppins
    # Las coordenadas X cambian según si es Eferton o Irresistible
    draw_justified_text(
        draw, 
        str(row['Legales']), 
        fonts['f_l'], 
        y_start=998, 
        x_start=90 if "EFERTON" in tipo else 73, 
        x_end=990 if "EFERTON" in tipo else 1007, 
        fill=(255,255,255), 
        auto_bold=True
    )