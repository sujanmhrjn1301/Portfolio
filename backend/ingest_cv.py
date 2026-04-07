"""
Script to ingest CV data from PDF into the Chroma vector database
Run this to initialize the RAG system with portfolio data

Installation:
1. Update CV_PDF_PATH variable in the CONFIGURATION section (line 12)
2. Run: python ingest_cv.py

Process:
1. Extract text from PDF
2. Clean and preprocess text
3. Split into chunks
4. Generate embeddings (vectorize)
5. Store in Chroma SQLite database
"""

import os
import sys
import re
import hashlib
from dotenv import load_dotenv
from rag_system import RAGSystem
from pypdf import PdfReader

load_dotenv()

# ==================== CONFIGURATION ====================
# Update this path to your CV PDF file (relative to backend directory)
CV_PDF_PATH = os.path.join(os.path.dirname(__file__), "data", "Sujan-Maharjan-September-2025.pdf")

# Additional data files path (can contain .txt or .pdf files with new information)
ADDITIONAL_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "additional_info.txt")
# ==========================================================


def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    print(f"📄 Reading PDF: {pdf_path}")
    reader = PdfReader(pdf_path)
    text = ""
    
    for page_num, page in enumerate(reader.pages, 1):
        text += page.extract_text() + "\n"
        print(f"   ✓ Extracted page {page_num}/{len(reader.pages)}")
    
    return text


def extract_text_from_file(file_path):
    """Extract text from either PDF or text file"""
    if file_path.lower().endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()


def clean_text(text):
    """Clean and preprocess CV text"""
    print("\n🧹 Cleaning text...")
    
    # Remove extra whitespace and newlines
    text = re.sub(r'\n\s*\n', '\n', text)  # Remove multiple blank lines
    text = re.sub(r'[ \t]+', ' ', text)   # Remove extra spaces/tabs
    text = text.strip()
    
    print(f"   ✓ Removed extra whitespace")
    print(f"   ✓ Text length: {len(text)} characters")
    
    return text


def check_duplicate(rag, chunk):
    """Check if a chunk already exists in the database using semantic similarity"""
    try:
        # Generate embedding for the chunk
        chunk_embedding = rag._get_embedding(chunk)
        
        # Query the collection for similar documents
        results = rag.collection.query(
            query_embeddings=[chunk_embedding],
            n_results=1,
            include=["documents", "distances"]
        )
        
        # Check if there's a very similar document (distance < 0.1 means very similar)
        if results["distances"] and len(results["distances"][0]) > 0:
            distance = results["distances"][0][0]
            if distance < 0.1:  # Very similar - likely duplicate
                return True
    except Exception as e:
        pass  # Silently skip if collection is empty or other errors
    
    return False


def get_unique_chunk_id(chunk):
    """Generate unique ID based on content hash"""
    chunk_hash = hashlib.md5(chunk.encode()).hexdigest()
    return f"chunk_{chunk_hash[:12]}"


