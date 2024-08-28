from datasets import load_dataset
import os
import pandas as pd
from tqdm import tqdm
import numpy as np

def convert_annotation(img_name,item,label_dir):
    bbox = np.array(item["objects"]['bbox'])
    label = item["objects"]['category']
    img_width = item["width"]
    img_height = item["height"]


    x_min, y_min, x_max, y_max = np.split(bbox,4,1) #split data into each column

    #convert pascal to YOLO format
    x_center = (x_min + x_max) / 2 / img_width
    y_center = (y_min + y_max) / 2 / img_height
    width = (x_max - x_min) / img_width
    height = (y_max - y_min) / img_height


    df = pd.DataFrame({
        'class': label,
        'x_center': np.squeeze(x_center),
        'y_center': np.squeeze(y_center),
        'width': np.squeeze(width),
        'height': np.squeeze(height)})


    df.to_csv(os.path.join(label_dir,img_name + ".txt"), sep='\t', index=False,header=False)

def save_images_and_labels(dataset, output_dir):
    # Create image directory if it doesn't exist

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image_dir = os.path.join(output_dir, 'images')
    os.makedirs(image_dir, exist_ok=True)
    label_dir = os.path.join(output_dir, 'labels')
    os.makedirs(label_dir, exist_ok=True)

    for item in tqdm(dataset):
        image_id = item['image_id']
        image_data = item['image']

        # Save image
        try:
          img_name = "image_{}".format(image_id)
          image_path = os.path.join(image_dir, img_name + ".jpg")
          image_data.save(image_path)
          # Convert and save annotation
          convert_annotation(img_name,item,label_dir)
        except Exception as e:
          print(e)


dataset = load_dataset("detection-datasets/fashionpedia_4_categories")

#YOLO expects everything to be under datasets directory
if not os.path.exists("datasets"):
    os.mkdir("datasets")

main_folder = "datasets/fashion_dataset"
if not os.path.exists(main_folder):
    os.mkdir(main_folder)


for key in dataset.keys():
    output_dir = os.path.join(main_folder,key)
    save_images_and_labels(dataset[key], output_dir)
