"""
GitHub Integration - Fetches repository data dynamically
"""
import httpx
from typing import List, Dict, Optional
from datetime import datetime

class GitHubIntegration:
    def __init__(self, github_token: Optional[str] = None):
        """Initialize GitHub API client"""
        self.github_token = github_token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        if github_token:
            self.headers["Authorization"] = f"token {github_token}"
        
        self.http_client = httpx.Client(headers=self.headers, timeout=30.0)
    
    def get_user_repositories(self, username: str) -> List[Dict]:
        """Fetch all public repositories for a user (handles pagination)"""
        try:
            print(f"📚 Fetching repositories for user: {username}")
            url = f"{self.base_url}/users/{username}/repos"
            all_repos = []
            page = 1
            
            while True:
                response = self.http_client.get(
                    url,
                    params={"per_page": 100, "sort": "updated", "page": page}
                )
                response.raise_for_status()
                
                repos = response.json()
                if not repos:
                    break
                
                all_repos.extend(repos)
                
                # Check if there's a next page
                if "Link" not in response.headers:
                    break
                
                link_header = response.headers["Link"]
                if 'rel="next"' not in link_header:
                    break
                
                page += 1
            
            print(f"✅ Found {len(all_repos)} repositories across {page} page(s)")
            return all_repos
        except Exception as e:
            print(f"❌ Error fetching repositories: {str(e)}")
            return []
    
    def get_repository_details(self, username: str, repo_name: str) -> Dict:
        """Fetch detailed information about a specific repository"""
        try:
            url = f"{self.base_url}/repos/{username}/{repo_name}"
            response = self.http_client.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error fetching repo details: {str(e)}")
            return {}
    
    def get_repository_readme(self, username: str, repo_name: str) -> Optional[str]:
        """Fetch README content from a repository"""
        try:
            url = f"{self.base_url}/repos/{username}/{repo_name}/readme"
            response = self.http_client.get(url, headers={"Accept": "application/vnd.github.v3.raw"})
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"⚠️  No README found for {repo_name}")
            return None
    
    def format_repo_for_context(self, repo: Dict, username: str) -> str:
        """Format repository data for RAG context"""
        readme = self.get_repository_readme(username, repo.get("name", ""))
        
        formatted = f"""
Repository: {repo.get('name', 'Unknown')}
Description: {repo.get('description', 'No description')}
URL: {repo.get('html_url', '')}
Language: {repo.get('language', 'N/A')}
Stars: {repo.get('stargazers_count', 0)}
Forks: {repo.get('forks_count', 0)}
Topics: {', '.join(repo.get('topics', [])) if repo.get('topics') else 'N/A'}
Last Updated: {repo.get('updated_at', 'N/A')}

"""
        
        if readme:
            formatted += f"README Content:\n{readme}\n"
        
        return formatted
    
    def get_all_repos_context(self, username: str) -> str:
        """Get all repositories as formatted context for RAG"""
        repos = self.get_user_repositories(username)
        if not repos:
            return "No repositories found."
        
        context = "# GitHub Projects\n\n"
        for repo in repos:
            context += self.format_repo_for_context(repo, username)
            context += "\n" + "="*80 + "\n\n"
        
        return context
    
    def search_repos_by_language(self, username: str, language: str) -> List[Dict]:
        """Search repositories by programming language"""
        repos = self.get_user_repositories(username)
        filtered = [
            repo for repo in repos 
            if repo.get("language", "").lower() == language.lower()
        ]
        return filtered
    
    def search_repos_by_topic(self, username: str, topic: str) -> List[Dict]:
        """Search repositories by topic"""
        repos = self.get_user_repositories(username)
        filtered = [
            repo for repo in repos 
            if topic.lower() in [t.lower() for t in repo.get("topics", [])]
        ]
        return filtered
