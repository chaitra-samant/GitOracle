import os
import re
import asyncio
import nest_asyncio

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

DATA_DIR = "data"

class RepoIngestor:
    def __init__(self, data_dir=DATA_DIR):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

    def clean_fname(self, url):
        """Clean filename by removing special characters"""
        return re.sub(r'[^\w\-_.]', '_', url)

    def ingest_repo(self, url):
        """Ingest repository and save content with better file structure"""
        try:
            print(f"Ingesting repository: {url}")
            
            # Try different approaches to handle async
            result = self._safe_ingest(url)
            
            if not result:
                print("Failed to get repository content")
                return False
            
            # Handle different return formats from gitingest
            if isinstance(result, tuple):
                if len(result) == 3:
                    summary, tree, content = result
                elif len(result) == 2:
                    tree, content = result
                    summary = ""
                else:
                    content = result[0] if result else ""
                    tree = ""
                    summary = ""
            else:
                content = str(result)
                tree = ""
                summary = ""

            print(f"Retrieved content length: {len(content)} characters")

            # making unique name for every repo -> main goal to avoid conflicts
            safe_name = self.clean_fname(url)
            content_file = os.path.join(self.data_dir, f"{safe_name}_content.txt")

            # storing file with a detailed structure
            with open(content_file, "w", encoding="utf-8") as f:
                if summary:
                    f.write("=== REPOSITORY SUMMARY ===\n")
                    f.write(summary)
                    f.write("\n\n")
                
                if tree:
                    f.write("=== REPOSITORY STRUCTURE ===\n")
                    f.write(tree)
                    f.write("\n\n")
                
                f.write("=== REPOSITORY CONTENT ===\n")
                f.write(content)

            print(f"Saved repository content to: {content_file}")
            
            # saving tree separately for repo structure
            if tree:
                tree_file = os.path.join(self.data_dir, f"{safe_name}_tree.txt")
                with open(tree_file, "w", encoding="utf-8") as f:
                    f.write(tree)
                print(f"Saved repository tree to: {tree_file}")

            return True

        except Exception as e:
            print(f"Failed to ingest repository: {e}")
            return False
    
    def _safe_ingest(self, url):
        """Safely handle gitingest with proper async handling"""
        try:
            from gitingest import ingest
            
            # Method 1: Try direct import and call
            try:
                return ingest(url)
            except RuntimeError as e:
                if "asyncio.run() cannot be called from a running event loop" in str(e):
                    # Method 2: Use nest_asyncio (already applied above)
                    try:
                        return ingest(url)
                    except:
                        # Method 3: Run in new thread
                        import concurrent.futures
                        import threading
                        
                        def run_ingest():
                            return ingest(url)
                        
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            future = executor.submit(run_ingest)
                            return future.result(timeout=300)  # 5 minute timeout
                else:
                    raise e
                    
        except Exception as e:
            print(f"Error in _safe_ingest: {e}")
            # Fallback: Try to get basic repo info via GitHub API
            return self._fallback_github_api(url)
    
    def _fallback_github_api(self, url):
        """Fallback method using GitHub API if gitingest fails"""
        try:
            import requests
            import base64
            
            # Extract owner and repo from URL
            parts = url.replace('https://github.com/', '').split('/')
            if len(parts) < 2:
                return None
                
            owner, repo = parts[0], parts[1]
            
            # Get repository contents via GitHub API
            api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
            
            def get_files_recursive(path=""):
                files_content = []
                api_path = f"{api_url}/{path}" if path else api_url
                
                try:
                    response = requests.get(api_path)
                    if response.status_code != 200:
                        return files_content
                    
                    items = response.json()
                    if not isinstance(items, list):
                        return files_content
                    
                    for item in items:
                        if item['type'] == 'file':
                            # Get file content
                            file_response = requests.get(item['download_url'])
                            if file_response.status_code == 200:
                                try:
                                    file_content = file_response.text
                                    files_content.append(f"\n=== {item['path']} ===\n{file_content}")
                                except:
                                    files_content.append(f"\n=== {item['path']} ===\n[Binary file]")
                        elif item['type'] == 'dir' and len(path.split('/')) < 3:  # Limit depth
                            files_content.extend(get_files_recursive(item['path']))
                    
                    return files_content
                except:
                    return files_content
            
            print("Using GitHub API fallback...")
            files = get_files_recursive()
            content = "\n".join(files)
            
            if content:
                return content
            else:
                return None
                
        except Exception as e:
            print(f"Fallback method also failed: {e}")
            return None

    def get_filename(self, url):
        """Returns the filename for the content file"""
        safe_name = self.clean_fname(url)
        return f"{safe_name}_content.txt"

    def get_tree_filename(self, url):
        """Returns the filename for the tree structure file"""
        safe_name = self.clean_fname(url)
        return f"{safe_name}_tree.txt"

    def list_ingested_repos(self):
        """List all ingested repositories"""
        files = [f for f in os.listdir(self.data_dir) if f.endswith('_content.txt')]
        repos = []
        for file in files:
            # formatting filename to reconstruct actual url 
            repo_name = file.replace('_content.txt', '').replace('_', '/')
            repos.append(repo_name)
        return repos

def main():
    """Test the ingestor"""
    import sys
    
    if len(sys.argv) >= 2:
        url = sys.argv[1].strip()
    else:
        url = "https://github.com/octocat/Hello-World"
    
    print(f"Testing ingestor with URL: {url}")
    
    ingestor = RepoIngestor()
    success = ingestor.ingest_repo(url)
    
    if success:
        print(f"Content filename: {ingestor.get_filename(url)}")
        print(f"Tree filename: {ingestor.get_tree_filename(url)}")
        
        # displaying all ingested repos
        repos = ingestor.list_ingested_repos()
        print(f"All ingested repositories: {repos}")
    else:
        print("Ingestion failed!")

if __name__ == "__main__":
    main()