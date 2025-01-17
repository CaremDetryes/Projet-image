from PIL import Image,ImageFilter
import sys
  
# def imageToMap(img):
#     img.filter(ImageFilter.GaussianBlur(radius=4))

def imageOverlay(img_list):
    l = len(img_list)
    (n,m) = img_list[l-1].size
    
    resizeImageList(img_list, (n,m))
    overlayMap = Image.new(mode="RGBA",size=(n,m))
    for x in range(n):
        sys.stdout.write(f"\rColoriage : {x + 1} / {n}")
        for y in range(n):
            color = sumPixel((x,y),img_list)
            overlayMap.putpixel((x,y), color)
    print()
    return overlayMap

def sumPixel(coordonnees, img_list):
    x, y = coordonnees
    r, g, b, a = 0, 0, 0, 0  # Initialisation des accumulateurs

    for i in range(len(img_list)-1):
        pixel = img_list[i].getpixel((x, y))
        r += int(pixel[0] // (2 ** i))
        g += int(pixel[1] // (2 ** i))
        b += int(pixel[2] // (2 ** i))
        a += int(pixel[3] // (2 ** i))

    return (r, g, b, a)

def resizeImageList(img_list, img_size):
    for i in range(len(img_list)-1):
        img_list[i] = img_list[i].resize(img_size) 
