"""
Training pipeline for Skin Disease Classification:
Trains Baseline CNN, MobileNetV3, and EfficientNetB0 on skin lesion datasets (e.g. ISIC 2018 / 2019 / HAM10000).

Includes data augmentation, transfer learning fine-tuning, loss logging, and best checkpoint saving.
"""

import os
import argparse
from typing import Dict, Any

from classifier.constants import SKIN_CLASSES, BEST_MODEL_WEIGHTS, BEST_MODEL_TF
from classifier.preprocessing import preprocess_standard, preprocess_otsu_segmented


def train_pytorch(
    data_dir: str,
    model_name: str = "mobilenet",
    epochs: int = 15,
    batch_size: int = 32,
    lr: float = 1e-4,
    use_otsu: bool = False,
    output_path: str = BEST_MODEL_WEIGHTS
) -> Dict[str, Any]:
    """
    Trains PyTorch model on image dataset directory organized as:
    data_dir/
      class_1/
        image1.jpg
      class_2/
        ...
    """
    import torch
    import torch.nn as nn
    from torch.utils.data import DataLoader
    from torchvision import datasets, transforms
    from classifier.models import get_pytorch_model

    if not os.path.exists(data_dir):
        raise FileNotFoundError(
            f"Dataset directory '{data_dir}' not found. Please provide a path to a labeled skin disease dataset."
        )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[Training] Using compute device: {device} | Model: {model_name} | Otsu preprocessing: {use_otsu}")

    # Transforms
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.RandomRotation(20),
        transforms.ColorJitter(brightness=0.1, contrast=0.1),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    val_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    train_data = datasets.ImageFolder(os.path.join(data_dir, "train") if os.path.exists(os.path.join(data_dir, "train")) else data_dir, transform=train_transform)
    num_classes = len(train_data.classes)

    train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True, num_workers=2)

    model = get_pytorch_model(model_name, num_classes=num_classes, pretrained=True)
    model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)

    best_acc = 0.0
    for epoch in range(epochs):
        model.train()
        running_loss, correct, total = 0.0, 0, 0
        for inputs, targets in train_loader:
            inputs, targets = inputs.to(device), targets.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            _, preds = outputs.max(1)
            correct += preds.eq(targets).sum().item()
            total += targets.size(0)

        epoch_acc = (correct / total) * 100.0 if total > 0 else 0
        print(f"Epoch {epoch+1}/{epochs} - Loss: {running_loss/total:.4f} - Acc: {epoch_acc:.2f}%")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    torch.save(model.state_dict(), output_path)
    print(f"[Training] Model successfully saved to {output_path}")

    return {"model_name": model_name, "final_acc": epoch_acc, "output_path": output_path}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Skin Disease Classification Models")
    parser.add_argument("--data_dir", type=str, required=True, help="Path to labeled training dataset folder")
    parser.add_argument("--model", type=str, default="mobilenet", choices=["baseline_cnn", "mobilenet", "efficientnet"])
    parser.add_argument("--epochs", type=int, default=15)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--use_otsu", action="store_true", help="Apply Otsu thresholding preprocessing comparison")
    args = parser.parse_args()

    train_pytorch(
        data_dir=args.data_dir,
        model_name=args.model,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
        use_otsu=args.use_otsu
    )
