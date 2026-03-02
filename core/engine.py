from PIL import ImageFont
import math

def formatear_precio(valor):
    """Lógica universal para la coma de miles."""
    try:
        return "{:,}".format(int(float(str(valor).strip())))
    except:
        return str(valor)

def draw_justified_text(draw, text, font, y_start, x_start, x_end, fill, line_spacing=5, prefix_width=0, auto_bold=False):
    """
    Función Universal: Soporta prefijo manual (LC) o negrita automática (EFE).
    """
    available_w = x_end - x_start
    if text.startswith("CONDICIONES GENERALES"):
        text = text.replace("CONDICIONES GENERALES:", "").strip()
    
    try:
        # Intentamos cargar la negrita para el auto_bold de EFE
        font_bold = ImageFont.truetype(font.path.replace("Regular", "SemiBold"), font.size)
    except:
        font_bold = font

    words = text.split()
    lines = []; current_line = []; current_w = prefix_width 

    for word in words:
        # Detecta si debe aplicar negrita a las 2 primeras palabras (Lógica EFE)
        is_bold = (auto_bold and len(lines) == 0 and len(current_line) <= 1)
        word_font = font_bold if is_bold else font
        word_w = draw.textlength(word + " ", font=word_font)
        if current_w + word_w <= available_w:
            current_line.append(word); current_w += word_w
        else:
            lines.append(current_line); current_line = [word]
            current_w = draw.textlength(word + " ", font=font)
    lines.append(current_line)

    y = y_start
    for i, line_words in enumerate(lines):
        if not line_words: continue
        line_x_start = x_start + (prefix_width if i == 0 else 0)
        line_available_w = available_w - (prefix_width if i == 0 else 0)
        total_text_w = sum(draw.textlength(w, font=font_bold if (auto_bold and i==0 and j<=1) else font) for j, w in enumerate(line_words))
        num_spaces = len(line_words) - 1
        target_space_w = (line_available_w - total_text_w) / num_spaces if num_spaces > 0 else 0

        curr_x = line_x_start
        for j, word in enumerate(line_words):
            current_font = font_bold if (auto_bold and i == 0 and j <= 1) else font
            draw.text((curr_x, y), word, font=current_font, fill=fill)
            if i < len(lines) - 1 and num_spaces > 0:
                curr_x += draw.textlength(word, font=current_font) + target_space_w
            else:
                curr_x += draw.textlength(word + " ", font=current_font)
        y += font.getbbox("Ay")[3] + line_spacing

def draw_dotted_line(draw, start, end, fill, width=2, gap=8):
    """Función de líneas punteadas para EFE."""
    curr_x, curr_y = start; dest_x, dest_y = end
    dx, dy = dest_x - curr_x, dest_y - curr_y
    dist = math.sqrt(dx**2 + dy**2)
    if dist == 0: return
    sx, sy = dx/dist, dy/dist
    for i in range(0, int(dist), gap * 2):
        s = (curr_x + sx * i, curr_y + sy * i)
        e = (curr_x + sx * (i + gap), curr_y + sy * (i + gap))
        draw.line([s, e], fill=fill, width=width)

def draw_efe_preciador(draw, x_center, y_center, text_s, text_price, f_ps, f_pv, scale=1.0, tracking=-2, padding_h=20):
    """Recuadro naranja para EFE."""
    num_w = sum(draw.textlength(char, font=f_pv) + tracking for char in text_price) - tracking
    sym_w = draw.textlength(text_s, font=f_ps)
    full_w = sym_w + (8 * scale) + num_w
    h = int(f_pv.size * 1.2 * scale)
    p_h = padding_h * scale
    draw.rounded_rectangle([x_center - full_w//2 - p_h, y_center - h//2, x_center + full_w//2 + p_h, y_center + h//2], radius=15, fill="#FFA002")
    draw.text((x_center - full_w//2, y_center), text_s, font=f_ps, fill=(255,255,255), anchor="lm")
    curr_x = x_center - full_w//2 + sym_w + (8 * scale)
    for char in text_price:
        draw.text((curr_x, y_center), char, font=f_pv, fill=(255,255,255), anchor="lm")
        curr_x += draw.textlength(char, font=f_pv) + tracking