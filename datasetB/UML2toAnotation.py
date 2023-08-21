from math import *
import glob
import shutil
import os


listOfFiles = glob.glob("./UML2/Class/*")
listOfFiles.sort()
try:
    os.mkdir("./dataset/")
except : 
    FileExistsError


i=1

for files in listOfFiles:
    name = files.split('\\')[-1]
    shutil.copy(f"./UML2/Class/{name}", f"./dataset/class{i}.jpg")
    i+=1



