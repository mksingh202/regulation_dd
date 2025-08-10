from PyPDF2 import PdfReader
from llm import get_embedding
from db import init_db, insert_chunks

def chunk_text(text, max_words=150):
    words = text.split()
    return [' '.join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

def extract_text_from_pdf(path):
    reader = PdfReader(path)
    return '\n'.join([page.extract_text() for page in reader.pages if page.extract_text()])

def main():
    init_db()
    text = extract_text_from_pdf("12-CFR-Part-1030.pdf")
    chunks = chunk_text(text)
    embeddings = [get_embedding(c) for c in chunks]
    insert_chunks(chunks, embeddings)

if __name__ == "__main__":
    main()
