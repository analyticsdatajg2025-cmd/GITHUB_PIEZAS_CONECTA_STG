import textwrap
from core.engine import draw_justified_text, draw_efe_preciador

def render(draw, row, fonts, precio_val, tipo):
    # Lógica común para ambos tipos de Display EFE [cite: 70]
    
    if "EFERTON" in tipo:
        # --- DISEÑO EFERTON (Centrado) --- [cite: 71, 75]
        cx = 260
        draw.text((cx, 250), row['Marca'], font=fonts['f_m'], fill=(255,255,255), anchor="mm")
        
        ny = 290
        for line in textwrap.wrap(str(row['Nombre del producto']), width=20)[:2]:
            draw.text((cx, ny), line, font=fonts['f_p'], fill=(255,255,255), anchor="mm")
            ny += 25
            
        y_sku = ny + 5
        draw.text((cx, y_sku), str(row['SKU']), font=fonts['f_s_ind'], fill=(255,255,255), anchor="mm")
        
        # El preciador naranja de Eferton centrado [cite: 75]
        y_precio = max(380, y_sku + 60)
        draw_efe_preciador(draw, cx, y_precio, "S/", precio_val, fonts['f_ps'], fonts['f_pv'], scale=1.0, tracking=-3)
    
    else:
        # --- DISEÑO PRECIO IRRESISTIBLE (Alineado a la izquierda) --- [cite: 77, 82]
        lx = 91
        draw.text((lx, 219), row['Marca'], font=fonts['f_m'], fill=(255,255,255), anchor="ls")
        
        ny = 255
        for lp in textwrap.wrap(row['Nombre del producto'], width=20)[:2]:
            draw.text((lx, ny), lp, font=fonts['f_p'], fill=(255,255,255), anchor="ls")
            ny += 25
            
        y_sku = ny + 5
        draw.text((lx, y_sku), str(row['SKU']), font=fonts['f_s_ind'], fill=(255,255,255), anchor="ls")
        
        # Precio dinámico a ras de texto [cite: 80, 82]
        y_precio = max(379, y_sku + 70)
        w_s = draw.textlength("s/", font=fonts['f_ps'])
        draw.text((lx, y_precio), "s/", font=fonts['f_ps'], fill=(255,255,255), anchor="ls")
        draw.text((lx + w_s + 10, y_precio), precio_val, font=fonts['f_pv'], fill=(255,255,255), anchor="ls")

    # Legales universales Display EFE con auto_bold activado para Poppins [cite: 83]
    draw_justified_text(
        draw, 
        str(row['Legales']), 
        fonts['f_l'], 
        y_start=485 if "EFERTON" in tipo else 490, 
        x_start=40, 
        x_end=960, 
        fill=(255,255,255), 
        auto_bold=True
    )