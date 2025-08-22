from PIL import Image

# Calculate distance between original and pallet values (not sqrt as this doesn't affect which will be smallest)
def getDistance(realColor, palletColor):
    realR, realG, realB = realColor
    palletR, palletG, palletB = palletColor
    return ((realR - palletR)**2 + (realB - palletB)**2 + (realG - palletG)**2)

# Get the closest color match to the real (original)
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
def getPallet(palletImage):
    palletColors = set()
    pixels = palletImage.load()
    width, height = palletImage.size
    for x in range(width):
        for y in range(height):
            palletColors.add(pixels[x, y])
    return palletColors