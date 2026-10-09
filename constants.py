# Classes definition for skin condition classification
# Standard ISIC / Fitzpatrick primary categories common in clinical dermatology
SKIN_CLASSES = [
    "Benign keratosis-like lesions",
    "Melanocytic nevi (moles)",
    "Dermatofibroma",
    "Melanoma (malignant)",
    "Basal cell carcinoma",
    "Vascular lesions",
    "Actinic keratoses"
]

MODEL_METRICS_PATH = "evaluation/model_comparison.json"
CONFUSION_MATRIX_PATH = "evaluation/confusion_matrix.png"
BEST_MODEL_WEIGHTS = "classifier/best_model.pth"
BEST_MODEL_TF = "classifier/best_model.h5"
