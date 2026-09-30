"""
Módulo: processamento/pontuais.py
Descrição: Contém as funções de transformação pontual de intensidade de pixels,
incluindo conversão para cinza, brilho, contraste, gama, negativo, sépia, 
posterização, binarização, alongamento de contraste e equalização de histograma.
"""

import numpy as np


def converter_para_cinza(imagem: np.ndarray) -> np.ndarray:
    """Converte RGB/RGBA em luminância Y' = 0,299R + 0,587G + 0,114B.

    Os pesos refletem a sensibilidade visual relativa aos canais primários. A
    saída colorida repete Y' nos três canais para manter o formato RGB; em RGBA,
    o alfa é copiado sem conversão. Entradas já 2D são devolvidas em uma cópia.
    """
    if len(imagem.shape) == 2:
        return imagem.copy()
    cinza = np.dot(imagem[..., :3].astype(np.float32), [0.299, 0.587, 0.114]).astype(np.uint8)
    if imagem.shape[2] == 4:
        return np.dstack((cinza, cinza, cinza, imagem[..., 3]))
    return np.dstack((cinza, cinza, cinza))


def ajustar_brilho(imagem: np.ndarray, valor: int) -> np.ndarray:
    """Aplica deslocamento aditivo uniforme às intensidades dos pixels.

    O cálculo intermediário em inteiro mais largo evita overflow de uint8; o
    recorte final limita valores a [0, 255]. Como a operação soma uma constante,
    ela desloca a faixa tonal sem multiplicar o contraste. O alfa é preservado.
    """
    if len(imagem.shape) == 3 and imagem.shape[2] == 4:
        rgb = np.clip(imagem[..., :3].astype(np.int16) + valor, 0, 255).astype(np.uint8)
        return np.dstack((rgb, imagem[..., 3]))
    resultado = np.clip(imagem.astype(np.int16) + valor, 0, 255).astype(np.uint8)
    return resultado


def ajustar_contraste(imagem: np.ndarray, fator: float) -> np.ndarray:
    """Escala intensidades por fator e recorta o resultado para [0, 255].

    Fator 1 mantém a entrada e fatores maiores aumentam a separação em relação
    ao preto (não ao ponto médio da faixa); por isso a operação também pode
    alterar o brilho e saturar realces. Em RGBA, o canal alfa não é escalado.
    """
    if len(imagem.shape) == 3 and imagem.shape[2] == 4:
        rgb = np.clip(imagem[..., :3].astype(np.float32) * fator, 0, 255).astype(np.uint8)
        return np.dstack((rgb, imagem[..., 3]))
    resultado = np.clip(imagem.astype(np.float32) * fator, 0, 255).astype(np.uint8)
    return resultado


def ajustar_gama(imagem: np.ndarray, gama: float) -> np.ndarray:
    """
    Aplica uma curva de potência por meio de uma tabela de consulta (LUT).

    Para cada intensidade normalizada x, calcula-se 255 * x^(1/gama). Nesta
    convenção, gama > 1 clareia meios-tons e gama entre 0 e 1 os escurece; os
    extremos 0 e 255 permanecem nos extremos. Valores não positivos são
    substituídos por 0,0001 para evitar divisão por zero ou expoente inválido.
    A LUT torna a transformação consistente e rápida para todos os pixels; alfa
    em RGBA é copiado sem alteração.
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
    """Inverte cada canal de cor com s = 255 - r, preservando o canal alfa."""
    if len(imagem.shape) == 3 and imagem.shape[2] == 4:
        resultado = 255 - imagem[..., :3]
        return np.dstack((resultado, imagem[..., 3]))
    return (255 - imagem).astype(np.uint8)


def aplicar_sepia(imagem: np.ndarray) -> np.ndarray:
    """
    Aplica uma transformação linear RGB que enfatiza tons quentes de sépia.

    Cada novo canal é uma combinação ponderada de R, G e B pela matriz fixa;
    valores acima de 255 são saturados. Uma entrada 2D é expandida para três
    canais iguais antes da transformação. Em RGBA, o alfa original é preservado.
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
    """Quantiza intensidades em faixas discretas, reduzindo níveis tonais.

    A divisão inteira agrupa valores em intervalos de largura aproximada
    256/niveis e os mapeia para o início de cada faixa. O parâmetro é limitado
    inferiormente a 1; como não há expansão para o centro do intervalo, a
    posterização tende a escurecer ligeiramente cada faixa. Alfa é preservado.
    """
    niveis = max(1, niveis)
    tamanho_intervalo = max(1, 256 // niveis)
    if len(imagem.shape) == 3 and imagem.shape[2] == 4:
        resultado = (imagem[..., :3] // tamanho_intervalo) * tamanho_intervalo
        return np.dstack((resultado, imagem[..., 3]))
    resultado = (imagem // tamanho_intervalo) * tamanho_intervalo
    return resultado.astype(np.uint8)


def binarizar(imagem: np.ndarray, limiar: int) -> np.ndarray:
    """Gera uma máscara binária: luminância > limiar vira 255; o restante, 0.

    A decisão é feita sobre luminância, não independentemente por canal. O
    resultado tem três canais RGB iguais (não mantém alfa), sendo útil para
    segmentação simples, mas descartando todos os tons intermediários.
    """
    cinza_img = converter_para_cinza(imagem)
    cinza = cinza_img[..., 0] if len(cinza_img.shape) == 3 else cinza_img
    preto_e_branco = np.where(cinza > limiar, 255, 0).astype(np.uint8)
    return np.dstack((preto_e_branco, preto_e_branco, preto_e_branco))


def alongar_contraste(imagem: np.ndarray) -> np.ndarray:
    """Aplica min-max stretching sobre a faixa observada para [0, 255].

    Usa os extremos globais da entrada e aplica a mesma transformação linear a
    todos os canais RGB; assim, as proporções entre canais são mantidas, mas
    pixels extremos podem ser amplificados. Se a imagem for constante, retorna
    uma cópia para evitar divisão por zero. Em RGBA, o alfa é preservado.
    """
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
    """Redistribui intensidades com a função de distribuição acumulada (CDF).

    A tabela de mapeamento é derivada do histograma de 256 níveis e da CDF
    normalizada, aumentando o contraste global quando os tons ocupam uma faixa
    estreita. Para RGB/RGBA, a CDF é calculada sobre luminância e a razão entre
    luminância equalizada e original escala os três canais, preservando melhor
    a relação de cor do que equalizar cada canal separadamente. Para imagens
    totalmente uniformes retorna uma cópia; RGBA mantém o alfa. Esta operação
    global pode amplificar ruído e não equivale a equalização adaptativa local.
    """
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