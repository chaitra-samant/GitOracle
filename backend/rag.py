import os
# import shutil
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from ingest import RepoIngestor 
load_dotenv()

# os.environ["GROQ_API_KEY"] = "your_actual_groq_api_key"
DATA_DIR = "data"
CHROMA_DIR = "chroma"

class Rag:
    def __init__(self,data_dir=DATA_DIR,chroma_dir=CHROMA_DIR):
        self.data_dir=data_dir
        self.chroma_dir=chroma_dir
        self.embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        self.prompt_template="""
        Answer the question about the codebase based on the context provided
        {context}
        ------------------------------------------------------
        Question:{question}
        """
        # os.makedirs(self.data_dir, exist_ok=True)

    def get_file(self,url):
        ingestor=RepoIngestor()
        filename=ingestor.get_filename(url)
        return os.path.join(self.data_dir,filename)
    
    def load_doc(self,filepath):
        if not os.path.exists(filepath):
            print(f"File not found at: {filepath}")
            return []
        else:
            loader=TextLoader(filepath,encoding="utf-8")
            return loader.load()
        
    def split_doc(self,documents):
        splitter=RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=300,length_function=len, add_start_index=True
        )

        chunks=splitter.split_documents(documents)
        print(f"Split {len(documents)} into {len(chunks)} chunks")
        return chunks
    
    def create_db(self, chunks):
        try:
            _ = self.embeddings.embed_query("test")  

            if os.path.exists(self.chroma_dir):
                # add to db
                db = Chroma(
                    embedding_function=self.embeddings,
                    persist_directory=self.chroma_dir
                )
                print("Loaded existing Chroma DB.")
                db.add_documents(chunks)
                print(f"Appended {len(chunks)} new chunks to the vector DB.")
            else:
                # new db
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
        
    def train(self,url):
        file=self.get_file(url)
        doc=self.load_doc(file)

        if not doc:
            print("No doc for training")
            return False
        chunks=self.split_doc(doc)
        return self.create_db(chunks)
    
    def query(self,query_text,k=5):
        if not os.path.exists(self.chroma_dir):
            print("Chroma DB not found. Train first.")
            return {"response": "No knowledge base available.", "sources": []}
        
        db = Chroma(embedding_function=self.embeddings, persist_directory=self.chroma_dir)
        results = db.similarity_search_with_relevance_scores(query_text, k=k)
        if not results:
            return {"response": "No relevant information found.", "sources": []}
        
        # building context and prompt for the llm
        context = "\n\n---\n\n".join([doc.page_content for doc, _ in results])

        prompt = ChatPromptTemplate.from_template(self.prompt_template).format(
            context=context, question=query_text
        )


        # llm response
        llm = ChatGroq(model="llama3-70b-8192")  
        response = llm.invoke(prompt)

        sources = [doc.metadata.get("source", None) for doc, _ in results]

        return {
            "response": response.content,
            "sources": sources
        }
    
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python rag_pipeline.py <github_repo_url>")
        exit(1)

    repo_url = sys.argv[1].strip()

    rag = Rag()
    trained = rag.train(repo_url)
    if trained:
        query = "Explain ReportGeneration.py."
        result = rag.query(query)
        print("Answer:\n", result["response"])
        print("Sources:", result["sources"])
    else:
        print("Training failed.")

