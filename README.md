# VisionCraft Studio

Aplicação web para estudo e prática de processamento digital de imagens. Ela permite carregar uma imagem, aplicar transformações pontuais de intensidade, transformações geométricas, filtros espaciais por vizinhança, detectores de borda e análise de histograma, acompanhando todo o processo em um pipeline/histórico visual interativo.

---

## 🛠️ Requisitos e Instalação

- Python 3.10 ou superior
- `streamlit`
- `numpy`
- `scipy`
- `matplotlib`
- `opencv-python`
- `Pillow`

Instale as dependências executando o comando no terminal:

```bash
pip install streamlit numpy scipy matplotlib opencv-python pillow
```

---

## 🚀 Como executar a aplicação

Com as dependências instaladas e no diretório raiz do projeto, execute:

```bash
streamlit run src/app.py
```

O Streamlit iniciará o servidor local e abrirá a aplicação no navegador em `http://localhost:8501`.

---

## 💡 Como usar

1. **Carregar Imagem**: No painel superior esquerdo (**IMAGEM**), envie um arquivo nos formatos **JPG, JPEG ou PNG**.
2. **Preservação da Original**: A imagem original é mantida intacta na memória para permitir a construção de diferentes pipelines de processamento.
3. **Seleção de Alvo**: Escolha se a nova operação será aplicada sobre a **Última Processada** ou sobre a imagem **Original**.
4. **Aplicação de Efeitos**: Abra uma das seções expansíveis no painel de **FERRAMENTAS** à direita, ajuste os parâmetros (sliders, selects, números) e clique no botão de aplicação.
5. **Histórico (Pipeline)**: Cada operação realizada é registrada no histórico. Use os botões **Desfazer**, **Refazer**, **Remover Etapa** ou selecione diretamente qualquer etapa anterior.
6. **Salvamento e Histograma**: No rodapé fixo da coluna direita, acompanhe o **Histograma de Intensidade (RGB ou Cinza)** e utilize o botão **Salvar Imagem Resultado** para exportar o produto final em PNG.

---

## ⚙️ Funcionalidades e Operações Implementadas

### 1. Transformações Pontuais (Intensidade)
- **Conversão para Escala de Cinza**: Converte imagens coloridas usando luminância ponderada padrão (`0.299R + 0.587G + 0.114B`).
- **Ajuste de Brilho**: Adiciona ou subtrai intensidade no intervalo `[0, 255]`.
- **Ajuste de Contraste**: Multiplica as intensidades por um fator de ajuste.
- **Ajuste de Gama**: Aplica a transformação não linear $s = c \cdot r^\gamma$ (clareia ou escurece tons médios).
- **Negativo da Imagem**: Inverte as intensidades através da fórmula $g(x,y) = 255 - f(x,y)$.
- **Efeito Sépia**: Aplica matriz de transformação de cor para estilo vintage.
- **Posterização**: Reduz o número de níveis de cinza/cor em intervalos quantizados.
- **Alongamento de Contraste**: Expande a faixa de intensidades para cobrir todo o intervalo `[0, 255]`.
- **Equalização de Histograma**: Redistribui os níveis de cinza para maximizar o contraste global.
- **Binarização (Limiarização)**: Converte a imagem para preto e branco com base em um limiar configurável (`0 a 255`).

### 2. Transformações Geométricas
- **Rotação 90°**: Rotaciona nos sentidos horário ou anti-horário.
- **Rotação por Ângulo Livre**: Rotaciona a imagem em qualquer ângulo em graus (positivo ou negativo) ajustando automaticamente as dimensões do container.
- **Espelhamento**: Inversão horizontal (esquerda/direita) e vertical (cima/baixo).
- **Redimensionamento (Escala)**: Redimensiona a imagem proporcionalmente de 25% a 200% via interpolação do vizinho mais próximo.
- **Translação**: Desloca a imagem espacialmente nos eixos $X$ e $Y$ em pixels.

### 3. Transformações por Vizinhança (Filtros Espaciais)
- **Filtro da Média**: Suavização por convolução com kernel de pesos iguais ($3\times3$, $5\times5$, $7\times7$).
- **Filtro Gaussiano**: Suavização com pesos gaussianos e controle de tamanho e $\sigma$ (sigma).
- **Adição de Ruído Gaussiano**: Adiciona ruído artificial para testes e avaliação dos filtros de suavização.
- **Realce de Nitidez (Unsharp Masking)**: Destaca contornos subtraindo a versão suavizada da imagem original.
- **Tratamento de Bordas**: Estratégia de **Reflexão (Mirroring/Reflect)** para lidar com pixels nas bordas durante as convoluções.

### 4. Detecção de Bordas
- **Operador Sobel**: Gradientes verticais e horizontais com máscaras $3\times3$ ponderadas no centro.
- **Operador Prewitt**: Detecção de bordas por convolução com máscaras uniformes nos eixos X e Y.
- **Operador Laplaciano**: Operador diferencial de segunda ordem para destacar variações bruscas de intensidade.

---

## 📁 Estrutura do Projeto

```text
VisionCraftStudio_2/
├── README.md                 # Documentação do projeto
├── __init__.py
├── src/                      # Código-fonte principal da aplicação
│   ├── app.py                # Ponto de entrada (Streamlit UI layout em 3 colunas)
│   ├── estado.py             # Gerenciamento do estado da sessão (session_state e pipeline)
│   └── __init__.py
├── componentes/              # Componentes modulares da interface de usuário
│   ├── cabecalho.py          # Barra superior e marca
│   ├── upload.py             # Carregamento de imagem e metadados
│   ├── visualizacao.py       # Exibição central (Resultado / Comparar)
│   ├── historico.py          # Painel do pipeline de histórico (Desfazer, Refazer, Etapas)
│   ├── ferramentas.py        # Grupos de controles expansíveis de processamento
│   ├── histograma.py         # Gráfico de histograma RGB/Cinza e download
│   └── __init__.py
├── processamento/            # Módulos com os algoritmos de processamento de imagem
│   ├── pontuais.py           # Operações de intensidade de pixel
│   ├── espaciais.py          # Filtros de vizinhança, convolução e ruído
│   ├── geometricas.py        # Rotação, translação, espelhamento e escala
│   └── __init__.py
└── static/                   # Arquivos estáticos e recursos
    ├── estilos.css           # Estilização visual CSS customizada
    ├── temp_download.png     # Cache temporário para download de imagens
    └── __init__.py
```
