from PIL import Image,ImageFilter
import random as rd
import mapGenerateur as maper
import sys
import matplotlib.pyplot as plt

EXTRA_PIXEL = 20
BASE_SIZE = 32

SIZE_LEVEL = 5
MIN_PROBABILITY = 0.001
MAX_PROBABILITY = 0.1
MIN_NB_SMOOTH = 0
MAX_NB_SMOOTH = 1000

NB_GALAXIE = 12

def main():
    galaxies_list = []
    for i in range(NB_GALAXIE):
        probability_list = probabilityListGenerator(SIZE_LEVEL, MIN_PROBABILITY, MAX_PROBABILITY)
        nbSmooth_list = smoothListGenerator(SIZE_LEVEL, MIN_NB_SMOOTH, MAX_NB_SMOOTH)
        galaxie = GenerateGalaxy(SIZE_LEVEL, probability_list, nbSmooth_list, i)
        galaxie.save("ImageGalaxie/Galaxie"+ str(i) +"/map.png")
        galaxies_list.append(galaxie)
    
    rows, cols = 3, 4
    axes = plt.subplots(rows, cols, figsize=(15, 10))
    for i, ax in enumerate(axes.flat):
        if i < len(galaxies_list):
            ax.imshow(galaxies_list[i]) 
        ax.axis('off')       

    plt.tight_layout()
    plt.show()



def PutPixel(img, x, y, proba) :
    rand = rd.random()
    if rand < proba :
        img.putpixel((x,y), (rd.randint(64,255),rd.randint(64,191),rd.randint(64,191)))
    return img
        
def GenerateImage(size_level, probability, nbSmooth) :
    
    img_size = 2 ** size_level * BASE_SIZE
    print("Création Image, taille = ", img_size, ", proba = ", probability,
          ", intensite = ", nbSmooth)
    
    img_size += EXTRA_PIXEL
    rgba = (0,0,0,255)
    img = Image.new('RGBA', (img_size,img_size),rgba)
    bruit=[]
    new_img = Image.new('RGBA', (img_size - EXTRA_PIXEL, img_size - EXTRA_PIXEL),rgba)
    
    for x in range(img_size) :
        sys.stdout.write(f"\rAjout Bruit : {x + 1} / {img_size}")
        for y in range(img_size) :
            img = PutPixel(img, x, y, probability)
            rgba = img.getpixel((x,y))
            if (rgba != (0,0,0,255)) :
                rgba = img.getpixel((x,y))
                bruit.append([(x,y),rgba])
    print("\nBruitage finis")
                
    for j in range(nbSmooth) :
        sys.stdout.write(f"\rAjout Filtrage : {j + 1} / {nbSmooth}")
        for k in range(len(bruit)) :
            img.putpixel(bruit[k][0], bruit[k][1])
        img = img.filter(ImageFilter.SMOOTH_MORE)
    print("\nFiltrage finis")

    for x in range(img_size - EXTRA_PIXEL):
        sys.stdout.write(f"\rRedimentionnement : {x + 1} / {img_size-EXTRA_PIXEL}")
        for y in range(img_size - EXTRA_PIXEL):
            new_img.putpixel((x, y), img.getpixel((x+EXTRA_PIXEL//2, y+EXTRA_PIXEL//2)))
    print("\nRedimentionnement finis")
    return new_img
            
def GenerateGalaxy(size_level, probability_list, nbSmooth_list, galaxie_id=0):
    assert(size_level == len(probability_list), "La liste de probabilité n'es pas de la bonne taille")
    assert(size_level == len(nbSmooth_list), "La liste du nombre de smooth n'es pas de la bonne taille")
    img_list = []
    # Génération et affichage de l'image (taille, probabilité de bruit, nombre de répétion du smooth)
    for i in range(size_level) :
        img = GenerateImage(i, probability_list[i], nbSmooth_list[i])
        img_list.append(img)
        save_path = "ImageGalaxie/Galaxie"+ str(galaxie_id) +"/map"+ str(i ** 2 * BASE_SIZE) +".png"
        img.save(save_path)
    return maper.GenerateMap(img_list)
        
def probabilityListGenerator(size_level, minP, maxP):
    random_probability_list = []
    for _ in range(size_level):
        random_probability = rd.random() * (maxP - minP) + minP
        random_probability_list.append(random_probability)
    return random_probability_list

def smoothListGenerator(size_level, minS, maxS):
    random_smooth_list = []
    for _ in range(size_level):
        random_smooth = (int) (rd.random() * (maxS - minS) + minS)
        random_smooth_list.append(random_smooth)
    return random_smooth_list
          
            
main()