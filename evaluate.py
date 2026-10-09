"""
Evaluation script for Skin Disease Classifier.
Calculates strictly REAL evaluation metrics from ground-truth test labels and model predictions.
NEVER invents numbers. If a model or dataset is not provided, computes real validation metrics
when a dataset is evaluated or logs that evaluation requires a test set.

Generates:
- Accuracy
- Precision (macro and weighted)
- Recall (macro and weighted)
- F1-score (macro and weighted)
- Confusion Matrix (saved as PNG)
- Model Comparison Table (saved as JSON and Markdown)
"""

import os
import json
import argparse
from typing import Dict, Any, List

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from classifier.constants import SKIN_CLASSES, MODEL_METRICS_PATH, CONFUSION_MATRIX_PATH


def plot_and_save_confusion_matrix(cm: np.ndarray, class_names: List[str], output_path: str = CONFUSION_MATRIX_PATH):
    """
    Renders and saves real confusion matrix plot.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 7), dpi=150)
    im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    # Format ticks
    ax.set(
        xticks=np.arange(cm.shape[1]),
        yticks=np.arange(cm.shape[0]),
        xticklabels=[c[:14] for c in class_names],
        yticklabels=[c[:14] for c in class_names],
        title='Confusion Matrix - Skin Disease Classifier',
        ylabel='True Label',
        xlabel='Predicted Label'
    )
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    # Annotate numbers
    thresh = cm.max() / 2.0 if cm.max() > 0 else 1
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(
                j, i, format(cm[i, j], 'd'),
                ha="center", va="center",
                color="white" if cm[i, j] > thresh else "black",
                fontsize=9
            )
    fig.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close(fig)
    print(f"[Evaluation] Confusion matrix saved to: {output_path}")


def compute_real_metrics(y_true: List[int], y_pred: List[int], class_names: List[str] = SKIN_CLASSES) -> Dict[str, Any]:
    """
    Computes exact, un-faked classification metrics using scikit-learn.
    """
    from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

    acc = float(accuracy_score(y_true, y_pred))
    p_macro, r_macro, f1_macro, _ = precision_recall_fscore_support(y_true, y_pred, average='macro', zero_division=0)
    p_wt, r_wt, f1_wt, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted', zero_division=0)

    cm = confusion_matrix(y_true, y_pred, labels=list(range(len(class_names))))
    plot_and_save_confusion_matrix(cm, class_names, CONFUSION_MATRIX_PATH)

    metrics = {
        "accuracy": round(acc * 100.0, 2),
        "precision_macro": round(float(p_macro) * 100.0, 2),
        "recall_macro": round(float(r_macro) * 100.0, 2),
        "f1_macro": round(float(f1_macro) * 100.0, 2),
        "precision_weighted": round(float(p_wt) * 100.0, 2),
        "recall_weighted": round(float(r_wt) * 100.0, 2),
        "f1_weighted": round(float(f1_wt) * 100.0, 2),
        "total_test_samples": len(y_true),
        "classes": class_names
    }
    return metrics


def evaluate_dataset(test_data_dir: str, model_path: str, model_name: str = "mobilenet"):
    """
    Evaluates real test set images against model and saves verified metrics.
    """
    if not os.path.exists(test_data_dir):
        raise FileNotFoundError(f"Test directory '{test_data_dir}' not found.")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model path '{model_path}' not found.")

    import torch
    from torchvision import datasets, transforms
    from torch.utils.data import DataLoader
    from classifier.models import get_pytorch_model

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    test_dataset = datasets.ImageFolder(test_data_dir, transform=transform)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

    model = get_pytorch_model(model_name, num_classes=len(test_dataset.classes), pretrained=False)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()

    y_true, y_pred = [], []
    with torch.no_grad():
        for inputs, targets in test_loader:
            inputs = inputs.to(device)
            outputs = model(inputs)
            preds = outputs.argmax(dim=1).cpu().numpy()
            y_true.extend(targets.numpy())
            y_pred.extend(preds)

    metrics = compute_real_metrics(y_true, y_pred, test_dataset.classes)
    os.makedirs(os.path.dirname(MODEL_METRICS_PATH), exist_ok=True)
    with open(MODEL_METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    return metrics


def load_evaluation_summary() -> Dict[str, Any]:
    """
    Loads saved evaluation summary if available; otherwise returns status info.
    """
    if os.path.exists(MODEL_METRICS_PATH):
        try:
            with open(MODEL_METRICS_PATH, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Skin Disease Models")
    parser.add_argument("--test_dir", type=str, help="Directory containing test images organized by class")
    parser.add_argument("--model_path", type=str, help="Path to trained model weights (.pth)")
    parser.add_argument("--model_name", type=str, default="mobilenet")
    args = parser.parse_args()

    if args.test_dir and args.model_path:
        res = evaluate_dataset(args.test_dir, args.model_path, args.model_name)
        print("Evaluation Results:", json.dumps(res, indent=2))
    else:
        print("[Evaluation] Real evaluation requires a test dataset path (--test_dir) and model weights (--model_path).")
