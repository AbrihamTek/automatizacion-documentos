from fpdf import FPDF
import os

def crear_factura(nombre_archivo, numero, empresa, fecha, items):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, f"FACTURA N {numero}", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Helvetica", size=12)
    pdf.cell(0, 8, f"Empresa: {empresa}", ln=True)
    pdf.cell(0, 8, f"Fecha: {fecha}", ln=True)
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(100, 8, "Descripcion", border=1)
    pdf.cell(45, 8, "Cantidad", border=1, align="C")
    pdf.cell(45, 8, "Total", border=1, align="C")
    pdf.ln()
    total = 0
    pdf.set_font("Helvetica", size=11)
    for desc, precio in items:
        pdf.cell(100, 8, desc, border=1)
        pdf.cell(45, 8, "1", border=1, align="C")
        pdf.cell(45, 8, f"${precio:,.0f}", border=1, align="R")
        pdf.ln()
        total += precio
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, f"TOTAL: ${total:,.0f}", ln=True, align="R")
    pdf.output(nombre_archivo)
    print(f"Creado: {nombre_archivo}")

os.makedirs("datos_ejemplo", exist_ok=True)

facturas = [
    ("datos_ejemplo/factura_001.pdf", "001", "Ferreteria Lopez", "2024-10-01",
     [("Tornillos x100", 5000), ("Pintura blanca 1L", 12000), ("Brocha", 3500)]),
    ("datos_ejemplo/factura_002.pdf", "002", "Panaderia El Trigo", "2024-10-05",
     [("Harina 25kg", 18000), ("Azucar 10kg", 8500)]),
    ("datos_ejemplo/factura_003.pdf", "003", "Gym FitZone", "2024-10-08",
     [("Mensualidad octubre", 35000), ("Clases spinning x4", 20000), ("Toalla", 5000)]),
]

for args in facturas:
    crear_factura(*args)

print("\nTodos los PDFs de prueba fueron creados en datos_ejemplo/")