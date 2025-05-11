# beginning of skin_analyzer.py
import torch

# Load the .pth file and print its keys
state_dict = torch.load("vit_skin_disease_model.pth", map_location=torch.device('cpu'))
print(state_dict.keys())


# skin_analyzer.py

import torch
import torch.nn as nn
from PIL import Image
import numpy as np
from torchvision import transforms
from transformers import ViTModel, ViTConfig
from utils.constants import MODEL_NAME, SKIN_CLASSES, PRODUCT_RECOMMENDATIONS

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Manually define the image processor based on README
image_processor = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Define a simplified model that matches the .pth file
class SkinDiseaseModel(nn.Module):
    def __init__(self, num_classes=len(SKIN_CLASSES)):
        super(SkinDiseaseModel, self).__init__()
        # Use the base ViT model without the pooler layer
        self.vit = ViTModel.from_pretrained('google/vit-base-patch16-224-in21k', add_pooling_layer=False)
        self.classifier = nn.Linear(self.vit.config.hidden_size, num_classes)

    def forward(self, x):
        outputs = self.vit(pixel_values=x)
        logits = self.classifier(outputs.last_hidden_state[:, 0, :])
        return logits

# Initialize model
model = SkinDiseaseModel(num_classes=len(SKIN_CLASSES))

# Load the .pth weights
try:
    model.load_state_dict(torch.load("vit_skin_disease_model.pth", map_location=device))
    model.to(device)
    model.eval()
except Exception as e:
    raise RuntimeError("Failed to load model weights. Make sure 'vit_skin_disease_model.pth' exists in the working directory.") from e

def analyze_skin(face_img):
    face_pil = Image.fromarray(face_img).convert("RGB")
    input_tensor = image_processor(face_pil).unsqueeze(0).to(device)

    with torch.no_grad():
        logits = model(input_tensor)
    probabilities = torch.nn.functional.softmax(logits, dim=-1).cpu().numpy()[0]
    predicted_class = logits.argmax(-1).item()

    label = SKIN_CLASSES.get(predicted_class, "unknown")
    confidence = probabilities[predicted_class].item()

    print(f"Detected: {label}, Confidence: {confidence:.2f}")
    return label, confidence