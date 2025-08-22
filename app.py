from PIL import Image

# Calculate distance between original and pallet values (not sqrt as this doesn't affect which one will be smallest)
def getDistance(realColor, palletColor):
    realR, realG, realB = realColor
    palletR, palletG, palletB = palletColor
    return ((realR - palletR)**2 + (realB - palletB)**2 + (realG - palletG)**2)

# Get the closest color match
def getClosestMatch(realColor, palletColors):
    closestMatch = None
    matchDistance = None
    for palletColor in palletColors:
        currentDistance = getDistance(realColor, palletColor)
        if (not closestMatch) or (currentDistance < matchDistance):
            closestMatch = palletColor
            matchDistance = currentDistance
    return closestMatch


# Get the pallet colors as a set
def getPallet(pallet):
    palletColors = set()
    pixels = pallet.load()
    width, height = pallet.size
    for x in range(width):
        for y in range(height):
            palletColors.add(pixels[x, y])
    return palletColors

originalImage = Image.open("./media/Testx16.png").convert("RGB")
palletImage = Image.open("./media/pallet.png").convert("RGB")
originalPixels = originalImage.load()
width, height = originalImage.size
palletColors = getPallet(palletImage)

colorMap = dict()

originalPixels = originalImage.load()
for x in range(width):
    for y in range(height):
        pixel = originalPixels[x, y]
        if pixel not in colorMap:
            colorMap[pixel] = getClosestMatch(pixel, palletColors)
        originalPixels[x, y] = colorMap[pixel]

originalImage.save("./media/edited.png")