CONFIG = {

    "pdf_path":"InformationRetrieval.pdf",

    "chunking": {
        "strategy":"recursive", # Possible values "fixed", "recursive"
        "chunk_size":1000,
        "chunk_overlap":150,
        "fixed_separator": " ",
        "separator_priority":["\n\n", "\n", ". ","? ","! ", " ", ""]
    },
    "embedding":{
        #"model":"models/text-embedding-005", "gemini-embedding-001"
        "model":"text-embedding-005"
    },
    "retrieval":{
        "strategy":"hybrid", # Possible values: "vector", "hybrid"
        "k":4,
    },
    "generation": {
        "model":"gemini-2.5-flash",
        "temperature":0.2, # low but non-zero: favors grounded/consistent answers over creative variation,
                             # while leaving enough room for the tutor persona's follow-up questions to vary.
                             # This is an experimental parameter (must be held constant across Experiments 1-2)
    },
    "mongodb":{
        "db_name":"smartstudy",
        "collection_name":"chunks",
        "vector_index_name":"vector_index",
        "embedding_field":"embedding",
        "text_field":"text",
        "text_index_name":"chunk_recursive_text_idx"
    },
    "metrics": {
        "collection_name": "usage_metrics",
        "pricing": {
            "gemini-2.5-flash": {
                "input_per_million": 0.30,
                "output_per_million": 2.50,
            },
            "text-embedding-005": {
                "embedding_rate_per_1k_chars": 0.000025,
            },
        },
    },
}

def resolve_mongo_cfg(cfg=CONFIG):
    mongo_cfg = dict(cfg["mongodb"])
    strategy = cfg["chunking"]["strategy"]
    mongo_cfg["collection_name"] = f"{mongo_cfg['collection_name']}_{strategy}"
    return mongo_cfg