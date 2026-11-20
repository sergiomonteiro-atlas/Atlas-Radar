# AtlasRadar // AtlasNews Live (MVP v0.2)

Plataforma proprietária (**Clean Room · Atlas-SI**) de inteligência global 24h, sala de situação ao vivo para a **AtlasNews** e servidor **MCP** nativo para o **Hermes-Agent / Atlas-Harness**.

> **Zero dependências externas no backend** (Python 3.10+ stdlib puro). Basta clonar e rodar em qualquer computador (Windows, macOS ou Linux).

---

## Recursos do MVP v0.2

- **Identidade Visual Oficial AtlasNews:** Midnight Navy, Atlas Electric Blue, Broadcast Red e Nightlight Gold.
- **Globo 3D Noturno HD (`Globe.gl` / WebGL):** Textura real noturna da Terra, atmosfera azul-ciano, arcos luminosos entre hubs, anéis pulsantes e clique direto em cada sinal.
- **Modo Orbital 24h:** Radar concêntrico (`1H`, `6H`, `12H`, `24H+`) com sinais orbitando por recência.
- **Live TV 24h Multi-Idioma (Resolução Dinâmica):** Verifica automaticamente quais canais (**PT, FR, EN**) estão ao vivo e com embed ativo (`GET /api/tv`), com modo **1X** e **Mosaico 2×2** (*CNN Brasil, Jovem Pan News, Record News, Band, SBT News, Euronews PT/FR/EN, France 24, BFMTV, Bloomberg, Sky News, DW News, Al Jazeera*).
- **Multi-Idioma Real:** Interface instantânea em **`PT-BR` · `PT-PT` · `FR` · `EN`** + filtro de fontes por idioma (`ALL | PT | FR | EN`).
- **Modelos de IA em Tempo Real (`🤖 MODELOS IA`):** Ranking ao vivo do Hugging Face Trending + GitHub AI Radar.
- **Integração Atlas-Harness & Atlas-Cortex:**
  - Exportação em 1 clique para Markdown Obsidian/GBRAIN (`data/cortex_export/`);
  - **Servidor MCP JSON-RPC 2.0** em `POST http://localhost:8787/mcp` com 4 tools:
    - `atlas_radar_get_trends`
    - `atlas_radar_search`
    - `atlas_radar_export_to_cortex`
    - `atlas_radar_get_ai_models`

---

## Como instalar e rodar em qualquer outro PC

### Pré-requisito
- **Python 3.10+** instalado (nenhum `pip install` necessário).

### Passo a passo
```bash
git clone https://github.com/sergiomonteiro-atlas/Atlas-Radar.git
cd Atlas-Radar
python backend/server.py
```

- **No Windows:** você também pode dar duplo clique em **`iniciar_atlas_radar.bat`**.
- Abra no navegador: **`http://localhost:8787`**

### Para atualizar depois em outro PC
```bash
git pull
```

---

## Comunidade & Ecossistema
Desenvolvido por **AtlasHub.SI** · Comunidade oficial: **[Club.Atlas-SI.com](https://Club.Atlas-SI.com)**
