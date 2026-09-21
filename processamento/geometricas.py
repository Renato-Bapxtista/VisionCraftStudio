"""
Módulo: processamento/geometricas.py
Descrição: Implementação das transformações geométricas de posição dos pixels,
incluindo rotação em 90°, rotação por ângulo genérico, translação, espelhamento e redimensionamento.
"""

import numpy as np
from scipy import ndimage


def rotacionar_90(imagem: np.ndarray, horario: bool = True) -> np.ndarray:
    """
    Rotaciona a imagem em 90 graus no sentido horário ou anti-horário.
    
    Parâmetros:
        imagem (np.ndarray): Matriz da imagem de entrada.
        horario (bool): Se True, rotaciona no sentido horário; se False, anti-horário.
    """
    # np.rot90 por padrão gira no sentido anti-horário k vezes.
    # Para o sentido horário, usamos k=-1 (ou k=3).
    k = -1 if horario else 1
    return np.rot90(imagem, k=k)


def rotacionar_angulo(imagem: np.ndarray, angulo: float) -> np.ndarray:
    """
    Rotaciona a imagem pelo ângulo informado em graus, ajustando as dimensões.
    
    Parâmetros:
        imagem (np.ndarray): Matriz da imagem.
        angulo (float): Ângulo de rotação em graus (aceita valores positivos e negativos).
    """
    return ndimage.rotate(imagem, angulo, reshape=True, mode='constant', cval=0)


def transladar(imagem: np.ndarray, dx: int, dy: int) -> np.ndarray:
    """
    Desloca a imagem horizontalmente (dx) e verticalmente (dy).
    
    Parâmetros:
        imagem (np.ndarray): Matriz da imagem.
        dx (int): Deslocamento horizontal em pixels.
        dy (int): Deslocamento vertical em pixels.
    """
    if len(imagem.shape) == 3:
        shift_tuple = (dy, dx, 0)
    else:
        shift_tuple = (dy, dx)
    return ndimage.shift(imagem, shift=shift_tuple, mode='constant', cval=0)


def espelhar_horizontal(imagem: np.ndarray) -> np.ndarray:
    """Inverte a imagem horizontalmente (esquerda <-> direita)."""
    return np.fliplr(imagem)


def espelhar_vertical(imagem: np.ndarray) -> np.ndarray:
    """Inverte a imagem verticalmente (cima <-> baixo)."""
    return np.flipud(imagem)


def redimensionar(imagem: np.ndarray, escala_percentual: float) -> np.ndarray:
    """
    Redimensiona a imagem proporcionalmente de acordo com a porcentagem informada.
    
    Parâmetros:
        imagem (np.ndarray): Matriz da imagem.
        escala_percentual (float): Porcentagem de redimensionamento (ex: 50 para 50%, 200 para 200%).
    """
    fator = escala_percentual / 100.0
    if len(imagem.shape) == 3:
        fatores_zoom = (fator, fator, 1.0)
    else:
        fatores_zoom = (fator, fator)
    
    # usa ordem 0 (vizinho mais próximo) para manter o tipo de dados uint8
    resultado = ndimage.zoom(imagem, fatores_zoom, order=0)
    return resultado.astype(np.uint8)