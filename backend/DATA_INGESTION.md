# CV Data Ingestion Guide

## Overview
This script ingests your CV and any additional information into a Chroma vector database for your portfolio chatbot.

## Features

### 1. **Automatic Duplicate Detection**
- Before adding any chunks to the database, the script checks for semantic similarity
- Prevents duplicate information from being stored
- Uses embeddings to compare chunks (distance < 0.1 = duplicate)

### 2. **Unique Content-Based IDs**
- Each chunk gets a unique ID based on MD5 hash of its content
- Prevents accidental duplicates even if you run the script multiple times

### 3. **Additional Data Support**
- Place your new/updated information in `data/additional_info.txt` or `data/additional_info.pdf`
- The script automatically detects and ingests it after the main CV
- Works with both `.txt` and `.pdf` files

## How to Use

### Step 1: Run the Script
```bash
cd d:\Websites\Portfolio_Ver2\backend
python ingest_cv.py
```

This will:
1. ✅ Ingest the main CV from PDF
2. ✅ Check each chunk for duplicates
3. ✅ Add unique chunks to the database
4. ✅ Look for additional data file
5. ✅ Test the system with a sample query

### Step 2: Add New Information

Create a file: `data/additional_info.txt`

Add your new information:
```
NEW CERTIFICATIONS (2025):
- AWS Solutions Architect
- Kubernetes Administration

RECENT PROJECTS:
- Built a portfolio chatbot using RAG
- Created a document search system

NEW SKILLS:
- Docker & Container Management
- Kubernetes & Orchestration
```

### Step 3: Run the Script Again
```bash
python ingest_cv.py
```

The script will:
- Skip existing CV chunks (duplicates)
- Add new information from `additional_info.txt`
- Prevent duplicate entries from the additional file
- Update the knowledge base

## Output Example

```
🚀 Initializing RAG system...

📋 Ingesting CV from PDF: data\Sujan-Maharjan-September-2025.pdf
📄 Reading PDF: ...
   ✓ Extracted page 1/2
   ✓ Extracted page 2/2

🧹 Cleaning text...
   ✓ Removed extra whitespace

📑 Creating text chunks...
   ✓ Created 8 chunks

🔤 Vectorizing and ingesting into Chroma SQLite database...
   ✓ Added 8 | Skipped (duplicates) 0 - 100%

📊 Statistics:
   • Total characters: 3,534
   • Total chunks: 8
   • Added: 8 | Skipped (duplicates): 0
   • Database: Chroma SQLite (./chroma_db)

📎 Found additional data file. Ingesting...
   ✓ Added 5 new chunks
   • Added: 5 | Skipped (duplicates): 0
```

## Key Configuration

In `ingest_cv.py`:

```python
# Main CV file
CV_PDF_PATH = os.path.join(os.path.dirname(__file__), "data", "Sujan-Maharjan-September-2025.pdf")

# Additional data file (supports .txt or .pdf)
ADDITIONAL_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "additional_info.txt")
```

## Tips

1. **Regular Updates**: Keep `additional_info.txt` in your `data/` folder and update it whenever you add new information
2. **Naming Convention**: The script looks for `additional_info.txt` by default. You can add any `.txt` or `.pdf` file
3. **Format**: Use clear sections with bullet points for better chunking
4. **Duplicates**: The script automatically prevents duplicates, so you can safely re-run it multiple times
5. **Unique Hashes**: Each chunk gets a unique ID based on its content, not sequential numbers

## How Duplicate Detection Works

```python
def check_duplicate(rag, chunk):
    # Generate embedding for new chunk
    chunk_embedding = rag._get_embedding(chunk)
    
    # Query database for similar chunks
    results = rag.collection.query(
        query_embeddings=[chunk_embedding],
        n_results=1,
        include=["documents", "distances"]
    )
    
    # If semantic similarity distance < 0.1, it's a duplicate
    if distance < 0.1:
        return True  # Skip this chunk
    return False
```

## Troubleshooting

- **"Additional data file not found"**: Create `data/additional_info.txt` (optional - CV alone works fine)
- **"OPENROUTER_API_KEY not found"**: Make sure your `.env` file has the API key
- **Slow processing**: Embedding generation takes time. This is normal.
- **No new chunks added**: Check if all your data is semantically similar to existing CV content

