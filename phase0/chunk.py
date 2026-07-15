"""
This python script will extract  pages into embeddable chunks.
There are two swappable strategies:
- "fixed", splitting purely at word boundaries, with no awareness of sentence of paragraph strcure.
- "recursive", trying paragraph -> line -> sentence -> word boundaries  
Both stretgies take the SAME chunk_size and chunk_overlap. 
"""

from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter


DEFAULT_RECURSIVE_SEPARATORS = ["\n\n", "\n", ". ", " ", ""]
DEFAULT_FIXED_SEPARATOR = " "

def chunk_pages(pages, strategy, chunk_size, chunk_overlap, separator_priority=None, fixed_separator=None):
    if strategy=="fixed":
        sep = fixed_separator if fixed_separator is not None else DEFAULT_FIXED_SEPARATOR
        splitter=CharacterTextSplitter(separator=sep, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        # separator: " "=splitter only breaks chunks at word spaces, never midword, but not respecting sentences or paragraph
        # chunk_size=character count oper chunk
        # chunk_overlap= characters repeated between consecutive chunks, so a sentence that gets cut at a chunk boundary in chunk N still appears in full inside chunk N+1
    elif strategy=="recursive":
        separators = separator_priority if separator_priority is not None else DEFAULT_RECURSIVE_SEPARATORS
        splitter=RecursiveCharacterTextSplitter(separators=separators, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    else:
        raise ValueError(f"Unknown chunking strategy: {strategy}")
    
    chunk=[]
    chunk_counter=0
    for page in pages:
        for text in splitter.split_text(page["text"]):
            chunk.append({
                "text":text,
                "page":page["page"],
                "source":page["source"],
                "chunk_id":f"{page["source"]}_p{page["page"]}_c{chunk_counter}",
            })
            chunk_counter += 1
    return chunk

if __name__ == "__main__":
    from phase0.extract import extract_pages
    from config import CONFIG

    pages = extract_pages(CONFIG["pdf_path"]) 
    chunks = chunk_pages(pages, 
                         strategy=CONFIG["chunking"]["strategy"], 
                         chunk_size=CONFIG["chunking"]["chunk_size"], 
                         chunk_overlap=CONFIG["chunking"]["chunk_overlap"],
                         separator_priority=CONFIG["chunking"].get("separator_priority"),
                         fixed_separator=CONFIG["chunking"].get("fixed_separator"))
    print(f"Strategy: {CONFIG["chunking"]["strategy"]}, {len(chunks)} chunks produced from {len(pages)} pages")
    print(chunks[0])
    print("---")
    print(chunks[1])