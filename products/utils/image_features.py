import torch
import torch.nn as nn
from torchvision import transforms
from torchvision.models import resnet50, ResNet50_Weights
from PIL import Image

# Загрузка предобученной модели ResNet50 с использованием актуального параметра weights
weights = ResNet50_Weights.DEFAULT
model = resnet50(weights=weights)
model = nn.Sequential(*list(model.children())[:-1])
model.eval()

# Получаем преобразование с использованием встроенного метода веса
preprocess = weights.transforms()

def extract_features(image_path):
    img = Image.open(image_path).convert('RGB')
    img_tensor = preprocess(img)
    img_tensor = img_tensor.unsqueeze(0)  # Добавляем размерность батча
    with torch.no_grad():
        features = model(img_tensor)
    return features.squeeze().numpy()
