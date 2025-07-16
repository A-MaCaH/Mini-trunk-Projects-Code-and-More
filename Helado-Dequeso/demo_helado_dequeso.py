import numpy as np
import pandas as pd
from helado_dequeso import HeladoDeQueso

# Instancia del toolkit
logger = HeladoDeQueso(active=True)

# 1. Logging general
datos = [1, 2, 3]
logger.log("Inicio del demo", title="INFO")

# 2. Inspección de variables
x = np.random.randn(10, 5)
logger.describe(x, name="x")

# 3. Impresión de diccionarios
data = {"accuracy": 0.95, "loss": 0.1}
logger.print_dict(data, title="Resultados")

# 4. Impresión de DataFrames
df = pd.DataFrame({"a": [1,2,3], "b": [4,5,6]})
logger.print_df(df, title="Mi DataFrame")

# 5. Visualización de imágenes
img = np.random.rand(28, 28)
logger.display_image(img, title="Imagen Aleatoria")

# 6. Visualización de grids de imágenes
imgs = np.random.rand(8, 28, 28)
logger.display_image_grid(imgs, title="Batch de imágenes")

# 7. Análisis de pesos de modelos
# PyTorch
try:
    import torch
    import torch.nn as nn
    model_torch = nn.Sequential(nn.Linear(10, 5), nn.ReLU(), nn.Linear(5, 2))
    logger.display_model_weights(model_torch)
except ImportError:
    logger.log("PyTorch no está instalado", title="WARN")

# TensorFlow/Keras
try:
    from tensorflow import keras
    model_keras = keras.Sequential([
        keras.layers.Dense(5, input_shape=(10,)),
        keras.layers.Dense(2)
    ])
    logger.display_model_weights(model_keras)
except ImportError:
    logger.log("TensorFlow no está instalado", title="WARN") 