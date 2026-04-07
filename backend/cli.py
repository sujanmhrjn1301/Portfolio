#!/usr/bin/env python3
"""
Portfolio Management CLI
Manage your AI-powered portfolio from the command line
"""

import os
import sys
import argparse
from pathlib import Path
from rag_system import RAGSystem
from chat_history import ChatHistory


def load_env():
    """Load environment variables from .env file"""
    from dotenv import load_dotenv
    load_dotenv()


class PortfolioCLI:
    def __init__(self):
        load_env()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            print("❌ Error: OPENAI_API_KEY not found in .env file")
            sys.exit(1)
        
        self.rag = RAGSystem(api_key=self.api_key)
        self.chat_history = ChatHistory()
    
    def ingest_cv(self, cv_file=None):
        """Ingest CV data from a file or stdin"""
        print("📝 Ingesting CV data...")
        
        if cv_file and os.path.exists(cv_file):
            with open(cv_file, 'r', encoding='utf-8') as f:
                cv_text = f.read()
            print(f"✓ Read CV from {cv_file}")
        else:
            print("Enter your CV text (press Ctrl+D when done):")
            cv_text = sys.stdin.read()
        
        if not cv_text.strip():
            print("❌ Error: No CV text provided")
            return
        
        try:
            self.rag.ingest_cv_data(cv_text, metadata={"source": "cv", "type": "portfolio"})
            print("✓ CV data ingested successfully!")
            print("The portfolio knowledge base is ready to use.")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            sys.exit(1)
    
    def test_rag(self, query):
        """Test the RAG system with a query"""
        print(f"\n🤖 Testing RAG with query: '{query}'")
        print("-" * 50)
        
        try:
            response = self.rag.generate_response(query)
            print(f"\n{response}")
            print("-" * 50)
            print("✓ RAG test successful!")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            sys.exit(1)
    
    def list_conversations(self):
        """List all conversations"""
        conversations = self.chat_history.get_all_conversations()
        
        if not conversations:
            print("No conversations found")
            return
        
        print("\n📋 Chat Conversations:")
        print("-" * 70)
        for conv in conversations:
            status = "🔗 Shared" if conv.get('is_shared') else "🔒 Private"
            print(f"ID: {conv['id'][:8]}...")
            print(f"Title: {conv['title']}")
            print(f"Status: {status}")
            print(f"Created: {conv['created_at']}")
            print("-" * 70)
        
        print(f"\nTotal: {len(conversations)} conversation(s)")
    
    def get_conversation(self, conversation_id):
        """Get details of a specific conversation"""
        messages = self.chat_history.get_conversation_messages(conversation_id)
        
        if not messages:
            print(f"No messages found for conversation {conversation_id}")
            return
        
        print(f"\n💬 Conversation {conversation_id}:")
        print("-" * 70)
        
        for msg in messages:
            role = "👤 User" if msg['role'] == 'user' else "🤖 Assistant"
            print(f"\n{role}:")
            print(msg['content'][:200] + "..." if len(msg['content']) > 200 else msg['content'])
        
        print("\n" + "-" * 70)
        print(f"Total: {len(messages)} message(s)")
    
    def delete_conversation(self, conversation_id):
        """Delete a conversation"""
        confirm = input(f"Delete conversation {conversation_id}? (y/n): ")
        if confirm.lower() != 'y':
            print("Cancelled")
            return
        
        try:
            self.chat_history.delete_conversation(conversation_id)
            print("✓ Conversation deleted successfully")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            sys.exit(1)
    
    def reset_database(self):
        """Reset all data"""
        confirm = input("⚠️  This will delete ALL conversations and chat history. Are you sure? (y/n): ")
        if confirm.lower() != 'y':
            print("Cancelled")
            return
        
        try:
            # Delete database files
            if os.path.exists("chat_history.db"):
                os.remove("chat_history.db")
                print("✓ Deleted chat_history.db")
            
            if os.path.exists("chroma_db"):
                import shutil
                shutil.rmtree("chroma_db")
                print("✓ Deleted chroma_db")
            
            print("✓ Database reset successfully")
            print("Run 'python cli.py ingest' to reinitialize")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Portfolio Management CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py ingest cv.txt          # Ingest CV from file
  python cli.py test "My experience"   # Test RAG system
  python cli.py list                   # List all conversations
  python cli.py get <id>               # Get conversation details
  python cli.py delete <id>            # Delete a conversation
  python cli.py reset                  # Reset all data
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Ingest command
    ingest_parser = subparsers.add_parser('ingest', help='Ingest CV data')
    ingest_parser.add_argument('cv_file', nargs='?', help='Path to CV file')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Test RAG system')
    test_parser.add_argument('query', help='Query to test')
    
    # List command
    subparsers.add_parser('list', help='List all conversations')
    
    # Get command
    get_parser = subparsers.add_parser('get', help='Get conversation details')
    get_parser.add_argument('id', help='Conversation ID')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a conversation')
    delete_parser.add_argument('id', help='Conversation ID')
    
    # Reset command
    subparsers.add_parser('reset', help='Reset all data')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = PortfolioCLI()
    
    if args.command == 'ingest':
        cli.ingest_cv(args.cv_file)
    elif args.command == 'test':
        cli.test_rag(args.query)
    elif args.command == 'list':
        cli.list_conversations()
    elif args.command == 'get':
        cli.get_conversation(args.id)
    elif args.command == 'delete':
        cli.delete_conversation(args.id)
    elif args.command == 'reset':
        cli.reset_database()


if __name__ == '__main__':
    main()
