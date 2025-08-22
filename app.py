from PIL import Image
from functions import *
import pyautogui

# Get original image information
originalName = input("Original Image (include extension): ")
originalImage = Image.open(f"./media/{originalName}").convert("RGB")
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
    while True:
        if input("Hover over color and press Enter to add, or type text and Enter to finish") != "":
            break
        cursorX, cursorY = pyautogui.position()
        originalColor = pyautogui.screenshot().getpixel((cursorX, cursorY))
        palletColors.add(originalColor)
        print(f"added color {originalColor}")
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