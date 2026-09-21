"""
Módulo: processamento/geometricas.py
Descrição: Transformações geométricas de posição dos pixels.
"""

import numpy as np
from scipy import ndimage


def rotacionar_angulo(imagem: np.ndarray, angulo: float) -> np.ndarray:
    """Rotaciona a imagem pelo ângulo informado em graus, ajustando as dimensões."""
    return ndimage.rotate(imagem, angulo, reshape=True, mode='constant', cval=0)


def transladar(imagem: np.ndarray, dx: int, dy: int) -> np.ndarray:
    """Desloca a imagem horizontalmente (dx) e verticalmente (dy)."""
    return ndimage.shift(imagem, shift=(dy, dx, 0) if len(imagem.shape) == 3 else (dy, dx), mode='constant', cval=0)


def espelhar_horizontal(imagem: np.ndarray) -> np.ndarray:
    """Inverte a imagem horizontalmente."""
    return np.fliplr(imagem)


def espelhar_vertical(imagem: np.ndarray) -> np.ndarray:
    """Inverte a imagem verticalmente."""
    return np.flipud(imagem)