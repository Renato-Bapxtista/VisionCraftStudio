"""
Módulo: processamento/espaciais.py
Descrição: Operaçoes por vizinhança, filtros e adição de ruído.
Estratégia de tratamento de bordas: Reflexão (mirroring/reflect).
"""

import numpy as np
from scipy import ndimage


def adicionar_ruido_gaussiano(imagem: np.ndarray, dev_padrao: float = 25.0) -> np.ndarray:
    """Adiciona ruído gaussiano artificial à imagem para testes de filtragem."""
    ruido = np.random.normal(0, dev_padrao, imagem[..., :3].shape)
    img_ruidosa = imagem[..., :3].astype(np.float32) + ruido
    img_ruidosa = np.clip(img_ruidosa, 0, 255).astype(np.uint8)
    
    if len(imagem.shape) == 3 and imagem.shape[2] == 4:
        return np.dstack((img_ruidosa, imagem[..., 3]))
    return img_ruidosa


def suavizar_media(imagem: np.ndarray, tamanho_kernel: int = 3) -> np.ndarray:
    """Filtro da Média usando convolução com tratamento de bordas por reflexão."""
    kernel = np.ones((tamanho_kernel, tamanho_kernel)) / (tamanho_kernel ** 2)
    
    if len(imagem.shape) == 3:
        resultado = np.zeros_like(imagem)
        for i in range(imagem.shape[2]):
            resultado[..., i] = ndimage.convolve(imagem[..., i], kernel, mode='reflect')
        return resultado
    return ndimage.convolve(imagem, kernel, mode='reflect')


def suavizar_gaussiano(imagem: np.ndarray, sigma: float = 1.0) -> np.ndarray:
    """Filtro Gaussiano com tratamento de bordas por reflexão."""
    if len(imagem.shape) == 3:
        resultado = np.zeros_like(imagem)
        for i in range(imagem.shape[2]):
            resultado[..., i] = ndimage.gaussian_filter(imagem[..., i], sigma=sigma, mode='reflect')
        return resultado
    return ndimage.gaussian_filter(imagem, sigma=sigma, mode='reflect')