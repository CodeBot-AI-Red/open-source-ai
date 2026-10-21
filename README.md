# 🎨 IA Open Source — Manga & Anime Image Generation Engine (Grande Porte / Enterprise)

<p align="center">
  <img src="https://img.shields.io/badge/Version-3.0.0--Enterprise-blueviolet?style=for-the-badge&logo=fastapi" alt="Versão API">
  <img src="https://img.shields.io/badge/Domain-Manga_%26_Anime_IA-ff69b4?style=for-the-badge&logo=artstation" alt="Especialização">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python" alt="Python 3.12">
  <img src="https://img.shields.io/badge/FastAPI-0.111%2B-009688?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/Tests-Passing-brightgreen?style=for-the-badge&logo=pytest" alt="Testes">
</p>

---

## 🌟 Visão Geral

A **Plataforma IA Open Source** foi totalmente **especializada e evoluída para uma arquitetura de grande porte (Enterprise Grade) focada exclusivamente na geração de imagens, ilustrações, personagens e diagramações nos estilos de Mangás e Animes**.

Nesta versão **v3.0.0**, todos os subsistemas foram atualizados para garantir alta fidelidade de traço, suporte a múltiplos presets estilísticos (Shonen, Shojo, Seinen, Chibi, Cyberpunk, Retículas P&B e Webtoon), controle estrito de semente (seed), algoritmos de amostragem (samplers), super-resolução (upscaling) e compilador inteligente de prompts.

---

## ✨ Destaques & Recursos da Plataforma

- 🎯 **Foco Exclusivo em Mangá & Anime**: Motor otimizado especificamente para arte sequencial japonesa, ilustrações de capa e visual keys.
- 🎭 **11 Presets de Estilos Pré-Configurados**: `shonen`, `shojo`, `seinen`, `chibi`, `classic_90s`, `cyberpunk_anime`, `ink_manga_bw`, `webtoon_color`, `cel_shaded`, `dark_fantasy_manga` e `mecha`.
- 🖌️ **Renderização Monochrome & Retículas (Screentones)**: Suporte avançado a traço em tinta nanquim (G-Pen) e níveis de densidade de retícula de mangá.
- 📐 **Formatos e Aspect Ratios de Grande Porte**: Mapeamento para `1:1`, `16:9` (Paisagem), `9:16` (Stories/Mobile), `3:4` (Capa de Mangá) e `4:3`.
- ⚡ **Enriquecedor e Compilador Otimizado de Prompts**: Adiciona automaticamente tags de qualidade de arte estúdio anime e negative prompts de anatomia.
- 🔍 **Pipeline de Upscaling (Super-Resolução)**: Aumento de resolução com preservação de nitidez de traço para impressão ou exibição 4K.
- 📦 **Processamento em Lote (Batch API)**: Endpoint preparado para gerar múltiplos quadros e variantes simultaneamente.
- 🛡️ **Segurança e Prontidão Enterprise**: Autenticação unificada JWT / API-Key, rate-limiting e observabilidade por `X-Request-ID`.

---

## 📑 Parâmetros Atuais do Motor de Geração

Abaixo consta a especificação técnica de **todos os parâmetros atuais** aceitos no endpoint principal de geração (`POST /api/v1/manga-anime/generate`):

| Parâmetro | Tipo | Padrão | Intervalo / Opções | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| `prompt` **(Obrigatório)** | `string` | — | 1 a 4000 chars | Descrição textual rica do personagem, ação, roupas, pose ou cenário de anime/mangá. |
| `negative_prompt` | `string` | `null` | max 2000 chars | Termos e defeitos visuais a serem evitados ativamente na geração. |
| `style_preset` | `string` | `"shonen"` | Ver lista de presets | Estilo estético pré-definido (Shonen, Shojo, Seinen, Chibi, Retro 90s, etc.). |
| `aspect_ratio` | `string` | `"1:1"` | `"1:1"`, `"16:9"`, `"9:16"`, `"3:4"`, `"4:3"` | Proporção e dimensões recomendadas da imagem. |
| `width` | `integer` | `null` | 256 a 3840 px | Largura customizada em pixels (múltiplo de 8). Sobrescreve `aspect_ratio`. |
| `height` | `integer` | `null` | 256 a 3840 px | Altura customizada em pixels (múltiplo de 8). Sobrescreve `aspect_ratio`. |
| `num_inference_steps` | `integer` | `30` | 10 a 150 | Número de passos do processo de difusão. Mais passos = mais detalhes. |
| `guidance_scale` | `float` | `7.5` | 1.0 a 30.0 | Escala CFG (Class-Free Guidance). Controla o quão estritamente a IA obedece o prompt. |
| `seed` | `integer` | `null` | `ge=0` | Semente numérica para reprodutibilidade exata da imagem. |
| `sampler` | `string` | `"Euler_a"` | `"Euler_a"`, `"DPM++_2M_Karras"`, `"DDIM"`, `"UniPC"` | Algoritmo de amostragem de difusão matemática. |
| `color_mode` | `string` | `"full_color"` | `"full_color"`, `"black_and_white"`, `"grayscale"` | Modo de renderização de cor ou nanquim PB. |
| `screentone_density` | `string` | `"medium"` | `"none"`, `"low"`, `"medium"`, `"high"` | Densidade de pontos de retícula de mangá (aplicável em modos PB). |
| `panel_layout` | `string` | `null` | `"single"`, `"2_panels"`, `"4_grid"`, `"splash_page"` | Estrutura de composição e diagramação de páginas de mangá. |
| `upscale_factor` | `float` | `1.0` | 1.0, 1.5, 2.0, 4.0 | Fator de super-resolução/upscale aplicado pós-geração. |

