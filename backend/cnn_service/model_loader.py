"""
Loads the PlantDiseaseModel from a .pth checkpoint.
Mirrors the architecture defined in plant_disease/inference_api.py.
"""

import json
import os
import torch
import torch.nn as nn

from backend.config import settings


class PlantDiseaseModel(nn.Module):
    """Custom CNN matching the trained architecture."""

    def __init__(self, num_classes: int = 38):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.head = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(0.5),
            nn.Linear(256 * 8 * 8, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.head(self.conv(x))


def load_class_names(path: str) -> list[str]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_model() -> tuple[PlantDiseaseModel, list[str], torch.device]:
    """
    Returns (model, class_names, device).
    Model is already in eval mode on the correct device.
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    class_names = load_class_names(settings.class_names_path)

    model = PlantDiseaseModel(num_classes=len(class_names)).to(device)
    state_dict = torch.load(settings.model_path, map_location=device, weights_only=True)
    model.load_state_dict(state_dict)
    model.eval()

    return model, class_names, device
