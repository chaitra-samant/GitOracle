import os
import shutil
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

class RAGSystem:
    def __init__(self, data_path="data", chroma_path="chroma"):
        self.data_path = data_path
        self.chroma_path = chroma_path
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )
        self.prompt_template = """
        Answer the question based only on the provided context.
        {context}
        - - - - - 
        Question:{question}
        """
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_path, exist_ok=True)

    def load_documents(self):
        """Load documents from the data directory"""
        loader = DirectoryLoader(
            self.data_path,
            glob="*.txt",
            loader_cls=TextLoader,
            loader_kwargs={'autodetect_encoding': True}
        )
        return loader.load()

    def split_documents(self, documents):
        """Split documents into chunks"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=300,
            length_function=len,
            add_start_index=True,
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
        return chunks

    def create_vector_db(self, chunks):
        """Create and save vector database"""
        if os.path.exists(self.chroma_path):
            shutil.rmtree(self.chroma_path)

        try:
            # Test embedding
            test_embed = self.embeddings.embed_query("test")
            print("Local embedding test successful!")

            # Create the database with persist_directory
            db = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=self.chroma_path
            )
            
            # No need to call persist() manually with newer versions
            print(f"Successfully saved {len(chunks)} chunks to Chroma DB.")
            return True
        except Exception as e:
            print(f"Error creating embeddings: {str(e)}")
            print("Please check model dependencies (e.g., torch) are installed")
            return False

    def train(self):
        """Train the RAG system on documents in the data directory"""
        documents = self.load_documents()
        if not documents:
            print("No documents found in data directory.")
            return False
            
        chunks = self.split_documents(documents)
        return self.create_vector_db(chunks)

    def query(self, query_text, k=5):
        """Query the RAG system"""
        # Load the database
        try:
            db = Chroma(embedding_function=self.embeddings, persist_directory=self.chroma_path)
        except Exception as e:
            print(f"Error loading database: {str(e)}")
            return {"response": "Database not found. Please train the system first.", "sources": []}

        # Get relevant documents
        results = db.similarity_search_with_relevance_scores(query_text, k=k)
        if len(results) == 0:
            return {"response": "No relevant information found in the knowledge base.", "sources": []}

        # Prepare context from relevant documents
        context = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        prompt_template = ChatPromptTemplate.from_template(self.prompt_template)
        prompt = prompt_template.format(context=context, question=query_text)

        # Query the LLM
        try:
            llm = ChatGroq(model="llama3-70b-8192")
            response = llm.invoke(prompt)
            sources = [doc.metadata.get("source", None) for doc, _score in results]
            
            return {
                "response": response.content,
                "sources": sources
            }
        except Exception as e:
            print(f"Error querying LLM: {str(e)}")
            return {"response": f"Error querying LLM: {str(e)}", "sources": []}

    def save_file(self, file_content, filename):
        """Save uploaded file content to data directory"""
        file_path = os.path.join(self.data_path, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(file_content)
        return file_path

    def clear_data(self):
        """Clear all data files"""
        if os.path.exists(self.data_path):
            for file in os.listdir(self.data_path):
                if file.endswith('.txt'):
                    os.remove(os.path.join(self.data_path, file))
        
        if os.path.exists(self.chroma_path):
            shutil.rmtree(self.chroma_path)
        
        return True


if __name__ == "__main__":
    # Example usage
    rag = RAGSystem()
    rag.train()
    result = rag.query("What is RAG?")
    print(result["response"])
    print("Sources:", result["sources"])