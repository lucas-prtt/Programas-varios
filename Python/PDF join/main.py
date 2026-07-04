from pathlib import Path
from pypdf import PdfWriter
# Hecho con IA para sacarme de un apuro


SALIDA = "PDF_UNIDO.pdf"


def listar_pdfs():
    return sorted(
        [p for p in Path(".").glob("*.pdf") if p.name != SALIDA],
        key=lambda x: x.name.lower()
    )


def pedir_orden(cantidad):
    while True:
        entrada = input(
            "\nIngresá el orden de los PDFs escribiendo los números separados por espacios.\n"
            "Ejemplo: 3 1 2 5 4\n\n> "
        ).strip()

        try:
            orden = [int(x) for x in entrada.split()]
        except ValueError:
            print("Hay valores que no son números.")
            continue

        if len(set(orden)) != len(orden):
            print("Hay números repetidos.")
            continue

        if any(n < 1 or n > cantidad for n in orden):
            print("Hay números fuera de rango.")
            continue

        return orden


def main():
    pdfs = listar_pdfs()

    if not pdfs:
        print("No se encontraron archivos PDF.")
        return

    print("\nPDF encontrados:\n")

    for i, pdf in enumerate(pdfs, start=1):
        print(f"{i}. {pdf.name}")

    orden = pedir_orden(len(pdfs))

    faltantes = [i for i in range(1, len(pdfs) + 1) if i not in orden]

    if faltantes:
        print("\nNo seleccionaste estos PDFs:")
        for i in faltantes:
            print(f"{i}. {pdfs[i-1].name}")

        resp = input("\n¿Querés agregarlos al final? (s/n): ").strip().lower()

        if resp.startswith("s"):
            orden.extend(faltantes)

    writer = PdfWriter()

    print("\nUniendo archivos...\n")

    for n in orden:
        pdf = pdfs[n - 1]
        print(f"Agregando: {pdf.name}")
        writer.append(str(pdf))

    with open(SALIDA, "wb") as f:
        writer.write(f)

    writer.close()

    print(f"\nListo. Se creó: {SALIDA}")


if __name__ == "__main__":
    main()