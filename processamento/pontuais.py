import numpy as np

def converter_para_cinza(imagem: np.ndarray) -> np.ndarray:
    """Converte a imagem para escala de cinza usando os pesos de luminância NTSC/PAL."""
    if len(imagem.shape) == 2:
        return imagem.copy()
    cinza = np.dot(imagem[..., :3], [0.299, 0.587, 0.114])
    cinza = np.clip(cinza, 0, 255).astype(np.uint8)
    if imagem.shape[2] == 4:
        return np.dstack((cinza, cinza, cinza, imagem[..., 3]))
    return cinza

def ajustar_brilho(imagem: np.ndarray, valor: int) -> np.ndarray:
    """Soma ou subtrai intensidades garantindo o limite de 8 bits."""
    resultado = imagem.copy()
    canais = resultado if len(imagem.shape) == 2 else resultado[..., :3]
    canais[...] = np.clip(canais.astype(np.int16) + valor, 0, 255).astype(np.uint8)
    return resultado

def ajustar_contraste(imagem: np.ndarray, fator: float) -> np.ndarray:
    """Ajusta o contraste multiplicando as intensidades a partir da média."""
    resultado = imagem.copy()
    canais = resultado if len(imagem.shape) == 2 else resultado[..., :3]
    canais[...] = np.clip(128.0 + fator * (canais.astype(np.float32) - 128.0), 0, 255).astype(np.uint8)
    return resultado

def aplicar_negativo(imagem: np.ndarray) -> np.ndarray:
    """Aplica a transformação g(x,y) = 255 - f(x,y)."""
    resultado = imagem.copy()
    canais = resultado if len(imagem.shape) == 2 else resultado[..., :3]
    canais[...] = 255 - canais
    return resultado

def aplicar_sepia(imagem: np.ndarray) -> np.ndarray:
    """Aplica uma tonalidade sépia preservando a transparência, quando houver."""
    if len(imagem.shape) == 2:
        return imagem.copy()

    matriz_sepia = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131],
    ])
    resultado = imagem.copy()
    resultado[..., :3] = np.clip(
        imagem[..., :3].astype(np.float32) @ matriz_sepia.T,
        0,
        255,
    ).astype(np.uint8)
    return resultado

def ajustar_gama(imagem: np.ndarray, gama: float) -> np.ndarray:
    """Ajusta os tons pela transformação g(x) = 255 * (x / 255)^gama."""
    resultado = imagem.copy()
    canais = resultado if len(imagem.shape) == 2 else resultado[..., :3]
    # Transformação de potência: gama menor que 1 expande tons escuros; maior que 1 os comprime.
    canais[...] = np.clip(
        255 * (canais.astype(np.float32) / 255) ** gama,
        0,
        255,
    ).astype(np.uint8)
    return resultado

def binarizar(imagem: np.ndarray, limiar: int) -> np.ndarray:
    """Converte a imagem em preto e branco a partir de um limiar de intensidade."""
    if len(imagem.shape) == 2:
        luminancia = imagem
    else:
        luminancia = np.dot(imagem[..., :3], [0.299, 0.587, 0.114])
    # Segmentação global: pixels acima do limiar viram branco; os demais, preto.
    return np.where(luminancia >= limiar, 255, 0).astype(np.uint8)

def posterizar(imagem: np.ndarray, niveis: int) -> np.ndarray:
    """Reduz a quantidade de tons por canal, criando regiões de cor definidas."""
    resultado = imagem.copy()
    canais = resultado if len(imagem.shape) == 2 else resultado[..., :3]
    # Quantização uniforme: cada canal é arredondado para um dos níveis permitidos.
    intervalo = 255 / (niveis - 1)
    canais[...] = np.clip(
        np.round(canais.astype(np.float32) / intervalo) * intervalo,
        0,
        255,
    ).astype(np.uint8)
    return resultado

def equalizar_histograma(imagem: np.ndarray) -> np.ndarray:
    """Equaliza o histograma. Em RGB, preserva os tons ajustando a luminância."""
    if len(imagem.shape) == 2:
        return _equalizar_canal(imagem)
    
    img_float = imagem.astype(np.float32)
    y = 0.299 * imagem[:, :, 0] + 0.587 * imagem[:, :, 1] + 0.114 * imagem[:, :, 2]
    y_eq = _equalizar_canal(y.astype(np.uint8)).astype(np.float32)
    
    fator = (y_eq + 1e-5) / (y + 1e-5)
    # O mesmo fator de luminância é aplicado aos três canais para reduzir alteração de matiz.
    img_res = img_float.copy()
    for c in range(3):
        img_res[:, :, c] = img_float[:, :, c] * fator
        
    return np.clip(img_res, 0, 255).astype(np.uint8)

def _equalizar_canal(canal: np.ndarray) -> np.ndarray:
    """Função auxiliar que aplica equalização via CDF em um canal de imagem."""
    hist, _ = np.histogram(canal.flatten(), 256, [0, 256])
    cdf = hist.cumsum()
    cdf_masked = np.ma.masked_equal(cdf, 0)
    cdf_masked = (cdf_masked - cdf_masked.min()) * 255 / (cdf_masked.max() - cdf_masked.min())
    cdf_final = np.ma.filled(cdf_masked, 0).astype(np.uint8)
    return cdf_final[canal]
