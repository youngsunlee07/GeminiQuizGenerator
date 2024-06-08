import sys
import os
import streamlit as st
sys.path.append(os.path.abspath('../../'))
from tasks.task_3.task_3 import DocumentProcessor
from tasks.task_4.task_4 import EmbeddingClient

from langchain_core.documents import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
class ChromaCollectionCreator:
    def __init__(self, processor, embed_model):
        self.processor = processor      # This will hold the DocumentProcessor from Task 3
        self.embed_model = embed_model  # This will hold the EmbeddingClient from Task 4
        self.db = None                  # This will hold the Chroma collection
    
    def create_chroma_collection(self):        
        # Check for processed documents
        if len(self.processor.pages) == 0:
            st.error("No documents found!", icon="🚨")
            return

        # Split documents into text chunks
        # Use a TextSplitter from Langchain to split the documents into smaller text chunks
        # https://python.langchain.com/docs/modules/data_connection/document_transformers/character_text_splitter
        text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(self.processor.pages)
        
        if texts is not None:
            st.success(f"Successfully split pages to {len(texts)} documents!", icon="✅")

        # Create the Chroma Collection
        # https://docs.trychroma.com/
        # Create a Chroma in-memory client using the text chunks and the embeddings model
        self.db = Chroma.from_documents(texts, self.embed_model)
        
        if self.db:
            st.success("Successfully created Chroma Collection!", icon="✅")
        else:
            st.error("Failed to create Chroma Collection!", icon="🚨")
    
    def query_chroma_collection(self, query) -> Document:
        if self.db:
            docs = self.db.similarity_search_with_relevance_scores(query)
            if docs:
                return docs[0]
            else:
                st.error("No matching documents found!", icon="🚨")
        else:
            st.error("Chroma Collection has not been created!", icon="🚨") 
            
    def as_retriever(self):
        if self.db:
            return self.db.as_retriever()            

if __name__ == "__main__":
    processor = DocumentProcessor() # Initialize from Task 3
    processor.ingest_documents()
    
    embed_config = {
        "model_name": "textembedding-gecko@003",
        "project": "geminiquizify-425218",
        "location": "us-central1"
    }
    
    embed_client = EmbeddingClient(**embed_config) # Initialize from Task 4
    
    chroma_creator = ChromaCollectionCreator(processor, embed_client)
    
    with st.form("Load Data to Chroma"):
        st.write("Select PDFs for Ingestion, then click Submit")
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            chroma_creator.create_chroma_collection()