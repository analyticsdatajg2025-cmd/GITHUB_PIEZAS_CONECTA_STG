import os
import json
from datetime import datetime, timedelta
from core.sheets_manager import get_sheets_data
from brands.efe import process_efe
from brands.lc import process_lc

# --- CONFIGURACIÓN DE RUTAS (CRÍTICO: Los brands importan esto) ---
USER_GH = "analyticsdatajg2025-cmd"
REPO_GH = "GITHUB_PIEZAS_CONECTA_STG"
RAW_URL = f"https://raw.githubusercontent.com/{USER_GH}/{REPO_GH}/main/output/"

# 1. CARGA DE DATOS (Centralizada)
data, res_sheet, viejos = get_sheets_data()
os.makedirs('output', exist_ok=True)
h_lima = (datetime.now() - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M")
archivos_generados = 0 

print(f"🚀 Iniciando automatización. Filas en Excel: {len(data)}")

# --- CICLO 1: PRODUCTOS INDIVIDUALES (STORY, PPL, DISPLAY) ---
for idx, row in data.iterrows():
    tienda = str(row.get('Tienda', 'LC')).strip().upper()
    formato = str(row['Formato']).upper().strip()
    
    # Saltamos Flyers (ciclo 2) y filas vacías
    if formato in ["FLYER", "", "0"]: continue 

    tipo_diseno = str(row['Tipo de diseño']).strip()
    # LC puede tener Amarillo/Azul, EFE es único (Amarillo por defecto)
    versiones = ["AMARILLO", "AZUL"] if (tienda == "LC" and tipo_diseno == "DSCTOS POWER") else ["AMARILLO"]
    
    for v in versiones:
        llave = f"{row['SKU']}_{formato}_{tienda}_{v}".upper()
        
        if llave not in viejos:
            try:
                print(f"🎨 Generando {tienda} {formato}: {llave}")
                if tienda == "EFE":
                    # EFE siempre devuelve URL y color "N/A"
                    url = process_efe(row, is_flyer=False, color_version=v)
                    color_final = "N/A"
                else:
                    # LC devuelve URL y el color generado
                    url, color_final = process_lc(row, is_flyer=False, color_version=v)
                
                if url:
                    # Estructura unificada: Fecha, ID, Tienda, Diseño, Formato, Color, Link
                    res_sheet.append_row([h_lima, llave, tienda, tipo_diseno, formato, color_final, url])
                    archivos_generados += 1
            except Exception as e:
                print(f"❌ Error en {llave}: {e}")

# --- CICLO 2: FLYERS (MÚLTIPLES PRODUCTOS) ---
fly_g = data[data['Formato'].astype(str).str.upper().str.strip() == "FLYER"]
for id_f, group in fly_g.groupby('ID_Flyer'):
    if str(id_f) in ["0", "0.0", ""]: continue
    
    primera_fila = group.iloc[0]
    tienda = str(primera_fila.get('Tienda', 'LC')).strip().upper()
    tipo_diseno = str(primera_fila['Tipo de diseño']).strip()
    versiones = ["AZUL", "AMARILLO"] if (tienda == "LC" and tipo_diseno == "DSCTOS POWER") else ["AMARILLO"]
    
    for v in versiones:
        llave = f"{id_f}_FLYER_{tienda}_{v}".upper()
        
        if llave not in viejos:
            try:
                print(f"🎨 Generando Flyer {tienda}: {llave}")
                if tienda == "EFE":
                    url = process_efe(group, is_flyer=True, color_version=v)
                    color_final = "N/A"
                else:
                    url, color_final = process_lc(group, is_flyer=True, color_version=v)
                
                if url:
                    res_sheet.append_row([h_lima, llave, tienda, tipo_diseno, "FLYER", color_final, url])
                    archivos_generados += 1
            except Exception as e:
                print(f"❌ Error en Flyer {llave}: {e}")

# --- FINALIZACIÓN Y LOG PARA GITHUB ACTIONS ---
if archivos_generados == 0:
    print("⚠️ No hay piezas nuevas para generar.")
    with open("last_run.txt", "w") as f: 
        f.write(f"Sin cambios: {h_lima}")
else:
    print(f"✅ Proceso terminado. Se crearon {archivos_generados} archivos nuevos.")