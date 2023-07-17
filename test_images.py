import os
import numpy as np
from ultralytics import YOLO
import csv
from shapely.geometry import Polygon
import re
from copy import deepcopy
from PIL import Image,ImageDraw
import shutil

dict_dim = {128 : "fleche", 512 : "classe"}
liste_name = ["a","b"]
Path_test = "./input/original_image/" # image to visualize
Path_results = "./output/" # directory with subdirectories "csv" and "image"
model = YOLO("./best.pt") # choose your model


# my version of Intersection over Union
def IoU(elt1,elt2):
    rect1 = Polygon(((elt1[0],elt1[1]),(elt1[2],elt1[1]),(elt1[2],elt1[3]),(elt1[0],elt1[3])))
    rect2 = Polygon(((elt2[0],elt2[1]),(elt2[2],elt2[1]),(elt2[2],elt2[3]),(elt2[0],elt2[3])))
    inter = rect1.intersection(rect2).area
    union = rect1.area+rect2.area-inter+0.001 #pour éviter la division par 0
    new_rect = rect1.union(rect2).bounds
    return inter/union,new_rect

# to be faster and don't confront 2 classes with important distances
def in_circle(elt,elt2):
    x1 = elt[0]
    x2 = elt2[0]
    y1 = elt[1]
    y2 = elt2[1]
    bool = abs(x1-x2)<=elt[2] and abs(y1-y2)<=elt[3]
    return bool

#changes the data storage format
 
# the data is : class x_center y_center width height
# center (0;0) top left of the image
# after
# the data is : class;x1;y1;x2;y2
# center (0;0) top left of the image
def centre_to_corner(elt,shape,delta):
    elt[1] = elt[1] * shape[1]
    elt[2] = elt[2] * shape[0]
    elt[3] = elt[3] * shape[1]
    elt[4] = elt[4] * shape[0]
    x = elt[1]
    y = elt[2]
    width = elt[3]/2
    height = elt[4]/2
    elt[1] = x - width + int(delta[0])
    elt[2] = y - height + int(delta[1])
    elt[3] = x + width + int(delta[0])
    elt[4] = y + height + int(delta[1])
    return elt


def combine_rectangle(liste):
    liste_final = []
    i = 1
    while len(liste)>1:
        elt = liste[0]
        elt2 = liste[i]
        if elt[0] == elt2[0] and in_circle(elt[1],elt2[1]):
            results = IoU(liste[0][1],liste[i][1])
            if results[0] >= 0.1: 
                liste[0] = [elt[0],results[1]]
                liste.remove(elt2)
                i = 1
            else : 
                if i==len(liste)-1: 
                    liste.remove(elt)
                    liste_final.append(elt)
                    i = 1
                else :
                    i += 1
        else :
            if i==len(liste)-1: 
                liste.remove(elt)
                liste_final.append(elt)
                i = 1
            else :
                i += 1
        
            
    liste_final.append(liste[0])
    return liste_final

