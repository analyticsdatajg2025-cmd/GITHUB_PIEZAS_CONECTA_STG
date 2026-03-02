import textwrap
from core.engine import draw_justified_text, draw_efe_preciador

def render(draw, row, fonts, precio_val, tipo, path_fonts):
    # Lógica de renderizado para formato STORY (9:16)
    
    if "EFERTON" in tipo:
        # --- DISEÑO EFERTON (Vertical con Preciador Naranja) ---
        ay = 1600
        # Marca
        draw.text((239, ay), row['Marca'], font=fonts['f_m'], fill=(255,255,255), anchor="ls")
        
        # Nombre del producto dinámico (hasta 4 líneas)
        ny = ay + 55
        for lp in textwrap.wrap(row['Nombre del producto'], width=20)[:4]:
            draw.text((239, ny), lp, font=fonts['f_p'], fill=(255,255,255), anchor="ls")
            ny += 45
            
        # SKU posicionado dinámicamente bajo el nombre
        draw.text((239, ny + 5), str(row['SKU']), font=fonts['f_s_ind'], fill=(255,255,255), anchor="ls")
        
        # Preciador naranja escalado a 1.1 para mayor visibilidad en Stories
        draw_efe_preciador(draw, 780, 1650, "S/", precio_val, fonts['f_ps'], fonts['f_pv'], scale=1.1, padding_h=30)
        
    else:
        # --- DISEÑO PRECIO IRRESISTIBLE (Vertical Texto Blanco) ---
        lx = 147
        # Marca
        draw.text((lx, 1563), row['Marca'], font=fonts['f_m'], fill=(255,255,255), anchor="ls")
        
        # Nombre del producto dinámico
        ny = 1615
        for lp in textwrap.wrap(row['Nombre del producto'], width=18)[:4]:
            draw.text((lx, ny), lp, font=fonts['f_p'], fill=(255,255,255), anchor="ls")
            ny += 42
            
        # SKU dinámico
        y_sku = ny + 10
        draw.text((lx, y_sku), str(row['SKU']), font=fonts['f_s_ind'], fill=(255,255,255), anchor="ls")
        
        # Precio alineado a ras de texto en la zona inferior derecha
        draw.text((566, 1658), "S/", font=fonts['f_ps'], fill=(255,255,255), anchor="ls")
        w_s = draw.textlength("S/", font=fonts['f_ps'])
        draw.text((566 + w_s + 15, 1658), precio_val, font=fonts['f_pv'], fill=(255,255,255), anchor="ls")

    # Bloque de Legales en la base de la historia (y=1800)
    # Se utiliza auto_bold=True para resaltar automáticamente "CONDICIONES GENERALES"
    draw_justified_text(
        draw, 
        str(row['Legales']), 
        fonts['f_l'], 
        y_start=1800, 
        x_start=70, 
        x_end=1010, 
        fill=(255,255,255), 
        auto_bold=True
    )