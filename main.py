from PIL import Image

def paste_images(background, paste, x, y):
    new_image = Image.new("RGBA", background.size)

    new_image.paste(background, (0, 0))
    new_image.paste(paste, (x, y), mask=paste)

    return new_image

# Open the image
image = Image.open("input.png")

# Define the tile size and spacing
tile_size = 16
spacing = 2

# Calculate the number of tiles horizontally and vertically
num_tiles_horizontal = image.width // tile_size
num_tiles_vertical = image.height // tile_size

# Calculate the new image size with spacing
new_width = (num_tiles_horizontal * (tile_size + spacing)) + spacing
new_height = (num_tiles_vertical * (tile_size + spacing)) + spacing

# Create a new image with the required size and RGBA mode
new_image = Image.new("RGBA", (new_width, new_height))

# Iterate over the tiles and move them with spacing
for i in range(num_tiles_horizontal):
    for j in range(num_tiles_vertical):
        x = i * tile_size
        y = j * tile_size
        tile = image.crop((x, y, x + tile_size, y + tile_size))
        new_x = (i * (tile_size + spacing)) + spacing
        new_y = (j * (tile_size + spacing)) + spacing
        new_image.paste(tile, (new_x, new_y))

ox, oy = new_image.size
outline_image = new_image.crop((2, 2, ox-4, oy-4))

output_image = Image.new("RGBA", new_image.size, (0, 0, 0, 0))

output_image = paste_images(output_image, outline_image, 2, 1)#up
output_image = paste_images(output_image, outline_image, 2, 3)#down
output_image = paste_images(output_image, outline_image, 1, 2)#left
output_image = paste_images(output_image, outline_image, 3, 2)#right
output_image = paste_images(output_image, new_image, 0, 0)

#TODO: slope mask must be a rectangle

output_image.save("output1.png")