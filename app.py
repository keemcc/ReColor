from PIL import Image, UnidentifiedImageError
from functions import *
import keyboard
import sys

# Get original image information
originalName = input("Original Image (include extension): ")
try:
    originalImage = Image.open(f"./media/{originalName}").convert("RGB")
except FileNotFoundError:
    print(f"Image with the name \"{originalName}\" was not found")
    sys.exit()
except UnidentifiedImageError:
    print("Image could not be opened")
    sys.exit()

originalPixels = originalImage.load()
width, height = originalImage.size

# Get pallet
palletFilePrompt = input("Use Pallet Image File? ( Y / n ): ")
usePalletFile = True if palletFilePrompt.lower() == "y" else False
palletColors = set()
if usePalletFile:
    palletName = input("Pallet Image (include extension): ")
    palletImage = Image.open(f"./media/{palletName}").convert("RGB")
    palletColors = getPallet(palletImage)
else:
    print("Press 'p' to add hovered color to pallet.\n Once done, press 'Escape' to complete pallet.")
    keyboard.on_press_key('p', lambda e: grabColor(palletColors))
    keyboard.wait('esc')
    keyboard.unhook_all()
print(palletColors)

# Edit the image
colorMap = dict()
for x in range(width):
    for y in range(height):
        originalColor = originalPixels[x, y]
        if originalColor not in colorMap:
            colorMap[originalColor] = getClosestMatch(originalColor, palletColors)
        originalPixels[x, y] = colorMap[originalColor]

# Save the image
editedName = input("Please enter a name for the result: ")
originalImage.save(f"./media/{editedName}.png")