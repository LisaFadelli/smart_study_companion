# Entry point that runs when a new file is uploaded to a Google Cloud Storage bucket

import os
import tempfile
from pathlib import Path

import functions_framework
from google.cloud import storage

from extract import extract_pages
from chunk_utils import chunk_pages
from store import get_embeddings, get_vector_store, upsert_chunks, clear_source
from config import CONFIG, resolve_mongo_cfg

@functions_framework.cloud_event
def process_pdf(cloud_event):
    """This function is automatically called when a new file is uploaded to the storage bucket."""
    data=cloud_event.data # get the information from the uploaded file
    bucket_name=data["bucket"] # automatically detected
    file_name=data["name"] # automatically detected

    # Only process PDF files (locked scope, space for future improvements)
    if not file_name.lower().endswith(".pdf"):
        print(f"Skipping non-PDF file: {file_name}")
        return

    print(f"[1/5] New uploaded detected: {bucket_name}/{file_name}")

    # Step 1: Doenload the PDF file to the temporary folder
    storage_client=storage.Client() # create a client ot access Cloud storage
    bucket=storage_client.bucket(bucket_name) # get the bucket object
    blob=bucket.blob(file_name)

    local_pdf_path=Path(tempfile.gettempdir()) / Path(file_name) .name
    blob.download_to_filename(str(local_pdf_path)) 
    print(f"[2/5] Download to {local_pdf_path}")

    # Step 2: Extract text and split into chunks
    pages=extract_pages(local_pdf_path)
    chunking_cfg=CONFIG["chunking"]
    chunks=chunk_pages(pages, strategy=chunking_cfg["strategy"], chunk_size=chunking_cfg["chunk_size"], chunk_overlap=chunking_cfg["chunk_overlap"],
                       separator_priority=chunking_cfg.get("separator_priority"), fixed_separator=chunking_cfg.get("fixed_separator"),)
    print(f"[3/5] Extracted {len(pages)} pages, produced len{chunks} chunks - (strategy: {chunking_cfg['strategy']})")

    # Step 3: Prepare embeddings and connect to the vector store
    mongo_cfg=resolve_mongo_cfg(CONFIG)
    embeddings=get_embeddings(CONFIG["embedding"]["model"])
    vector_store=get_vector_store(mongo_cfg, embeddings)

    # Step 4: Remove old chunks for this file
    deleted=clear_source(vector_store, source=local_pdf_path.name)
    print(f"[4/5] Cleared {deleted} existing chunks")

    # Step 5: Create embeddings for chunks and store them
    ids, batch_log=upsert_chunks(vector_store, chunks)
    print(f"[5/5] Upserted {len(ids)} chunks. Batches: {len(batch_log)}")

    local_pdf_path.unlink(missing_ok=True)

    return f"Ingested {len(chunks)} chunks from {file_name}"