def main():
    dir_test = os.listdir(Path_test)
    for img_name in dir_test:

        img = Image.open(Path_test+img_name)
        Path_pred = f"./input/image_crop/{img_name[:-4]}/" 

        
        try :
            os.mkdir(Path_pred)
            os.mkdir(Path_pred+"fleche/")
            os.mkdir(Path_pred+"classe/")
        except : 
            FileExistsError
            
        #shutil.copy(Path_test+img_name,Path_pred+"original_x0_y0.jpg")
        
        img_name = img_name[:-4]

        # convert image to RGB
        if img.mode == "RGBA" and np.array(img)[0,0,3]==0 and np.array(img)[0,0,0]==0:
                img = np.array(img)
                img_final = img[:,:,:3]
                img_final[:,:,0] += img[:,:,3]
                img_final[:,:,1] += img[:,:,3]
                img_final[:,:,2] += img[:,:,3]
                img= Image.fromarray(img_final)
        else :
            img = img.convert("RGB")

        # crop global image in multiple image
        for val in dict_dim:
            delta_x = 0
            dim = min(val,min(np.shape(img)[1],np.shape(img)[0]))
            while delta_x+dim<=np.shape(img)[1]:
                delta_y = 0

                while delta_y+dim<=np.shape(img)[0]:
                    img_crop = img.crop((delta_x,delta_y,delta_x+dim,delta_y+dim))
                    if dict_dim[val] == "classe":
                        img_crop.save(Path_pred+f"classe/x{delta_x}_y{delta_y}_{dict_dim[val]}.jpg")
                    else : img_crop.save(Path_pred+f"fleche/x{delta_x}_y{delta_y}_{dict_dim[val]}.jpg")
                    delta_y+=int(dim/4)

                delta_x+=int(dim/4)

        

        # predict on image cropped

        #model.predict(Path_test+img_name+".jpg",save=True,save_txt = True,conf=0.35,save_conf=True,device=0)

        Path = f"./runs/detect/{img_name}/"

        model = YOLO("./best.pt") # choose your model

        model.predict(Path_pred+"classe",save=True,save_txt = True,conf=0.35,save_conf=True,device=0)

        model.predict(Path_pred+"fleche",save=True,save_txt = True,conf=0.2,save_conf=True,device=0,classes=[0,1,2,3,4,5])

        try :
            os.rename("./runs/detect/predict/",Path)
        except FileExistsError :
            print(f"{Path} already exists, please try an other image or remove this folder")
            break
        

        #shutil.copy(f"./runs/detect/predict/labels/{img_name}.txt",Path+"labels")
        #shutil.copy(f"./runs/detect/predict/{img_name}.jpg",Path)

        # regroup all label in .txt to a single liste 
        liste = []
        dir = os.listdir(Path+"labels/")
        for files in dir:
            if files[:3] == "test":
                delta = [0,0]
            else:
                delta = re.findall(r'\d+', files)
            with open (Path+"labels/"+files,"r") as txt:
                filereader = csv.reader(txt,delimiter=" ")
                for row in filereader:
                    if row != "":
                        rect = []
                        for nmb in row:
                            rect.append(round(float(nmb),2))
                        rect[0] = int(rect[0])
                        shape = np.shape(Image.open(Path+files[:-4]+".jpg"))
                        rect = centre_to_corner(rect,shape,delta)
                        liste.append([rect[0],(rect[1],rect[2],rect[3],rect[4])])



        # use IoU to regroup all same label in one group of this label
        liste_one_etape = combine_rectangle(liste)
        liste_final = []
        while liste_final!=liste_one_etape:
            liste_final = deepcopy(liste_one_etape)
            liste_one_etape = combine_rectangle(liste_one_etape)
            


        
        texte = ""
        for row in liste_final:
            for elt in row:
                texte+=str(elt)
            texte+="\n"
        texte = texte.replace("("," ")
        texte = texte.replace(")"," ")
        texte = texte.replace(",","")
        with open(Path_results+f"csv/pred_{img_name}.csv","w") as file:
            file.write(texte)

        # for view boxes on the global image
        liste_color = ["violet","indigo","blue","green","yellow","orange","red"]
        liste_data = ["navigable","inheritance","realization","dependency","aggregation","composition","classe"]

        #liste_color = ["blue","red"]
        #liste_data = ["fleche","classe"]

        img = Image.open(Path_test+f"{img_name}.jpg")
        img1 = ImageDraw.Draw(img)



        with open(Path_results+f"csv/pred_{img_name}.csv", newline='') as csvfile:
                filereader = np.loadtxt(csvfile, delimiter=' ',usecols=(0,1,2,3,4))
                if len(np.shape(filereader)) == 1:
                    filereader = [filereader]
                for row in filereader:
                    shape = [(row[1],row[2]),(row[3],row[4])]
                    img1.rectangle(shape,outline=liste_color[int(row[0])],width = 3)
                    img1.text((row[1]+1,row[2]+1),text = liste_data[int(row[0])] , fill = liste_color[int(row[0])])

        if img.mode == "RGBA":
            img.save(Path_results+f"image/pred_{img_name}.png")
        else:
            img = img.convert("RGB")
            img.save(Path_results+f"image/pred_{img_name}.jpg")

try:
    os.mkdir("./input/image_crop/")
    os.mkdir("./output/")
    os.mkdir("./output/image/")
    os.mkdir("./output/csv/")
except:
    FileExistsError

main()