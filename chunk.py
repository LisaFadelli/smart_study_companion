"""
This python script will extract  pages into embeddable chunks.
There are two swappable strategies:
- "fixed", splitting purely at word boundaries, with no awareness of sentence of paragraph strcure.
- "recursive", trying paragraph -> line -> sentence -> word boundaries  
Both stretgies take the SAME chunk_size and chunk_overlap. 
"""

from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter

def chunk_pages(pages, strategy: str, chunk_size: int, chunk_overlap:int):
    if strategy=="fixed":
        splitter=CharacterTextSplitter(separator=" ", chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        # separator: " "=splitter only breaks chunks at word spaces, never midword, but not respecting sentences or paragraph
        # chunk_size=character count oper chunk
        # chunk_overlap= characters repeated between consecutive chunks, so a sentence that gets cut at a chunk boundary in chunk N still appears in full inside chunk N+1
    elif strategy=="recursive":
        raise NotImplementedError("Recursive not yet implemented") #placeholder
    else:
        raise ValueError(f"Unknown chunking strategy: {strategy}")
    
    chunk=[]
    for page in pages:
        if not page["text"].strip():
            continue
        for i, chunk_text in enumerate(splitter.split_text(page["text"])):
            chunk.append({
                "text":chunk_text,
                "page":page["page"],
                "source":page["source"],
                "chunk_id":f"{page["source"]}_p{page["page"]}_c{i}",
            })
    return chunk

if __name__ == "__main__":
    from extract import extract_pages
    pages = extract_pages("InformationRetrieval.pdf")  # same file we already tested
    chunks = chunk_pages(pages, strategy="fixed", chunk_size=1000, chunk_overlap=150)
    print(f"{len(chunks)} chunks produced from {len(pages)} pages")
    print(chunks[0])
    print("---")
    print(chunks[1])