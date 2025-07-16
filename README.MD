# 📂 XML to CSV API (FastAPI)

Convierte archivos `.xml` con estructura de predios/interesados en un archivo `.csv` descargable.  
Procesa todo en memoria, sin guardar archivos en disco. Ideal para trámites, catastro, etc.

---

## 🚀 Características

- ✅ API REST con FastAPI
- 🔄 Sube un archivo `.xml` y recibe `.csv` al instante
- 🧠 Procesamiento en memoria con `BytesIO`
- 🐳 Listo para Docker y deploy inmediato
- 🌍 CORS habilitado para conectar con frontend (Next.js, React, etc.)

---

## 📦 Requisitos

- Python 3.11+
- pip
- Docker (opcional, para contenedor)

---

## ⚙️ Instalación local

```bash
git clone https://github.com/tu-usuario/xml-to-csv-api.git
cd xml-to-csv-api
pip install -r requirements.txt
uvicorn main:app --reload