def ingest_cv(cv_file_path):
    """Ingest CV data from PDF into the RAG system with detailed progress tracking"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in .env file")
    
    if not cv_file_path or not os.path.exists(cv_file_path):
        raise FileNotFoundError(f"❌ Error: CV PDF file not found at {cv_file_path}")
    
    print("🚀 Initializing RAG system...")
    rag = RAGSystem(api_key=api_key)
    
    # Step 1: Extract text
    print(f"\n📋 Ingesting CV from PDF: {cv_file_path}")
    cv_text = extract_text_from_file(cv_file_path)
    
    print(f"   ✓ Extracted {len(cv_text)} characters")
    
    # Step 2: Clean text
    cv_text = clean_text(cv_text)
    
    # Step 3: Split into chunks
    print("\n📑 Creating text chunks...")
    chunks = rag._chunk_text(cv_text, chunk_size=500, overlap=50)
    print(f"   ✓ Created {len(chunks)} chunks")
    for i, chunk in enumerate(chunks[:3], 1):
        preview = chunk[:80].replace('\n', ' ') + "..."
        print(f"      Chunk {i}: {preview}")
    if len(chunks) > 3:
        print(f"      ... and {len(chunks) - 3} more chunks")
    
    # Step 4: Vectorize and ingest
    print("\n🔤 Vectorizing and ingesting into Chroma SQLite database...")
    total_chunks = len(chunks)
    added_count = 0
    skipped_count = 0
    
    for i, chunk in enumerate(chunks, 1):
        try:
            # Check for duplicates
            if check_duplicate(rag, chunk):
                skipped_count += 1
                continue
            
            # Generate embedding (vectorization)
            embedding = rag._get_embedding(chunk)
            
            # Get unique ID based on content hash
            unique_id = get_unique_chunk_id(chunk)
            
            # Store in Chroma database
            rag.collection.add(
                ids=[unique_id],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{"source": "cv", "chunk": i, "total_chunks": total_chunks}]
            )
            added_count += 1
            
            # Progress indicator
            if i % max(1, total_chunks // 5) == 0 or i == total_chunks:
                progress = (i / total_chunks) * 100
                print(f"   ✓ Added {added_count} | Skipped (duplicates) {skipped_count} - {progress:.0f}%")
        
        except Exception as e:
            print(f"   ❌ Error processing chunk {i}: {str(e)}")
            raise
    
    print(f"\n✅ CV data ingested successfully!")
    print(f"📊 Statistics:")
    print(f"   • Total characters: {len(cv_text):,}")
    print(f"   • Total chunks: {total_chunks}")
    print(f"   • Added: {added_count} | Skipped (duplicates): {skipped_count}")
    print(f"   • Average chunk size: {len(cv_text) // total_chunks:,} characters")
    print(f"   • Database: Chroma SQLite (./chroma_db)")
    print(f"🎯 The portfolio knowledge base is now ready to use!\n")
    
    # Step 5: Check for additional data
    if os.path.exists(ADDITIONAL_DATA_PATH):
        print("📎 Found additional data file. Ingesting...")
        ingest_additional_data(rag, ADDITIONAL_DATA_PATH)
    
    # Step 6: Test the system
    print("🧪 Testing RAG system...")
    test_query = "Tell me about Sujan's experience"
    print(f"Question: {test_query}")
    
    response = rag.generate_response(test_query)
    print(f"\n💬 Response:\n{response}\n")
    
    return True


def ingest_additional_data(rag, additional_file_path):
    """Ingest additional data from .txt or .pdf files"""
    print(f"\n📎 Ingesting additional data from: {os.path.basename(additional_file_path)}")
    
    # Extract text from file
    additional_text = extract_text_from_file(additional_file_path)
    print(f"   ✓ Extracted {len(additional_text)} characters")
    
    # Clean text
    additional_text = clean_text(additional_text)
    
    # Split into chunks
    print("\n📑 Creating text chunks...")
    chunks = rag._chunk_text(additional_text, chunk_size=500, overlap=50)
    print(f"   ✓ Created {len(chunks)} chunks")
    
    # Vectorize and ingest with duplicate checking
    print("\n🔤 Vectorizing and ingesting additional data...")
    added_count = 0
    skipped_count = 0
    
    for i, chunk in enumerate(chunks, 1):
        try:
            # Check for duplicates
            if check_duplicate(rag, chunk):
                skipped_count += 1
                continue
            
            # Generate embedding
            embedding = rag._get_embedding(chunk)
            
            # Get unique ID
            unique_id = get_unique_chunk_id(chunk)
            
            # Store in database
            rag.collection.add(
                ids=[unique_id],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{"source": "additional", "chunk": i}]
            )
            added_count += 1
            
            if i % max(1, len(chunks) // 5) == 0 or i == len(chunks):
                progress = (i / len(chunks)) * 100
                print(f"   ✓ Processed {i}/{len(chunks)} (added: {added_count}, skipped: {skipped_count}) - {progress:.0f}%")
        
        except Exception as e:
            print(f"   ❌ Error processing chunk {i}: {str(e)}")
    
    print(f"\n✅ Additional data ingested!")
    print(f"   • Added: {added_count} | Skipped (duplicates): {skipped_count}")


if __name__ == "__main__":
    print("🔍 Using CV path from configuration...")
    print(f"   📁 Path: {CV_PDF_PATH}\n")
    
    try:
        success = ingest_cv(CV_PDF_PATH)
        if not success:
            sys.exit(1)
    except FileNotFoundError as e:
        print(str(e))
        sys.exit(1)
