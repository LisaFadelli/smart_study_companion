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
        #"model":"models/text-embedding-005",
        "model":"text-embedding-005"
    },
    "retrieval":{
        "strategy":"vector",
        "k":4,
    },
    "generation": {
        "model":"gemini-2.5-flash",
        "temperature":0.2, # low but non-zero: favors grounded/consistent answers over creative variation,
                             # while leaving enough room for the tutor persona's follow-up questions to vary.
                             # This is an experimental parameter -- must be held constant across Experiments 1-2
                             # or generation itself becomes a second, unintended independent variable.
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