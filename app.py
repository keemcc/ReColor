from PIL import Image, UnidentifiedImageError
from functions import *
import keyboard, sys, traceback

# Get original image information
originalName = input("Original Image (include extension): ")
originalImage = safeOpenImage(originalName)

try:
    originalPixels = originalImage.load()
except (OSError, ValueError):
    print("Image data could not be loaded")
    sys.exit()
except Exception as e:
    print(f"Unexpected error: {type(e).__name__} - {e}")
    traceback.print_exc()
    sys.exit()

width, height = originalImage.size

# Get pallet
palletFilePrompt = input("Use Pallet Image File? ( Y / n ): ")
usePalletFile = True if palletFilePrompt.lower() == "y" else False
palletColors = set()
if usePalletFile:
    palletName = input("Pallet Image (include extension): ")
    palletImage = safeOpenImage(palletName)
    try:
        palletColors = getPallet(palletImage)
    except (UnidentifiedImageError, OSError):
        print("Image could not be opened")
        sys.exit()
    except Exception as e:
        print(f"Unexpected error: {type(e).__name__} - {e}")
        traceback.print_exc()
        sys.exit()
else:
    print("Press 'p' to add hovered color to pallet.\n Once done, press 'Escape' to complete pallet.")
    try:
        def safeGrab(event):
            try:
                grabColor(palletColors)
            except (OSError, ValueError):
                print("Screen capture failed or coordinates invalid")
            except Exception as e:
                print(f"Unexpected error in grabColor: {type(e).__name__} - {e}")
                traceback.print_exc()
        keyboard.on_press_key('p', safeGrab)
        keyboard.wait('esc')
        keyboard.unhook_all()
    except Exception as e:
        print(f"Unexpected error during keyboard handling: {type(e).__name__} - {e}")
        traceback.print_exc()
        sys.exit()
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
safeSaveImage(originalImage, editedName)