# NOTA: Este toolkit requiere numpy, pandas, matplotlib, y opcionalmente torch y tensorflow.
# Instala los paquetes necesarios con:
# pip install numpy pandas matplotlib torch tensorflow

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from typing import Any, Optional, List, Union

class HeladoDeQueso:
    """
    Toolkit para manejo de mensajes, depuración y análisis de datos/modelos en proyectos de Machine Learning y Deep Learning.
    """
    def __init__(self, active: bool = True):
        """
        Inicializa el toolkit.
        :param active: Si es False, desactiva toda la salida del toolkit.
        """
        self.active = active

    def log(self, message: str, title: str = "INFO"):
        """
        Imprime un mensaje con un título contextual.
        """
        if not self.active:
            return
        print(f"[{title}] {message}")

    def describe(self, variable: Any, name: str, n: int = 5):
        """
        Imprime información sobre una variable: nombre, tipo, forma y primeros elementos.
        :param variable: Variable a describir.
        :param name: Nombre de la variable.
        :param n: Número de elementos a mostrar.
        """
        if not self.active:
            return
        print(f"\n[DESCRIBE] {name}")
        print(f"  Tipo: {type(variable)}")
        # Forma
        shape = getattr(variable, 'shape', None)
        if shape is not None:
            print(f"  Forma: {shape}")
        # Primeros elementos
        try:
            if isinstance(variable, (np.ndarray, list, tuple)):
                preview = variable[:n]
            elif hasattr(variable, 'cpu') and hasattr(variable, 'numpy'):
                # PyTorch tensor
                preview = variable.cpu().numpy().flatten()[:n]
            elif hasattr(variable, 'numpy'):
                # TensorFlow tensor
                preview = variable.numpy().flatten()[:n]
            else:
                preview = str(variable)
            print(f"  Primeros {n} elementos: {preview}")
        except Exception as e:
            print(f"  No se pudo mostrar preview: {e}")

    def print_dict(self, data: dict, title: str = "DICT"):
        """
        Imprime un diccionario de forma legible con indentación y título.
        """
        if not self.active:
            return
        import pprint
        print(f"\n[{title}] Diccionario:")
        pprint.pprint(data, indent=2, width=80, stream=sys.stdout)

    def print_df(self, df: pd.DataFrame, title: str = "DATAFRAME"):
        """
        Imprime un DataFrame mostrando head, tail e info general.
        """
        if not self.active:
            return
        print(f"\n[{title}] DataFrame:")
        print("Head:")
        print(df.head())
        print("\nTail:")
        print(df.tail())
        print("\nInfo:")
        print(df.info())

    def display_image(self, image: Any, title: str = "IMAGE"):
        """
        Muestra una imagen (NumPy array o tensor) con un título.
        """
        if not self.active:
            return
        plt.figure()
        plt.title(title)
        if hasattr(image, 'cpu') and hasattr(image, 'numpy'):
            # PyTorch tensor
            img = image.cpu().numpy()
        elif hasattr(image, 'numpy'):
            # TensorFlow tensor
            img = image.numpy()
        else:
            img = np.array(image)
        if img.ndim == 2:
            plt.imshow(img, cmap='gray')
        else:
            plt.imshow(img)
        plt.axis('off')
        plt.show()

    def display_image_grid(self, images: Union[List[Any], np.ndarray], title: str = "IMAGE GRID", ncols: int = 5):
        """
        Muestra un lote de imágenes en una cuadrícula.
        :param images: Lista o array de imágenes (N, H, W, C) o (N, H, W).
        :param title: Título de la visualización.
        :param ncols: Número de columnas en la cuadrícula.
        """
        if not self.active:
            return
        # Convertir a array si es lista
        if isinstance(images, list):
            n_images = len(images)
            images_arr = np.array(images)
        else:
            images_arr = images
            n_images = images_arr.shape[0]
        ncols = min(ncols, n_images)
        nrows = int(np.ceil(n_images / ncols))
        plt.figure(figsize=(ncols * 2, nrows * 2))
        plt.suptitle(title)
        for i in range(n_images):
            plt.subplot(nrows, ncols, i + 1)
            img = images_arr[i]
            if img.ndim == 2:
                plt.imshow(img, cmap='gray')
            else:
                plt.imshow(img)
            plt.axis('off')
        plt.tight_layout()
        plt.show()

    def display_model_weights(self, model: Any, layer_name: Optional[str] = None):
        """
        Muestra información y visualización de los pesos de un modelo de red neuronal (PyTorch o Keras/TensorFlow).
        :param model: Modelo de red neuronal.
        :param layer_name: Si se especifica, solo muestra esa capa.
        """
        if not self.active:
            return
        # PyTorch
        if 'torch' in sys.modules and hasattr(model, 'named_parameters'):
            try:
                import torch
            except ImportError:
                print("torch no está instalado.")
                return
            for name, param in model.named_parameters():
                if (layer_name is not None) and (layer_name not in name):
                    continue
                w = param.data.cpu().numpy()
                print(f"\n[WEIGHTS] Capa: {name}")
                print(f"  Forma: {w.shape}")
                print(f"  Media: {w.mean():.4f}, Std: {w.std():.4f}")
                if w.ndim in [2, 4]:
                    plt.figure()
                    plt.title(f"{name} (heatmap)")
                    plt.imshow(w.reshape(w.shape[0], -1), aspect='auto', cmap='viridis')
                    plt.colorbar()
                    plt.show()
        # TensorFlow/Keras
        elif 'tensorflow' in sys.modules and hasattr(model, 'layers'):
            try:
                import tensorflow as tf
            except ImportError:
                print("tensorflow no está instalado.")
                return
            for layer in model.layers:
                if not hasattr(layer, 'get_weights'):
                    continue
                if (layer_name is not None) and (layer_name != layer.name):
                    continue
                weights = layer.get_weights()
                if not weights:
                    continue
                for idx, w in enumerate(weights):
                    print(f"\n[WEIGHTS] Capa: {layer.name} (peso {idx})")
                    print(f"  Forma: {w.shape}")
                    print(f"  Media: {w.mean():.4f}, Std: {w.std():.4f}")
                    if w.ndim in [2, 4]:
                        plt.figure()
                        plt.title(f"{layer.name} (heatmap)")
                        plt.imshow(w.reshape(w.shape[0], -1), aspect='auto', cmap='viridis')
                        plt.colorbar()
                        plt.show()
        else:
            print("Modelo no reconocido. Soporta PyTorch y Keras/TensorFlow.") 