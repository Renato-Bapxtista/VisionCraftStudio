# VisionCraft Studio

Aplicação web para estudo de processamento digital de imagens. Ela permite carregar uma imagem, aplicar operações pontuais, filtros espaciais, detectores de borda e transformações geométricas, acompanhando todo o processo em um histórico visual.

## Requisitos

- Python 3.10 ou superior
- `streamlit`
- `numpy`
- `matplotlib`
- `Pillow`

Instale as dependências no terminal, dentro da pasta do projeto:

```bash
pip install streamlit numpy matplotlib pillow
```

## Como executar

```bash
streamlit run app.py
```

O Streamlit exibirá no terminal o endereço local para abrir a aplicação no navegador.

## Como usar

1. Em **Imagem**, carregue um arquivo JPG, JPEG ou PNG.
2. Confira o nome, dimensões, formato e modo de cor exibidos abaixo do carregador.
3. Escolha se a próxima operação será aplicada à **Última Processada** ou à **Original**.
4. Abra um dos painéis de ferramentas, ajuste os controles e clique no botão de aplicação.
5. A imagem resultante aparecerá no centro e a operação será incluída no histórico.
6. Use **Salvar Imagem Resultado** para baixar o resultado em PNG.

Imagens PNG com transparência são aceitas. O canal alfa é preservado durante as operações compatíveis.

## Pré-visualização

Na coluna central há dois modos:

- **Resultado**: mostra somente a imagem atualmente selecionada no histórico.
- **Comparar**: mostra a imagem original e o resultado lado a lado.

## Histórico de processamento

O histórico registra a carga inicial e cada transformação aplicada.

- **Desfazer** volta para a etapa anterior.
- **Refazer** avança para uma etapa posterior já existente.
- **Remover Etapa** exclui a etapa atual e todas as posteriores, pois elas dependem dela.
- A lista em **Etapas do Processamento** permite selecionar diretamente qualquer resultado salvo.

Ao aplicar um efeito sobre uma etapa intermediária, a aplicação solicita confirmação antes de descartar as etapas posteriores e criar uma nova ramificação.

## Ferramentas disponíveis

### Ajustes de tom

| Ferramenta | Uso |
| --- | --- |
| Preto & Branco | Converte a imagem para escala de cinza. |
| Brilho | Aumenta ou reduz a intensidade dos pixels. |
| Contraste | Amplia ou reduz a diferença entre tons claros e escuros. |
| Gama | Valores menores que 1 clareiam tons médios; valores maiores que 1 os escurecem. |

### Efeitos visuais

| Ferramenta | Uso |
| --- | --- |
| Negativo | Inverte as cores da imagem. |
| Sépia | Aplica tonalidade quente inspirada em fotografias antigas. |
| Posterização | Reduz a quantidade de níveis de cor. |

### Filtros espaciais

| Ferramenta | Uso |
| --- | --- |
| Média | Suaviza a imagem usando a média dos pixels vizinhos. Janelas maiores produzem mais suavização. |
| Gaussiano | Suaviza com pesos gaussianos e tende a preservar melhor transições suaves. |
| Nitidez | Realça detalhes e contornos; intensidades altas podem destacar ruídos. |

### Detecção de bordas

| Operador | Uso |
| --- | --- |
| Sobel | Calcula gradientes com maior peso nos vizinhos centrais. |
| Prewitt | Calcula gradientes com pesos uniformes. |
| Laplaciano | Destaca variações de intensidade em todas as direções. |

O resultado dos detectores de borda é apresentado em escala de cinza. O controle de intensidade amplifica ou reduz a resposta das bordas.

### Transformações geométricas

- Rotação de 90 graus nos sentidos horário ou anti-horário.
- Espelhamento horizontal e vertical.
- Redimensionamento proporcional entre 25% e 200%, por interpolação do vizinho mais próximo.

### Análise e histograma

- **Binarização** transforma a imagem em preto e branco usando o limiar escolhido.
- **Equalização de histograma** redistribui os tons para melhorar o contraste global.
- O histograma do resultado é exibido por canais RGB ou em escala de cinza, conforme a imagem atual.

## Estrutura do projeto


