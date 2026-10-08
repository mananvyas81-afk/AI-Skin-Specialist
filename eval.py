"""Evaluation metrics. Put labelled test images in test_data/<condition>/*.jpg, then: python eval.py
Prints accuracy, precision, recall, F1 and a confusion matrix; saves metrics.txt for the report."""
import pathlib
from collections import Counter

from Doctors_Brain import brain_of_the_doctor

root = pathlib.Path("test_data")
y_true, y_pred = [], []
for folder in sorted(p for p in root.iterdir() if p.is_dir()):
    for img in list(folder.glob("*.*"))[:10]:
        try:
            top = brain_of_the_doctor("", str(img))["predictions"][0][0].lower()
        except Exception as e:
            print("skip", img.name, e); continue
        y_true.append(folder.name.lower()); y_pred.append(top)
        print(img.name, "->", top)

# a prediction counts as correct if the true label appears in the predicted text
y_pred = [t if t in p else p for t, p in zip(y_true, y_pred)]
labels = sorted(set(y_true))
acc = sum(t == p for t, p in zip(y_true, y_pred)) / len(y_true)
out = [f"Samples: {len(y_true)}   Accuracy: {acc:.2%}", f"{'class':20}{'prec':>8}{'recall':>8}{'f1':>8}"]
for c in labels:
    tp = sum(t == c and p == c for t, p in zip(y_true, y_pred))
    pr = tp / max(1, sum(p == c for p in y_pred)); rc = tp / max(1, sum(t == c for t in y_true))
    out.append(f"{c:20}{pr:8.2f}{rc:8.2f}{(2*pr*rc/(pr+rc) if pr+rc else 0):8.2f}")
out.append("Confusion (true -> predicted): " + str(dict(Counter(zip(y_true, y_pred)))))
print("\n".join(out)); open("metrics.txt", "w").write("\n".join(out))
