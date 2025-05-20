###used to test rag on cli not required for gui


import argparse
import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv




load_dotenv()
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
CHROMA_PATH="chroma"

PROMPT_TEMPLATE="""
Answer the question based only on the provided context.
{context}
- - - - - 
Question:{question}
"""

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("query_text",type=str,help="query text")
    args=parser.parse_args()
    query_text=args.query_text

    ##prepare db
    embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )
    
    db=Chroma(embedding_function=embeddings, persist_directory=CHROMA_PATH)

    results=db.similarity_search_with_relevance_scores(query_text, k=5)
    if len(results)==0:

        print(f"No results found: {len(results)}")
        return
    
    ##prepare prompt for llm
    context = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template=ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context, question=query_text)

    llm=ChatGroq(model="llama3-70b-8192")
    res = llm.invoke(prompt)

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"Response: {res}\nSources: {sources}"
    print(formatted_response)

if __name__ == "__main__":
    main()
    