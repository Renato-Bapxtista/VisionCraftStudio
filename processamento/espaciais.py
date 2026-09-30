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
    Adiciona ruído gaussiano independente aos canais RGB para testar filtros.

    Cada amostra é perturbada por N(0, dev_padrao^2), portanto o valor esperado
    permanece inalterado antes do recorte. A saturação em [0, 255] evita
    intensidades inválidas, mas pode introduzir viés próximo aos extremos.
    Para imagens RGBA, o canal alfa é copiado sem ruído.
    """
    ruido = np.random.normal(0, dev_padrao, imagem[..., :3].shape)
    img_ruidosa = imagem[..., :3].astype(np.float32) + ruido
    img_ruidosa = np.clip(img_ruidosa, 0, 255).astype(np.uint8)
    
    if len(imagem.shape) == 3 and imagem.shape[2] == 4:
        return np.dstack((img_ruidosa, imagem[..., 3]))
    return img_ruidosa


def suavizar_media(imagem: np.ndarray, tamanho_kernel: int = 3) -> np.ndarray:
    """
    Suaviza por convolução com uma janela quadrada de pesos uniformes.

    O kernel soma 1, preservando aproximadamente o nível médio de intensidade.
    A operação reduz variações locais e ruído, mas também desfoca bordas e
    detalhes finos. A reflexão nas bordas evita preencher a vizinhança externa
    com zeros; em RGBA, somente os canais de cor são filtrados.
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
    Suaviza com um kernel gaussiano separável e bordas refletidas.

    O parâmetro sigma controla o desvio-padrão espacial do kernel: valores
    maiores espalham mais a contribuição dos vizinhos e produzem mais desfoque.
    A ponderação maior dos pixels próximos tende a preservar estrutura melhor
    que a média uniforme. Para RGBA, o alfa original é mantido sem filtragem.
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
    Realça detalhes por máscara de nitidez (unsharp masking).

    Subtrai da imagem uma versão suavizada para estimar componentes de alta
    frequência e soma essa máscara à imagem original. Intensidade zero não
    acrescenta detalhes; valores maiores reforçam contornos, mas podem amplificar
    ruído e gerar saturação, limitada aqui ao intervalo [0, 255]. Em RGBA, o
    processamento usa RGB e preserva o alfa original.
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
    Converte a entrada para uma matriz 2D float32 apropriada aos operadores.

    Para RGB/RGBA, calcula luminância ponderada (0,299R + 0,587G + 0,114B),
    aproximando a sensibilidade visual humana. O canal alfa não participa do
    cálculo; imagens já 2D são apenas convertidas para float32.
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
    Estima bordas pelo gradiente de primeira ordem usando operadores Sobel.

    A imagem é convertida para luminância e filtrada nos eixos de linhas e
    colunas. A magnitude sqrt(Gx^2 + Gy^2) combina as duas direções e reduz a
    dependência da orientação da borda; intensidade escala essa magnitude antes
    do recorte para 8 bits. O resultado é uma imagem RGB em tons de cinza.
    """
    cinza = _obter_matriz_cinza_2d(imagem)
    
    sx = ndimage.sobel(cinza, axis=0, mode='reflect')
    sy = ndimage.sobel(cinza, axis=1, mode='reflect')
    
    magnitude = np.hypot(sx, sy) * intensidade
    magnitude = np.clip(magnitude, 0, 255).astype(np.uint8)
    
    return np.dstack((magnitude, magnitude, magnitude))


def detectar_prewitt(imagem: np.ndarray, intensidade: float = 1.0) -> np.ndarray:
    """
    Estima bordas por diferenças de primeira ordem com máscaras Prewitt 3x3.

    As máscaras aproximam derivadas nas direções horizontal e vertical, com
    pesos uniformes na direção de agregação. A magnitude euclidiana combina os
    dois gradientes; intensidade a escala antes da conversão para 8 bits. A
    saída é RGB em tons de cinza, com as bordas mais fortes mais claras.
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
    Realça transições de intensidade usando o Laplaciano de segunda ordem.

    Ao contrário de Sobel e Prewitt, o Laplaciano responde a variações em todas
    as direções sem estimar um vetor de orientação. O valor absoluto mantém
    transições positivas e negativas; intensidade escala a resposta antes do
    recorte para 8 bits. Como derivadas de segunda ordem são sensíveis a ruído,
    uma suavização prévia pode ser necessária em imagens ruidosas.
    """
    cinza = _obter_matriz_cinza_2d(imagem)
    
    lap = ndimage.laplace(cinza, mode='reflect')
    magnitude = np.abs(lap) * intensidade
    magnitude = np.clip(magnitude, 0, 255).astype(np.uint8)
    
    return np.dstack((magnitude, magnitude, magnitude))