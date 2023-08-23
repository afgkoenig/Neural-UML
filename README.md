# NEURAL-UML
This repository contains the source code for our paper:

**NEURAL-UML: Intelligent Recognition System of Structural Elements in UML Class Diagram**

## **Updates**
- code for scraping coming soon!

## **Installation**
Create and activate conda environment:
```
conda create -n NEURAL-UML
conda activate NEURAL-UML
```

Install all dependencies:
```
pip install -r requirements.txt
```

Install Jupyter Lab to visualize demo:
```
conda install -c conda-forge jupyterlab
```

## Testing

With this code you can use the neural network create to detect element in a class diagram.

For example we have put two image in folder : 
```
├── input
  ├── oringinal_image
```
```
python test_images.py
```

The results are in the folder :

```
├── output
  ├── image
```


Just run the code "test_images.py" and you obtain a visualisation of the result in a folder "./output/image/". You also have the associate csv.

You can test on your own image, you have just to put her in the folder "./input/original_image/" with name "test*"

If you have an error with the utilisation of YOLO try to use the command "pip install --upgrade ultralytics"

In the folder "DatasetA" you have all annotations from Lindholmen Dataset.

In the folder "DatasetB" you have all annotation from the paper "Multiclass classification of four types of uml diagrams from images using deep learning".

You also have the link of all images come from Lindholmen Dataset and declare to be a class diagram in "dataset_without_annotation.csv"
