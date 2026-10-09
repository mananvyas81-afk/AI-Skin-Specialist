import numpy as np
from PIL import Image

try:
    import cv2
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False


def preprocess_standard(image_input, target_size=(224, 224)):
    """
    Standard preprocessing for dermatological images:
    - Resize image with high-quality bicubic resampling
    - Convert to RGB
    - Normalize RGB pixel values to [0.0, 1.0] float32
    
    Returns:
        np.ndarray: Preprocessed float32 array normalized to [0, 1] of shape (H, W, C)
    """
    if isinstance(image_input, str):
        image = Image.open(image_input).convert("RGB")
    elif isinstance(image_input, Image.Image):
        image = image_input.convert("RGB")
    elif isinstance(image_input, np.ndarray):
        if image_input.ndim == 2:
            image = Image.fromarray(image_input).convert("RGB")
        else:
            image = Image.fromarray(image_input.astype(np.uint8)).convert("RGB")
    else:
        raise ValueError(f"Unsupported image type: {type(image_input)}")

    resized_image = image.resize(target_size, Image.Resampling.BILINEAR)
    arr = np.array(resized_image, dtype=np.float32) / 255.0
    return arr


def otsu_threshold(image_input):
    """
    Applies Otsu's automatic thresholding to isolate lesion from skin background.
    Used for preprocessing comparative study against standard normalization.
    """
    if isinstance(image_input, str):
        img = Image.open(image_input).convert("L")
        gray = np.array(img, dtype=np.uint8)
    elif isinstance(image_input, Image.Image):
        gray = np.array(image_input.convert("L"), dtype=np.uint8)
    elif isinstance(image_input, np.ndarray):
        if image_input.ndim == 3:
            if HAS_OPENCV:
                gray = cv2.cvtColor(image_input.astype(np.uint8), cv2.COLOR_RGB2GRAY)
            else:
                gray = np.dot(image_input[..., :3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)
        else:
            gray = image_input.astype(np.uint8)
    else:
        raise ValueError(f"Unsupported image type: {type(image_input)}")

    if HAS_OPENCV:
        # Otsu's thresholding after Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return thresh
    else:
        # Pure numpy implementation of Otsu thresholding
        hist, bin_edges = np.histogram(gray.ravel(), bins=256, range=(0, 256))
        total = gray.size
        current_max, threshold = 0.0, 0
        sum_total = np.dot(np.arange(256), hist)
        sum_back, weight_back = 0.0, 0

        for t in range(256):
            weight_back += hist[t]
            if weight_back == 0:
                continue
            weight_fore = total - weight_back
            if weight_fore == 0:
                break
            sum_back += t * hist[t]
            mean_back = sum_back / weight_back
            mean_fore = (sum_total - sum_back) / weight_fore
            var_between = float(weight_back) * float(weight_fore) * ((mean_back - mean_fore) ** 2)
            if var_between > current_max:
                current_max = var_between
                threshold = t

        thresh = (gray > threshold).astype(np.uint8) * 255
        return thresh


def preprocess_otsu_segmented(image_input, target_size=(224, 224)):
    """
    Applies Otsu thresholding mask to extract the lesion ROI, then resizes and normalizes.
    Used in preprocessing ablation comparison.
    """
    mask = otsu_threshold(image_input)
    if isinstance(image_input, str):
        rgb = np.array(Image.open(image_input).convert("RGB"), dtype=np.uint8)
    elif isinstance(image_input, Image.Image):
        rgb = np.array(image_input.convert("RGB"), dtype=np.uint8)
    elif isinstance(image_input, np.ndarray):
        rgb = image_input.astype(np.uint8) if image_input.ndim == 3 else np.stack([image_input]*3, axis=-1)
    else:
        raise ValueError("Unsupported image type")

    # Invert mask if background is brighter than foreground
    if np.mean(mask == 255) > 0.5:
        mask = cv2.bitwise_not(mask) if HAS_OPENCV else 255 - mask

    # Apply mask
    masked = np.zeros_like(rgb)
    for c in range(3):
        masked[:, :, c] = rgb[:, :, c] * (mask > 0)

    return preprocess_standard(masked, target_size=target_size)
