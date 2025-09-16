import pyautogui, traceback, sys, keyboard, os, pickle
from PIL import Image

# Saves passed palette set into a pickle at the passed path
#   If the path does not exist, it will be created
def savePalette(palette, path):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, "palette.pkl"), "wb") as file:
        pickle.dump(palette, file)

# Returns the palette stored within the pickle file at the given path
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

# Gets the color from the palette that is the closest to the original color
#   Returns the color with the minimum distance from the original color
def getClosestMatch(originalColor, paletteColors):
    closestMatch = None
    matchDistance = None
    for paletteColor in paletteColors:
        currentDistance = getDistance(originalColor, paletteColor)
        if (not closestMatch) or (currentDistance < matchDistance):
            closestMatch = paletteColor
            matchDistance = currentDistance
    return closestMatch

# Get the palette colors as a set
#   Load an image where all colors within the image will be added to a set and returned
def getPalette(paletteImage):
    paletteColors = set()
    pixels = paletteImage.load()
    width, height = paletteImage.size
    for x in range(width):
        for y in range(height):
            paletteColors.add(pixels[x, y])
    return paletteColors

# Grab color hovered by mouse and add it to the palette
#   returns that grabbed color
def grabColor(paletteColors):
    cursorX, cursorY = pyautogui.position()
    grabbedColor = pyautogui.screenshot().getpixel((cursorX, cursorY))
    paletteColors.add(grabbedColor)
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

# Runs the color picker, adding each picked color to the passed paletteColors set
#   Color picker lets user minimize terminal and pick any color within the screen the program is executed on
def runColorPicker(paletteColors):
    print("Press 'p' to add hovered color to palette.\n Once done, press 'Escape' to complete palette.")
    keyboard.on_press_key('p', lambda e: grabColor(paletteColors))
    keyboard.wait('esc')
    keyboard.unhook_all()