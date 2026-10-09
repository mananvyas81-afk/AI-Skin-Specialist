"""
Model Architectures for Skin Disease Classification:
1. Baseline CNN: Lightweight custom Convolutional Neural Network
2. MobileNetV3 (Small/Large): Efficient mobile-targeted transfer learning architecture
3. EfficientNetB0: State-of-the-art scalable transfer learning architecture

Supports PyTorch and TensorFlow / Keras backends seamlessly.
"""

def get_pytorch_model(model_name: str, num_classes: int = 7, pretrained: bool = True):
    """
    Constructs PyTorch model architecture with ImageNet pretrained weights (where requested).
    """
    import torch
    import torch.nn as nn
    import torchvision.models as models

    model_name = model_name.lower().replace("-", "").replace("_", "")

    if "baseline" in model_name or "cnn" in model_name:
        class BaselineCNN(nn.Module):
            def __init__(self, num_classes=num_classes):
                super().__init__()
                self.features = nn.Sequential(
                    nn.Conv2d(3, 32, kernel_size=3, padding=1),
                    nn.BatchNorm2d(32),
                    nn.ReLU(inplace=True),
                    nn.MaxPool2d(2, 2),  # 112x112

                    nn.Conv2d(32, 64, kernel_size=3, padding=1),
                    nn.BatchNorm2d(64),
                    nn.ReLU(inplace=True),
                    nn.MaxPool2d(2, 2),  # 56x56

                    nn.Conv2d(64, 128, kernel_size=3, padding=1),
                    nn.BatchNorm2d(128),
                    nn.ReLU(inplace=True),
                    nn.MaxPool2d(2, 2),  # 28x28

                    nn.Conv2d(128, 256, kernel_size=3, padding=1),
                    nn.BatchNorm2d(256),
                    nn.ReLU(inplace=True),
                    nn.AdaptiveAvgPool2d((1, 1))
                )
                self.classifier = nn.Sequential(
                    nn.Dropout(0.4),
                    nn.Linear(256, 128),
                    nn.ReLU(inplace=True),
                    nn.Dropout(0.3),
                    nn.Linear(128, num_classes)
                )

            def forward(self, x):
                x = self.features(x)
                x = torch.flatten(x, 1)
                x = self.classifier(x)
                return x

        return BaselineCNN(num_classes)

    elif "mobilenet" in model_name:
        weights = models.MobileNet_V3_Small_Weights.DEFAULT if pretrained else None
        model = models.mobilenet_v3_small(weights=weights)
        in_features = model.classifier[3].in_features
        model.classifier[3] = nn.Linear(in_features, num_classes)
        return model

    elif "efficientnet" in model_name:
        weights = models.EfficientNet_B0_Weights.DEFAULT if pretrained else None
        model = models.efficientnet_b0(weights=weights)
        in_features = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(in_features, num_classes)
        return model

    else:
        raise ValueError(f"Unknown model name: {model_name}")


def get_tf_model(model_name: str, num_classes: int = 7, pretrained: bool = True):
    """
    Constructs TensorFlow/Keras model architecture.
    """
    import tensorflow as tf
    from tensorflow.keras import layers, models

    model_name = model_name.lower().replace("-", "").replace("_", "")

    if "baseline" in model_name or "cnn" in model_name:
        model = models.Sequential([
            layers.Input(shape=(224, 224, 3)),
            layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),

            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),

            layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),

            layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.GlobalAveragePooling2D(),

            layers.Dropout(0.4),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(num_classes, activation='softmax')
        ])
        return model

    elif "mobilenet" in model_name:
        weights = "imagenet" if pretrained else None
        base = tf.keras.applications.MobileNetV3Small(
            input_shape=(224, 224, 3),
            include_top=False,
            weights=weights,
            pooling='avg'
        )
        x = layers.Dropout(0.3)(base.output)
        out = layers.Dense(num_classes, activation='softmax')(x)
        return tf.keras.Model(inputs=base.input, outputs=out)

    elif "efficientnet" in model_name:
        weights = "imagenet" if pretrained else None
        base = tf.keras.applications.EfficientNetB0(
            input_shape=(224, 224, 3),
            include_top=False,
            weights=weights,
            pooling='avg'
        )
        x = layers.Dropout(0.3)(base.output)
        out = layers.Dense(num_classes, activation='softmax')(x)
        return tf.keras.Model(inputs=base.input, outputs=out)

    else:
        raise ValueError(f"Unknown model name: {model_name}")
