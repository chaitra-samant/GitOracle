import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings  
from langchain_chroma import Chroma
import shutil




# Load environment variables
load_dotenv()
DATA_PATH = "data"
CHROMA_PATH = "chroma"

def load_documents():
    loader = DirectoryLoader(
        DATA_PATH, 
        glob="*.txt",
        loader_cls=TextLoader,
        loader_kwargs={'autodetect_encoding': True}
    )
    return loader.load()

def split_doc(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=300,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks

def save_to_db(chunks):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    try:
        
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )

        test_embed = embeddings.embed_query("test")
        print("Local embedding test successful!")

        db = Chroma.from_documents(
            chunks,
            embeddings,
            persist_directory=CHROMA_PATH
        )
        db.persist()
        print(f"Successfully saved {len(chunks)} chunks to Chroma DB.")
    except Exception as e:
        print(f"Error creating embeddings: {str(e)}")
        print("Please check model dependencies (e.g., torch) are installed")

if __name__ == "__main__":
    documents = load_documents()
    chunks = split_doc(documents)
    save_to_db(chunks)
