import sys
import json
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

from extract import extract_pages
from chunk import chunk_pages
from store import get_embeddings, get_vector_store, upsert_chunks, clear_source
from config import CONFIG, resolve_mongo_cfg

load_dotenv()

RUN_LOG_DIR=Path("run_logs")

def main(pdf_path, cfg=CONFIG):
    source_name=Path(pdf_path).name
    mongo_cfg=resolve_mongo_cfg(cfg)

    resolved = {
            "run_started_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "pdf_path": str(pdf_path),
            "source_name": source_name,
            "chunking": cfg["chunking"],
            "embedding": cfg["embedding"],
            "retrieval": cfg["retrieval"],
            "generation": cfg["generation"],
            "mongodb_resolved": mongo_cfg,
        }
    print("[1/6] Resolved config for this run:")
    print(json.dumps(resolved, indent=2))

    RUN_LOG_DIR.mkdir(exist_ok=True)
    stamp = resolved["run_started_utc"].replace(":", "-")
    log_path = RUN_LOG_DIR / f"ingest_{stamp}_{cfg['chunking']['strategy']}.json"
    log_path.write_text(json.dumps(resolved, indent=2))
    print(f"Config snapshot saved to {log_path}")

    print(f"[2/6] Extracting text from {pdf_path}")
    pages=extract_pages(pdf_path)
    print(f"{len(pages)} pages")

    print(f"[3/6] Chunking (strategy={cfg['chunking']['strategy']}) ...")
    chunks = chunk_pages(
        pages,
        cfg["chunking"]["strategy"],
        cfg["chunking"]["chunk_size"],
        cfg["chunking"]["chunk_overlap"],
        separator_priority=cfg["chunking"].get("separator_priority"),
        fixed_separator=cfg["chunking"].get("fixed_separator"),
    )
    print(f"{len(chunks)} chunks produced")
    
    print(f"[4/6] Loading embedding model ({cfg['embedding']['model']}) -> collection={mongo_cfg["collection_name"]} ...")
    embeddings=get_embeddings(cfg["embedding"]["model"])
    vectore_store=get_vector_store(mongo_cfg, embeddings)

    print(f"[5/6] Clearing existing chunks for source={source_name} ...")
    deleted=clear_source(vectore_store, source_name) 
    print(f"{deleted} old chunks removed")


    print(f"[6/6] Embedding + upserting {len(chunks)} chunks ...")
    ids=upsert_chunks(vectore_store, chunks)
    print(f"Done. {len(ids)} documents upserted")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_ingest.py path/to/lecture.pdf")
        sys.exit(1)
    main(sys.argv[1])

    