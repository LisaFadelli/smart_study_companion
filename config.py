CONFIG = {
    "chunking": {
        "strategy":"fixed",
        "chunk_size":1000,
        "chunk_overlap":150,
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