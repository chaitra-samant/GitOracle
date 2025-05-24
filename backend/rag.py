import os
import hashlib
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document
from ingest import RepoIngestor 
import json

load_dotenv()

DATA_DIR = "data"
CHROMA_DIR = "chroma"
PROCESSED_FILES_PATH = "processed_files.json"

class Rag:
    def __init__(self, data_dir=DATA_DIR, chroma_dir=CHROMA_DIR):
        self.data_dir = data_dir
        self.chroma_dir = chroma_dir
        self.processed_files_path = PROCESSED_FILES_PATH
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        self.prompt_template = """
Answer the question about the codebase based on the context provided. Pay special attention to the file names mentioned in the context.

Context:
{context}

Question: {question}

Please provide a detailed answer based on the context above. If you're discussing specific files, mention their names clearly.
"""
        self.processed_files = self.load_processed_files()

    def load_processed_files(self):
        """Load the list of already processed files"""
        if os.path.exists(self.processed_files_path):
            try:
                with open(self.processed_files_path, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_processed_files(self):
        """Save the list of processed files"""
        with open(self.processed_files_path, 'w') as f:
            json.dump(self.processed_files, f)

    def get_file_hash(self, filepath):
        """Generate hash of file content to detect changes"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None

    def get_file(self, url):
        ingestor = RepoIngestor()
        filename = ingestor.get_filename(url)
        return os.path.join(self.data_dir, filename)
    
    def load_doc(self, filepath):
        if not os.path.exists(filepath):
            print(f"File not found at: {filepath}")
            return []
        else:
            loader = TextLoader(filepath, encoding="utf-8")
            return loader.load()
        
    def split_doc_with_filenames(self, documents):
        """Enhanced document splitting that preserves file information"""
        all_chunks = []
        
        for doc in documents:
            content = doc.page_content
            
            # Split by common file separators or patterns
            file_sections = self.parse_files_from_content(content)
            
            if not file_sections:
                # Fallback: treat as single document
                file_sections = [{"filename": "unknown", "content": content}]
            
            for section in file_sections:
                filename = section["filename"]
                file_content = section["content"]
                
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=300,
                    length_function=len,
                    add_start_index=True
                )
                
                # Create a temporary document for splitting
                temp_doc = Document(
                    page_content=file_content,
                    metadata={"source": filename, "original_source": doc.metadata.get("source", "")}
                )
                
                chunks = splitter.split_documents([temp_doc])
                
                # Add filename to each chunk's metadata
                for chunk in chunks:
                    chunk.metadata["filename"] = filename
                    chunk.metadata["file_type"] = self.get_file_type(filename)
                    # Add filename context to the beginning of chunk content
                    chunk.page_content = f"[File: {filename}]\n\n{chunk.page_content}"
                
                all_chunks.extend(chunks)
        
        print(f"Split into {len(all_chunks)} chunks across multiple files")
        return all_chunks

    def parse_files_from_content(self, content):
        """Parse the ingested content to identify individual files"""
        file_sections = []
        
        lines = content.split('\n')
        current_file = None
        current_content = []
        
        for line in lines:
            # Look for file headers (adjust pattern based on your ingest format)
            if line.startswith('=== ') and line.endswith(' ==='):
                # Save previous file
                if current_file and current_content:
                    file_sections.append({
                        "filename": current_file,
                        "content": '\n'.join(current_content)
                    })
                
                # Start new file
                current_file = line.replace('=== ', '').replace(' ===', '').strip()
                current_content = []
            elif line.startswith('--- ') and line.endswith(' ---'):
                # Alternative file separator pattern
                if current_file and current_content:
                    file_sections.append({
                        "filename": current_file,
                        "content": '\n'.join(current_content)
                    })
                
                current_file = line.replace('--- ', '').replace(' ---', '').strip()
                current_content = []
            elif line.startswith('File: '):
                # Another common pattern
                if current_file and current_content:
                    file_sections.append({
                        "filename": current_file,
                        "content": '\n'.join(current_content)
                    })
                
                current_file = line.replace('File: ', '').strip()
                current_content = []
            else:
                if current_file:
                    current_content.append(line)
        
        # Don't forget the last file
        if current_file and current_content:
            file_sections.append({
                "filename": current_file,
                "content": '\n'.join(current_content)
            })
        
        return file_sections

    def get_file_type(self, filename):
        """Determine file type based on extension"""
        if '.' in filename:
            ext = filename.split('.')[-1].lower()
            return ext
        return "unknown"
    
    def create_db(self, chunks):
        try:
            # Test embeddings
            _ = self.embeddings.embed_query("test")  

            if os.path.exists(self.chroma_dir):
                # Load existing db
                db = Chroma(
                    embedding_function=self.embeddings,
                    persist_directory=self.chroma_dir
                )
                print("Loaded existing Chroma DB.")
                
                # Add new chunks
                db.add_documents(chunks)
                print(f"Added {len(chunks)} new chunks to the vector DB.")
            else:
                # Create new db
                db = Chroma.from_documents(
                    documents=chunks,
                    embedding=self.embeddings,
                    persist_directory=self.chroma_dir
                )
                print(f"Created new Chroma DB with {len(chunks)} chunks.")

            return True

        except Exception as e:
            print(f"Error with vector DB: {str(e)}")
            return False
        
    def train(self, url):
        """Train the model, but skip if file already processed and unchanged"""
        file_path = self.get_file(url)
        
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return False
        
        # Check if file already processed
        file_hash = self.get_file_hash(file_path)
        if file_path in self.processed_files and self.processed_files[file_path] == file_hash:
            print(f"File {file_path} already processed and unchanged. Skipping.")
            return True
        
        # Load and process document
        doc = self.load_doc(file_path)
        if not doc:
            print("No doc for training")
            return False
        
        # Split with filename preservation
        chunks = self.split_doc_with_filenames(doc)
        
        # Create/update database
        success = self.create_db(chunks)
        
        if success:
            # Mark file as processed
            self.processed_files[file_path] = file_hash
            self.save_processed_files()
            print(f"Successfully processed and stored: {file_path}")
        
        return success
    
    def search_and_answer(self, query_text, k=5):
        """Search the knowledge base and provide an answer - THIS IS THE METHOD THE API CALLS"""
        if not os.path.exists(self.chroma_dir):
            print("Chroma DB not found. Train first.")
            return {"response": "No knowledge base available.", "sources": []}
        
        db = Chroma(embedding_function=self.embeddings, persist_directory=self.chroma_dir)
        
        # Search for similar documents
        results = db.similarity_search(query_text, k=k)
        
        if not results:
            return {"response": "No relevant information found.", "sources": []}
        
        # Build context from results
        context_parts = []
        sources = []
        
        for doc in results:
            context_parts.append(doc.page_content)
            # Get filename from metadata
            filename = doc.metadata.get("filename", "unknown")
            source = doc.metadata.get("source", "unknown")
            sources.append(f"{filename} (from {source})")
        
        context = "\n\n---\n\n".join(context_parts)

        # Create and format prompt
        prompt_template = ChatPromptTemplate.from_template(self.prompt_template)
        prompt = prompt_template.format(context=context, question=query_text)

        # Get LLM response
        llm = ChatGroq(model="llama3-70b-8192")  
        response = llm.invoke(prompt)

        return {
            "response": response.content,
            "sources": list(set(sources))  # Remove duplicates
        }

    def interactive_query(self):
        """Interactive query loop for command line usage"""
        if not os.path.exists(self.chroma_dir):
            print("Chroma DB not found. Please train first.")
            return
        
        print("\n" + "="*50)
        print("Interactive RAG Query System")
        print("Type 'quit', 'exit', or 'q' to stop")
        print("="*50 + "\n")
        
        while True:
            try:
                query = input("\nEnter your query: ").strip()
                
                if query.lower() in ['quit', 'exit', 'q', '']:
                    print("Goodbye!")
                    break
                
                print("\nSearching...")
                result = self.search_and_answer(query)
                
                print(f"\nAnswer:\n{result['response']}")
                print(f"\nSources: {', '.join(result['sources'])}")
                print("\n" + "-"*50)
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

def main():
    import sys
    
    rag = Rag()
    
    if len(sys.argv) >= 2:
        repo_url = sys.argv[1].strip()
        
        print(f"Training on repository: {repo_url}")
        trained = rag.train(repo_url)
        
        if trained:
            print("Training completed successfully!")
            # Start interactive query loop
            rag.interactive_query()
        else:
            print("Training failed.")
    else:
        # Check if we have an existing database
        if os.path.exists(rag.chroma_dir):
            print("Found existing database. Starting interactive mode...")
            rag.interactive_query()
        else:
            print("Usage: python rag.py <github_repo_url>")
            print("Or run with existing database for interactive queries.")

if __name__ == "__main__":
    main()