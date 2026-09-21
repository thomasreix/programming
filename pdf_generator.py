from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape

words = [
    "ASTEROID",
    "BAMBOO",
    "CALCULUS",
    "DOLPHIN",
    "EMERALD",
    "FRICTION",
    "GALLOP",
    "HORIZON",
    "IGLOO",
    "JUGGLING",
    "KEYBOARD",
    "LABYRINTH",
    "MARMALADE",
    "NEURON",
    "OBELISK",
    "PYRAMID",
    "QUICKSAND",
    "RESIN",
    "SCULPTURE",
    "TORNADO",
    "UKULELE",
    "VOLCANO",
    "WATERFALL",
    "YACHT",
    "ZODIAC",
]

width, height = landscape(A4)  # 842 x 595 points
c = canvas.Canvas("code-names.pdf", pagesize=(width, height))

cols = 5
rows = 5
cell_w = width / cols
cell_h = height / rows

c.setFont("Helvetica-Bold", 16)

for i, word in enumerate(words):
    col = i % cols
    row = i // cols
    x_center = col * cell_w + cell_w / 2
    y_mid = height - row * cell_h - cell_h / 2

    # Normal word (just above center)
    c.drawCentredString(x_center, y_mid + 4, word)

    # Upside-down word (just below center)
    c.saveState()
    c.translate(x_center, y_mid - 4)
    c.rotate(180)
    c.drawCentredString(0, 0, word)
    c.restoreState()

c.save()
print("PDF created: code-names.pdf (A4 landscape)")
