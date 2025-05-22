import os
import shutil
from dotenv import load_dotenv
from langchain_community.document_loaders import (
    DirectoryLoader, 
    TextLoader,
    PyPDFLoader,  
    Docx2txtLoader,  
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

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
        documents = []
        
        # Load TXT files
        txt_loader = DirectoryLoader(
            self.data_path,
            glob="*.txt",
            loader_cls=TextLoader,
            loader_kwargs={'autodetect_encoding': True}
        )
        documents.extend(txt_loader.load())
        
        # Load PDF files - using PyPDFLoader instead of UnstructuredPDFLoader
        pdf_loader = DirectoryLoader(
            self.data_path,
            glob="*.pdf",
            loader_cls=PyPDFLoader
        )
        documents.extend(pdf_loader.load())
        
        # Load DOCX files
        docx_loader = DirectoryLoader(
            self.data_path,
            glob="*.docx",
            loader_cls=Docx2txtLoader
        )
        documents.extend(docx_loader.load())
        
        return documents

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
           
            test_embed = self.embeddings.embed_query("test")
            print("Local embedding test successful!")

            # Create the database with persist_directory
            #persist ensures data is stored permanantly and isnt volatile
            
            db = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=self.chroma_path
            )
            
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
        
        db = Chroma(embedding_function=self.embeddings, persist_directory=self.chroma_path)
        
    
        results = db.similarity_search_with_relevance_scores(query_text, k=k)
        if len(results) == 0:
            return {"response": "No relevant information found in the knowledge base.", "sources": []}

        # creating context
        context = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        prompt_template = ChatPromptTemplate.from_template(self.prompt_template)
        prompt = prompt_template.format(context=context, question=query_text)

        # Query
        llm = ChatGroq(model="llama3-70b-8192")
        response = llm.invoke(prompt)
        sources = [doc.metadata.get("source", None) for doc, _score in results]
        
        return {
            "response": response.content,
            "sources": sources
        }
        

    def save_file(self, file_content, filename):
        """Save uploaded file content to data directory"""
        file_path = os.path.join(self.data_path, filename)
        
        # For text files
        if filename.endswith('.txt'):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
        else:
            # For binary files (pdf, docx)
            with open(file_path, 'wb') as f:
                f.write(file_content)
        return file_path

    def clear_data(self):
        """Clear all data files"""
        if os.path.exists(self.data_path):
            for file in os.listdir(self.data_path):
                if file.endswith(('.txt', '.pdf', '.docx')):
                    os.remove(os.path.join(self.data_path, file))
        
        if os.path.exists(self.chroma_path):
            shutil.rmtree(self.chroma_path)
        
        return True


if __name__ == "__main__":
   
    rag = RAGSystem()
    rag.train()

    #testing
    result = rag.query("What is RAG?")
    print(result["response"])
    print("Sources:", result["sources"])