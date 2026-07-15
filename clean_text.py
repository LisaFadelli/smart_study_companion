"""
Based on the chosen pdf to ingest for my chatbot

1. Noticed that every page in the corpus of the files starts with "Fact Sheet on the European Union"
2. Hyphen linebreak handling Every single one was a genuine hyphenated term split
   across a line break (e.g. "East-\\nWest", "decision-\\nmaking",
   "Advocates-\\nGeneral"), not a word wrapped mid-word. Naive de-hyphenation
   (deleting the hyphen and joining, e.g. "govern-\\nment" -> "government")
   would have corrupted every one of these into "EastWest", "decisionmaking",
   etc. The correct handling here is to remove the LINE BREAK but KEEP the
   hyphen ("East-\\nWest" -> "East-West"), which is correct for all observed
   cases in this corpus and only imperfect in the (unobserved, in this
   corpus) case of genuine mid-word line-wrap, where it would leave a
   stray hyphen rather than silently merging two words incorrectly --
   the safer failure direction of the two.

3. Curly quotes/apostrophes (U+2018/2019/201C/201D) are left untouched --
   these are legitimate typographic characters used throughout the source
   documents

4.  All remaining whitespace (including newlines from normal paragraph
   wrapping) is collapsed to single spaces

"""


import re # 
import unicodedata #

# Remove the Europarl document header (title line + URL line) from each page
_HEADER_PATTERN = re.compile(
    r"^Fact Sheets on the European Union.*?(?:\n|\r\n)"
    r"^www\.europarl\.europa\.eu/factsheets/en\s*(?:\n|\r\n)?",
    re.MULTILINE
)

def clean_page_text(raw_text):
    text=raw_text

    # 1. Strip repeated header boilerplate (corpus specific)
    text=_HEADER_PATTERN.sub("",text)

    # 2. Unicode normalization
    text=unicodedata.normalize("NFKC", text)

    # 3. Hyphen linebreak
    text=re.sub(r"-\n","-",text)

    # 4. Collapse all remaining whitespace
    text=" ".join(text.split())

    return text.strip()

# # Test against real corpus pages
# if __name__=="__main__":
#     import pypdf
#     reader=pypdf.PdfReader(r"C:\Users\lisaf\Documents\Thesis\Thesis-project\docs\en-chapter-1.pdf")
#     raw=reader.pages[170].extract_text()
#     cleaned=clean_page_text(raw)
#     print("RAW first 1000 chars:", repr(raw[:1000]))
#     print("CLEANED first 1000 chars:", repr(cleaned[:1000]))
