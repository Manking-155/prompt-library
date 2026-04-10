import os
import hashlib
import yaml
import re
import chromadb
from chromadb.utils import embedding_functions

# Configs
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPTS_DIR = os.path.join(BASE_DIR, 'prompts')
DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.chroma_db')
EXCLUDED_DIRS = ['assets', 'scripts', '.archive']

# Initialize ChromaDB client and Embedding
client = chromadb.PersistentClient(path=DB_DIR)
emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

collection = client.get_or_create_collection(
    name="prompts_db",
    embedding_function=emb_fn,
    metadata={"hnsw:space": "cosine"}
)

def compute_md5(text: str) -> str:
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def extract_frontmatter_and_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        frontmatter_str = match.group(1)
        body = match.group(2)
        try:
            metadata = yaml.safe_load(frontmatter_str) or {}
            # Keep the raw content combined for better embedding context
            return metadata, content
        except:
            return {}, content
    return {}, content

def index_prompts():
    print(f"Index running on {PROMPTS_DIR}...")
    
    # Fetch existing metadata to optimize indexing (MD5 check)
    existing_docs = collection.get(include=["metadatas"])
    existing_hashes = {}
    if existing_docs and existing_docs["ids"]:
        for i, doc_id in enumerate(existing_docs["ids"]):
            meta = existing_docs["metadatas"][i]
            if meta and "md5" in meta:
                existing_hashes[doc_id] = meta["md5"]
                
    batch_ids = []
    batch_docs = []
    batch_metadatas = []
    
    for root, dirs, files in os.walk(PROMPTS_DIR):
        # Exclude specified subdirectories
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        
        for f in files:
            if not f.endswith('.md'):
                continue
                
            file_path = os.path.join(root, f)
            rel_path = os.path.relpath(file_path, PROMPTS_DIR)
            doc_id = rel_path
            
            metadata, full_content = extract_frontmatter_and_content(file_path)
            content_hash = compute_md5(full_content)
            
            if doc_id in existing_hashes and existing_hashes[doc_id] == content_hash:
                continue # No changes
                
            clean_meta = {
                "md5": content_hash,
                "file_path": rel_path,
                "name": str(metadata.get('name', f)),
                "category": str(metadata.get('category', 'Tasks'))
            }
            
            batch_ids.append(doc_id)
            batch_docs.append(full_content)
            batch_metadatas.append(clean_meta)
            
    if batch_ids:
        print(f"Upserting {len(batch_ids)} documents to ChromaDB...")
        collection.upsert(
            documents=batch_docs,
            metadatas=batch_metadatas,
            ids=batch_ids
        )
        print("Indexed successfully.")
    else:
        print("No changes detected. DB is up to date.")

if __name__ == "__main__":
    index_prompts()
