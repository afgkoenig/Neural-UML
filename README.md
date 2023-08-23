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

For example, we have put two images in folder : 
```
├── input
  ├── oringinal_image
```
Run the command :
```
python test_images.py
```

Then you can view the results and obtain the corresponding csv file in the folders :

```
├── output
  ├── image
  ├── csv
```

If you have an error with the utilisation of YOLO try to use the command :

```
pip install --upgrade ultralytics"
```

## Dataset A

In the folder "DatasetA" you have all annotations from Lindholmen Dataset.

In the folder "DatasetB" you have all annotation from the paper "Multiclass classification of four types of uml diagrams from images using deep learning".

You also have the link of all images come from Lindholmen Dataset and declare to be a class diagram in "dataset_without_annotation.csv"
