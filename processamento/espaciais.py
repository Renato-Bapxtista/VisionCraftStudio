"""
Módulo: processamento/espaciais.py
Descrição: Implementação das operações por vizinhança, filtros espaciais,
detecção de bordas e adição de ruído artificial.

Estratégia de tratamento de bordas: Reflexão (mirroring/reflect).
"""

import numpy as np
from scipy import ndimage


def adicionar_ruido_gaussiano(imagem: np.ndarray, dev_padrao: float = 25.0) -> np.ndarray:
    """
    Adiciona ruído gaussiano artificial à imagem para testes de filtros de suavização.
    """
    ruido = np.random.normal(0, dev_padrao, imagem[..., :3].shape)
    img_ruidosa = imagem[..., :3].astype(np.float32) + ruido
    img_ruidosa = np.clip(img_ruidosa, 0, 255).astype(np.uint8)
    
    if len(imagem.shape) == 3 and imagem.shape[2] == 4:
        return np.dstack((img_ruidosa, imagem[..., 3]))
    return img_ruidosa


def suavizar_media(imagem: np.ndarray, tamanho_kernel: int = 3) -> np.ndarray:
    """
    Filtro da Média usando convolução com pesos iguais.
    """
    kernel = np.ones((tamanho_kernel, tamanho_kernel)) / (tamanho_kernel ** 2)
    
    if len(imagem.shape) == 3:
        resultado = np.zeros_like(imagem)
        limite_canais = 3 if imagem.shape[2] == 4 else imagem.shape[2]
        for i in range(limite_canais):
            resultado[..., i] = ndimage.convolve(imagem[..., i], kernel, mode='reflect')
        if imagem.shape[2] == 4:
            resultado[..., 3] = imagem[..., 3]
        return resultado
    return ndimage.convolve(imagem, kernel, mode='reflect')


def suavizar_gaussiano(imagem: np.ndarray, sigma: float = 1.0) -> np.ndarray:
    """
    Filtro Gaussiano com tratamento de bordas por reflexão.
    """
    if len(imagem.shape) == 3:
        resultado = np.zeros_like(imagem)
        limite_canais = 3 if imagem.shape[2] == 4 else imagem.shape[2]
        for i in range(limite_canais):
            resultado[..., i] = ndimage.gaussian_filter(imagem[..., i], sigma=sigma, mode='reflect')
        if imagem.shape[2] == 4:
            resultado[..., 3] = imagem[..., 3]
        return resultado
    return ndimage.gaussian_filter(imagem, sigma=sigma, mode='reflect')


def realcar_nitidez(imagem: np.ndarray, intensidade: float = 1.0) -> np.ndarray:
    """
    Realça detalhes e contornos da imagem (Unsharp Masking).
    """
    suavizada = suavizar_gaussiano(imagem, sigma=1.0).astype(np.float32)
    original_float = imagem[..., :3].astype(np.float32)
    
    detalhes = original_float - suavizada[..., :3]
    nitida = original_float + (intensidade * detalhes)
    nitida = np.clip(nitida, 0, 255).astype(np.uint8)
    
    if len(imagem.shape) == 3 and imagem.shape[2] == 4:
        return np.dstack((nitida, imagem[..., 3]))
    return nitida


def _obter_matriz_cinza_2d(imagem: np.ndarray) -> np.ndarray:
    """
    Função auxiliar interna para garantir que a imagem de entrada 
    seja convertida para uma matriz 2D (escala de cinzas).
    """
    if len(imagem.shape) == 2:
        return imagem.astype(np.float32)
    elif len(imagem.shape) == 3:
        # Fórmula padrão de luminância
        cinza_2d = np.dot(imagem[..., :3].astype(np.float32), [0.299, 0.587, 0.114])
        return cinza_2d
    return imagem.astype(np.float32)


def detectar_sobel(imagem: np.ndarray, intensidade: float = 1.0) -> np.ndarray:
    """
    Detetor de bordas Sobel.
    Calcula os gradientes horizontais e verticais em uma matriz 2D.
    """
    cinza = _obter_matriz_cinza_2d(imagem)
    
    sx = ndimage.sobel(cinza, axis=0, mode='reflect')
    sy = ndimage.sobel(cinza, axis=1, mode='reflect')
    
    magnitude = np.hypot(sx, sy) * intensidade
    magnitude = np.clip(magnitude, 0, 255).astype(np.uint8)
    
    return np.dstack((magnitude, magnitude, magnitude))


def detectar_prewitt(imagem: np.ndarray, intensidade: float = 1.0) -> np.ndarray:
    """
    Detetor de bordas Prewitt.
    Aplica as máscaras de convolução Prewitt nos eixos X e Y.
    """
    cinza = _obter_matriz_cinza_2d(imagem)
    
    kernel_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
    kernel_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
    
    px = ndimage.convolve(cinza, kernel_x, mode='reflect')
    py = ndimage.convolve(cinza, kernel_y, mode='reflect')
    
    magnitude = np.hypot(px, py) * intensidade
    magnitude = np.clip(magnitude, 0, 255).astype(np.uint8)
    
    return np.dstack((magnitude, magnitude, magnitude))


def detectar_laplaciano(imagem: np.ndarray, intensidade: float = 1.0) -> np.ndarray:
    """
    Detetor de bordas Laplaciano.
    Aplica o operador diferencial de segunda ordem.
    """
    cinza = _obter_matriz_cinza_2d(imagem)
    
    lap = ndimage.laplace(cinza, mode='reflect')
    magnitude = np.abs(lap) * intensidade
    magnitude = np.clip(magnitude, 0, 255).astype(np.uint8)
    
    return np.dstack((magnitude, magnitude, magnitude))