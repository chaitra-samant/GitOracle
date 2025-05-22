from gitingest import ingest
import os
import re

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
            result = ingest(url)
            
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