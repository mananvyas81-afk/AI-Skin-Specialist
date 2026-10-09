"""
Predictor module for Skin Disease Classification.

Executes inference using the selected best model (PyTorch, ONNX, or TensorFlow).
Gracefully falls back when model weights or deep learning frameworks are not installed,
ensuring the application never crashes and existing Groq vision flow continues smoothly.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

import numpy as np
from PIL import Image

from classifier.constants import SKIN_CLASSES, BEST_MODEL_WEIGHTS, BEST_MODEL_TF
from classifier.preprocessing import preprocess_standard


class SkinDiseasePredictor:
    """
    Inference engine for Skin Disease Classification.
    """

    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path or (
            BEST_MODEL_WEIGHTS if os.path.exists(BEST_MODEL_WEIGHTS)
            else (BEST_MODEL_TF if os.path.exists(BEST_MODEL_TF) else None)
        )
        self.model = None
        self.backend = None
        self.model_name = "MobileNetV3 (Selected Best Model)"
        self.classes = SKIN_CLASSES
        self._load_model_if_available()

    def _load_model_if_available(self):
        """Attempts to load PyTorch or TensorFlow model if available."""
        if not self.model_path or not os.path.exists(self.model_path):
            return

        # Try PyTorch
        if self.model_path.endswith((".pth", ".pt")):
            try:
                import torch
                from classifier.models import get_pytorch_model
                # Default selected best architecture: MobileNetV3
                model = get_pytorch_model("mobilenet", num_classes=len(self.classes), pretrained=False)
                state = torch.load(self.model_path, map_location="cpu")
                model.load_state_dict(state)
                model.eval()
                self.model = model
                self.backend = "pytorch"
                return
            except Exception as e:
                print(f"[SkinDiseasePredictor] Notice: PyTorch model load skipped ({e})")

        # Try TensorFlow/Keras
        if self.model_path.endswith((".h5", ".keras")):
            try:
                import tensorflow as tf
                self.model = tf.keras.models.load_model(self.model_path)
                self.backend = "tensorflow"
                return
            except Exception as e:
                print(f"[SkinDiseasePredictor] Notice: TF model load skipped ({e})")

    def is_model_loaded(self) -> bool:
        """Returns True if a real trained model is loaded in memory."""
        return self.model is not None

    def predict(self, image_path: str) -> Dict[str, Any]:
        """
        Runs prediction on the given skin lesion image.

        Returns:
            dict containing:
                - success (bool): True if classified by local model, False if fallback
                - predicted_class (str or None): name of predicted disease class
                - confidence (float or None): confidence percentage (0-100)
                - top_classes (list): list of top-k (label, confidence)
                - model_name (str): model identifier used
                - message (str): descriptive status message
        """
        if not self.is_model_loaded():
            return {
                "success": False,
                "predicted_class": None,
                "confidence": None,
                "top_classes": [],
                "model_name": "Groq Vision Direct (Classifier Weights Not Loaded)",
                "message": (
                    "Local trained model weights not found or deep learning framework uninitialized. "
                    "Gracefully using Groq Multimodal Vision analysis."
                )
            }

        try:
            # Preprocess image
            img_arr = preprocess_standard(image_path, target_size=(224, 224))

            if self.backend == "pytorch":
                import torch
                # (H, W, C) -> (1, C, H, W)
                tensor = torch.from_numpy(img_arr.transpose(2, 0, 1)).unsqueeze(0).float()
                # Normalize ImageNet mean/std
                mean = torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1)
                std = torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1)
                tensor = (tensor - mean) / std

                with torch.no_grad():
                    logits = self.model(tensor)
                    probs = torch.softmax(logits, dim=1).squeeze().numpy()

            elif self.backend == "tensorflow":
                # (H, W, C) -> (1, H, W, C)
                batch = np.expand_dims(img_arr, axis=0)
                probs = self.model.predict(batch, verbose=0)[0]
            else:
                raise RuntimeError("No active backend")

            top_idx = int(np.argmax(probs))
            top_conf = float(probs[top_idx]) * 100.0
            pred_class = self.classes[top_idx]

            sorted_indices = np.argsort(probs)[::-1]
            top_classes = [
                {"class": self.classes[i], "confidence": round(float(probs[i]) * 100.0, 2)}
                for i in sorted_indices[:3]
            ]

            return {
                "success": True,
                "predicted_class": pred_class,
                "confidence": round(top_conf, 2),
                "top_classes": top_classes,
                "model_name": self.model_name,
                "message": "Prediction generated by local neural network classifier."
            }

        except Exception as err:
            return {
                "success": False,
                "predicted_class": None,
                "confidence": None,
                "top_classes": [],
                "model_name": "Groq Vision Fallback",
                "message": f"Prediction error: {str(err)}. Falling back to Groq Vision."
            }


# Singleton instance
_PREDICTOR_INSTANCE: Optional[SkinDiseasePredictor] = None


def get_predictor() -> SkinDiseasePredictor:
    global _PREDICTOR_INSTANCE
    if _PREDICTOR_INSTANCE is None:
        _PREDICTOR_INSTANCE = SkinDiseasePredictor()
    return _PREDICTOR_INSTANCE


def predict_skin_disease(image_path: str) -> Dict[str, Any]:
    """Convenience helper to predict skin disease."""
    return get_predictor().predict(image_path)
