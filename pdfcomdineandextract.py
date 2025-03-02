import os
from pypdf import PdfWriter, PdfReader

# Folder where PDFs are located
pdf_folder = "combinepdf"

# Get all PDF files in the folder
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

# Sort files to maintain order
pdf_files.sort()

# Ensure there are at least 2 PDFs
if len(pdf_files) < 2:
    print("❌ Need at least two PDFs to merge!")
else:
    # Get first and second file names (without extensions)
    first_name = os.path.splitext(pdf_files[0])[0]
    second_name = os.path.splitext(pdf_files[1])[0]

    # Create output file name
    output_pdf = f"{first_name}_{second_name}.pdf"
    output_path = os.path.join(pdf_folder, output_pdf)

    # Merge PDFs
    writer = PdfWriter()
    for pdf in pdf_files:
        writer.append(os.path.join(pdf_folder, pdf))

    # Save merged file
    with open(output_path, "wb") as out_file:
        writer.write(out_file)

    print(f"✅ Merged PDF saved as: {output_path}")

    # 🔹 Extract Text from Merged PDF 🔹
    reader = PdfReader(output_path)
    extracted_text = ""

    for i, page in enumerate(reader.pages, start=1):
        extracted_text += f"--- Page {i} ---\n{page.extract_text()}\n\n"

    # Save extracted text to a .txt file
    text_output_file = output_pdf.replace(".pdf", ".txt")
    text_output_path = os.path.join(pdf_folder, text_output_file)

    with open(text_output_path, "w", encoding="utf-8") as text_file:
        text_file.write(extracted_text)

    print(f"📄 Extracted text saved as: {text_output_path}")
