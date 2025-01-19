

from PIL import Image, ImageOps

# Bild laden
input_image = "/home/wolff/Bilder/Bildschirmfoto vom 2024-02-20 16-43-47.png"  # Pfad zu deinem Bild
output_image = "/home/wolff/Bilder/ausgabe_bild.jpg"

# Bild öffnen
img = Image.open(input_image)

# Zielgröße und Hintergrundfarbe festlegen
target_size = (250, 250)
background_color = (0, 49, 83)  # Preußisch Blau

# Bild mit weißem Rand erweitern
img_with_border = ImageOps.expand(img, border=(20, 20), fill=background_color)

# Zentrieren und auf Zielgröße bringen
img_with_border = ImageOps.pad(img_with_border, target_size, color=background_color)

# In RGB konvertieren, falls das Bild Transparenz hat
if img_with_border.mode == 'RGBA':
    img_with_border = img_with_border.convert('RGB')

# Ergebnis speichern
img_with_border.save(output_image, format="JPEG")

print(f"Das Bild wurde erfolgreich auf {target_size} skaliert und gespeichert als {output_image}")
