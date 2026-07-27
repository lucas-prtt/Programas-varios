from pathlib import Path
from pypdf import PdfWriter
# Hecho con IA para sacarme de un apuro
#pip install pypdf

SALIDA = "PDF_UNIDO.pdf"


def listar_pdfs():
    return sorted(
        [p for p in Path(".").glob("*.pdf") if p.name != SALIDA],
        key=lambda x: x.name.lower()
    )

def pedir_orden(pdfs):
    disponibles = list(enumerate(pdfs, start=1))
    orden = []

    while disponibles:
        print("\nPDF disponibles:\n")
        for idx, pdf in disponibles:
            print(f"{idx}. {pdf.name}")

        if orden:
            print("\nOrden actual:")
            for i, pdf in enumerate(orden, start=1):
                print(f"{i}. {pdf.name}")

        entrada = input(
            "\nElegí un PDF por número (Enter para terminar): "
        ).strip()

        if entrada == "":
            resp = input("¿Querés finalizar la selección? (s/n): ").strip().lower()
            if resp.startswith("s"):
                break
            else:
                continue

        try:
            numero = int(entrada)
        except ValueError:
            print("Ingresá un número válido.")
            continue

        encontrado = False

        for i, (idx_original, pdf) in enumerate(disponibles):
            if idx_original == numero:
                orden.append(pdf)
                disponibles.pop(i)
                encontrado = True
                break

        if not encontrado:
            print("Ese PDF ya fue seleccionado o el número no existe.")

    return orden



def main():
    pdfs = listar_pdfs()

    if not pdfs:
        print("No se encontraron archivos PDF.")
        return

    print("\nPDF encontrados:\n")

    for i, pdf in enumerate(pdfs, start=1):
        print(f"{i}. {pdf.name}")

    orden = pedir_orden(pdfs)

    faltantes = [pdf for pdf in pdfs if pdf not in orden]


    if faltantes:
        print("\nNo seleccionaste estos PDFs:")
        for pdf in faltantes:
            print(f"- {pdf.name}")

        resp = input("\n¿Querés agregarlos al final? (s/n): ").strip().lower()

        if resp.startswith("s"):
            orden.extend(faltantes)

    writer = PdfWriter()

    print("\nUniendo archivos...\n")
        
    for pdf in orden:
        print(f"Agregando: {pdf.name}")
        writer.append(str(pdf))

    with open(SALIDA, "wb") as f:
        writer.write(f)

    writer.close()

    print(f"\nListo. Se creó: {SALIDA}")


if __name__ == "__main__":
    main()