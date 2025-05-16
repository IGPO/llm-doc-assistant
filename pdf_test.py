from pypdf import PdfReader

reader = PdfReader("data/samples/example.pdf")
print(f"страниц в документе {len(reader.pages)}")