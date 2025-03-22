import os
import requests
from duckduckgo_search import DDGS
from PIL import Image
from io import BytesIO
import time

# Criar pasta para salvar as imagens
pasta = "utensilios_domesticos"
if not os.path.exists(pasta):
    os.makedirs(pasta)

# Lista de utensílios domésticos para buscar
utensilios = ["panela", "colher", "faca", "prato", "copo", "frigideira"]

# Tamanho ideal para visão computacional
tamanho = (224, 224)
imagens_por_objeto = 100  # Número de imagens desejado por objeto

# Buscar e salvar imagens
for item in utensilios:
    print(f"Baixando imagens de: {item}")
    
    with DDGS() as ddgs:
        resultados = ddgs.images(item, max_results=imagens_por_objeto)
    
    for i, img in enumerate(resultados):
        url = img["image"]
        try:
            resposta = requests.get(url, timeout=10)
            if resposta.status_code == 200:
                # Abrir imagem e redimensionar
                imagem = Image.open(BytesIO(resposta.content))
                imagem = imagem.convert("RGB")
                imagem = imagem.resize(tamanho)
                
                # Criar pasta para cada tipo de utensílio
                pasta_objeto = os.path.join(pasta, item)
                if not os.path.exists(pasta_objeto):
                    os.makedirs(pasta_objeto)
                
                # Salvar imagem redimensionada
                caminho = os.path.join(pasta_objeto, f"{item}_{i}.jpg")
                imagem.save(caminho, "JPEG")
                print(f"Imagem salva: {caminho}")
            
            # Aguardar um pouco para evitar bloqueios
            time.sleep(0.5)
        
        except Exception as e:
            print(f"Erro ao baixar {url}: {e}")

print("Download concluído!")

