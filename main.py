import os
from PIL import Image

def paste_images(background, paste, x, y):
    new_image = Image.new("RGBA", background.size)

    new_image.paste(background, (0, 0))
    new_image.paste(paste, (x, y), mask=paste)

    return new_image

# Open the tileset input image
image = Image.open("input.png")

tile_size = 16
spacing = 2
total_tile_size = tile_size + spacing

num_tiles_horizontal = image.width // tile_size
num_tiles_vertical = image.height // tile_size

print(num_tiles_vertical)
print(num_tiles_horizontal)

new_width = (num_tiles_horizontal * (tile_size + spacing)) + spacing
new_height = (num_tiles_vertical * (tile_size + spacing)) + spacing

new_image = Image.new("RGBA", (new_width, new_height))


for i in range(num_tiles_horizontal):
    for j in range(num_tiles_vertical):
        x = i * tile_size
        y = j * tile_size
        tile = image.crop((x, y, x + tile_size, y + tile_size))
        new_x = (i * (tile_size + spacing)) + spacing
        new_y = (j * (tile_size + spacing)) + spacing
        new_image.paste(tile, (new_x, new_y))


ox, oy = new_image.size
outline_image = new_image.crop((spacing, spacing, ox-spacing, oy-spacing))


outline_image.save("outline.png")
tiles_with_empty_pixels = []

if not os.path.exists("tiles"):
    os.makedirs("tiles")

# Iterate over each tile
for j in range(num_tiles_vertical):
    for i in range(num_tiles_horizontal):
        x = i * total_tile_size
        y = j * total_tile_size

        tile = outline_image.crop((x, y, x + tile_size, y + tile_size))
        tile.save(f"tiles/tile_{int(x/total_tile_size)}_{int(y/total_tile_size)}.png")

        # Check if the tile has any empty pixels
        empty_pixel_found = False
        for pixel in tile.getdata():
            if pixel[3] == 0: 
                empty_pixel_found = True
                break

        if empty_pixel_found:
            tiles_with_empty_pixels.append((i, j))


print("Tiles with empty pixels:")
print(tiles_with_empty_pixels)

output_image = Image.new("RGBA", new_image.size, (0, 0, 0, 0))

# Outline adding

output_image = paste_images(output_image, outline_image, 1, 1)# up left 
output_image = paste_images(output_image, outline_image, 3, 1)# up right
output_image = paste_images(output_image, outline_image, 3, 3)# down right
output_image = paste_images(output_image, outline_image, 1, 3)# down left

output_image = paste_images(output_image, outline_image, 2, 1)# up
output_image = paste_images(output_image, outline_image, 2, 3)# down
output_image = paste_images(output_image, outline_image, 1, 2)# left
output_image = paste_images(output_image, outline_image, 3, 2)# right


output_image = paste_images(output_image, new_image, 0, 0)

output_image.save("output1.png")