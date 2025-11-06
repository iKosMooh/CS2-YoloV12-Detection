# 📁 Estrutura Completa do Projeto

## 📂 Diretório Raiz (Trained/)

```
Trained/
├── 📁 datasets/              # Datasets de treinamento
│   └── cs2-1/               # Dataset CS2 (Roboflow)
│       ├── data.yaml        # Config do dataset
│       ├── train/           # Imagens de treino (2151)
│       ├── valid/           # Imagens de validação (614)
│       └── test/            # Imagens de teste (297)
│
├── 📁 runs/                 # Resultados de treinamento
│   └── detect/
│       └── train/
│           ├── weights/
│           │   ├── best.pt  # ⭐ Melhor modelo (usar este)
│           │   └── last.pt  # Último checkpoint
│           ├── results.png  # Gráficos de treinamento
│           └── confusion_matrix.png
│
├── 📁 CS2/                  # ⭐ APLICATIVO DO BOT
│   ├── bot.py              # 🎮 Aplicativo principal
│   ├── capture.py          # 📸 Captura de tela
│   ├── detector.py         # 🔍 Detector YOLO
│   ├── input_controller.py # 🖱️ Controle de entrada
│   ├── config.yaml         # ⚙️ Configurações
│   ├── requirements.txt    # 📦 Dependências
│   ├── install.bat         # 🔧 Instalação automática
│   ├── run_bot.bat         # ▶️ Executar bot
│   ├── test_installation.py # ✅ Teste de instalação
│   ├── README.md           # 📖 Documentação completa
│   └── QUICKSTART.md       # 🚀 Guia rápido
│
├── 📄 config.yaml           # Config de treinamento
├── 📄 train.py             # Script de treinamento
├── 📄 download_dataset.py  # Download de dataset
├── 📄 validate.py          # Validação do modelo
├── 📄 inference.py         # Inferência/teste
├── 📄 monitor_gpu.py       # Monitorar GPU
├── 📄 benchmark.py         # Benchmark de performance
├── 📄 export_model.py      # Exportar modelo
├── 📄 requirements.txt     # Dependências de treinamento
├── 📄 setup.bat           # Setup automático
├── 📄 start_training.bat  # Iniciar treinamento
├── 📄 README.md           # Documentação do projeto
└── 📄 QUICKSTART.md       # Guia rápido de treino
```

## 🎯 Dois Ambientes Distintos

### 1️⃣ Ambiente de Treinamento (Pasta Raiz)

**Objetivo**: Treinar modelo YOLOv12 para detectar jogadores CS2

**Arquivos Principais**:
- `train.py` - Treina o modelo
- `download_dataset.py` - Baixa dataset do Roboflow
- `validate.py` - Valida modelo treinado
- `inference.py` - Testa inferência

**Como Usar**:
```bash
# 1. Baixar dataset
python download_dataset.py

# 2. Treinar modelo
python train.py

# 3. Validar
python validate.py
```

**Resultado**: Modelo treinado em `runs/detect/train/weights/best.pt`

---

### 2️⃣ Aplicativo do Bot (Pasta CS2/)

**Objetivo**: Usar modelo treinado para jogar CS2 automaticamente

**Arquivos Principais**:
- `bot.py` - Aplicativo principal
- `capture.py` - Captura tela do jogo
- `detector.py` - Roda YOLO no frame
- `input_controller.py` - Controla mouse/teclado

**Como Usar**:
```bash
cd CS2

# 1. Instalar dependências
install.bat

# 2. Executar bot
run_bot.bat
```

**Controles**:
- `INSERT` - Liga/desliga bot
- `END` - Encerra
- `Q` - Fecha preview

---

## 🔄 Fluxo de Trabalho Completo

```
┌─────────────────────────────────────────────────────────────┐
│ 1. PREPARAR AMBIENTE                                         │
├─────────────────────────────────────────────────────────────┤
│ • Instalar Python 3.8+                                       │
│ • Instalar PyTorch com CUDA                                  │
│ • pip install -r requirements.txt                            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. TREINAR MODELO                                            │
├─────────────────────────────────────────────────────────────┤
│ • python download_dataset.py                                 │
│ • python train.py (300 epochs, ~10-25 horas)                │
│ • Resultado: runs/detect/train/weights/best.pt              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. VALIDAR MODELO                                            │
├─────────────────────────────────────────────────────────────┤
│ • python validate.py                                         │
│ • python inference.py --source image.jpg                    │
│ • Verificar mAP, precisão, recall                            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. INSTALAR BOT                                              │
├─────────────────────────────────────────────────────────────┤
│ • cd CS2                                                     │
│ • install.bat                                                │
│ • Editar config.yaml                                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. TESTAR BOT                                                │
├─────────────────────────────────────────────────────────────┤
│ • python test_installation.py                                │
│ • Verificar todos os componentes                             │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. EXECUTAR BOT                                              │
├─────────────────────────────────────────────────────────────┤
│ • Abrir CS2                                                  │
│ • run_bot.bat                                                │
│ • Pressionar INSERT para ativar                              │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Componentes do Sistema

### Treinamento (Backend)

```
YOLOv12 (8.3M params)
    ↓
