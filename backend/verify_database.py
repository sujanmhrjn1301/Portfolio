"""
Verify what data is in the Chroma database
Shows breakdown by source (cv, additional, etc.)
"""

import os
from dotenv import load_dotenv
from rag_system import RAGSystem

load_dotenv()

def verify_database():
    """Check what's in the database and show statistics"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        print("❌ Error: OPENROUTER_API_KEY not found in .env file")
        return
    
    print("🔍 Verifying Database Contents...")
    print("=" * 60)
    
    rag = RAGSystem(api_key=api_key)
    
    # Get all data from the collection
    try:
        # Query with a very broad search to get all chunks
        all_data = rag.collection.get(include=["documents", "metadatas", "embeddings"])
        
        total_chunks = len(all_data["ids"])
        print(f"\n📊 Total chunks in database: {total_chunks}\n")
        
        if total_chunks == 0:
            print("❌ Database is empty!")
            return
        
        # Group by source
        sources = {}
        metadatas = all_data.get("metadatas") or []
        documents = all_data.get("documents") or []
        ids = all_data.get("ids") or []
        
        for i, metadata in enumerate(metadatas):
            source = metadata.get("source", "unknown") if metadata else "unknown"
            if source not in sources:
                sources[source] = []
            doc_text = documents[i] if i < len(documents) else "[No document]"
            doc_preview = doc_text[:100] + "..." if doc_text and len(doc_text) > 100 else doc_text
            sources[source].append({
                "id": ids[i] if i < len(ids) else "[No ID]",
                "doc_preview": doc_preview,
                "metadata": metadata
            })
        
        # Display breakdown
        print("📋 Breakdown by Source:\n")
        for source, chunks in sources.items():
            print(f"  ✓ {source.upper()}: {len(chunks)} chunks")
            for idx, chunk in enumerate(chunks[:2], 1):  # Show first 2 previews
                print(f"     [{idx}] {chunk['doc_preview']}")
            if len(chunks) > 2:
                print(f"     ... and {len(chunks) - 2} more chunks")
            print()
        
        # Test with a query
        print("\n" + "=" * 60)
        print("🧪 Testing with Sample Queries:\n")
        
        test_queries = [
            "Tell me about Sujan's experience",
            "What are Sujan's skills"
        ]
        
        for query in test_queries:
            print(f"  Q: {query}")
            context = rag.retrieve_relevant_docs(query, n_results=2)
            if context:
                for ctx in context:
                    print(f"     • {ctx[:80]}...")
            print()
        
        print("=" * 60)
        print("✅ Database verification complete!")
        
    except Exception as e:
        print(f"❌ Error reading database: {str(e)}")


if __name__ == "__main__":
    verify_database()
