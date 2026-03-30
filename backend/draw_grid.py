from PIL import Image, ImageDraw, ImageFont
import urllib.request
import os

img_path = 'c:/Users/Praveen/OneDrive/Desktop/navisphere-railway-station-resource-tracker-main/frontend/public/gadwal.png'
img = Image.open(img_path)
draw = ImageDraw.Draw(img)

# Image might be quite large, lets draw a grid of 10x10 blocks on coordinates (0-100, 0-100)
width, height = img.size

# We assume coordinates given are percentages (0-100) of width and height.
font = ImageFont.load_default()

for x_pct in range(0, 101, 10):
    x = int(x_pct * width / 100)
    draw.line([(x, 0), (x, height)], fill="red", width=2)
    draw.text((x+2, 5), str(x_pct), fill="red", font=font)

for y_pct in range(0, 101, 10):
    y = int(y_pct * height / 100)
    draw.line([(0, y), (width, y)], fill="blue", width=2)
    draw.text((5, y+2), str(y_pct), fill="blue", font=font)

# Draw some fine dots every 5%
for x_pct in range(0, 101, 5):
    for y_pct in range(0, 101, 5):
        x = int(x_pct * width / 100)
        y = int(y_pct * height / 100)
        draw.ellipse([x-2, y-2, x+2, y+2], fill="green")
        if x_pct % 10 != 0 and y_pct % 10 != 0:
            draw.text((x+5, y+5), f"{x_pct},{y_pct}", fill="green", font=font)

out_dir = 'c:/Users/Praveen/OneDrive/Desktop/navisphere-railway-station-resource-tracker-main/artifacts'
os.makedirs(out_dir, exist_ok=True)
img.save(f'{out_dir}/gadwal_grid.png')
print("Grid saved.")
