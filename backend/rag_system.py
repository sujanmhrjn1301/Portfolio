import chromadb
import httpx
import json
import os
import random
from typing import List, Dict, Optional
from portfolio_instructions import (
    SYSTEM_PROMPT,
    GEN_Z_SYSTEM_PROMPT,
    GREETING_KEYWORDS,
    WORK_KEYWORDS,
    GENERIC_RESPONSE,
    GREETING_RESPONSE
)
from gen_z_slangs import GEN_Z_PHRASES, GEN_Z_SENTENCE_STARTERS, GEN_Z_SENTENCE_ENDERS, GEN_Z_REPLACEMENTS

class RAGSystem:
    def __init__(self, api_key: str, persist_directory: str = "./chroma_db"):
        """Initialize the RAG system with Chroma vector database"""
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1"
        self.http_client = httpx.Client(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            timeout=60.0  # Increase timeout to 60 seconds for API requests
        )
        
        # Initialize Chroma client with persistent storage (new API)
        self.chroma_client = chromadb.PersistentClient(path=persist_directory)
        
        # Create or get collection for CV data
        self.collection = self.chroma_client.get_or_create_collection(
            name="portfolio_cv",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Initialize GitHub integration (optional, lazy loaded)
        self.github_integration = None
        self._init_github_integration()
    
    def _init_github_integration(self):
        """Initialize GitHub integration if available"""
        try:
            from github_integration import GitHubIntegration
            from config import GITHUB_CONFIG
            
            if GITHUB_CONFIG.get("enabled"):
                github_token = os.getenv("GITHUB_TOKEN")
                self.github_integration = GitHubIntegration(github_token=github_token)
                print("✅ GitHub integration initialized")
        except Exception as e:
            print(f"⚠️ GitHub integration not available: {str(e)}")
            self.github_integration = None
    
    def ingest_cv_data(self, cv_text: str, metadata: Optional[Dict] = None):
        """Ingest CV text and split into chunks for RAG"""
        chunks = self._chunk_text(cv_text, chunk_size=500, overlap=50)
        
        for i, chunk in enumerate(chunks):
            embedding = self._get_embedding(chunk)
            
            self.collection.add(
                ids=[f"cv_chunk_{i}"],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[metadata or {"source": "cv", "chunk": i}]
            )
    
    def retrieve_relevant_docs(self, query: str, n_results: int = 5) -> List[str]:
        """Retrieve relevant documents from the knowledge base"""
        query_embedding = self._get_embedding(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "distances"]
        )
        
        # Return documents with decent relevance scores
        documents = results.get("documents", [[]]) or [[]]
        documents = documents[0] if documents else []
        distances = results.get("distances", [[]]) or [[]]
        distances = distances[0] if distances else []
        
        # Filter by distance threshold (lower is better)
        relevant_docs = [doc for doc, dist in zip(documents, distances) if dist < 1.5]
        return relevant_docs if relevant_docs else documents[:n_results]
    
    def _get_embedding(self, text: str) -> List[float]:
        """Get embedding from OpenRouter using text-embedding-3-small"""
        try:
            response = self.http_client.post(
                f"{self.base_url}/embeddings",
                json={
                    "model": "text-embedding-3-small",
                    "input": text
                }
            )
            response.raise_for_status()
            result = response.json()
            
            # Check for error in response
            if "error" in result:
                print(f"❌ Embedding API Error: {result.get('error')}")
                # Return a dummy embedding if API fails
                return [0.0] * 1536
            
            if "data" not in result:
                print(f"⚠️ Unexpected embedding response format: {result}")
                return [0.0] * 1536
            
            return result["data"][0]["embedding"]
        except Exception as e:
            print(f"❌ Embedding error: {str(e)}")
            # Return a dummy embedding to prevent crashes
            return [0.0] * 1536
    
    def _chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunks.append(text[start:end])
            start = end - overlap if end < len(text) else len(text)
        
        return chunks
    
    def _is_greeting(self, query: str) -> bool:
        """Check if query is ONLY a greeting - must be short and simple"""
        query_lower = query.lower().strip()
        
        # Only consider it a greeting if it's very short (less than 8 words)
        # and matches a greeting keyword
        word_count = len(query_lower.split())
        
        if word_count > 7:  # Not a greeting if query is long
            return False
        
        # Check for exact greeting keywords at start or as complete phrases
        greeting_phrases = [
            "hello", "hi", "hey", "how are you", "what's up", 
            "greetings", "good morning", "good afternoon", "good evening", "howdy"
        ]
        
        for greeting in greeting_phrases:
            if greeting == query_lower or query_lower.startswith(greeting):
                return True
        
        return False
    
    def _is_project_query(self, query: str) -> bool:
        """Check if query is asking about projects/repositories"""
        query_lower = query.lower()
        project_keywords = [
            "project", "projects", "repository", "repositories", "repo", "repos",
            "github", "code", "built", "created", "developed", "work",
            "portfolio", "showcase", "github repo", "github repository",
            "what have you", "what've you created", "your work"
        ]
        
        for keyword in project_keywords:
            if keyword in query_lower:
                return True
        
        return False
    
    def _fetch_github_context(self, query: str) -> Optional[str]:
        """Fetch GitHub repositories and format as context"""
        if not self.github_integration:
            print("⚠️ GitHub integration not available")
            return None
        
        try:
            from config import GITHUB_CONFIG
            username = GITHUB_CONFIG.get("username", "sujanmhrjn1301")
            
            # First, check if a specific project name is mentioned
            query_lower = query.lower()
            repos = self.github_integration.get_user_repositories(username)
            
            if not repos:
                print("❌ No repositories found")
                return None
            
            # Look for specific project mentions
            specific_repo = None
            for repo in repos:
                repo_name_lower = repo.get("name", "").lower()
                if repo_name_lower in query_lower:
                    specific_repo = repo
                    print(f"🎯 Found specific project: {repo.get('name')}")
                    break
            
            # If specific project found, fetch its details
            if specific_repo:
                repo_name = specific_repo.get("name", "")
                if not repo_name:
                    print("❌ Repository name not found")
                    return None
                print(f"📖 Fetching detailed info for: {repo_name}")
                detailed_repo = self.github_integration.get_repository_details(username, repo_name)
                readme = self.github_integration.get_repository_readme(username, repo_name)
                
                context = f"# Project Details: {detailed_repo.get('name', 'Unknown')}\n\n"
                context += f"**Description:** {detailed_repo.get('description', 'No description')}\n"
                context += f"**Language:** {detailed_repo.get('language', 'N/A')}\n"
                context += f"**Stars:** {detailed_repo.get('stargazers_count', 0)}\n"
                context += f"**Forks:** {detailed_repo.get('forks_count', 0)}\n"
                context += f"**URL:** {detailed_repo.get('html_url', '')}\n"
                context += f"**Created:** {detailed_repo.get('created_at', 'N/A')}\n"
                context += f"**Last Updated:** {detailed_repo.get('updated_at', 'N/A')}\n"
                
                if detailed_repo.get('topics'):
                    context += f"**Topics:** {', '.join(detailed_repo.get('topics', []))}\n"
                
                if readme:
                    context += f"\n## README\n{readme}\n"
                
                return context
            
            # Otherwise, check if query mentions a specific language
            language_keywords = {
                "python": "Python",
                "javascript": "JavaScript",
                "typescript": "TypeScript",
                "react": "JavaScript",
                "node": "JavaScript",
                "java": "Java",
                "c++": "C++",
                "go": "Go",
                "rust": "Rust",
            }
            
            specific_language = None
            for keyword, language in language_keywords.items():
                if keyword in query_lower:
                    specific_language = language
                    break
            
            # Fetch repositories based on language filter
            if specific_language:
                print(f"🔍 Fetching {specific_language} repositories from GitHub...")
                filtered_repos = self.github_integration.search_repos_by_language(username, specific_language)
            else:
                print(f"🔍 Fetching all repositories from GitHub...")
                filtered_repos = repos
            
            if not filtered_repos:
                print("❌ No repositories found with filter")
                return None
            
            # Format repositories as context
            context = f"# GitHub Projects ({len(filtered_repos)} repositories)\n\n"
            
            for repo in filtered_repos[:10]:  # Limit to top 10 repos
                context += f"## {repo.get('name', 'Unknown')}\n"
                context += f"**Description:** {repo.get('description', 'No description')}\n"
                context += f"**Language:** {repo.get('language', 'N/A')}\n"
                context += f"**Stars:** {repo.get('stargazers_count', 0)}\n"
                context += f"**URL:** {repo.get('html_url', '')}\n"
                
                if repo.get('topics'):
                    context += f"**Topics:** {', '.join(repo.get('topics', []))}\n"
                
                context += "\n"
            
            print(f"✅ GitHub context prepared ({len(filtered_repos)} repos)")
            return context
        
        except Exception as e:
            print(f"⚠️ Error fetching GitHub context: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def _is_relevant_query(self, query: str) -> bool:
        """Check if query should get a response - now more flexible"""
        # Accept all queries and let the system prompt guide behavior
        return True
    
    def _get_generic_response(self) -> str:
        """Return a generic response for off-topic questions"""
        return GENERIC_RESPONSE

    def _apply_gen_z_style(self, response: str) -> str:
        """Apply aggressive Gen-Z slang and style to response"""
        styled_response = response
        
        # Aggressively add Gen-Z phrases throughout
        # Split into sentences and add slang between them
        sentences = styled_response.split('. ')
        styled_sentences = []
        
        for i, sentence in enumerate(sentences):
            styled_sentences.append(sentence)
            # Add Gen-Z phrases after random sentences
            if i < len(sentences) - 1 and random.random() > 0.3:
                styled_sentences.append(random.choice(GEN_Z_PHRASES))
        
        styled_response = '. '.join([s for s in styled_sentences if s])
        
        # Replace common words with Gen-Z equivalents
        for common_word, gen_z_word in GEN_Z_REPLACEMENTS.items():
            # Case-insensitive replacement
            styled_response = styled_response.replace(common_word, gen_z_word)
            styled_response = styled_response.replace(common_word.capitalize(), gen_z_word)
        
        # Add emojis to make it pop
        emoji_additions = [" ✨", " 🔥", " 💯", " 🎯", " 💅", " 🚀"]
        if len(styled_response) > 50 and random.random() > 0.5:
            split_point = random.randint(len(styled_response) // 3, 2 * len(styled_response) // 3)
            styled_response = styled_response[:split_point] + random.choice(emoji_additions) + styled_response[split_point:]
        
        # End with Gen-Z energy
        styled_response = styled_response.rstrip('.') + " " + random.choice(["no cap! ✨", "fr fr! 🔥", "periodt! 💅", "slay! 🎯", "ate! ✨"])
        
        print(f"✨ Applied AGGRESSIVE Gen-Z styling to response")
        return styled_response

    def generate_response(self, query: str, context: Optional[List[str]] = None, github_mode: bool = False, gen_z_mode: bool = False) -> str:
        """Generate response using OpenRouter with gpt-4o-mini model"""
        print(f"\n{'='*60}")
        print(f"🔵 GENERATE_RESPONSE CALLED")
        print(f"   Query: {query}")
        print(f"   GitHub Mode: {github_mode}")
        print(f"   Gen-Z Mode: {gen_z_mode}")
        print(f"{'='*60}")
        
        # Check if it's a greeting - if so, respond directly without API call
        if self._is_greeting(query):
            print(f"👋 Greeting detected: {query}")
            greeting_response = GREETING_RESPONSE
            if gen_z_mode:
                greeting_response = self._apply_gen_z_style(greeting_response)
            return greeting_response
        
        # SPECIAL HANDLING FOR GITHUB MODE
        # If GitHub Mode is enabled, prioritize GitHub data fetching
        if github_mode:
            print(f"🐙 GitHub Mode is ENABLED - Processing with GitHub data")
            is_project_query = self._is_project_query(query)
            print(f"   Is Project Query: {is_project_query}")
            
            if context is None:
                context = []
                
                # Always try to fetch GitHub data in GitHub mode
                print(f"🐙 Attempting to fetch GitHub data...")
                github_context = self._fetch_github_context(query)
                if github_context:
                    print(f"✅ GitHub context fetched successfully")
                    context.append(github_context)
                else:
                    print(f"⚠️ GitHub context not available")
                
                # Add CV database context as fallback
                print(f"📚 Retrieving CV context...")
                cv_context = self.retrieve_relevant_docs(query)
                if cv_context:
                    print(f"✅ CV context retrieved: {len(cv_context)} docs")
                    context.extend(cv_context)
            
            # Generate response with whatever context we have
            print(f"\n📝 Query: {query}")
            print(f"📚 Total context docs: {len(context)}")
            
            if not context:
                print("⚠️ WARNING: No context documents available, but proceeding with GitHub Mode")
            
            context_text = "\n\n".join(context) if context else "No context found in database (GitHub Mode enabled)."
            
            try:
                user_message = f"""Portfolio Context:
{context_text}

User Query: {query}

Provide a professional, complete answer using the context above. Include relevant links and evidence."""
                
                print(f"🔄 Sending request to OpenRouter API (GitHub Mode)...")
                system_prompt = GEN_Z_SYSTEM_PROMPT if gen_z_mode else SYSTEM_PROMPT
                response = self.http_client.post(
                    f"{self.base_url}/chat/completions",
                    json={
                        "model": "openai/gpt-4o-mini",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_message}
                        ],
                        "temperature": 0.4,
                        "max_tokens": 350
                    }
                )
                
                print(f"📨 API Response Status: {response.status_code}")
                response.raise_for_status()
                result = response.json()
                
                if "choices" in result and len(result["choices"]) > 0:
                    content = result["choices"][0].get("message", {}).get("content")
                    if content:
                        print(f"✅ Generated response: {content[:100]}...")
                        if gen_z_mode:
                            content = self._apply_gen_z_style(content)
                        return content
                
                print("❌ No content in API response")
                error_msg = "I couldn't generate a response. Please try again."
                if gen_z_mode:
                    error_msg = self._apply_gen_z_style(error_msg)
                return error_msg
            
            except Exception as e:
                print(f"❌ Error generating response: {str(e)}")
                import traceback
                traceback.print_exc()
                error_response = f"Error generating response: {str(e)}"
                if gen_z_mode:
                    error_response = self._apply_gen_z_style(error_response)
                return error_response
        
        # NORMAL MODE - Process query normally
        print(f"📖 Normal Mode - Processing query")
        
        # Removed strict relevance check - now always try to respond
        
        # Build context for normal mode
        if context is None:
            context = []
            
            # Add CV database context
            print(f"📚 Retrieving CV context for normal mode...")
            cv_context = self.retrieve_relevant_docs(query)
            if cv_context:
                print(f"✅ CV context retrieved: {len(cv_context)} docs")
                context.extend(cv_context)
        
        # Log for debugging
        print(f"\n📝 Query: {query}")
        print(f"📚 Retrieved {len(context)} context documents")
        if not context:
            print("⚠️ WARNING: No context documents retrieved")
        
        context_text = "\n\n".join(context) if context else "No specific context found in database."
        
        # Use imported system prompt from portfolio_instructions
        try:
            user_message = f"""Portfolio Context:
{context_text}

User Query: {query}

Provide a professional, complete answer using the context above. Include relevant links and evidence."""
            
            print(f"🔄 Sending request to OpenRouter API (Normal Mode)...")
            system_prompt = GEN_Z_SYSTEM_PROMPT if gen_z_mode else SYSTEM_PROMPT
            response = self.http_client.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": "openai/gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    "temperature": 0.4,
                    "max_tokens": 350
                }
            )
            
            print(f"📨 API Response Status: {response.status_code}")
            response.raise_for_status()
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0].get("message", {}).get("content")
                if content:
                    print(f"✅ Generated response: {content[:100]}...")
                    if gen_z_mode:
                        content = self._apply_gen_z_style(content)
                    return content
                else:
                    print("❌ Empty content in API response")
                    error_msg = "I couldn't generate a response. Please try again."
                    if gen_z_mode:
                        error_msg = self._apply_gen_z_style(error_msg)
                    return error_msg
            else:
                print(f"❌ Unexpected API response format")
                error_response = f"Unexpected API response format. Status: {response.status_code}"
                if gen_z_mode:
                    error_response = self._apply_gen_z_style(error_response)
                return error_response
        
        except Exception as e:
            print(f"❌ Error generating response: {str(e)}")
            import traceback
            traceback.print_exc()
            error_response = f"Error generating response: {str(e)}"
            if gen_z_mode:
                error_response = self._apply_gen_z_style(error_response)
            return error_response
