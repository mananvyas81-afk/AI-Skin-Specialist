"""
Classifier package for AI Skin Specialist:
Provides preprocessing, model architectures, training, evaluation, and inference.
"""

from classifier.constants import SKIN_CLASSES, BEST_MODEL_WEIGHTS
from classifier.preprocessing import preprocess_standard, otsu_threshold, preprocess_otsu_segmented
from classifier.prediction import predict_skin_disease, get_predictor, SkinDiseasePredictor

__all__ = [
    "SKIN_CLASSES",
    "BEST_MODEL_WEIGHTS",
    "preprocess_standard",
    "otsu_threshold",
    "preprocess_otsu_segmented",
    "predict_skin_disease",
    "get_predictor",
    "SkinDiseasePredictor"
]
