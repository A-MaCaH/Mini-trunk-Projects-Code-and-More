# DebugLogger Toolkit

Herramienta autocontenida para manejo de mensajes, depuración y análisis de datos y modelos en proyectos de Machine Learning y Deep Learning.

## Descripción

`DebugLogger` es una clase de Python diseñada para facilitar el logging, la inspección de variables, la visualización de datos y el análisis de modelos de redes neuronales (PyTorch y Keras/TensorFlow). Es fácil de integrar y portable a cualquier proyecto.

## Instalación de dependencias

Instala las dependencias necesarias con:

```bash
pip install numpy pandas matplotlib torch tensorflow
```

Puedes omitir `torch` o `tensorflow` si no usas esos frameworks.

## Uso básico

Copia el archivo `debug_logger.py` a tu proyecto e impórtalo:

```python
from debug_logger import DebugLogger
logger = DebugLogger(active=True)
```

## Métodos principales y ejemplos

### 1. Logging general
```python
logger.log("Entrenamiento iniciado", title="INFO")
logger.log("¡Error en la carga de datos!", title="ERROR")
```

### 2. Inspección de variables
```python
import numpy as np
x = np.random.randn(10, 5)
logger.describe(x, name="x")
```

### 3. Impresión de diccionarios
```python
data = {"accuracy": 0.95, "loss": 0.1}
logger.print_dict(data, title="Resultados")
```

### 4. Impresión de DataFrames
```python
import pandas as pd
df = pd.DataFrame({"a": [1,2,3], "b": [4,5,6]})
logger.print_df(df, title="Mi DataFrame")
```

### 5. Visualización de imágenes
```python
img = np.random.rand(28, 28)
logger.display_image(img, title="Imagen Aleatoria")
```

### 6. Visualización de grids de imágenes
```python
imgs = np.random.rand(8, 28, 28)
logger.display_image_grid(imgs, title="Batch de imágenes")
```

### 7. Análisis de pesos de modelos
#### PyTorch
```python
import torch.nn as nn
model = nn.Sequential(nn.Linear(10, 5), nn.ReLU(), nn.Linear(5, 2))
logger.display_model_weights(model)
```
#### TensorFlow/Keras
```python
from tensorflow import keras
model = keras.Sequential([
    keras.layers.Dense(5, input_shape=(10,)),
    keras.layers.Dense(2)
])
logger.display_model_weights(model)
```

## Notas
- Si inicializas con `active=False`, ningún método producirá salida.
- El toolkit es extensible y puede adaptarse a otros frameworks.

---

**Autor:** Desarrollador experto en Python y Deep Learning 