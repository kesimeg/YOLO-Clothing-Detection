from ultralytics import YOLO
import argparse

parser = argparse.ArgumentParser(description="YOLOv8 training script")
parser.add_argument("--epochs", type=int, default=30, help="number of epochs")
parser.add_argument("--patience", type=int, default=5, help="patience for early stopping")
parser.add_argument("--batch_size", type=int, default=64, help="batch size")
parser.add_argument("--model_name", type=str, default="yolov8n.pt", help="pretrained model to finetune")
args = parser.parse_args()

# Load YOLO model
model = YOLO(args.model_name)  # or 'yolov8s.pt', 'yolov8m.pt', 'yolov8l.pt', etc.

# Specify the data configuration
data_config = {
    'train': 'fashion_dataset/train/images',
    'val': 'fashion_dataset/val/images',
    'nc': 4,  # Number of classes in your dataset
    'names': ["accessories","bags","clothing","shoes"]
}

# Save the data configuration to a YAML file
import yaml
with open('data.yaml', 'w') as f:
    yaml.dump(data_config, f)

# Train the model
model.train(data='data.yaml', epochs=args.epochs, batch=args.batch_size,patience=args.patience)