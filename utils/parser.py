import fitz  # PyMuPDF

def parse_pdf(file):
    text = ""
    paragraphs = []
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page_number, page in enumerate(doc, start=1):
            page_text = page.get_text()
            for para in page_text.split("\n\n"):
                clean_para = para.strip()
                if clean_para:
                    paragraphs.append((clean_para, page_number))
            text += page_text + "\n"
    return text, paragraphs

def parse_txt(file):
    content = file.read().decode("utf-8")
    raw_paragraphs = content.split("\n\n")
    paragraphs = [(p.strip(), 1) for p in raw_paragraphs if p.strip()]
    return content, paragraphs

def parse_document(file, content_type):
    if content_type == "application/pdf":
        return parse_pdf(file)
    elif content_type == "text/plain":
        return parse_txt(file)
    else:
        return "", []
