import os
from PIL import ImageFont
from . import flyer, story, ppl, display
from core.engine import formatear_precio

def process_efe(data_input, is_flyer=False, color_version="AMARILLO"):
    # Detectamos si es fila única o grupo (Flyer)
    row = data_input.iloc[0] if is_flyer else data_input
    formato = str(row['Formato']).upper().strip()
    tipo = str(row['Tipo de diseño']).upper().strip()
    path_fonts = f"TIPOGRAFIA/EFE"
    
    # 1. Preparación de datos
    precio_val = formatear_precio(row['Precio desc'])

    # 2. Carga de fuentes Poppins (Tamaños exactos EFE) [cite: 18-22]
    try:
        p_size = 90; s_size = 35; l_size = 10
        if formato == "DISPLAY": p_size = 60; s_size = 30; l_size = 8
        elif formato == "STORY": p_size = 100; s_size = 40
        elif formato == "FLYER": p_size = 50; s_size = 25

        fonts = {
            'f_m': ImageFont.truetype(f"{path_fonts}/Poppins-Medium.ttf", 44 if formato == "STORY" else 32),
            'f_p': ImageFont.truetype(f"{path_fonts}/Poppins-Medium.ttf", 30 if formato == "STORY" else 20),
            'f_pv': ImageFont.truetype(f"{path_fonts}/Poppins-ExtraBold.ttf", p_size),
            'f_ps': ImageFont.truetype(f"{path_fonts}/Poppins-ExtraBold.ttf", s_size),
            'f_s_ind': ImageFont.truetype(f"{path_fonts}/Poppins-Regular.ttf", 18 if formato == "STORY" else 15),
            'f_l': ImageFont.truetype(f"{path_fonts}/Poppins-Regular.ttf", l_size),
            'f_f': ImageFont.truetype(f"{path_fonts}/Poppins-Medium.ttf", 26)
        }
    except:
        fonts = {k: ImageFont.load_default() for k in ['f_m','f_p','f_pv','f_ps','f_s_ind','f_l','f_f']}

    # --- LÓGICA DE FONDO (Similar a LC pero para EFE) ---
    from PIL import Image, ImageDraw
    f_names = [f"EFE - {tipo} - {formato}", f"EFE - REPOWER {tipo} - {formato}"]
    path_fondos = f"FONDOS/EFE/{tipo}"
    full_p = next((os.path.join(path_fondos, f"{v}{e}") for v in f_names for e in [".jpg", ".png", ".JPG"] if os.path.exists(os.path.join(path_fondos, f"{v}{e}"))), None)
    
    if not full_p: return None
    img = Image.open(full_p).convert("RGB"); draw = ImageDraw.Draw(img)

    # 3. Renderizado según formato [cite: 23, 40, 56, 70]
    if formato == "FLYER":
        flyer.render(draw, img, data_input, fonts, path_fonts, row, tipo)
    elif formato == "DISPLAY":
        display.render(draw, row, fonts, precio_val, tipo)
    elif formato == "STORY":
        story.render(draw, row, fonts, precio_val, tipo, path_fonts)
    elif formato == "PPL":
        ppl.render(draw, row, fonts, precio_val, tipo, path_fonts)
    
    # 4. Guardado y Retorno (Centralizado para orden) 
    from main import RAW_URL
    fname = f"{row['SKU'] or row['ID_Flyer']}_{formato}_EFE.jpg"
    img.save(f"output/{fname}", quality=95)
    
    return f"{RAW_URL}{fname}"