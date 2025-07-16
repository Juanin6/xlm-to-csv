from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from processor import xml_to_csv  # la versión en memoria
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/convertir")
async def convertir_archivo(file: UploadFile = File(...)):
    if not file.filename.endswith(".xml"):
        return {"error": "Solo se permiten archivos .xml"}

    try:
        content = await file.read()
        csv_buffer = xml_to_csv(content)
        return StreamingResponse(
            csv_buffer,
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={file.filename.replace('.xml', '.csv')}"
            }
        )
    except Exception as e:
        return {"error": f"Error al procesar el archivo: {str(e)}"}