Dataset CS2 (3062 imagens)
    ↓
GPU Training (RTX 3050)
    ↓
Modelo Treinado (best.pt)
```

### Bot (Frontend)

```
CS2 Window
    ↓
Screen Capture (MSS)
    ↓
YOLO Detection (best.pt)
    ↓
Target Selection (closest)
    ↓
Input Simulation (pydirectinput)
    ↓
Mouse/Keyboard Control
```

## 🔑 Arquivos-Chave

| Arquivo | Descrição | Quando Usar |
|---------|-----------|-------------|
| `config.yaml` (raiz) | Config de treino | Antes de treinar |
| `train.py` | Treinar modelo | Uma vez, 10-25h |
| `best.pt` | Modelo treinado | Gerado pelo treino |
| `CS2/config.yaml` | Config do bot | Antes de usar bot |
| `CS2/bot.py` | Executar bot | Sempre que jogar |
| `CS2/test_installation.py` | Verificar instalação | Após instalar |

## 💾 Tamanhos Aproximados

```
datasets/cs2-1/         ~500 MB  (imagens)
runs/detect/train/      ~50 MB   (modelo + logs)
CS2/ (código)           ~100 KB  (scripts)
.venv/                  ~3 GB    (ambiente Python)
Ultralytics cache       ~500 MB  (modelos base)
```

## 🎓 Dependências Principais

### Treinamento
- PyTorch 2.8.0 (CUDA 12.9)
- Ultralytics 8.3.63
- Roboflow 1.2.11
- TensorBoard 2.20.0

### Bot
- Ultralytics (YOLO)
- OpenCV (processamento)
- MSS (captura tela)
- pywin32 (Win32 API)
- pydirectinput (entrada)
- pynput (controle)

## 🚀 Comandos Essenciais

### Treinamento
```bash
# Download dataset
python download_dataset.py

# Treinar
python train.py

# Validar
python validate.py

# Testar
python inference.py --source test.jpg

# Monitorar
tensorboard --logdir runs/train

# Exportar
python export_model.py
```

### Bot
```bash
cd CS2

# Instalar
install.bat

# Testar
python test_installation.py

# Executar
run_bot.bat
# OU
python bot.py

# Verificar processo CS2
tasklist | findstr cs2.exe
```

## 📝 Configurações Importantes

### Treino (config.yaml)
```yaml
model:
  architecture: "yolov12s.yaml"
  
training:
  epochs: 300
  batch: 8
  imgsz: 640
  cache: true
  
gpu:
  memory_min: 4.0
  memory_max: 5.5
```

### Bot (CS2/config.yaml)
```yaml
bot:
  auto_aim: true       # Liga auto-mira
  auto_shoot: true     # Liga auto-disparo
  aim_fov: 200         # Raio de mira
  aim_smoothing: 0.3   # Suavização

detection:
  confidence_threshold: 0.5
  target_classes: ["T", "T_head"]
  prioritize_heads: true

mouse:
  sensitivity: 1.0
  smooth_move: true
```

## ⚡ Performance

### Treinamento
- **Tempo**: 10-25 horas (300 épocas)
- **VRAM**: 4-5.5 GB
- **GPU**: RTX 3050 6GB

### Bot
- **FPS**: 15-30 (depende GPU)
- **Latência**: 50-100ms
- **VRAM**: 2-4 GB

## 🔐 Segurança

### Treinamento
✅ Seguro - apenas treina modelo localmente

### Bot
⚠️ Cuidado:
- Pode violar ToS do CS2
- Pode resultar em ban VAC
- Use apenas em modo offline/casual
- Não use competitivamente

## 📚 Documentação

| Arquivo | Conteúdo |
|---------|----------|
| `README.md` (raiz) | Documentação completa de treino |
| `QUICKSTART.md` (raiz) | Guia rápido de treino |
| `CS2/README.md` | Documentação completa do bot |
| `CS2/QUICKSTART.md` | Guia rápido do bot |
| `PROJECT_STRUCTURE.md` | Este arquivo |

## 🎯 Próximos Passos

1. ✅ Ambiente criado
2. ✅ Scripts preparados
3. ⏳ **Treinar modelo** ← Você está aqui
4. ⏳ Instalar bot
5. ⏳ Testar bot
6. ⏳ Ajustar configurações
7. ⏳ Usar bot (com responsabilidade)

---

**Dúvidas?** Consulte os arquivos README.md e QUICKSTART.md de cada pasta!
