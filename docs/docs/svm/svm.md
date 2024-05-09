---
sidebar_position: 1
---

# SVM class

A class to store the data, methods and artifacts for _Principal Component Analysis_.

## Syntax

```python
PCA(fused_data, settings)
```

## Constructor parameters

- `fused_data`: object of type [`LLDF`](../lldf/lldf.md). Contains the data to be analyzed.
- `settings`: object of type [`SVMSettings`](./svmsettings.md). Contains the settings for
  the `SVM` object.

The constructor raises:
- `ValueError("Fused data input cannot be empty.")` if the input data is null
- `valueError("Settings cannot be empty.")` if the settings are null

## Fields

- `fused_data`: object of type [`LLDF`](../lldf/lldf.md). Contains the data to be analyzed.
- `settings`: object of type [`SVMSettings`](./svmsettings.md). Contains the settings for
  the `PCA` object. 
- `pca_model`: an `SVM` model from `scikit-learn`. Defaults to `None`.

## Methods

- `svm(self)`: performs Support Vector Machine analysis.
  - *raises*:
    - `ValueError(SVM: this type of kernel does not exist.")` if the kernel type is invalid
- `predict(self, x_data)`: performs classification based on SVM
  - *raises*:
    - `RuntimeError("The model hasn't been trained yet!")` if the model is null
    -  `TypeError("X data for prediction cannot be empty.")` if the input data is null

## Example

```python
from svm import SVM

# Initialize and run the SVM class
svm = LDA(lldf.fused_data, settings)
svm.svm()
```