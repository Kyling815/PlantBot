"""Utility functions for image processing."""

import io
from PIL import Image


def validate_image(image_bytes: bytes) -> bool:
    """Return True if the bytes represent a valid image."""
    try:
        Image.open(io.BytesIO(image_bytes)).verify()
        return True
    except Exception:
        return False


def resize_image(image_bytes: bytes, size: tuple[int, int] = (256, 256)) -> bytes:
    """Resize an image to the given dimensions and return as JPEG bytes."""
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize(size)
    output = io.BytesIO()
    image.save(output, format="JPEG")
    return output.getvalue()
