"""
Image preprocessing pipeline matching training transforms.
"""

import io
from PIL import Image
from torchvision import transforms
import torch

# Matches the training transform in train_plant_disease_test.py
_transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
])


def preprocess_image(image_bytes: bytes) -> torch.Tensor:
    """
    Convert raw image bytes → normalised [1, 3, 256, 256] tensor.

    Raises:
        ValueError: if the bytes cannot be decoded as an image.
    """
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception as exc:
        raise ValueError(f"Cannot decode image: {exc}") from exc

    tensor = _transform(image)          # (3, 256, 256)
    return tensor.unsqueeze(0)          # (1, 3, 256, 256)
