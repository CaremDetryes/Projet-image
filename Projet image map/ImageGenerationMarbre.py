from PIL.Image import *
import random as rd

def generateImage(taille, contraste) :
    # Création de l'image
    img = new('L', (taille, taille), color=0)
    img.putpixel((0,0),rd.randint(0,255))
    #On traverse une première fois la liste pour initialiser
    for x in range(taille-1) :
        
        random_contraste = rd.randint(-contraste,contraste)
        if (img.getpixel((x,0)) + random_contraste > 255
        or img.getpixel((x,0)) + random_contraste < 0) :
            img.putpixel((x+1,0),(img.getpixel((x,0))-random_contraste))
        else :
            img.putpixel((x+1,0),(img.getpixel((x,0))+random_contraste))
        
        random_contraste = rd.randint(-contraste,contraste)
        if (img.getpixel((0,x)) + random_contraste > 255
        or img.getpixel((0,x)) + random_contraste < 0) :
            img.putpixel((0,x+1),img.getpixel((0,x))-random_contraste)
        else :
            img.putpixel((0,x+1),img.getpixel((0,x))+random_contraste)
        
    # On traverse tout les pixel de l'image
    for x in range(taille-1) :
        for y in range(taille -1) :
            random_contraste = rd.randint(-contraste,contraste)
            moyenne_pixel = (img.getpixel((x,y))+img.getpixel((x+1,y))+img.getpixel((x+1,y))+img.getpixel((x,y+1)))//4
            if (moyenne_pixel + random_contraste > 255
            or moyenne_pixel + random_contraste < 0
                ) :
                img.putpixel((x+1,y+1), moyenne_pixel - random_contraste)
            else :
                img.putpixel((x+1,y+1), moyenne_pixel + random_contraste)
    return img
    
# Génération et affichage de l'image
img256 = generateImage(256, 40)
img128 = generateImage(128, 40)
img64 = generateImage(64, 40)
dossier = "ImageMarbre/"
img256.save(dossier+"map256.png")
img128.save(dossier+"map128.png")
img64.save(dossier+"map64.png")