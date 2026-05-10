import os
from PIL import Image, ImageDraw, ImageFont

# --- Configuración de Archivos y Carpetas ---
# Asegúrate de tener estas carpetas y archivos en tu proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(BASE_DIR, "fonts")
IMAGES_DIR = os.path.join(BASE_DIR, "images")

# Nombres de archivos de recursos (Añade los tuyos aquí)
FONT_SCRIPT_FILE = "script_font.ttf"  # Descarga una fuente manuscrita elegante
FONT_SERIF_FILE = "serif_font.ttf"    # Descarga una fuente serif bonita
IMAGE_BACKGROUND_FILE = "background.png"  # PNG de textura de acuarela suave
IMAGE_WREATH_FILE = "wreath.png"          # PNG transparente de la corona floral

# --- Configuración del Diseño ---
CARD_SIZE = (1200, 1600)  # Ancho x Alto (en píxeles)
BACKGROUND_COLOR = (255, 255, 255) # Color de fondo base

# Color dorado aproximado en Hex (para el texto)
GOLD_COLOR_HEX = "#B38F6A"

# --- Configuración de Texto (Personalizable) ---
FECHA = "10 DE MAYO"
TITULO_1 = "PARA EL AMOR"
TITULO_2 = "Amor de mi vida"
SUBTITULO = "Hoy y siempre"
MENSAJE_FINAL = "Gracias por existir"

def hex_to_rgb(hex_color):
    """Convierte un código de color hex a una tupla RGB."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def load_resource_image(filename):
    """Carga una imagen de recurso y maneja errores."""
    path = os.path.join(IMAGES_DIR, filename)
    if not os.path.exists(path):
        print(f"Error: No se encontró la imagen '{filename}' en '{IMAGES_DIR}'.")
        print("Por favor, añade tus propias imágenes de fondo y corona (PNG).")
        return None
    return Image.open(path)

def load_resource_font(filename, size):
    """Carga una fuente de recurso y maneja errores."""
    path = os.path.join(FONTS_DIR, filename)
    if not os.path.exists(path):
        print(f"Error: No se encontró la fuente '{filename}' en '{FONTS_DIR}'.")
        print("Por favor, añade tus propias fuentes (.ttf). Usando fuente por defecto.")
        return ImageFont.load_default()
    return ImageFont.truetype(path, size)

def center_text(draw, text, font, current_y, card_width, color):
    """Centra el texto horizontalmente en la tarjeta."""
    # En Pillow >= 9.2.0, textbbox es preferible a textsize
    if hasattr(draw, 'textbbox'):
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    else: # Para versiones antiguas de Pillow
        text_width, text_height = draw.textsize(text, font=font)

    text_x = (card_width - text_width) // 2
    draw.text((text_x, current_y), text, fill=color, font=font)
    return current_y + text_height

def generar_tarjeta():
    print("Iniciando generación de la tarjeta...")

    # 1. Crear lienzo base
    card = Image.new('RGB', CARD_SIZE, BACKGROUND_COLOR)
    draw = ImageDraw.Draw(card)
    text_color = hex_to_rgb(GOLD_COLOR_HEX)

    # 2. Cargar y superponer fondo de acuarela
    bg_img = load_resource_image(IMAGE_BACKGROUND_FILE)
    if bg_img:
        # Redimensionar el fondo para que cubra la tarjeta
        bg_img = bg_img.resize(CARD_SIZE, Image.Resampling.LANCZOS)
        card.paste(bg_img, (0, 0))

    # 3. Cargar y centrar la corona floral
    wreath_img = load_resource_image(IMAGE_WREATH_FILE)
    if wreath_img:
        # Redimensionar la corona si es necesario
        wreath_img.thumbnail((800, 800), Image.Resampling.LANCZOS)
        wreath_w, wreath_h = wreath_img.size
        wreath_x = (CARD_SIZE[0] - wreath_w) // 2
        wreath_y = (CARD_SIZE[1] - wreath_h) // 2
        
        # Usar la imagen como máscara para la transparencia
        card.paste(wreath_img, (wreath_x, wreath_y), wreath_img)

    # 4. Cargar Fuentes
    font_script_title = load_resource_font(FONT_SCRIPT_FILE, 100)
    font_serif_regular = load_resource_font(FONT_SERIF_FILE, 40)
    font_serif_date = load_resource_font(FONT_SERIF_FILE, 70)
    font_serif_small = load_resource_font(FONT_SERIF_FILE, 30)

    # 5. Escribir el Texto
    current_y = 100  # Margen superior inicial

    # Texto Superior (Pequeño)
    current_y = center_text(draw, TITULO_1, font_serif_regular, current_y, CARD_SIZE[0], text_color)
    current_y += 20  # Espaciado

    # Título (Grande, Manuscrito)
    current_y = center_text(draw, TITULO_2, font_script_title, current_y, CARD_SIZE[0], text_color)
    current_y += 50  # Espaciado grande antes de la corona

    # Ajustar Y para texto dentro de la corona (si se cargó)
    if wreath_img:
        current_y = wreath_y + (wreath_h // 2) - 80 # Centrar dentro de la corona
    else:
        current_y += 300 # Espaciado si no hay corona

    # Fecha (Grande, Serif)
    current_y = center_text(draw, FECHA, font_serif_date, current_y, CARD_SIZE[0], text_color)
    current_y += 10  # Espaciado

    # Subtítulo (Pequeño)
    current_y = center_text(draw, SUBTITULO, font_serif_regular, current_y, CARD_SIZE[0], text_color)

    # Mensaje Final (Abajo)
    current_y_bottom = CARD_SIZE[1] - 100  # Margen inferior
    center_text(draw, MENSAJE_FINAL, font_serif_small, current_y_bottom, CARD_SIZE[0], text_color)

    # 6. Guardar la imagen final
    output_path = os.path.join(BASE_DIR, "tarjeta_amor_final.png")
    card.save(output_path)
    print(f"¡Tarjeta generada con éxito en: {output_path}!")

if __name__ == "__main__":
    generar_tarjeta()
