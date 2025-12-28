import time
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from openai import OpenAI

# =========================
# CONFIG
# =========================

SITES = {
    "Meganoticias": "https://www.meganoticias.cl",
    "EMOL": "https://www.emol.com",
    "LaTercera": "https://www.latercera.com",
    "BioBioChile": "https://www.biobiochile.cl",
}

# =========================
# 1️⃣ SCRAPING
# =========================

print("Iniciando scraping multi-medios...")

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

all_titles = {}

for site, url in SITES.items():
    print(f"\nScrapeando {site}...")
    driver.get(url)
    time.sleep(5)

    elements = driver.find_elements(By.TAG_NAME, "h1") + \
               driver.find_elements(By.TAG_NAME, "h2") + \
               driver.find_elements(By.TAG_NAME, "h3")

    titles = []
    for e in elements:
        text = e.text.strip()
        if len(text) > 30:
            titles.append(text)

    all_titles[site] = list(set(titles))  # quitar duplicados
    print(f"  → {len(all_titles[site])} titulares")

driver.quit()

# =========================
# 2️⃣ CLASIFICACIÓN IA
# =========================

print("\nIniciando clasificación con IA...")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

prompt = f"""
Clasifica los titulares POR MEDIO y POR CATEGORÍA.

Para CADA medio, clasifica SUS titulares en estas categorías:
- Politica
- Economia
- Farandula
- Internacional
- Deportes
- Seguridad
- Otros

Devuelve SOLO un JSON con ESTE formato exacto:

{{
  "Meganoticias": {{
    "Politica": [],
    "Economia": [],
    "Farandula": [],
    "Internacional": [],
    "Deportes": [],
    "Seguridad": [],
    "Otros": []
  }},
  "EMOL": {{
    "Politica": [],
    "Economia": [],
    "Farandula": [],
    "Internacional": [],
    "Deportes": [],
    "Seguridad": [],
    "Otros": []
  }},
  "LaTercera": {{
    "Politica": [],
    "Economia": [],
    "Farandula": [],
    "Internacional": [],
    "Deportes": [],
    "Seguridad": [],
    "Otros": []
  }},
  "BioBioChile": {{
    "Politica": [],
    "Economia": [],
    "Farandula": [],
    "Internacional": [],
    "Deportes": [],
    "Seguridad": [],
    "Otros": []
  }}
}}

Titulares por medio:
{json.dumps(all_titles, ensure_ascii=False, indent=2)}
"""


response = client.chat.completions.create(
    model="xiaomi/mimo-v2-flash:free",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.2
)

classified_json = response.choices[0].message.content

print("\n📊 RESULTADO FINAL:\n")
print(classified_json)

# =========================
# 3️⃣ GUARDAR JSON
# =========================

with open("titulares_clasificados_multi_medio.json", "w", encoding="utf-8") as f:
    f.write(classified_json)

print("\n✅ Guardado en titulares_clasificados_multi_medio.json")


