import os
from mcp.server.fastmcp import FastMCP
import chromadb
from chromadb.utils import embedding_functions

# Configs
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPTS_DIR = os.path.join(BASE_DIR, 'prompts')
DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.chroma_db')

# Initialize DB connection
try:
    client = chromadb.PersistentClient(path=DB_DIR)
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    collection = client.get_collection(name="prompts_db", embedding_function=emb_fn)
except Exception as e:
    collection = None

# Create FastMCP Server
mcp = FastMCP("MasterPrompt Memory")

@mcp.tool()
def search_prompts(query: str, limit: int = 3) -> str:
    """
    Search the prompt library for relevant AI personas, components, or workflows based on a semantic query.
    Always use this tool when you need to find an appropriate specialist or instruction.
    Returns the file path, name, category, and markdown content of the best matches.
    """
    if not collection:
        return "Error: ChromaDB collection not found. Make sure to run indexer.py first."
        
    results = collection.query(
        query_texts=[query],
        n_results=limit
    )
    
    if not results['documents'] or not results['documents'][0]:
        return "No relevant prompts found."
        
    response = []
    for i in range(len(results['documents'][0])):
        doc = results['documents'][0][i]
        meta = results['metadatas'][0][i]
        score = results['distances'][0][i]
        
        response.append(f"--- MATCH {i+1} (Score: {score:.4f}) ---\n"
                        f"File: {meta['file_path']}\n"
                        f"Category: {meta['category']}\n"
                        f"Name: {meta['name']}\n\n"
                        f"{doc[:1500]}...\n") # Truncate to limit token context
        
    return "\n".join(response)

@mcp.tool()
def get_prompt_content(file_path: str) -> str:
    """
    Retrieve the exact full content of a specific prompt file using its file_path (obtained from search_prompts).
    Use this to strictly load a workflow or role into your context before executing a task.
    """
    full_path = os.path.join(PROMPTS_DIR, file_path)
    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()
    return f"Error: Cannot find file at {file_path}"

if __name__ == "__main__":
    mcp.run()
