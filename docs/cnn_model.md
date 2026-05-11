# CNN Model Documentation

## Model Summary

| Property | Value |
|---|---|
| Architecture | Custom CNN (5 conv blocks) |
| Input Size | 256 × 256 × 3 (RGB) |
| Output Classes | 38 (plant × disease combinations) |
| Best Accuracy | 98% (plant_disease_98.pth) |
| Framework | PyTorch |
| Device | CUDA / CPU |

## Architecture Details

```
Input (3, 256, 256)
  ↓ Conv2d(3→16, 3×3) + BN + ReLU + MaxPool(2)     → (16, 128, 128)
  ↓ Conv2d(16→32, 3×3) + BN + ReLU + MaxPool(2)    → (32, 64, 64)
  ↓ Conv2d(32→64, 3×3) + BN + ReLU + MaxPool(2)    → (64, 32, 32)
  ↓ Conv2d(64→128, 3×3) + BN + ReLU + MaxPool(2)   → (128, 16, 16)
  ↓ Conv2d(128→256, 3×3) + BN + ReLU + MaxPool(2)  → (256, 8, 8)
  ↓ Flatten → Dropout(0.5) → Linear(16384, 38)
Output: logits (38,)
```

## Training

- **Dataset**: PlantVillage (38 classes, ~87,000 images)
- **Augmentation**: Random flips, rotations, color jitter
- **Optimizer**: Adam
- **Loss**: Cross-entropy
- **Epochs**: ~30 (early stopping)
- **Hardware**: NVIDIA RTX 3050

## Class Labels

38 classes covering 14 plant species:
Apple, Blueberry, Cherry, Corn, Grape, Orange, Peach, Pepper, Potato, Raspberry, Soybean, Squash, Strawberry, Tomato.

See `plant_disease/class_names.json` for the full list.

## Inference

```python
from backend.cnn_service.predictor import predict

with open("leaf.jpg", "rb") as f:
    result = predict(f.read())

print(result.label)       # e.g. "Tomato - Early blight"
print(result.confidence)  # e.g. 94.3
print(result.status)      # "Disease detected"
```
