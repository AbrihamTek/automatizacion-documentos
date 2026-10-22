# 📄 Automatización de Documentos — PDF a Excel

Convierte facturas y cotizaciones en PDF a una planilla Excel limpia con informe automático.

## ¿Qué problema resuelve?

Muchas pymes reciben decenas de facturas en PDF cada mes y las procesan a mano.
Este script las lee automáticamente y genera un Excel con todos los datos organizados
y un resumen con el total general — en segundos.

## Demo

**Entrada:** 3 facturas PDF de distintos proveedores

**Salida generada automáticamente:**

| Archivo | Empresa | Fecha | Total | Estado |
|---|---|---|---|---|
| factura_001.pdf | Ferreteria Lopez | 2024-10-01 | $20,500 | OK |
| factura_002.pdf | Panaderia El Trigo | 2024-10-05 | $26,500 | OK |
| factura_003.pdf | Gym FitZone | 2024-10-08 | $60,000 | OK |

**Resumen automático:**
- Total documentos: 3
- Procesados OK: 3
- TOTAL GENERAL: $107,000

## Cómo usarlo

**1. Instalar dependencias:**
```bash
pip install -r requirements.txt
```

**2. Poner los PDFs en la carpeta `datos_ejemplo/`**

**3. Ejecutar:**
```bash
python src/procesar.py
```

**4. Abrir el Excel generado en la carpeta `salida/`**

## Casos marcados para revisión

Si un PDF no tiene los campos esperados, el script lo marca como `REVISAR`
en lugar de inventar datos. Nunca genera información falsa.

## Stack

- Python 3.13
- pdfplumber — extracción de texto desde PDF
- pandas — procesamiento de datos
- openpyxl — generación de Excel

## Autor

**AbrihamTek** — Estudiante de Ingeniería en Computación, UCSH, Chile.
Disponible para automatizaciones a medida para pymes.
Contacto: [github.com/AbrihamTek](https://github.com/AbrihamTek)