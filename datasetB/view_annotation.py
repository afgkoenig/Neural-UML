from PIL import Image,ImageDraw
import os
import csv


try:
    os.mkdir("./results/")
except : 
    FileExistsError


# for view boxes on the global image
liste_color = ["violet","indigo","blue","green","yellow","orange","red"]
liste_data = ["navigable","inheritance","realization","dependency","aggregation","composition","classe"]

#liste_color = ["blue","red"]
#liste_data = ["fleche","classe"]
for elt in os.listdir("./test/"):
    img = Image.open(f"./test/{elt}")
    img1 = ImageDraw.Draw(img)



    with open("./datasetB.csv", newline='') as csvfile:
            filereader = csv.reader(csvfile, delimiter=';')
            for row in filereader:
                if row[0]==elt:
                    annotation = row[2:]
                    try:
                        while len(annotation)>=5:
                            shape = [(float(annotation[0])/2,float(annotation[1])/2),(float(annotation[2])/2,float(annotation[3])/2)]
                            if int(annotation[4]) >6:
                                print(int(annotation[4]))
                            img1.rectangle(shape,outline=liste_color[int(annotation[4])],width = 3)
                            img1.text((float(annotation[0])/2+1,float(annotation[1])/2+1),text = liste_data[int(annotation[4])] , fill = liste_color[int(annotation[4])])
                            annotation = annotation[5:]

                        if img.mode == "RGBA":
                            img.save(f"./results/{elt[:-4]}.png")
                        else:
                            img = img.convert("RGB")
                            img.save(f"./results/{elt}")
                    except : ValueError