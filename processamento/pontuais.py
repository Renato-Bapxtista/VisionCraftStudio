"""
Módulo: processamento/pontuais.py
Descrição: Implementação das transformações de intensidade e histograma.
"""

import numpy as np


def converter_para_cinza(imagem: np.ndarray) -> np.ndarray:
    """Converte uma imagem RGB para escala de cinzas usando luminância."""
    if len(imagem.shape) == 2:
        return imagem.copy()
    cinza = np.dot(imagem[..., :3], [0.299, 0.587, 0.114]).astype(np.uint8)
    if imagem.shape[2] == 4:
        return np.dstack((cinza, cinza, cinza, imagem[..., 3]))
    return cinza


def ajustar_brilho(imagem: np.ndarray, valor: int) -> np.ndarray:
    """Soma/subtrai um valor escalar garantindo o limite de 8 bits (0-255)."""
    resultado = imagem.astype(np.int16) + valor
    return np.clip(resultado, 0, 255).astype(np.uint8)


def ajustar_contraste(imagem: np.ndarray, fator: float) -> np.ndarray:
    """Multiplica as intensidades pelo fator de contraste."""
    resultado = imagem.astype(np.float32) * fator
    return np.clip(resultado, 0, 255).astype(np.uint8)


def aplicar_negativo(imagem: np.ndarray) -> np.ndarray:
    """Inverte os valores de intensidade (255 - pixel)."""
    resultado = 255 - imagem[..., :3]
    if len(imagem.shape) == 3 and imagem.shape[2] == 4:
        return np.dstack((resultado, imagem[..., 3]))
    return resultado.astype(np.uint8)


def alongar_contraste(imagem: np.ndarray) -> np.ndarray:
    """Expande a faixa dinamica de intensidades para ocupar todo o intervalo [0, 255]."""
    img_float = imagem[..., :3].astype(np.float32)
    i_min = np.min(img_float)
    i_max = np.max(img_float)
    
    if i_max == i_min:
        return imagem.copy()

    alongado = ((img_float - i_min) / (i_max - i_min)) * 255.0
    alongado = np.clip(alongado, 0, 255).astype(np.uint8)

    if len(imagem.shape) == 3 and imagem.shape[2] == 4:
        return np.dstack((alongado, imagem[..., 3]))
    return alongado


def equalizar_histograma(imagem: np.ndarray) -> np.ndarray:
    """Equaliza o histograma das intensidades da imagem."""
    if len(imagem.shape) == 3 and imagem.shape[2] >= 3:
        # Para imagens coloridas, trabalha na luminancia para preservar tons
        cinza = converter_para_cinza(imagem)[..., 0]
        hist, _ = np.histogram(cinza.flatten(), 256, [0, 256])
        cdf = hist.cumsum()
        cdf_m = np.ma.masked_equal(cdf, 0)
        cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf.max() - cdf_m.min())
        tabela = np.ma.filled(cdf_m, 0).astype('uint8')
        
        # Aplica a variacao de ganho mantendo proporcao
        fator = tabela[cinza].astype(np.float32) / (cinza.astype(np.float32) + 1e-5)
        res = np.clip(imagem[..., :3].astype(np.float32) * fator[..., None], 0, 255).astype(np.uint8)
        if imagem.shape[2] == 4:
            return np.dstack((res, imagem[..., 3]))
        return res
    else:
        hist, _ = np.histogram(imagem.flatten(), 256, [0, 256])
        cdf = hist.cumsum()
        cdf_m = np.ma.masked_equal(cdf, 0)
        cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf.max() - cdf_m.min())
        return np.ma.filled(cdf_m, 0).astype('uint8')[imagem]