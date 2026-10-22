import pdfplumber
import pandas as pd
import re
import os
from datetime import datetime

CARPETA_ENTRADA = "datos_ejemplo"
CARPETA_SALIDA = "salida"

def buscar_patron(texto, patrones):
    for patron in patrones:
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None

def extraer_datos_factura(ruta_pdf):
    datos = {
        "archivo":        os.path.basename(ruta_pdf),
        "numero_factura": None,
        "empresa":        None,
        "fecha":          None,
        "total":          None,
        "estado":         "OK",
        "notas":          ""
    }

    try:
        with pdfplumber.open(ruta_pdf) as pdf:
            texto = ""
            for pagina in pdf.pages:
                texto += pagina.extract_text() or ""

        # Número de documento
        datos["numero_factura"] = buscar_patron(texto, [
            r"FACTURA\s*N[°º]?\s*(\w+)",
            r"BOLETA\s*N[°º]?\s*(\w+)",
            r"N[°º]\s*(\w+)",
            r"FOLIO[:\s]+(\w+)",
        ])
        if not datos["numero_factura"]:
            datos["numero_factura"] = "S/N"
            datos["notas"] += "Sin N° documento (asignado S/N). "

        # Empresa o proveedor
        datos["empresa"] = buscar_patron(texto, [
            r"Empresa:\s*(.+)",
            r"Proveedor:\s*(.+)",
            r"Raz[oó]n Social:\s*(.+)",
            r"Emitido por:\s*(.+)",
            r"De:\s*(.+)",
        ])
        if not datos["empresa"]:
            datos["notas"] += "Sin empresa. "

        # Fecha
        datos["fecha"] = buscar_patron(texto, [
            r"Fecha:\s*(\d{4}-\d{2}-\d{2})",
            r"Fecha:\s*(\d{2}/\d{2}/\d{4})",
            r"Emisi[oó]n:\s*(\d{2}/\d{2}/\d{4})",
            r"Emisi[oó]n:\s*(\d{4}-\d{2}-\d{2})",
            r"Fecha\s+de\s+emisi[oó]n:\s*(\d[\d/\-]+)",
        ])
        if not datos["fecha"]:
            datos["notas"] += "Sin fecha. "

        # Total — único campo que fuerza REVISAR si falta
        total_str = buscar_patron(texto, [
            r"TOTAL:\s*\$([0-9.,]+)",
            r"Monto total:\s*\$([0-9.,]+)",
            r"Total\s+a\s+pagar:\s*\$([0-9.,]+)",
            r"Total\s+factura:\s*\$([0-9.,]+)",
            r"TOTAL\s+NETO:\s*\$([0-9.,]+)",
            r"Valor\s+total:\s*\$([0-9.,]+)",
        ])
        if total_str:
            datos["total"] = int(total_str.replace(".", "").replace(",", ""))
        else:
            datos["notas"] += "Sin total. "
            datos["estado"] = "REVISAR"

    except Exception as e:
        datos["estado"] = "ERROR"
        datos["notas"]  = str(e)

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
        ruta  = os.path.join(CARPETA_ENTRADA, nombre)
        datos = extraer_datos_factura(ruta)
        resultados.append(datos)

        if datos["estado"] == "OK":
            print(f"  OK       {nombre} | {datos['empresa']} | ${datos['total']:,}")
        else:
            print(f"  REVISAR  {nombre} | {datos['notas']}")

    df            = pd.DataFrame(resultados)
    total_general = df["total"].sum()
    archivos_ok   = len(df[df["estado"] == "OK"])
    archivos_rev  = len(df[df["estado"] != "OK"])

    timestamp  = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta_excel = os.path.join(CARPETA_SALIDA, f"informe_{timestamp}.xlsx")

    with pd.ExcelWriter(ruta_excel, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Facturas", index=False)
        resumen = pd.DataFrame([
            ["Total documentos",   len(pdfs)],
            ["Procesados OK",      archivos_ok],
            ["Requieren revision", archivos_rev],
            ["TOTAL GENERAL ($)",  total_general],
            ["Fecha del informe",  datetime.now().strftime("%Y-%m-%d %H:%M")],
        ], columns=["Concepto", "Valor"])
        resumen.to_excel(writer, sheet_name="Resumen", index=False)

    print(f"\n{'='*45}")
    print(f"INFORME GENERADO: {ruta_excel}")
    print(f"  OK: {archivos_ok}  |  Revisar: {archivos_rev}")
    print(f"  TOTAL GENERAL: ${total_general:,}")
    print(f"{'='*45}")

if __name__ == "__main__":
    procesar_carpeta()