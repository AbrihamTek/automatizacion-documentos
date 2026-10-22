import pdfplumber
import pandas as pd
import re
import os
from datetime import datetime

CARPETA_ENTRADA = "datos_ejemplo"
CARPETA_SALIDA = "salida"

def extraer_datos_factura(ruta_pdf):
    datos = {
        "archivo": os.path.basename(ruta_pdf),
        "numero_factura": None,
        "empresa": None,
        "fecha": None,
        "total": None,
        "estado": "OK",
        "notas": ""
    }
    try:
        with pdfplumber.open(ruta_pdf) as pdf:
            texto = ""
            for pagina in pdf.pages:
                texto += pagina.extract_text() or ""
        match = re.search(r"FACTURA N[°º]?\s*(\w+)", texto, re.IGNORECASE)
        if match:
            datos["numero_factura"] = match.group(1)
        else:
            datos["notas"] += "Sin N factura. "
        match = re.search(r"Empresa:\s*(.+)", texto)
        if match:
            datos["empresa"] = match.group(1).strip()
        else:
            datos["notas"] += "Sin empresa. "
        match = re.search(r"Fecha:\s*(\d{4}-\d{2}-\d{2})", texto)
        if match:
            datos["fecha"] = match.group(1)
        else:
            datos["notas"] += "Sin fecha. "
        match = re.search(r"TOTAL:\s*\$([0-9.,]+)", texto)
        if match:
            total_str = match.group(1).replace(".", "").replace(",", "")
            datos["total"] = int(total_str)
        else:
            datos["notas"] += "Sin total. "
            datos["estado"] = "REVISAR"
    except Exception as e:
        datos["estado"] = "ERROR"
        datos["notas"] = str(e)
    return datos

def procesar_carpeta():
    os.makedirs(CARPETA_SALIDA, exist_ok=True)
    pdfs = [f for f in os.listdir(CARPETA_ENTRADA) if f.endswith(".pdf")]
    if not pdfs:
        print("No se encontraron PDFs en la carpeta.")
        return
    print(f"Procesando {len(pdfs)} archivos...\n")
    resultados = []
    for nombre in sorted(pdfs):
        ruta = os.path.join(CARPETA_ENTRADA, nombre)
        datos = extraer_datos_factura(ruta)
        resultados.append(datos)
        if datos["estado"] == "OK":
            print(f"  OK       {nombre} | {datos['empresa']} | ${datos['total']:,}")
        else:
            print(f"  REVISAR  {nombre} | {datos['notas']}")
    df = pd.DataFrame(resultados)
    total_general = df["total"].sum()
    archivos_ok = len(df[df["estado"] == "OK"])
    archivos_revisar = len(df[df["estado"] != "OK"])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta_excel = os.path.join(CARPETA_SALIDA, f"informe_{timestamp}.xlsx")
    with pd.ExcelWriter(ruta_excel, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Facturas", index=False)
        resumen = pd.DataFrame([
            ["Total documentos",   len(pdfs)],
            ["Procesados OK",      archivos_ok],
            ["Requieren revision", archivos_revisar],
            ["TOTAL GENERAL ($)",  total_general],
            ["Fecha del informe",  datetime.now().strftime("%Y-%m-%d %H:%M")],
        ], columns=["Concepto", "Valor"])
        resumen.to_excel(writer, sheet_name="Resumen", index=False)
    print(f"\n{'='*45}")
    print(f"INFORME GENERADO: {ruta_excel}")
    print(f"  OK: {archivos_ok}  |  Revisar: {archivos_revisar}")
    print(f"  TOTAL GENERAL: ${total_general:,}")
    print(f"{'='*45}")

if __name__ == "__main__":
    procesar_carpeta()