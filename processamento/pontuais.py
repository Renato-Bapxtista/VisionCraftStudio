"""
Módulo: processamento/pontuais.py
Descrição: Contém as funções de transformação pontual de intensidade de pixels,
incluindo conversão para cinza, brilho, contraste, gama, negativo, sépia, 
posterização, binarização, alongamento de contraste e equalização de histograma.
"""

import numpy as np


def converter_para_cinza(imagem: np.ndarray) -> np.ndarray:
    """Converte uma imagem RGB/RGBA para escala de cinza usando luminância."""
    if len(imagem.shape) == 2:
        return imagem.copy()
    cinza = np.dot(imagem[..., :3].astype(np.float32), [0.299, 0.587, 0.114]).astype(np.uint8)
    if imagem.shape[2] == 4:
        return np.dstack((cinza, cinza, cinza, imagem[..., 3]))
    return np.dstack((cinza, cinza, cinza))


def ajustar_brilho(imagem: np.ndarray, valor: int) -> np.ndarray:
    """Aumenta ou reduz o brilho somando/subtraindo um valor das intensidades."""
    if len(imagem.shape) == 3 and imagem.shape[2] == 4:
        rgb = np.clip(imagem[..., :3].astype(np.int16) + valor, 0, 255).astype(np.uint8)
        return np.dstack((rgb, imagem[..., 3]))
    resultado = np.clip(imagem.astype(np.int16) + valor, 0, 255).astype(np.uint8)
    return resultado


def ajustar_contraste(imagem: np.ndarray, fator: float) -> np.ndarray:
    """Aumenta ou reduz o contraste multiplicando as intensidades pelo fator."""
    if len(imagem.shape) == 3 and imagem.shape[2] == 4:
        rgb = np.clip(imagem[..., :3].astype(np.float32) * fator, 0, 255).astype(np.uint8)
        return np.dstack((rgb, imagem[..., 3]))
    resultado = np.clip(imagem.astype(np.float32) * fator, 0, 255).astype(np.uint8)
    return resultado


def ajustar_gama(imagem: np.ndarray, gama: float) -> np.ndarray:
    """
    Aplica a correção de gama na imagem.
    Gama < 1.0 clareia a imagem, Gama > 1.0 escurece a imagem.
    """
    if gama <= 0:
        gama = 0.0001
    inv_gama = 1.0 / gama
    tabela = np.array([((i / 255.0) ** inv_gama) * 255 for i in np.arange(0, 256)]).astype(np.uint8)
    
    if len(imagem.shape) == 3 and imagem.shape[2] == 4:
        rgb_gama = tabela[imagem[..., :3]]
        return np.dstack((rgb_gama, imagem[..., 3]))
    
    return tabela[imagem]


def aplicar_negativo(imagem: np.ndarray) -> np.ndarray:
    """Inverte os valores de intensidade (255 - valor_atual)."""
    if len(imagem.shape) == 3 and imagem.shape[2] == 4:
        resultado = 255 - imagem[..., :3]
        return np.dstack((resultado, imagem[..., 3]))
    return (255 - imagem).astype(np.uint8)


def aplicar_sepia(imagem: np.ndarray) -> np.ndarray:
    """
    Aplica o filtro visual Sépia multiplicando as cores RGB pela matriz de transformação padrão.
    """
    matriz_sepia = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131]
    ])
    
    if len(imagem.shape) == 2:
        rgb = np.dstack((imagem, imagem, imagem)).astype(np.float32)
        sepia = np.dot(rgb, matriz_sepia.T)
        return np.clip(sepia, 0, 255).astype(np.uint8)

    rgb = imagem[..., :3].astype(np.float32)
    sepia = np.dot(rgb, matriz_sepia.T)
    sepia = np.clip(sepia, 0, 255).astype(np.uint8)
    
    if len(imagem.shape) == 3 and imagem.shape[2] == 4:
        return np.dstack((sepia, imagem[..., 3]))
    
    return sepia


def posterizar(imagem: np.ndarray, niveis: int) -> np.ndarray:
    """Reduz o número de tonalidades da imagem em intervalos definidos."""
    niveis = max(1, niveis)
    tamanho_intervalo = max(1, 256 // niveis)
    if len(imagem.shape) == 3 and imagem.shape[2] == 4:
        resultado = (imagem[..., :3] // tamanho_intervalo) * tamanho_intervalo
        return np.dstack((resultado, imagem[..., 3]))
    resultado = (imagem // tamanho_intervalo) * tamanho_intervalo
    return resultado.astype(np.uint8)


def binarizar(imagem: np.ndarray, limiar: int) -> np.ndarray:
    """Converte a imagem para preto e branco com base no valor de limiar escolhido."""
    cinza_img = converter_para_cinza(imagem)
    cinza = cinza_img[..., 0] if len(cinza_img.shape) == 3 else cinza_img
    preto_e_branco = np.where(cinza > limiar, 255, 0).astype(np.uint8)
    return np.dstack((preto_e_branco, preto_e_branco, preto_e_branco))


def alongar_contraste(imagem: np.ndarray) -> np.ndarray:
    """Expande a faixa de intensidades para ocupar todo o intervalo [0, 255]."""
    if len(imagem.shape) == 3 and imagem.shape[2] == 4:
        rgb = imagem[..., :3].astype(np.float32)
        i_min, i_max = np.min(rgb), np.max(rgb)
        if i_max == i_min:
            return imagem.copy()
        alongado = np.clip(((rgb - i_min) / (i_max - i_min)) * 255.0, 0, 255).astype(np.uint8)
        return np.dstack((alongado, imagem[..., 3]))

    img_float = imagem.astype(np.float32)
    i_min, i_max = np.min(img_float), np.max(img_float)
    if i_max == i_min:
        return imagem.copy()
    alongado = np.clip(((img_float - i_min) / (i_max - i_min)) * 255.0, 0, 255).astype(np.uint8)
    return alongado


def equalizar_histograma(imagem: np.ndarray) -> np.ndarray:
    """Equaliza o histograma das intensidades da imagem."""
    if len(imagem.shape) == 3 and imagem.shape[2] >= 3:
        cinza_img = converter_para_cinza(imagem)
        cinza = cinza_img[..., 0] if len(cinza_img.shape) == 3 else cinza_img
        hist, _ = np.histogram(cinza.flatten(), 256, [0, 256])
        cdf = hist.cumsum()
        cdf_m = np.ma.masked_equal(cdf, 0)
        if cdf_m.max() == cdf_m.min():
            return imagem.copy()
        cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf.max() - cdf_m.min())
        tabela = np.ma.filled(cdf_m, 0).astype('uint8')
        fator = tabela[cinza].astype(np.float32) / (cinza.astype(np.float32) + 1e-5)
        res = np.clip(imagem[..., :3].astype(np.float32) * fator[..., None], 0, 255).astype(np.uint8)
        if imagem.shape[2] == 4:
            return np.dstack((res, imagem[..., 3]))
        return res
    else:
        hist, _ = np.histogram(imagem.flatten(), 256, [0, 256])
        cdf = hist.cumsum()
        cdf_m = np.ma.masked_equal(cdf, 0)
        if cdf_m.max() == cdf_m.min():
            return imagem.copy()
        cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf.max() - cdf_m.min())
        return np.ma.filled(cdf_m, 0).astype('uint8')[imagem]