# 🚀 Guia Rápido - CS2 YOLOv12 Detection Demo

## ⚡ Início Rápido (3 minutos)

### 1️⃣ Instalar Dependências
```bash
setup_demo.bat
```
Aguarde a instalação completa (~2 minutos)

### 2️⃣ Abrir CS2 (Opcional mas Recomendado)
- Abra o Counter-Strike 2
- Entre em qualquer mapa ou modo
- Deixe o jogo rodando em segundo plano

### 3️⃣ Executar Demo
```bash
demo_yolo.bat
```

**Pronto!** 🎉 O demo deve abrir mostrando detecções em tempo real.

---

## 🎮 Controles

| Tecla | Função |
|-------|--------|
| **Q** | Sair do demo |
| **S** | Salvar screenshot |
| **C** | Mostrar/ocultar nomes das classes |
| **R** | Reconectar à janela do CS2 |

---

## 📊 O Que Você Verá

### HUD (Canto Superior Esquerdo)
```
FPS: 60.3              ← Performance em tempo real
Detections: 4          ← Número de alvos detectados
Model: YOLOv12         ← Modelo usado
Resolution: 1920x1080  ← Resolução da captura
Mode: CS2 Window       ← Modo de captura
```

### Legenda (Canto Inferior Esquerdo)
```
■ CT       - Counter-Terrorist (corpo)
■ CT_head  - Counter-Terrorist (cabeça)
■ T        - Terrorist (corpo)
■ T_head   - Terrorist (cabeça)
```

### Detecções
- **Boxes coloridas** ao redor dos alvos
- **Ponto central** no meio de cada detecção
- **Labels** com classe e confiança (ex: "CT_head 0.87")
- **Crosshair verde** no centro da tela

---

## 🔧 Resolução de Problemas

### ❌ "Model not found"
**Problema:** Modelo YOLOv12 não encontrado

**Solução:**
```bash
# Certifique-se que o modelo existe em:
runs\train\weights\best.pt

# Se não tiver, treine primeiro:
start_training.bat
```

---

### ❌ "CS2 window not found"
**Problema:** Demo não encontrou a janela do CS2

**Solução:**
1. Abra o Counter-Strike 2
2. Certifique-se que está em fullscreen ou windowed
3. Pressione `R` no demo para reconectar
4. Se não funcionar, use o teste:
   ```bash
   python test_cs2_capture.py
   ```

---

### ❌ "ModuleNotFoundError: No module named 'win32gui'"
**Problema:** pywin32 não instalado

**Solução:**
```bash
pip install pywin32
```
Ou rode novamente:
```bash
setup_demo.bat
```

---

### ❌ FPS muito baixo (< 30)
**Problema:** Performance abaixo do esperado

**Soluções possíveis:**
1. **Feche outros programas** consumindo GPU
2. **Reduza a resolução do CS2** (Settings > Video)
3. **Use GPU NVIDIA** (CUDA acelera muito)
4. **Verifique se está usando GPU:**
   ```bash
   python -c "import torch; print(torch.cuda.is_available())"
   ```
   Se False, instale PyTorch com CUDA

---

### ❌ Erro do OpenCV (highgui)
**Problema:** OpenCV sem suporte GUI no Windows

**Solução:**
```bash
pip uninstall opencv-python opencv-python-headless -y
pip install opencv-contrib-python==4.10.0.84
```

---

## 📈 Performance Esperada

| Componente | Especificação | FPS Esperado |
|------------|---------------|--------------|
| RTX 4090   | 1920x1080     | 120+ FPS     |
| RTX 4070   | 1920x1080     | 80-100 FPS   |
| RTX 3060   | 1920x1080     | 60-80 FPS    |
| GTX 1660   | 1920x1080     | 40-50 FPS    |
| CPU only   | 1920x1080     | 10-15 FPS    |

**Nota:** 4K (3840x2160) reduz FPS em ~40%

---

## 🎥 Gravando um Vídeo Demo

