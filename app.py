from PIL import Image

# Calculate distance between original and pallet values (not sqrt as this doesn't affect which one will be smallest)
def getDistance(realColor, palletColor):
    realR, realG, realB = realColor
    palletR, palletG, palletB = palletColor
    return ((realR - palletR)**2 + (realB - palletB)**2 + (realG - palletG)**2)

# Get the pallet colors as a set
def getPallet(pallet):
    palletColors = set()
    pixels = pallet.load()
    width, height = pallet.size
    for x in range(width):
        for y in range(height):
            palletColors.add(pixels[x, y])
    return palletColors

original = Image.open("./media/Testx16.png").convert("RGB")
pixels = original.load()
width, height = original.size

palletImage = Image.open("./media/pallet.png").convert("RGB")


colors = getPallet(original)


# #Set grayscale
# for x in range(width):
#     for y in range(height):
#         r, g, b = pixels[x, y]
#         gray = int((r + g + b) / 3)
#         pixels[x, y] = (gray, gray, gray)

# original.save("./media/edited.png")