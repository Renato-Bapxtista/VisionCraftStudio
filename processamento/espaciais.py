"""Filtros espaciais implementados somente com NumPy."""

import numpy as np


def _convoluir_canais(imagem: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """Aplica convolução aos canais de cor e preserva alfa, quando existir."""
    altura_kernel, largura_kernel = kernel.shape
    margem_y = altura_kernel // 2
    margem_x = largura_kernel // 2

    if len(imagem.shape) == 2:
        canais = imagem
        padding = ((margem_y, margem_y), (margem_x, margem_x))
    else:
        canais = imagem[..., :3]
        padding = ((margem_y, margem_y), (margem_x, margem_x), (0, 0))

    # Repete os pixels das bordas para que a convolução não crie uma moldura preta.
    canais_preenchidos = np.pad(canais.astype(np.float32), padding, mode="edge")
    resultado_canais = np.zeros_like(canais, dtype=np.float32)

    # Cada posição do kernel pondera uma vizinhança deslocada da imagem.
    for y in range(altura_kernel):
        for x in range(largura_kernel):
            resultado_canais += kernel[y, x] * canais_preenchidos[
                y:y + canais.shape[0],
                x:x + canais.shape[1],
                ...,
            ]

    resultado = imagem.copy()
    destino = resultado if len(imagem.shape) == 2 else resultado[..., :3]
    destino[...] = np.clip(resultado_canais, 0, 255).astype(np.uint8)
    return resultado


def suavizar_media(imagem: np.ndarray, tamanho: int = 3) -> np.ndarray:
    """Suaviza a imagem usando a média dos vizinhos em uma janela quadrada."""
    # A soma dos pesos é 1, preservando aproximadamente o brilho médio da imagem.
    kernel = np.ones((tamanho, tamanho), dtype=np.float32) / (tamanho * tamanho)
    return _convoluir_canais(imagem, kernel)


def suavizar_gaussiano(imagem: np.ndarray, sigma: float = 1.0) -> np.ndarray:
    """Suaviza com pesos gaussianos, preservando melhor as transições suaves."""
    # A janela cobre aproximadamente dois desvios-padrão em cada direção.
    raio = max(1, int(np.ceil(sigma * 2)))
    eixo = np.arange(-raio, raio + 1, dtype=np.float32)
    xx, yy = np.meshgrid(eixo, eixo)
    kernel = np.exp(-(xx ** 2 + yy ** 2) / (2 * sigma ** 2))
    # Normalização: evita que o filtro aumente ou diminua o brilho global.
    kernel /= kernel.sum()
    return _convoluir_canais(imagem, kernel)


def realcar_nitidez(imagem: np.ndarray, intensidade: float = 1.0) -> np.ndarray:
    """Realça contornos com uma máscara de nitidez baseada no Laplaciano."""
    # Centro positivo e vizinhos negativos reforçam diferenças locais de intensidade.
    kernel = np.array([
        [0, -intensidade, 0],
        [-intensidade, 1 + 4 * intensidade, -intensidade],
        [0, -intensidade, 0],
    ], dtype=np.float32)
    return _convoluir_canais(imagem, kernel)


def _para_cinza(imagem: np.ndarray) -> np.ndarray:
    """Obtém a luminância usada pelos detectores de bordas."""
    if len(imagem.shape) == 2:
        return imagem.astype(np.float32)
    # Pesos de luminância: o olho humano percebe verde com maior intensidade.
    return np.dot(imagem[..., :3].astype(np.float32), [0.299, 0.587, 0.114])


def _convoluir_matriz(matriz: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """Convolui uma matriz mantendo valores negativos para os gradientes."""
    margem_y, margem_x = kernel.shape[0] // 2, kernel.shape[1] // 2
    # Mantém valores negativos, necessários para derivadas e detecção de bordas.
    preenchida = np.pad(matriz.astype(np.float32), ((margem_y, margem_y), (margem_x, margem_x)), mode="edge")
    resultado = np.zeros_like(matriz, dtype=np.float32)

    for y in range(kernel.shape[0]):
        for x in range(kernel.shape[1]):
            resultado += kernel[y, x] * preenchida[
                y:y + matriz.shape[0],
                x:x + matriz.shape[1],
            ]
    return resultado


def _magnitude_gradiente(imagem: np.ndarray, kernel_x: np.ndarray, kernel_y: np.ndarray, intensidade: float) -> np.ndarray:
    cinza = _para_cinza(imagem)
    gradiente_x = _convoluir_matriz(cinza, kernel_x)
    gradiente_y = _convoluir_matriz(cinza, kernel_y)
    # Combina as derivadas horizontal e vertical na magnitude euclidiana do gradiente.
    magnitude = np.hypot(gradiente_x, gradiente_y) * intensidade
    return np.clip(magnitude, 0, 255).astype(np.uint8)


def detectar_sobel(imagem: np.ndarray, intensidade: float = 1.0) -> np.ndarray:
    """Detecta bordas com o operador Sobel, considerando gradientes horizontal e vertical."""
    # Sobel usa peso 2 na linha/coluna central, tornando o gradiente mais estável.
    kernel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
    kernel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32)
    return _magnitude_gradiente(imagem, kernel_x, kernel_y, intensidade)


def detectar_prewitt(imagem: np.ndarray, intensidade: float = 1.0) -> np.ndarray:
    """Detecta bordas com o operador Prewitt, usando pesos uniformes nos vizinhos."""
    # Prewitt calcula a derivada com pesos uniformes em toda a vizinhança 3x3.
    kernel_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float32)
    kernel_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=np.float32)
    return _magnitude_gradiente(imagem, kernel_x, kernel_y, intensidade)


def detectar_laplaciano(imagem: np.ndarray, intensidade: float = 1.0) -> np.ndarray:
    """Detecta bordas em todas as direções com o operador Laplaciano."""
    # O Laplaciano é uma derivada de segunda ordem e responde a mudanças em qualquer direção.
    kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float32)
    resposta = np.abs(_convoluir_matriz(_para_cinza(imagem), kernel)) * intensidade
    return np.clip(resposta, 0, 255).astype(np.uint8)