### Opção 1: OBS Studio (Recomendado)
1. Baixe [OBS Studio](https://obsproject.com/)
2. Adicione "Window Capture" da janela do demo
3. Grave em 1080p 60fps
4. Use para LinkedIn/GitHub

### Opção 2: Windows Game Bar
1. Pressione `Win + G`
2. Clique em "Capturar"
3. Grave a tela

### Opção 3: Screenshots
1. Pressione `S` no demo
2. Screenshots salvas como `demo_screenshot_1.jpg`
3. Use para documentação

---

## 🧪 Testando o Sistema

### Teste 1: Verificar Instalação
```bash
python -c "import cv2, ultralytics, win32gui, mss; print('OK')"
```
Deve imprimir: `OK`

### Teste 2: Verificar Modelo
```bash
python -c "from ultralytics import YOLO; m = YOLO('runs/train/weights/best.pt'); print(m.names)"
```
Deve mostrar: `{0: 'CT', 1: 'CT_head', 2: 'T', 3: 'T_head'}`

### Teste 3: Verificar CS2
```bash
python test_cs2_capture.py
```
Deve mostrar janela do CS2 capturada em tempo real

### Teste 4: GPU Check
```bash
python -c "import torch; print('CUDA:', torch.cuda.is_available())"
```
Deve mostrar: `CUDA: True` (se tiver NVIDIA GPU)

---

## 💡 Dicas de Uso

### Para Melhor Performance
1. ✅ Use GPU NVIDIA com CUDA
2. ✅ Feche Discord/Chrome durante gravação
3. ✅ Use resolução 1920x1080 no CS2
4. ✅ Desative G-Sync/FreeSync temporariamente

### Para Melhores Detecções
1. ✅ Use mapas com boa iluminação (Dust2, Mirage)
2. ✅ Ajuste brilho do jogo (Settings > Video)
3. ✅ Mantenha distância média dos alvos (5-30m)
4. ✅ Evite fumaça/flash que atrapalham visão

### Para Demonstrações
1. ✅ Use modo offline com bots
2. ✅ Configure bots para ficarem parados
3. ✅ Mostre diferentes ângulos
4. ✅ Demonstre todas as 4 classes (CT, CT_head, T, T_head)

---

## 📱 Compartilhando no LinkedIn

### Texto Sugerido:
```
🎯 Novo Projeto: CS2 YOLOv12 Real-Time Detection

Acabei de finalizar um projeto educacional de Computer Vision 
usando YOLOv12 para detecção em tempo real no Counter-Strike 2!

✨ Destaques:
• Captura automática da janela do CS2
• 30+ FPS garantido em qualquer resolução
• 4 classes detectadas (CT, CT_head, T, T_head)
• Pipeline completo de ML (treino → inferência)

🛠️ Stack:
#Python #YOLOv12 #ComputerVision #DeepLearning #PyTorch #OpenCV

🔗 GitHub: [seu-link-aqui]
📹 Demo: [vídeo-no-youtube]

Projeto 100% open-source para fins educacionais!

#MachineLearning #AI #ObjectDetection #GameDev
```

---

## 🎓 Conceitos Demonstrados

Este projeto educacional ensina:

### 1. Computer Vision
- Detecção de objetos em tempo real
- Bounding box prediction
- Multi-class classification
- Non-maximum suppression

### 2. Deep Learning
- Transfer learning (YOLOv12)
- Data augmentation
- Model optimization
- GPU acceleration

### 3. Software Engineering
- Windows API integration
- Real-time performance optimization
- Error handling e fallbacks
- User-friendly CLI tools

### 4. Game Integration
- Process detection
- Window capture techniques
- Frame timing e sync
- Cross-resolution support

---

## 📞 Suporte

### Problemas?
1. Leia este guia completamente
2. Execute `test_cs2_capture.py` para debug
3. Verifique [CHANGELOG.md](CHANGELOG.md) para atualizações
4. Abra uma issue no GitHub

### Funciona?
⭐ Dê uma estrela no GitHub!  
📢 Compartilhe no LinkedIn!  
🤝 Contribua com melhorias!

---

**Bom demo! 🚀**

*Última atualização: 6 de novembro de 2025*
