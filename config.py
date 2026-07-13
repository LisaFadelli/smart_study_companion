CONFIG = {

    "pdf_path":"InformationRetrieval.pdf",

    "chunking": {
        "strategy":"fixed", # Possible values "fixed", "recursive"
        "chunk_size":1000,
        "chunk_overlap":150,
        "fixed_separator": " ",
        "separator_priority":["\n\n", "\n", ". ","? ","! ", " ", ""]
    },
    "embedding":{
        "model":"models/text-embedding-005",
    },
    "retrieval":{
        "strategy":"vector",
        "k":4,
    },
    "generation": {
        "model":"gemini-2.5-flash",
    },
    "mongodb":{
        "db_name":"smartstudy",
        "collection_name":"chunks",
        "vector_index_name":"vector_index",
        "embedding_field":"embedding",
        "text_field":"text"
    },
}

def resolve_mongo_cfg(cfg=CONFIG):
    mongo_cfg = dict(cfg["mongodb"])
    strategy = cfg["chunking"]["strategy"]
    mongo_cfg["collection_name"] = f"{mongo_cfg['collection_name']}_{strategy}"
    return mongo_cfg