---

## 🎨 Presets de Estilos Disponíveis

1. `shonen`: Linhas de ação dinâmicas, alto contraste, poses energéticas e composição marcante.
2. `shojo`: Linhas finas e delicadas, iluminação etérea, olhos expressivos e tons pastel.
3. `seinen`: Hachuras detalhadas em tinta preta, proporções maduras e forte contraste de luz e sombra.
4. `chibi`: Proporções fofas (2 cabeças de altura), olhos grandes e brilhantes, contornos limpos.
5. `classic_90s`: Estética vintage anos 90, cel shading clássico e textura analógica de anime OVA.
6. `cyberpunk_anime`: Cidades futuristas, néon brilhante, trajes tecnológicos e elementos sci-fi.
7. `ink_manga_bw`: Estilo de página de mangá tradicional japonês com pena G-Pen e retículas.
8. `webtoon_color`: Estilo webcomic moderno em cores vibrantes com gradientes suaves e iluminação digital.
9. `cel_shaded`: Key art de estúdio de animação moderno com sombreamento cel nítido e limpo.
10. `dark_fantasy_manga`: Atmosfera sombria, sombras dramáticas em chiaroscuro e armaduras detalhadas.
11. `mecha`: Robôs e armaduras mecânicas de precisão, painéis metálicos e sensores ópticos.

---

## 🛠️ Endpoints Principais da API v1

- **`POST /api/v1/manga-anime/generate`** — Endpoint principal de geração individual de imagem.
- **`POST /api/v1/manga-anime/generate/batch`** — Processamento e geração em lote (até 8 imagens).
- **`GET /api/v1/manga-anime/styles`** — Consulta pública de presets, recomendações e proporções suportadas.
- **`POST /api/v1/manga-anime/enhance-prompt`** — Compilador e enriquecedor de prompts para estilo anime/mangá.
- **`POST /api/v1/manga-anime/upscale`** — Aplica super-resolução em artes geradas.
- **`GET /api/v1/health`** — Liveness probe da API.
- **`GET /api/v1/ready`** — Readiness probe com verificação do motor de geração.

---

## 🚀 Executando Localmente

### 1. Requisitos
- Python 3.12+
- `pip` e `virtualenv`

### 2. Instalação de Dependências

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Iniciar a API Gateway e o Motor

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

Para executar o serviço dedicado de geração:

```bash
uvicorn services.manga_anime_generator.service:app --host 0.0.0.0 --port 8003 --reload
```

---

## 🧪 Testes Automatizados

A suíte de testes cobre testes unitários dos algoritmos do motor e testes de integração das rotas de API:

```bash
PYTHONPATH=. pytest
```

---

## 💡 Exemplos de Uso

### 1. Criando um Token de Acesso (Desenvolvimento)
Como a API utiliza autenticação via Bearer Token JWT, você pode gerar um token via script ou utilizar a chave em dev.

### 2. Exemplo via `cURL` (Geração Seinen P&B)

```bash
curl -X POST "http://localhost:8000/api/v1/manga-anime/generate" \
  -H "Authorization: Bearer SEU_TOKEN_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Samurai em guarda sob chuva e luar em templo antigo",
    "style_preset": "seinen",
    "aspect_ratio": "3:4",
    "color_mode": "black_and_white",
    "screentone_density": "high",
    "num_inference_steps": 40,
    "guidance_scale": 8.0,
    "seed": 999123
  }'
```

### 3. Exemplo em Python (`httpx`)

```python
import httpx

url = "http://localhost:8000/api/v1/manga-anime/generate"
headers = {"Authorization": "Bearer SEU_TOKEN_JWT"}
payload = {
    "prompt": "Garota cibernética com asas de energia néon",
    "style_preset": "cyberpunk_anime",
    "aspect_ratio": "16:9",
    "color_mode": "full_color",
    "num_inference_steps": 35,
    "upscale_factor": 1.5
}

response = httpx.post(url, json=payload, headers=headers)
data = response.json()

print(f"ID da Geração: {data['id']}")
print(f"Resolução: {data['width']}x{data['height']}")
print(f"Prompt Final Enriquecido: {data['prompt_used']}")
print(f"Imagem Payload (Base64/URI): {data['image_url_or_base64'][:60]}...")
```

---

## 📄 Licença

Este projeto está licenciado sob os termos da licença [LICENCE](LICENCE).
