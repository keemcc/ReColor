import pyautogui, traceback, sys, keyboard, os, pickle
from PIL import Image

def savePalette(palette, path):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, "palette.pkl"), "wb") as file:
        pickle.dump(palette, file)

def loadPalette(path):
    with open(os.path.join(path, "palette.pkl"), "rb") as file:
        return pickle.load(file)


# Calculate the distance between two passed colors
#   This is done using the 3 respective (R, G, B) values passed in the color tuple and the 3 dimensional distance formula
#   Square root is not needed as the minimum distance is still found when calculating distance squared
def getDistance(color1, color2):
    red1, green1, blue1 = color1
    red2, green2, blue2 = color2
    return ((red1 - red2)**2 + (blue1 - blue2)**2 + (green1 - green2)**2)

# Gets the color from the pallet that is the closest to the original color
#   Returns the color with the minimum distance from the original color
def getClosestMatch(originalColor, palletColors):
    closestMatch = None
    matchDistance = None
    for palletColor in palletColors:
        currentDistance = getDistance(originalColor, palletColor)
        if (not closestMatch) or (currentDistance < matchDistance):
            closestMatch = palletColor
            matchDistance = currentDistance
    return closestMatch

# Get the pallet colors as a set
#   Load an image where all colors within the image will be added to a set and returned
def getPalette(palletImage):
    palletColors = set()
    pixels = palletImage.load()
    width, height = palletImage.size
    for x in range(width):
        for y in range(height):
            palletColors.add(pixels[x, y])
    return palletColors

# Grab color hovered by mouse and add it to the pallet
#   returns that grabbed color
def grabColor(palletColors):
    cursorX, cursorY = pyautogui.position()
    grabbedColor = pyautogui.screenshot().getpixel((cursorX, cursorY))
    palletColors.add(grabbedColor)
    print(f"Grabbed color {grabbedColor}")

# Open an image relative to the media directory
#   Print error message and exit the program on error
def safeOpenImage(filepath):
    try:
        return Image.open(filepath).convert("RGB")
    except FileNotFoundError:
        print(f"Image with that name was not found")
    except OSError:
        print("Image could not be opened")
    except Exception as e:
        print(f"Unexpected error: {type(e).__name__} - {e}")
        traceback.print_exc()
    sys.exit()

# Save the image passed, giving it the passed name
#   Prints an error if one occurs and exits the program
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

def runColorPicker(palletColors):
    print("Press 'p' to add hovered color to pallet.\n Once done, press 'Escape' to complete pallet.")
    keyboard.on_press_key('p', lambda e: grabColor(palletColors))
    keyboard.wait('esc')
    keyboard.unhook_all()