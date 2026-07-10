import sys
from dotenv import load_dotenv

from extract import extract_pages
from chunk import chunk_pages
from store import get_embeddings, get_vector_store, upsert_chunks
from config import CONFIG

load_dotenv()

def main(pdf_path, cfg=CONFIG):
    print(f"[1/4] Extracting text from {pdf_path}")
    pages=extract_pages(pdf_path)
    print(f"{len(pages)} pages")

    print(f"[2/4] Chunking (strategy={cfg['chunking']['strategy']}) ...")
    chunks = chunk_pages(
        pages,
        cfg["chunking"]["strategy"],
        cfg["chunking"]["chunk_size"],
        cfg["chunking"]["chunk_overlap"],
    )
    print(f"{len(chunks)} chunks produced")
    
    print(f"[3/4] Loading embedding model ({cfg['embedding']['model']}) ...")
    embeddings=get_embeddings(cfg["embedding"]["model"])
    vectore_store=get_vector_store(cfg["mongodb"], embeddings)

    print(f"[4/4] Embedding + upserting {len(chunks)} chunks ...")
    ids=upsert_chunks(vectore_store, chunks)
    print(f"Done. {len(ids)} documents upserted")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_ingest.py path/to/lecture.pdf")
        sys.exit(1)
    main(sys.argv[1])

    