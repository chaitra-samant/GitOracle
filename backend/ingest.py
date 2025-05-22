from gitingest import ingest
import os
import re

DATA_DIR = "data"

class RepoIngestor:
    def __init__(self, data_dir=DATA_DIR):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

    def clean_fname(self, url):
        return re.sub(r'[^\w\-_.]', '_', url)

    def ingest_repo(self, url):
        result = ingest(url)
        # print(f"ingest() returned: {type(result)}")

        try:
            summary, tree, content = result
            # print(f"Types -> summary: {type(summary)}, tree: {type(tree)}, content: {type(content)}")
        except Exception as e:
            print(f"Failed to unpack ingest() result: {e}")
            return False

        '''
        we will store the file as {github_url}_content.txt. 
        to do this we need to remove all the special characters
        '''
        safe_name = self.clean_fname(url)

        with open(os.path.join(self.data_dir, f"{safe_name}_content.txt"), "w", encoding="utf-8") as f:
            f.write(content)
        print("Saved repo content as single file.")
        return True
    
    def get_filename(self, url):
        """
        Returns the filename for the content file
        """
        safe_name = self.clean_fname(url)
        return f"{safe_name}_content.txt"



if __name__ == "__main__":
    url = "https://github.com/octocat/Hello-World"
    url = url.strip()

    ingestor = RepoIngestor()
    ingestor.ingest_repo(url)
    print(ingestor.get_filename(url))
