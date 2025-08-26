import pyautogui, traceback, sys
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

# Grab color on keypress
def grabColor(palletColors):
    cursorX, cursorY = pyautogui.position()
    grabbedColor = pyautogui.screenshot().getpixel((cursorX, cursorY))
    palletColors.add(grabbedColor)
    print(f"added color {grabbedColor}")

# Open an image relative to the media directory. will print an error and exit the program on error
def safeOpenImage(filepath):
    try:
        return Image.open(f"./media/{filepath}").convert("RGB")
    except FileNotFoundError:
        print(f"Image with that name was not found")
    except OSError:
        print("Image could not be opened")
    except Exception as e:
        print(f"Unexpected error: {type(e).__name__} - {e}")
        traceback.print_exc()
    sys.exit()

# Save the image passed, giving it the passed name. prints an error if one occurs and exits the program.
def safeSaveImage(image, name):
    try:
        image.save(f"./media/{name}.png")
        return
    except PermissionError:
        print("Permission denied. Cannot save image to './media/'.")
    except (OSError, ValueError) as e:
        print(f"Image could not be saved: {type(e).__name__} - {e}")
    except Exception as e:
        print(f"Unexpected error while saving: {type(e).__name__} - {e}")
        traceback.print_exc()
    sys.exit()