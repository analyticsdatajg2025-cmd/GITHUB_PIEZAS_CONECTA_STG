import os
from PIL import ImageFont
from . import flyer, story, ppl, display
from core.engine import formatear_precio

def process_lc(row, draw, img, path_fonts, is_flyer=False, data_input=None):
    formato = str(row['Formato']).upper().strip()
    # [cite_start]Detectamos la versión de color para LC [cite: 96]
    color_version = "AZUL" if "AZUL" in str(row.get('Color', '')) else "AMARILLO"
    
    # [cite_start]Colores base según tu diseño original [cite: 96]
    txt_c = (0,0,0) if color_version == "AMARILLO" else (255,255,255)
    border_c = (254, 215, 0) if color_version == "AMARILLO" else (10, 6, 60)
    precio_val = formatear_precio(row['Precio desc'])

    try:
        # [cite_start]--- CARGA DE FUENTES CON TAMAÑOS EXACTOS [cite: 98-103] ---
        f_f = ImageFont.truetype(f"{path_fonts}/HurmeGeometricSans1 Bold.otf", 24)
        f_s_fly = None 

        if formato == "STORY":
            f_m = ImageFont.truetype(f"{path_fonts}/HurmeGeometricSans1 Bold.otf", 53)
            f_p = ImageFont.truetype(f"{path_fonts}/HurmeGeometricSans1 Bold.otf", 32)
            f_pv = ImageFont.truetype(f"{path_fonts}/HurmeGeometricSans1 Bold.otf", 106)
            f_ps = ImageFont.truetype(f"{path_fonts}/HurmeGeometricSans1 Bold.otf", 42)
            f_s_ind = ImageFont.truetype(f"{path_fonts}/HurmeGeometricSans1.otf", 18)
            f_l = ImageFont.truetype(f"{path_fonts}/HurmeGeometricSans1.otf", 14)
        elif formato == "PPL":
            f_m = ImageFont.truetype(f"{path_fonts}/HurmeGeometricSans1 Bold.otf", 43)
            f_p = ImageFont.truetype(f"{path_fonts}/HurmeGeometricSans1 Bold.otf", 23)
            f_pv = ImageFont.truetype(f"{path_fonts}/HurmeGeometricSans1 Bold.otf", 85)
            f_ps = ImageFont.truetype(f"{path_fonts}/HurmeGeometricSans1 Bold.otf", 36)
            f_s_ind = ImageFont.truetype(f"{path_fonts}/HurmeGeometricSans1.otf", 14)
            f_l = ImageFont.truetype(f"{path_fonts}/HurmeGeometricSans1.otf", 13)
        elif formato == "FLYER":
            f_pv = ImageFont.truetype(f"{path_fonts}/HurmeGeometricSans1 Bold.otf", 73) 
            f_s_fly = ImageFont.truetype(f"{path_fonts}/HurmeGeometricSans1.otf", 13)    
            f_l = ImageFont.truetype(f"{path_fonts}/HurmeGeometricSans1.otf", 16)
            f_p = ImageFont.truetype(f"{path_fonts}/HurmeGeometricSans1 Bold.otf", 18)
            f_ps = ImageFont.truetype(f"{path_fonts}/HurmeGeometricSans1 Bold.otf", 30)
            f_m = f_s_ind = f_f 
        else: # DISPLAY
            f_m = ImageFont.truetype(f"{path_fonts}/HurmeGeometricSans1 Bold.otf", 34)
            f_p = ImageFont.truetype(f"{path_fonts}/HurmeGeometricSans1 Bold.otf", 20)
            f_pv = ImageFont.truetype(f"{path_fonts}/HurmeGeometricSans1 Bold.otf", 75)
            f_ps = ImageFont.truetype(f"{path_fonts}/HurmeGeometricSans1 Bold.otf", 30)
            f_s_ind = ImageFont.truetype(f"{path_fonts}/HurmeGeometricSans1.otf", 13)
            f_l = ImageFont.truetype(f"{path_fonts}/HurmeGeometricSans1.otf", 9)
    except: 
        f_m = f_p = f_pv = f_ps = f_s_ind = f_s_fly = f_f = f_l = ImageFont.load_default()

    # --- EMPAQUETADO DE FUENTES PARA LOS MÓDULOS ---
    fonts_list = [f_f, f_m, f_p, f_pv, f_ps, f_s_ind, f_l, f_s_fly]
    colors = {'txt': txt_c, 'border': border_c}

    # [cite_start]--- DESPACHO A RENDERIZADO [cite: 104, 117, 124, 132] ---
    if formato == "FLYER":
        flyer.render(draw, img, data_input, fonts_list, border_c, txt_c, path_fonts, row)
    elif formato == "DISPLAY":
        display.render(draw, row, fonts_list, colors, precio_val, path_fonts)
    elif formato == "STORY":
        story.render(draw, row, fonts_list, colors, precio_val, path_fonts)
    elif formato == "PPL":
        ppl.render(draw, row, fonts_list, colors, precio_val, path_fonts)
    
    # --- GUARDADO Y RETORNO DE URL ---
    # Importamos RAW_URL del main para mantener la consistencia
    from main import RAW_URL
    fname = f"{row['SKU'] or row['ID_Flyer']}_{formato}_{color_version}.jpg"
    img.save(f"output/{fname}", quality=95)
    
    return f"{RAW_URL}{fname}", color_version