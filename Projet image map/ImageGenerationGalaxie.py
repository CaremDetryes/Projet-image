from PIL import Image,ImageFilter
import random as rd
import mapGenerateur as maper
import sys
import matplotlib.pyplot as plt
import os

EXTRA_PIXEL = 20
BASE_SIZE = 32

SIZE_LEVEL = 3
MIN_PROBABILITY = 0.0001
MAX_PROBABILITY = 0.1
MIN_NB_SMOOTH = 0
MAX_NB_SMOOTH = 100

NB_GALAXIE = 12

def main():
    galaxies_list = []
    for i in range(NB_GALAXIE):
        print("\n___________________________________________________________________________________________")
        print("Galaxie n°" + str(i) + " :")
        probability_list = probabilityListGenerator(SIZE_LEVEL, MIN_PROBABILITY, MAX_PROBABILITY)
        nbSmooth_list = smoothListGenerator(SIZE_LEVEL, MIN_NB_SMOOTH, MAX_NB_SMOOTH)
        galaxie = GenerateGalaxy(SIZE_LEVEL, probability_list, nbSmooth_list, i)
        galaxie.save("ImageGalaxie/Galaxie"+ str(i) +"/map.png")
        galaxies_list.append((galaxie, probability_list, nbSmooth_list))
    
    rows, cols = 3, 4
    fig, axes = plt.subplots(rows, cols, figsize=(15, 10))
    for i, ax in enumerate(axes.flat):
        if i < len(galaxies_list):
            ax.imshow(galaxies_list[i][0])
            ax.text(0.5, 0.5, f"Liste 1 : {galaxies_list[i][1]}\nListe 2 : {galaxies_list[i][2]}",
                fontsize=10, ha='center', va='bottom', transform=ax.transAxes)
        ax.axis('off')       

    plt.tight_layout()
    plt.show()


def PutPixel(img, x, y, proba) :
    rand = rd.random()
    if rand < proba :
        img.putpixel((x,y), (rd.randint(128,255),rd.randint(64,160),rd.randint(64,160)))
    return img
        
def GenerateImage(size_level, probability, nbSmooth) :
    
    img_size = 2 ** size_level * BASE_SIZE
    print("___________________________________________________________________________________________")
    print("Création de l'image, taille = "+ str(img_size) +", probabilité = "+ str(probability)+
          ", nombre de smooth = "+ str(nbSmooth))
    
    img_size += EXTRA_PIXEL
    rgba = (0,0,0,255)
    img = Image.new('RGBA', (img_size,img_size),rgba)
    star_list=[]
    new_img = Image.new('RGBA', (img_size - EXTRA_PIXEL, img_size - EXTRA_PIXEL),rgba)
    
    for x in range(img_size) :
        for y in range(img_size) :
            sys.stdout.write(f"\rCréation de la liste d'étoile : {x + 1} / {img_size}")
            img = PutPixel(img, x, y, probability)
            rgba = img.getpixel((x,y))
            if (rgba != (0,0,0,255)) :
                rgba = img.getpixel((x,y))
                star_list.append([(x,y),rgba])
    print()
                
    for j in range(nbSmooth) :
        sys.stdout.write(f"\rAjout Filtrage : {j + 1} / {nbSmooth}")
        for k in range(len(star_list)) :
            img.putpixel(star_list[k][0], star_list[k][1])
        img = img.filter(ImageFilter.SMOOTH_MORE)
    print()

    for x in range(img_size - EXTRA_PIXEL):
        sys.stdout.write(f"\rRedimentionnement : {x + 1} / {img_size-EXTRA_PIXEL}")
        for y in range(img_size - EXTRA_PIXEL):
            new_img.putpixel((x, y), img.getpixel((x+EXTRA_PIXEL//2, y+EXTRA_PIXEL//2)))
    print()
    return new_img

            
def GenerateGalaxy(size_level, probability_list, nbSmooth_list, galaxie_id=0):
    img_list = []
    # Génération et affichage de l'image (taille, probabilité de bruit, nombre de répétion du smooth)
    for i in range(size_level) :
        img = GenerateImage(i, probability_list[i], nbSmooth_list[i])
        img_list.append(img)
        save_path = "ImageGalaxie/Galaxie"+ str(galaxie_id) +"/map"+ str(2 ** i * BASE_SIZE) +".png"
        img.save(save_path)
    return maper.imageOverlay(img_list)
        
def probabilityListGenerator(size_level, minP, maxP):
    random_probability_list = [round(rd.uniform(minP,maxP), 4) for _ in range(size_level)]
    return random_probability_list

def smoothListGenerator(size_level, minS, maxS):
    random_smooth_list = [(int) (rd.uniform(minS,maxS)) for _ in range(size_level)]
    return random_smooth_list
          
            
def fileReset():
    file_path = "ImageGalaxie/"
    try :
        os.remove(file_path)
    except Exception as e:
        print(f"Erreur : {e}")
    for i in range(NB_GALAXIE):
        try :
            os.makedirs(file_path + "Galaxie"+ str(i) +"/")
        except Exception as e:
            print(f"Erreur : {e}")

fileReset()   
main()