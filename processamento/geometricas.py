"""Transformações geométricas implementadas com NumPy."""

import numpy as np


def rotacionar_90(imagem: np.ndarray, sentido_horario: bool = True) -> np.ndarray:
    """Rotaciona a imagem em 90 graus no sentido escolhido."""
    # np.rot90 apenas reorganiza os índices, sem interpolar ou perder detalhes.
    return np.rot90(imagem, k=-1 if sentido_horario else 1).copy()


def espelhar_horizontal(imagem: np.ndarray) -> np.ndarray:
    """Inverte a imagem da esquerda para a direita."""
    return imagem[:, ::-1].copy()


def espelhar_vertical(imagem: np.ndarray) -> np.ndarray:
    """Inverte a imagem de cima para baixo."""
    return imagem[::-1, :].copy()


def redimensionar(imagem: np.ndarray, escala_percentual: int) -> np.ndarray:
    """Redimensiona preservando a proporção, por interpolação do vizinho mais próximo."""
    altura, largura = imagem.shape[:2]
    nova_altura = max(1, round(altura * escala_percentual / 100))
    nova_largura = max(1, round(largura * escala_percentual / 100))
    # Mapeia cada pixel de saída ao pixel de entrada mais próximo.
    indices_y = (np.arange(nova_altura) * altura // nova_altura).astype(int)
    indices_x = (np.arange(nova_largura) * largura // nova_largura).astype(int)
    return imagem[indices_y[:, np.newaxis], indices_x].copy()
